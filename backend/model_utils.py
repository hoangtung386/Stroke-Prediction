"""Model training and evaluation utilities for stroke prediction."""

import os

import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import StratifiedKFold, RandomizedSearchCV
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    StackingClassifier,
    VotingClassifier,
)
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from imblearn.ensemble import BalancedBaggingClassifier

from config import SEED, K_FOLD, PARAM_GRIDS


def get_base_models():
    """Return dictionary of base classification models.

    Returns:
        Dictionary mapping model names to classifier instances.
    """
    return {
        "LR-AGD": LogisticRegression(
            solver="saga", max_iter=100, random_state=SEED
        ),
        "Neural Network": MLPClassifier(
            hidden_layer_sizes=(24, 36, 48, 36, 24),
            random_state=SEED,
            max_iter=500,
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=100, random_state=SEED
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=100, random_state=SEED
        ),
        "CatBoost": CatBoostClassifier(
            iterations=100, random_state=SEED, verbose=0
        ),
        "LightGBM": LGBMClassifier(
            n_estimators=100, random_state=SEED, verbose=-1
        ),
        "XGBoost": XGBClassifier(
            n_estimators=100, random_state=SEED, eval_metric="logloss"
        ),
        "Balanced Bagging": BalancedBaggingClassifier(
            estimator=RandomForestClassifier(random_state=SEED),
            n_estimators=5,
            random_state=SEED,
        ),
    }


def evaluate_model_kfold(model, x, y, k=K_FOLD, model_name="Model"):
    """Evaluate a model using stratified k-fold cross validation.

    Args:
        model: Classifier instance to evaluate.
        x: Feature matrix.
        y: Target labels.
        k: Number of folds.
        model_name: Display name for results.

    Returns:
        Dictionary with mean metrics across folds.
    """
    skf = StratifiedKFold(n_splits=k, shuffle=True, random_state=SEED)

    metrics = {
        "accuracy": [],
        "precision": [],
        "recall": [],
        "f1": [],
        "auc": [],
    }

    for train_idx, val_idx in skf.split(x, y):
        x_fold_train = x.iloc[train_idx]
        x_fold_val = x.iloc[val_idx]
        y_fold_train = y.iloc[train_idx]
        y_fold_val = y.iloc[val_idx]

        model.fit(x_fold_train, y_fold_train)

        y_pred = model.predict(x_fold_val)
        y_pred_proba = (
            model.predict_proba(x_fold_val)[:, 1]
            if hasattr(model, "predict_proba")
            else y_pred
        )

        metrics["accuracy"].append(accuracy_score(y_fold_val, y_pred))
        metrics["precision"].append(
            precision_score(y_fold_val, y_pred, zero_division=0)
        )
        metrics["recall"].append(
            recall_score(y_fold_val, y_pred, zero_division=0)
        )
        metrics["f1"].append(
            f1_score(y_fold_val, y_pred, zero_division=0)
        )

        try:
            metrics["auc"].append(roc_auc_score(y_fold_val, y_pred_proba))
        except ValueError:
            metrics["auc"].append(0)

    return {
        "Model": model_name,
        "Accuracy": np.mean(metrics["accuracy"]),
        "Precision": np.mean(metrics["precision"]),
        "Recall": np.mean(metrics["recall"]),
        "F1-Score": np.mean(metrics["f1"]),
        "AUC": np.mean(metrics["auc"]),
        "Accuracy_std": np.std(metrics["accuracy"]),
    }


def train_all_models(x_train, y_train):
    """Train all base models and return ranked results.

    Args:
        x_train: Training features.
        y_train: Training labels.

    Returns:
        Tuple of (results_dataframe, models_dict).
    """
    models = get_base_models()
    all_results = []

    print("Training Baseline Logistic Regression...")
    baseline = LogisticRegression(random_state=SEED, max_iter=1000)
    baseline_results = evaluate_model_kfold(
        baseline, x_train, y_train, k=K_FOLD, model_name="Baseline LR"
    )
    all_results.append(baseline_results)
    print(f"Baseline Accuracy: {baseline_results['Accuracy']:.4f}")

    for model_name, model in models.items():
        print(f"\nTraining {model_name}...")
        results = evaluate_model_kfold(
            model, x_train, y_train, k=K_FOLD, model_name=model_name
        )
        all_results.append(results)
        print(f"Accuracy: {results['Accuracy']:.4f}")

    results_df = pd.DataFrame(all_results)
    results_df = results_df.sort_values("Accuracy", ascending=False)

    return results_df, models


def fine_tune_top_models(top_models, models_dict, x_train, y_train):
    """Fine-tune top performing models using RandomizedSearchCV.

    Args:
        top_models: List of model names to tune.
        models_dict: Dictionary of model name to instance.
        x_train: Training features.
        y_train: Training labels.

    Returns:
        Dictionary of tuned model name to best estimator.
    """
    tuned_models = {}

    for model_name in top_models:
        if model_name not in PARAM_GRIDS or model_name not in models_dict:
            continue

        print(f"\nFine-tuning {model_name}...")
        search = RandomizedSearchCV(
            models_dict[model_name],
            PARAM_GRIDS[model_name],
            n_iter=10,
            cv=3,
            scoring="f1",
            random_state=SEED,
            n_jobs=-1,
        )
        search.fit(x_train, y_train)
        tuned_models[model_name] = search.best_estimator_

        print(f"Best parameters: {search.best_params_}")
        print(f"Best CV score: {search.best_score_:.4f}")

    return tuned_models


def build_dse_ensemble(
    base_models_for_ensemble, meta_classifier, x_train, y_train
):
    """Build a Dense Stacking Ensemble (DSE) model.

    Architecture (4 layers):
      1. Voting Ensemble (soft voting)
      2. Blending Ensemble (stacking with meta-classifier)
      3. Fusion Ensemble (stacking with passthrough)
      4. DSE (stacking the 3 ensembles above)

    Args:
        base_models_for_ensemble: List of (name, model) tuples.
        meta_classifier: Model to use as final estimator.
        x_train: Training features.
        y_train: Training labels.

    Returns:
        Fitted DSE model.
    """
    print("\n=== Building Dense Stacking Ensemble (DSE) ===")

    filtered_models = [
        (name, model)
        for name, model in base_models_for_ensemble
        if name != "NGBoost"
    ]

    print("Building Voting Ensemble...")
    voting = VotingClassifier(estimators=filtered_models, voting="soft")
    voting.fit(x_train, y_train)

    print("Building Blending Ensemble...")
    blending = StackingClassifier(
        estimators=filtered_models,
        final_estimator=meta_classifier,
        cv=5,
    )
    blending.fit(x_train, y_train)

    print("Building Fusion Ensemble...")
    fusion = StackingClassifier(
        estimators=filtered_models,
        final_estimator=meta_classifier,
        cv=5,
        passthrough=True,
    )
    fusion.fit(x_train, y_train)

    print("Building DSE (Final Model)...")
    dse_base = [
        ("voting", voting),
        ("blending", blending),
        ("fusion", fusion),
    ]
    dse_model = StackingClassifier(
        estimators=dse_base,
        final_estimator=meta_classifier,
        cv=5,
    )
    dse_model.fit(x_train, y_train)

    return dse_model


def evaluate_final_model(dse_model, x_test, y_test):
    """Evaluate the final DSE model on the test set.

    Args:
        dse_model: Fitted DSE model.
        x_test: Test features.
        y_test: Test labels.

    Returns:
        Dictionary with all evaluation metrics.
    """
    y_pred = dse_model.predict(x_test)
    y_pred_proba = dse_model.predict_proba(x_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    auc = roc_auc_score(y_test, y_pred_proba)

    print(f"\n{'=' * 50}")
    print("DSE MODEL PERFORMANCE")
    print(f"{'=' * 50}")
    print(f"Accuracy:  {accuracy:.4f} ({accuracy * 100:.2f}%)")
    print(f"Precision: {precision:.4f} ({precision * 100:.2f}%)")
    print(f"Recall:    {recall:.4f} ({recall * 100:.2f}%)")
    print(f"F1-Score:  {f1:.4f} ({f1 * 100:.2f}%)")
    print(f"AUC:       {auc:.4f} ({auc * 100:.2f}%)")

    cm = confusion_matrix(y_test, y_pred)
    print("\nConfusion Matrix:")
    print(cm)

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "auc": auc,
        "confusion_matrix": cm,
    }


def save_model_artifacts(
    dse_model, scaler, encoder, x_train, folder_name, suffix
):
    """Save trained model and preprocessing artifacts to disk.

    Args:
        dse_model: Fitted DSE model.
        scaler: Fitted StandardScaler.
        encoder: Fitted OneHotEncoder.
        x_train: Training features (for column names).
        folder_name: Output directory path.
        suffix: File name suffix for this variant.
    """
    os.makedirs(folder_name, exist_ok=True)

    artifacts = {
        f"dse_stroke_prediction_{suffix}.pkl": dse_model,
        f"scaler_{suffix}.pkl": scaler,
        f"encoder_{suffix}.pkl": encoder,
        f"model_columns_{suffix}.pkl": x_train.columns.tolist(),
    }

    for filename, artifact in artifacts.items():
        filepath = os.path.join(folder_name, filename)
        joblib.dump(artifact, filepath)
        print(f"Saved: {filepath}")

    print(f"\nAll artifacts saved successfully in '{folder_name}'")
