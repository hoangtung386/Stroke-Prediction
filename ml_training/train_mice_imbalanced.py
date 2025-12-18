"""
Training script for MICE Imputation + Imbalanced dataset
"""
import warnings
warnings.filterwarnings('ignore')

from data_preprocessing import *
from model_utils import *
from config import *


def main():
    print("="*70)
    print(" MICE IMPUTATION + IMBALANCED DATASET TRAINING")
    print("="*70)
    
    # 1. Load and preprocess data
    print("\n[Step 1] Loading dataset...")
    data = load_dataset()
    
    print("\n[Step 2] Preprocessing...")
    df, encoder, scaler = preprocess_basic(data)
    
    print("\n[Step 3] Applying MICE Imputation strategy...")
    df_processed, _ = impute_mice(df)
    
    # 2. Prepare train-test split
    print("\n[Step 4] Splitting data...")
    X_train, X_test, y_train, y_test = prepare_train_test_split(df_processed)
    print(f"Train set: {X_train.shape}")
    print(f"Test set: {X_test.shape}")
    
    # 3. Train all models
    print("\n[Step 5] Training all base models...")
    results_df, models = train_all_models(X_train, y_train)
    print("\n📊 Model Performance Ranking:")
    print(results_df.to_string(index=False))
    
    # 4. Get best model for meta-classifier
    best_model_name = results_df.iloc[0]['Model']
    print(f"\n🏆 Best performing model: {best_model_name}")
    
    # 5. Fine-tune top 3 models
    print("\n[Step 6] Fine-tuning top 3 models...")
    top_3_models = results_df.head(3)['Model'].tolist()
    tuned_models = fine_tune_top_models(top_3_models, models, X_train, y_train)
    
    # 6. Prepare models for ensemble
    base_models_for_ensemble = []
    for model_name, model in models.items():
        if model_name in tuned_models:
            base_models_for_ensemble.append((model_name, tuned_models[model_name]))
        else:
            base_models_for_ensemble.append((model_name, model))
    
    # Set meta-classifier
    meta_classifier = RandomForestClassifier(n_estimators=100, random_state=SEED)
    if best_model_name in tuned_models:
        meta_classifier = tuned_models[best_model_name]
    
    # 7. Build DSE model
    print("\n[Step 7] Building Dense Stacking Ensemble...")
    dse_model = build_dse_ensemble(base_models_for_ensemble, meta_classifier, X_train, y_train)
    
    # 8. Evaluate on test set
    print("\n[Step 8] Evaluating final model...")
    metrics = evaluate_final_model(dse_model, X_test, y_test)
    
    # 9. Save model artifacts
    print("\n[Step 9] Saving model artifacts...")
    folder_name = MODEL_DIRS['mice_imbalanced']
    save_model_artifacts(
        dse_model, scaler, encoder, X_train,
        folder_name, 'imbalanced_mice'
    )
    
    print("\n" + "="*70)
    print("✅ TRAINING COMPLETED SUCCESSFULLY!")
    print("="*70)
    
    return dse_model, metrics


if __name__ == "__main__":
    model, metrics = main()
