"""
Model training and evaluation utilities
"""
import numpy as np
import pandas as pd
import joblib
import os
from sklearn.model_selection import StratifiedKFold, RandomizedSearchCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, roc_auc_score, confusion_matrix
)
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import (
    RandomForestClassifier, GradientBoostingClassifier,
    StackingClassifier, VotingClassifier
)
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from ngboost import NGBClassifier
from imblearn.ensemble import BalancedBaggingClassifier
from config import *


def get_base_models():
    """Return dictionary of base classification models"""
    models = {
        'LR-AGD': LogisticRegression(solver='saga', max_iter=100, random_state=SEED),
        
        'Neural Network': MLPClassifier(
            hidden_layer_sizes=(24, 36, 48, 36, 24),
            random_state=SEED,
            max_iter=500
        ),
        
        'Random Forest': RandomForestClassifier(
            n_estimators=100,
            random_state=SEED
        ),
        
        'Gradient Boosting': GradientBoostingClassifier(
            n_estimators=100,
            random_state=SEED
        ),
        
        'CatBoost': CatBoostClassifier(
            iterations=100,
            random_state=SEED,
            verbose=0
        ),
        
        'LightGBM': LGBMClassifier(
            n_estimators=100,
            random_state=SEED,
            verbose=-1
        ),
        
        'XGBoost': XGBClassifier(
            n_estimators=100,
            random_state=SEED,
            eval_metric='logloss'
        ),
        
        'Balanced Bagging': BalancedBaggingClassifier(
            estimator=RandomForestClassifier(random_state=SEED),
            n_estimators=5,
            random_state=SEED
        ),
        

    }
    return models


def evaluate_model_kfold(model, X, y, k=K_FOLD, model_name="Model"):
    """
    Evaluate model using k-fold cross validation
    """
    skf = StratifiedKFold(n_splits=k, shuffle=True, random_state=SEED)
    
    accuracy_scores = []
    precision_scores = []
    recall_scores = []
    f1_scores = []
    auc_scores = []
    
    for train_idx, val_idx in skf.split(X, y):
        X_fold_train, X_fold_val = X.iloc[train_idx], X.iloc[val_idx]
        y_fold_train, y_fold_val = y.iloc[train_idx], y.iloc[val_idx]
        
        # Train model
        model.fit(X_fold_train, y_fold_train)
        
        # Predict
        y_pred = model.predict(X_fold_val)
        y_pred_proba = model.predict_proba(X_fold_val)[:, 1] if hasattr(model, 'predict_proba') else y_pred
        
        # Calculate metrics
        accuracy_scores.append(accuracy_score(y_fold_val, y_pred))
        precision_scores.append(precision_score(y_fold_val, y_pred, zero_division=0))
        recall_scores.append(recall_score(y_fold_val, y_pred, zero_division=0))
        f1_scores.append(f1_score(y_fold_val, y_pred, zero_division=0))
        
        try:
            auc_scores.append(roc_auc_score(y_fold_val, y_pred_proba))
        except:
            auc_scores.append(0)
    
    results = {
        'Model': model_name,
        'Accuracy': np.mean(accuracy_scores),
        'Precision': np.mean(precision_scores),
        'Recall': np.mean(recall_scores),
        'F1-Score': np.mean(f1_scores),
        'AUC': np.mean(auc_scores),
        'Accuracy_std': np.std(accuracy_scores)
    }
    
    return results


def train_all_models(X_train, y_train):
    """
    Train all base models and return results
    """
    models = get_base_models()
    all_results = []
    
    # Train baseline
    print("Training Baseline Logistic Regression...")
    baseline_model = LogisticRegression(random_state=SEED, max_iter=1000)
    baseline_results = evaluate_model_kfold(
        baseline_model, X_train, y_train, 
        k=K_FOLD, model_name="Baseline LR"
    )
    all_results.append(baseline_results)
    print(f"Baseline Accuracy: {baseline_results['Accuracy']:.4f}")
    
    # Train all models
    for model_name, model in models.items():
        print(f"\nTraining {model_name}...")
        results = evaluate_model_kfold(
            model, X_train, y_train,
            k=K_FOLD, model_name=model_name
        )
        all_results.append(results)
        print(f"Accuracy: {results['Accuracy']:.4f}")
    
    # Create results DataFrame
    results_df = pd.DataFrame(all_results)
    results_df = results_df.sort_values('Accuracy', ascending=False)
    
    return results_df, models


def fine_tune_top_models(top_models, models_dict, X_train, y_train):
    """
    Fine-tune top performing models using RandomizedSearchCV
    """
    tuned_models = {}
    
    for model_name in top_models:
        if model_name in PARAM_GRIDS and model_name in models_dict:
            print(f"\nFine-tuning {model_name}...")
            
            random_search = RandomizedSearchCV(
                models_dict[model_name],
                PARAM_GRIDS[model_name],
                n_iter=10,
                cv=3,
                scoring='f1',
                random_state=SEED,
                n_jobs=-1
            )
            
            random_search.fit(X_train, y_train)
            tuned_models[model_name] = random_search.best_estimator_
            
            print(f"Best parameters: {random_search.best_params_}")
            print(f"Best CV score: {random_search.best_score_:.4f}")
    
    return tuned_models


def build_dse_ensemble(base_models_for_ensemble, meta_classifier, X_train, y_train):
    """
    Build Dense Stacking Ensemble (DSE) model
    """
    print("\n=== Building Dense Stacking Ensemble (DSE) ===")
    
    # Exclude NGBoost from ensembles (compatibility issues)
    base_models_filtered = [
        (name, model) for name, model in base_models_for_ensemble 
        if name != 'NGBoost'
    ]
    
    # 1. Voting Ensemble
    print("Building Voting Ensemble...")
    voting_ensemble = VotingClassifier(
        estimators=base_models_filtered,
        voting='soft'
    )
    voting_ensemble.fit(X_train, y_train)
    
    # 2. Blending Ensemble
    print("Building Blending Ensemble...")
    blending_ensemble = StackingClassifier(
        estimators=base_models_filtered,
        final_estimator=meta_classifier,
        cv=5
    )
    blending_ensemble.fit(X_train, y_train)
    
    # 3. Fusion Ensemble
    print("Building Fusion Ensemble...")
    fusion_ensemble = StackingClassifier(
        estimators=base_models_filtered,
        final_estimator=meta_classifier,
        cv=5,
        passthrough=True
    )
    fusion_ensemble.fit(X_train, y_train)
    
    # 4. Dense Stacking Ensemble (DSE)
    print("Building DSE (Final Model)...")
    dse_base_models = [
        ('voting', voting_ensemble),
        ('blending', blending_ensemble),
        ('fusion', fusion_ensemble)
    ]
    
    dse_model = StackingClassifier(
        estimators=dse_base_models,
        final_estimator=meta_classifier,
        cv=5
    )
    dse_model.fit(X_train, y_train)
    
    return dse_model


def evaluate_final_model(dse_model, X_test, y_test):
    """
    Evaluate final DSE model and print metrics
    """
    # Predictions
    y_pred = dse_model.predict(X_test)
    y_pred_proba = dse_model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    auc = roc_auc_score(y_test, y_pred_proba)
    
    print("\n" + "="*50)
    print("DSE MODEL PERFORMANCE")
    print("="*50)
    print(f"Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"Precision: {precision:.4f} ({precision*100:.2f}%)")
    print(f"Recall:    {recall:.4f} ({recall*100:.2f}%)")
    print(f"F1-Score:  {f1:.4f} ({f1*100:.2f}%)")
    print(f"AUC:       {auc:.4f} ({auc*100:.2f}%)")
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print("\nConfusion Matrix:")
    print(cm)
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'auc': auc,
        'confusion_matrix': cm
    }


def save_model_artifacts(dse_model, scaler, encoder, X_train, folder_name, suffix):
    """
    Save model, scaler, encoder, and feature columns
    """
    os.makedirs(folder_name, exist_ok=True)
    
    # Save model
    model_path = os.path.join(folder_name, f'dse_stroke_prediction_{suffix}.pkl')
    joblib.dump(dse_model, model_path)
    print(f"Model saved at: '{model_path}'")
    
    # Save scaler
    scaler_path = os.path.join(folder_name, f'scaler_{suffix}.pkl')
    joblib.dump(scaler, scaler_path)
    print(f"Scaler saved at: '{scaler_path}'")
    
    # Save encoder
    encoder_path = os.path.join(folder_name, f'encoder_{suffix}.pkl')
    joblib.dump(encoder, encoder_path)
    print(f"Encoder saved at: '{encoder_path}'")
    
    # Save model columns
    columns_path = os.path.join(folder_name, f'model_columns_{suffix}.pkl')
    joblib.dump(X_train.columns.tolist(), columns_path)
    print(f"Model columns saved at: '{columns_path}'")
    
    print(f"\n✅ All artifacts saved successfully in '{folder_name}'")
