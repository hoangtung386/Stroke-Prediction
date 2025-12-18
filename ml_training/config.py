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
    'drop_imbalanced': 'models/drop_imbalanced',
    'mean_imbalanced': 'models/mean_imbalanced',
    'mice_imbalanced': 'models/mice_imbalanced',
    'agegroup_imbalanced': 'models/agegroup_imbalanced',
    'augmented_imbalanced': 'models/augmented_imbalanced',
    'drop_smote': 'models/drop_smote',
    'mean_smote': 'models/mean_smote',
    'mice_smote': 'models/mice_smote',
    'agegroup_smote': 'models/agegroup_smote',
    'augmented_smote': 'models/augmented_smote'
}
