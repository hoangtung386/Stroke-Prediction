"""
Main orchestrator for training all model variants
Run this file to train all 10 model combinations
"""
import argparse
import warnings
warnings.filterwarnings('ignore')

# Import all training scripts
import train_drop_imbalanced
import train_mean_imbalanced
import train_mice_imbalanced
import train_agegroup_imbalanced
import train_augmented_imbalanced
import train_drop_smote
import train_mean_smote
import train_mice_smote
import train_agegroup_smote
import train_augmented_smote


def train_all_models():
    """Train all 10 model variants"""
    
    print("\n" + "="*70)
    print(" STROKE PREDICTION MODEL TRAINING - ALL 10 VARIANTS")
    print("="*70)
    
    results = {}
    
    # IMBALANCED VARIANTS
    print("\n\n" + "="*70)
    print(" PART 1: IMBALANCED DATASET VARIANTS")
    print("="*70)
    
    # 1. Drop + Imbalanced
    print("\n\n[1/10] Training: Drop Missing Values + Imbalanced")
    print("-"*70)
    try:
        _, metrics = train_drop_imbalanced.main()
        results['drop_imbalanced'] = metrics
    except Exception as e:
        print(f"❌ Error: {e}")
        results['drop_imbalanced'] = None
    
    # 2. Mean + Imbalanced
    print("\n\n[2/10] Training: Mean Imputation + Imbalanced")
    print("-"*70)
    try:
        _, metrics = train_mean_imbalanced.main()
        results['mean_imbalanced'] = metrics
    except Exception as e:
        print(f"❌ Error: {e}")
        results['mean_imbalanced'] = None
    
    # 3. MICE + Imbalanced
    print("\n\n[3/10] Training: MICE Imputation + Imbalanced")
    print("-"*70)
    try:
        _, metrics = train_mice_imbalanced.main()
        results['mice_imbalanced'] = metrics
    except Exception as e:
        print(f"❌ Error: {e}")
        results['mice_imbalanced'] = None
    
    # 4. Age Group + Imbalanced
    print("\n\n[4/10] Training: Age Group Imputation + Imbalanced")
    print("-"*70)
    try:
        _, metrics = train_agegroup_imbalanced.main()
        results['agegroup_imbalanced'] = metrics
    except Exception as e:
        print(f"❌ Error: {e}")
        results['agegroup_imbalanced'] = None
    
    # 5. Augmented + Imbalanced
    print("\n\n[5/10] Training: Augmented Dataset + Imbalanced")
    print("-"*70)
    try:
        _, metrics = train_augmented_imbalanced.main()
        results['augmented_imbalanced'] = metrics
    except Exception as e:
        print(f"❌ Error: {e}")
        results['augmented_imbalanced'] = None
    
    # SMOTE VARIANTS
    print("\n\n" + "="*70)
    print(" PART 2: SMOTE BALANCED DATASET VARIANTS")
    print("="*70)
    
    # 6. Drop + SMOTE
    print("\n\n[6/10] Training: Drop Missing Values + SMOTE")
    print("-"*70)
    try:
        _, metrics = train_drop_smote.main()
        results['drop_smote'] = metrics
    except Exception as e:
        print(f"❌ Error: {e}")
        results['drop_smote'] = None
    
    # 7. Mean + SMOTE
    print("\n\n[7/10] Training: Mean Imputation + SMOTE")
    print("-"*70)
    try:
        _, metrics = train_mean_smote.main()
        results['mean_smote'] = metrics
    except Exception as e:
        print(f"❌ Error: {e}")
        results['mean_smote'] = None
    
    # 8. MICE + SMOTE
    print("\n\n[8/10] Training: MICE Imputation + SMOTE")
    print("-"*70)
    try:
        _, metrics = train_mice_smote.main()
        results['mice_smote'] = metrics
    except Exception as e:
        print(f"❌ Error: {e}")
        results['mice_smote'] = None
    
    # 9. Age Group + SMOTE
    print("\n\n[9/10] Training: Age Group Imputation + SMOTE")
    print("-"*70)
    try:
        _, metrics = train_agegroup_smote.main()
        results['agegroup_smote'] = metrics
    except Exception as e:
        print(f"❌ Error: {e}")
        results['agegroup_smote'] = None
    
    # 10. Augmented + SMOTE
    print("\n\n[10/10] Training: Augmented Dataset + SMOTE")
    print("-"*70)
    try:
        _, metrics = train_augmented_smote.main()
        results['augmented_smote'] = metrics
    except Exception as e:
        print(f"❌ Error: {e}")
        results['augmented_smote'] = None
    
    # Print summary
    print("\n\n" + "="*70)
    print(" TRAINING SUMMARY - ALL 10 MODELS")
    print("="*70)
    
    successful_count = 0
    failed_count = 0
    
    for variant_name, metrics in results.items():
        if metrics:
            successful_count += 1
            print(f"\n✅ {variant_name.upper().replace('_', ' ')}:")
            print(f"   Accuracy:  {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
            print(f"   Precision: {metrics['precision']:.4f}")
            print(f"   Recall:    {metrics['recall']:.4f}")
            print(f"   F1-Score:  {metrics['f1']:.4f}")
            print(f"   AUC:       {metrics['auc']:.4f}")
        else:
            failed_count += 1
            print(f"\n❌ {variant_name.upper().replace('_', ' ')}: Failed to train")
    
    print("\n" + "="*70)
    print(f"✅ Successfully trained: {successful_count}/10 models")
    print(f"❌ Failed: {failed_count}/10 models")
    print("="*70)
    
    return results


def train_single_model(variant):
    """Train a single model variant"""
    
    variant_map = {
        'drop_imbalanced': train_drop_imbalanced,
        'mean_imbalanced': train_mean_imbalanced,
        'mice_imbalanced': train_mice_imbalanced,
        'agegroup_imbalanced': train_agegroup_imbalanced,
        'augmented_imbalanced': train_augmented_imbalanced,
        'drop_smote': train_drop_smote,
        'mean_smote': train_mean_smote,
        'mice_smote': train_mice_smote,
        'agegroup_smote': train_agegroup_smote,
        'augmented_smote': train_augmented_smote,
    }
    
    if variant not in variant_map:
        print(f"❌ Unknown variant: {variant}")
        print(f"\nAvailable variants:")
        for i, v in enumerate(variant_map.keys(), 1):
            print(f"  {i}. {v}")
        return None
    
    print(f"\n🚀 Training model: {variant.upper().replace('_', ' ')}")
    print("="*70)
    
    _, metrics = variant_map[variant].main()
    
    print(f"\n✅ Training completed for: {variant}")
    print(f"   Accuracy: {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
    
    return metrics


def main():
    parser = argparse.ArgumentParser(
        description='Train stroke prediction models - All 10 variants available'
    )
    parser.add_argument(
        '--variant',
        type=str,
        default='all',
        help='Model variant to train (default: all). Options: all, drop_imbalanced, mean_imbalanced, mice_imbalanced, agegroup_imbalanced, augmented_imbalanced, drop_smote, mean_smote, mice_smote, agegroup_smote, augmented_smote'
    )
    
    args = parser.parse_args()
    
    if args.variant == 'all':
        results = train_all_models()
    else:
        results = train_single_model(args.variant)
    
    return results


if __name__ == "__main__":
    main()
