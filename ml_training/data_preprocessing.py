"""
Data preprocessing utilities for stroke prediction
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from imblearn.over_sampling import BorderlineSMOTE
import kagglehub
from config import *


def load_dataset():
    """Download and load the stroke prediction dataset from Kaggle"""
    print("Downloading dataset from Kaggle...")
    path = kagglehub.dataset_download("fedesoriano/stroke-prediction-dataset")
    data = pd.read_csv(f"{path}/healthcare-dataset-stroke-data.csv")
    print(f"Dataset loaded: {data.shape}")
    return data


def preprocess_basic(df):
    """
    Basic preprocessing: remove id, handle 'Other' gender, encode, scale
    Returns: df, encoder, scaler
    """
    df = df.copy()
    
    # Remove id column
    df = df.drop(['id'], axis=1)
    
    # Remove 'Other' gender
    df = df.drop(df[df['gender'] == 'Other'].index)
    
    # Map ever_married
    df['ever_married'] = df['ever_married'].map({'No': 0, 'Yes': 1})
    
    # One-Hot Encoding for categorical features
    encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    encoded_features = encoder.fit_transform(df[CATEGORICAL_COLS])
    new_feature_names = encoder.get_feature_names_out(CATEGORICAL_COLS)
    encoded_df = pd.DataFrame(encoded_features, columns=new_feature_names, index=df.index)
    
    # Drop original categorical columns and concatenate encoded
    df = df.drop(columns=CATEGORICAL_COLS)
    df = pd.concat([df, encoded_df], axis=1)
    
    # Remove extreme outliers using IQR method
    Q1 = df[NUMERICAL_COLS].quantile(0.25)
    Q3 = df[NUMERICAL_COLS].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 3 * IQR
    upper_bound = Q3 + 3 * IQR
    condition = ~((df[NUMERICAL_COLS] < lower_bound) | (df[NUMERICAL_COLS] > upper_bound)).any(axis=1)
    df = df[condition].copy()
    
    # Standard Normalization
    scaler = StandardScaler()
    df[NUMERICAL_COLS] = scaler.fit_transform(df[NUMERICAL_COLS])
    
    return df, encoder, scaler


def impute_drop(df):
    """Drop missing values"""
    df_drop = df.copy()
    df_drop = df_drop.dropna()
    print(f'After dropping missing values: {df_drop.shape}')
    return df_drop


def impute_mean(df):
    """Mean imputation for BMI"""
    df_mean = df.copy()
    df_mean['bmi'] = df['bmi'].fillna(df['bmi'].mean())
    print(f'Mean imputation completed: {df_mean.shape}')
    return df_mean


def impute_mice(df):
    """MICE imputation for BMI"""
    df_mice = df.copy()
    mice_imputer = IterativeImputer(random_state=SEED, max_iter=10)
    df_mice['bmi'] = mice_imputer.fit_transform(df_mice[['bmi']])
    print(f'MICE imputation completed: {df_mice.shape}')
    return df_mice, mice_imputer


def impute_age_group(df, scaler):
    """Age group-based mean imputation for BMI"""
    df_age_group = df.copy()
    
    # Get scaled age parameters
    age_col_index = NUMERICAL_COLS.index('age')
    mean_age_scaled = scaler.mean_[age_col_index]
    std_age_scaled = scaler.scale_[age_col_index]
    
    # Convert age boundaries to scaled values
    scaled_bins = [(val - mean_age_scaled) / std_age_scaled for val in ORIGINAL_AGE_BOUNDARIES]
    
    # Create age groups
    df_age_group['age_group'] = pd.cut(
        df_age_group['age'],
        bins=scaled_bins,
        labels=AGE_GROUP_LABELS,
        include_lowest=True
    )
    
    # Fill missing values with group mean
    df_age_group['bmi'] = df_age_group.groupby('age_group', observed=True)['bmi'].transform(
        lambda x: x.fillna(x.mean())
    )
    
    # Remove age_group column
    df_age_group = df_age_group.drop('age_group', axis=1)
    print(f'Age group imputation completed: {df_age_group.shape}')
    return df_age_group


def create_augmented_dataset(df_mean, df_mice, df_age_group):
    """
    Create augmented dataset by combining three imputation methods
    """
    # Select only important features
    df_mean_important = df_mean[IMPORTANT_FEATURES].copy()
    df_mice_important = df_mice[IMPORTANT_FEATURES].copy()
    df_age_group_important = df_age_group[IMPORTANT_FEATURES].copy()
    
    # Concatenate datasets
    augmented_dataset = pd.concat([
        df_mean_important,
        df_mice_important,
        df_age_group_important
    ], ignore_index=True)
    
    print(f'Before removing duplicates: {len(augmented_dataset)}')
    
    # Remove duplicates
    augmented_dataset = augmented_dataset.drop_duplicates()
    
    print(f'After removing duplicates: {len(augmented_dataset)}')
    print(f'Augmented dataset shape: {augmented_dataset.shape}')
    
    return augmented_dataset


def apply_smote(X_train, y_train):
    """Apply BorderlineSMOTE to balance the dataset"""
    smote = BorderlineSMOTE(random_state=SEED)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
    
    print(f'Before SMOTE: {X_train.shape}')
    print(f'After SMOTE: {X_train_resampled.shape}')
    print(f'Class distribution after SMOTE:')
    print(pd.Series(y_train_resampled).value_counts())
    
    return X_train_resampled, y_train_resampled


def prepare_train_test_split(df, test_size=TEST_SIZE):
    """
    Split data into train and test sets
    Returns: X_train, X_test, y_train, y_test
    """
    from sklearn.model_selection import train_test_split
    
    X = df.drop('stroke', axis=1)
    y = df['stroke']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=SEED,
        stratify=y
    )
    
    return X_train, X_test, y_train, y_test
