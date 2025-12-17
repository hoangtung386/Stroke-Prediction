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
import train_augmented_imbalanced
import train_drop_smote


def train_all_models():
    """Train all 10 model variants"""
    
    print("\n" + "="*70)
    print(" STROKE PREDICTION MODEL TRAINING - ALL VARIANTS")
    print("="*70)
    
    results = {}
    
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
    
    # 3. Augmented + Imbalanced
    print("\n\n[3/10] Training: Augmented Dataset + Imbalanced")
    print("-"*70)
    try:
        _, metrics = train_augmented_imbalanced.main()
        results['augmented_imbalanced'] = metrics
    except Exception as e:
        print(f"❌ Error: {e}")
        results['augmented_imbalanced'] = None
    
    # 4. Drop + SMOTE
    print("\n\n[4/10] Training: Drop Missing Values + SMOTE")
    print("-"*70)
    try:
        _, metrics = train_drop_smote.main()
        results['drop_smote'] = metrics
    except Exception as e:
        print(f"❌ Error: {e}")
        results['drop_smote'] = None
    
    # TODO: Add remaining 6 training scripts when created
    # 5. Mean + SMOTE
    # 6. MICE + Imbalanced
    # 7. MICE + SMOTE
    # 8. Age Group + Imbalanced
    # 9. Age Group + SMOTE
    # 10. Augmented + SMOTE
    
    print("\n\n" + "="*70)
    print(" TRAINING SUMMARY")
    print("="*70)
    
    for variant_name, metrics in results.items():
        if metrics:
            print(f"\n{variant_name.upper()}:")
            print(f"  Accuracy:  {metrics['accuracy']:.4f}")
            print(f"  Precision: {metrics['precision']:.4f}")
            print(f"  Recall:    {metrics['recall']:.4f}")
            print(f"  F1-Score:  {metrics['f1']:.4f}")
            print(f"  AUC:       {metrics['auc']:.4f}")
        else:
            print(f"\n{variant_name.upper()}: Failed to train")
    
    print("\n" + "="*70)
    print("✅ ALL TRAINING COMPLETED!")
    print("="*70)
    
    return results


def train_single_model(variant):
    """Train a single model variant"""
    
    variant_map = {
        'drop_imbalanced': train_drop_imbalanced,
        'mean_imbalanced': train_mean_imbalanced,
        'augmented_imbalanced': train_augmented_imbalanced,
        'drop_smote': train_drop_smote,
        # Add more as they are created
    }
    
    if variant not in variant_map:
        print(f"❌ Unknown variant: {variant}")
        print(f"Available variants: {list(variant_map.keys())}")
        return None
    
    print(f"\n🚀 Training model: {variant}")
    print("="*70)
    
    _, metrics = variant_map[variant].main()
    
    print(f"\n✅ Training completed for: {variant}")
    print(f"   Accuracy: {metrics['accuracy']:.4f}")
    
    return metrics


def main():
    parser = argparse.ArgumentParser(
        description='Train stroke prediction models'
    )
    parser.add_argument(
        '--variant',
        type=str,
        default='all',
        help='Model variant to train (default: all). Options: all, drop_imbalanced, mean_imbalanced, augmented_imbalanced, drop_smote'
    )
    
    args = parser.parse_args()
    
    if args.variant == 'all':
        results = train_all_models()
    else:
        results = train_single_model(args.variant)
    
    return results


if __name__ == "__main__":
    main()
