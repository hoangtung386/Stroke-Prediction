"""Unified training script for all stroke prediction model variants.

Replaces 10 separate training scripts with a single parameterized script.

Usage:
    python train.py --imputation drop --balancing imbalanced
    python train.py --imputation mean --balancing smote
    python train.py --all
"""
import argparse
import warnings

from sklearn.ensemble import RandomForestClassifier

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config import SEED, MODEL_DIRS
from data_preprocessing import (
    load_dataset,
    preprocess_basic,
    impute_drop,
    impute_mean,
    impute_mice,
    impute_age_group,
    create_augmented_dataset,
    apply_smote,
    prepare_train_test_split,
)
from model_utils import (
    train_all_models,
    fine_tune_top_models,
    build_dse_ensemble,
    evaluate_final_model,
    save_model_artifacts,
)

warnings.filterwarnings("ignore")

IMPUTATION_METHODS = ["drop", "mean", "mice", "agegroup", "augmented"]
BALANCING_OPTIONS = ["imbalanced", "smote"]

SUFFIX_MAP = {
    "drop_imbalanced": "imbalanced_drop",
    "mean_imbalanced": "imbalanced_mean",
    "mice_imbalanced": "imbalanced_mice",
    "agegroup_imbalanced": "imbalanced_agegroup",
    "augmented_imbalanced": "imbalanced_augmented",
    "drop_smote": "smote_drop",
    "mean_smote": "smote_mean",
    "mice_smote": "smote_mice",
    "agegroup_smote": "smote_agegroup",
    "augmented_smote": "smote_augmented",
}


def _apply_imputation(df, scaler, method):
    """Apply the specified imputation method to the dataframe.

    Args:
        df: Preprocessed dataframe with possible missing values.
        scaler: StandardScaler fitted during preprocessing.
        method: Imputation method name.

    Returns:
        Imputed dataframe.
    """
    if method == "drop":
        return impute_drop(df)
    elif method == "mean":
        return impute_mean(df)
    elif method == "mice":
        result = impute_mice(df)
        return result[0]  # Return df only, discard imputer
    elif method == "agegroup":
        return impute_age_group(df, scaler)
    elif method == "augmented":
        df_mean = impute_mean(df)
        df_mice, _ = impute_mice(df)
        df_age_group = impute_age_group(df, scaler)
        return create_augmented_dataset(df_mean, df_mice, df_age_group)
    else:
        raise ValueError(f"Unknown imputation method: {method}")


def train(imputation, balancing):
    """Train a single model variant.

    Args:
        imputation: Imputation method (drop, mean, mice, agegroup, augmented).
        balancing: Balancing strategy (imbalanced, smote).

    Returns:
        Tuple of (dse_model, metrics).
    """
    variant = f"{imputation}_{balancing}"
    variant_label = variant.upper().replace("_", " ")

    print(f"\n{'=' * 70}")
    print(f" {variant_label} TRAINING")
    print(f"{'=' * 70}")

    # Step 1: Load and preprocess data
    print("\n[Step 1] Loading dataset...")
    data = load_dataset()

    print("\n[Step 2] Preprocessing...")
    df, encoder, scaler = preprocess_basic(data)

    # Step 2: Apply imputation
    print(f"\n[Step 3] Applying {imputation} imputation strategy...")
    df_processed = _apply_imputation(df, scaler, imputation)

    # Step 3: Train-test split
    print("\n[Step 4] Splitting data...")
    X_train, X_test, y_train, y_test = prepare_train_test_split(df_processed)

    # Step 4: Apply SMOTE if requested
    if balancing == "smote":
        print("\n[Step 5] Applying SMOTE to balance training data...")
        X_train, y_train = apply_smote(X_train, y_train)

    print(f"Train set: {X_train.shape}")
    print(f"Test set: {X_test.shape}")

    # Step 5: Train all base models
    step = 6 if balancing == "smote" else 5
    print(f"\n[Step {step}] Training all base models...")
    results_df, models = train_all_models(X_train, y_train)
    print("\nModel Performance Ranking:")
    print(results_df.to_string(index=False))

    # Step 6: Get best model for meta-classifier
    best_model_name = results_df.iloc[0]["Model"]
    print(f"\nBest performing model: {best_model_name}")

    # Step 7: Fine-tune top 3 models
    step += 1
    print(f"\n[Step {step}] Fine-tuning top 3 models...")
    top_3_models = results_df.head(3)["Model"].tolist()
    tuned_models = fine_tune_top_models(top_3_models, models, X_train, y_train)

    # Step 8: Prepare models for ensemble
    base_models_for_ensemble = []
    for model_name, model in models.items():
        if model_name in tuned_models:
            base_models_for_ensemble.append((model_name, tuned_models[model_name]))
        else:
            base_models_for_ensemble.append((model_name, model))

    meta_classifier = RandomForestClassifier(n_estimators=100, random_state=SEED)
    if best_model_name in tuned_models:
        meta_classifier = tuned_models[best_model_name]

    # Step 9: Build DSE model
    step += 1
    print(f"\n[Step {step}] Building Dense Stacking Ensemble...")
    dse_model = build_dse_ensemble(
        base_models_for_ensemble, meta_classifier, X_train, y_train
    )

    # Step 10: Evaluate on test set
    step += 1
    print(f"\n[Step {step}] Evaluating final model...")
    metrics = evaluate_final_model(dse_model, X_test, y_test)

    # Step 11: Save model artifacts
    step += 1
    print(f"\n[Step {step}] Saving model artifacts...")
    folder_name = MODEL_DIRS[variant]
    suffix = SUFFIX_MAP[variant]
    save_model_artifacts(dse_model, scaler, encoder, X_train, folder_name, suffix)

    print(f"\n{'=' * 70}")
    print("TRAINING COMPLETED SUCCESSFULLY!")
    print(f"{'=' * 70}")

    return dse_model, metrics


def train_all_variants():
    """Train all 10 model variants (5 imputation x 2 balancing).

    Returns:
        Dictionary mapping variant names to their metrics.
    """
    print(f"\n{'=' * 70}")
    print(" STROKE PREDICTION MODEL TRAINING - ALL 10 VARIANTS")
    print(f"{'=' * 70}")

    results = {}
    total = len(IMPUTATION_METHODS) * len(BALANCING_OPTIONS)
    current = 0

    for balancing in BALANCING_OPTIONS:
        part = "IMBALANCED" if balancing == "imbalanced" else "SMOTE BALANCED"
        print(f"\n\n{'=' * 70}")
        print(f" PART: {part} DATASET VARIANTS")
        print(f"{'=' * 70}")

        for imputation in IMPUTATION_METHODS:
            current += 1
            variant = f"{imputation}_{balancing}"
            print(f"\n\n[{current}/{total}] Training: {variant}")
            print("-" * 70)

            try:
                _, metrics = train(imputation, balancing)
                results[variant] = metrics
            except Exception as e:
                print(f"Error training {variant}: {e}")
                results[variant] = None

    _print_summary(results)
    return results


def _print_summary(results):
    """Print training summary for all variants.

    Args:
        results: Dictionary mapping variant names to metrics dicts.
    """
    print(f"\n\n{'=' * 70}")
    print(" TRAINING SUMMARY - ALL MODELS")
    print(f"{'=' * 70}")

    successful = 0
    failed = 0

    for variant_name, metrics in results.items():
        if metrics:
            successful += 1
            label = variant_name.upper().replace("_", " ")
            print(f"\n  {label}:")
            print(f"   Accuracy:  {metrics['accuracy']:.4f}")
            print(f"   Precision: {metrics['precision']:.4f}")
            print(f"   Recall:    {metrics['recall']:.4f}")
            print(f"   F1-Score:  {metrics['f1']:.4f}")
            print(f"   AUC:       {metrics['auc']:.4f}")
        else:
            failed += 1
            label = variant_name.upper().replace("_", " ")
            print(f"\n  {label}: Failed to train")

    print(f"\n{'=' * 70}")
    print(f"Successfully trained: {successful}/{len(results)} models")
    print(f"Failed: {failed}/{len(results)} models")
    print(f"{'=' * 70}")


def main():
    """CLI entry point for training."""
    parser = argparse.ArgumentParser(
        description="Train stroke prediction models"
    )
    parser.add_argument(
        "--imputation",
        choices=IMPUTATION_METHODS,
        help="Imputation method to use",
    )
    parser.add_argument(
        "--balancing",
        choices=BALANCING_OPTIONS,
        default="imbalanced",
        help="Balancing strategy (default: imbalanced)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Train all 10 variants",
    )

    args = parser.parse_args()

    if args.all:
        return train_all_variants()
    elif args.imputation:
        _, metrics = train(args.imputation, args.balancing)
        return metrics
    else:
        parser.print_help()
        return None


if __name__ == "__main__":
    main()
