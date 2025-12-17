"""
Configuration file for stroke prediction model training
"""

# Random seed for reproducibility
SEED = 42

# Cross-validation folds
K_FOLD = 5

# Train-test split ratio
TEST_SIZE = 0.3

# Important features based on paper
IMPORTANT_FEATURES = [
    'age', 'bmi', 'avg_glucose_level', 
    'heart_disease', 'hypertension', 'ever_married', 'stroke'
]

# Numerical columns for scaling
NUMERICAL_COLS = ['age', 'avg_glucose_level', 'bmi']

# Categorical columns for encoding
CATEGORICAL_COLS = ['gender', 'work_type', 'Residence_type', 'smoking_status']

# Age group boundaries (for age-based imputation)
ORIGINAL_AGE_BOUNDARIES = [0, 20, 40, 60, 80, 100]
AGE_GROUP_LABELS = ['0-20', '21-40', '41-60', '61-80', '81+']

# Model hyperparameter grids
PARAM_GRIDS = {
    'Random Forest': {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 20, 30, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    },
    'XGBoost': {
        'n_estimators': [100, 200, 300],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1, 0.3],
        'subsample': [0.8, 0.9, 1.0]
    },
    'LightGBM': {
        'n_estimators': [100, 200, 300],
        'max_depth': [5, 10, 15],
        'learning_rate': [0.01, 0.1, 0.2],
        'num_leaves': [31, 50, 70]
    },
    'LR-AGD': {
        'C': [0.001, 0.01, 0.1, 1, 10],
        'max_iter': [100, 200, 500]
    },
    'Gradient Boosting': {
        'n_estimators': [100, 200],
        'learning_rate': [0.01, 0.1],
        'max_depth': [3, 5, 7]
    }
}

# Model output directories
MODEL_DIRS = {
    'drop_imbalanced': 'Model for Drop Missing Value Imbalanced',
    'mean_imbalanced': 'Model for Mean Imputation',
    'mice_imbalanced': 'Model for Mice Imputation Imbalanced',
    'agegroup_imbalanced': 'Model for Age Group Imputation Imbalanced',
    'augmented_imbalanced': 'Model for Augmented Imbalanced Dataset',
    'drop_smote': 'Model for Drop Missing Value SMOTE',
    'mean_smote': 'Model for Mean Imputation SMOTE',
    'mice_smote': 'Model for Mice Imputation SMOTE',
    'agegroup_smote': 'Model for Age Group Imputation SMOTE',
    'augmented_smote': 'Model for Augmented SMOTE Dataset'
}
