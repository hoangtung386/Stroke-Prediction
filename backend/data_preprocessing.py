"""Data preprocessing utilities for stroke prediction."""

import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import IterativeImputer
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import BorderlineSMOTE
import kagglehub

from config import (
    SEED,
    TEST_SIZE,
    NUMERICAL_COLS,
    CATEGORICAL_COLS,
    ORIGINAL_AGE_BOUNDARIES,
    AGE_GROUP_LABELS,
    IMPORTANT_FEATURES,
)


def load_dataset():
    """Download and load the stroke prediction dataset from Kaggle.

    Returns:
        DataFrame with raw stroke prediction data.
    """
    print("Downloading dataset from Kaggle...")
    path = kagglehub.dataset_download("fedesoriano/stroke-prediction-dataset")
    data = pd.read_csv(f"{path}/healthcare-dataset-stroke-data.csv")
    print(f"Dataset loaded: {data.shape}")
    return data


def preprocess_basic(df):
    """Apply basic preprocessing: remove id, encode, scale, remove outliers.

    Args:
        df: Raw dataframe from load_dataset().

    Returns:
        Tuple of (processed_df, encoder, scaler).
    """
    df = df.copy()

    df = df.drop(["id"], axis=1)
    df = df.drop(df[df["gender"] == "Other"].index)

    df["ever_married"] = df["ever_married"].map({"No": 0, "Yes": 1})

    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    encoded_features = encoder.fit_transform(df[CATEGORICAL_COLS])
    new_feature_names = encoder.get_feature_names_out(CATEGORICAL_COLS)
    encoded_df = pd.DataFrame(
        encoded_features, columns=new_feature_names, index=df.index
    )

    df = df.drop(columns=CATEGORICAL_COLS)
    df = pd.concat([df, encoded_df], axis=1)

    q1 = df[NUMERICAL_COLS].quantile(0.25)
    q3 = df[NUMERICAL_COLS].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 3 * iqr
    upper_bound = q3 + 3 * iqr
    mask = ~(
        (df[NUMERICAL_COLS] < lower_bound) | (df[NUMERICAL_COLS] > upper_bound)
    ).any(axis=1)
    df = df[mask].copy()

    scaler = StandardScaler()
    df[NUMERICAL_COLS] = scaler.fit_transform(df[NUMERICAL_COLS])

    return df, encoder, scaler


def impute_drop(df):
    """Drop rows with missing values.

    Args:
        df: Preprocessed dataframe.

    Returns:
        Dataframe with missing rows removed.
    """
    result = df.dropna()
    print(f"After dropping missing values: {result.shape}")
    return result


def impute_mean(df):
    """Fill missing BMI values with column mean.

    Args:
        df: Preprocessed dataframe.

    Returns:
        Dataframe with mean-imputed BMI.
    """
    result = df.copy()
    result["bmi"] = result["bmi"].fillna(result["bmi"].mean())
    print(f"Mean imputation completed: {result.shape}")
    return result


def impute_mice(df):
    """Apply MICE (Multiple Imputation by Chained Equations) for BMI.

    Args:
        df: Preprocessed dataframe.

    Returns:
        Tuple of (imputed_df, mice_imputer).
    """
    result = df.copy()
    mice_imputer = IterativeImputer(random_state=SEED, max_iter=10)
    result["bmi"] = mice_imputer.fit_transform(result[["bmi"]])
    print(f"MICE imputation completed: {result.shape}")
    return result, mice_imputer


def impute_age_group(df, scaler):
    """Apply age group-based mean imputation for BMI.

    Args:
        df: Preprocessed dataframe.
        scaler: StandardScaler fitted during preprocessing.

    Returns:
        Dataframe with age-group imputed BMI.
    """
    result = df.copy()

    age_col_index = NUMERICAL_COLS.index("age")
    mean_age = scaler.mean_[age_col_index]
    std_age = scaler.scale_[age_col_index]

    scaled_bins = [
        (val - mean_age) / std_age for val in ORIGINAL_AGE_BOUNDARIES
    ]

    result["age_group"] = pd.cut(
        result["age"],
        bins=scaled_bins,
        labels=AGE_GROUP_LABELS,
        include_lowest=True,
    )
    result["bmi"] = result.groupby("age_group", observed=True)[
        "bmi"
    ].transform(lambda x: x.fillna(x.mean()))
    result = result.drop("age_group", axis=1)

    print(f"Age group imputation completed: {result.shape}")
    return result


def create_augmented_dataset(df_mean, df_mice, df_age_group):
    """Combine three imputation methods into an augmented dataset.

    Args:
        df_mean: Mean-imputed dataframe.
        df_mice: MICE-imputed dataframe.
        df_age_group: Age group-imputed dataframe.

    Returns:
        Augmented dataframe with duplicates removed.
    """
    df_mean_imp = df_mean[IMPORTANT_FEATURES].copy()
    df_mice_imp = df_mice[IMPORTANT_FEATURES].copy()
    df_age_imp = df_age_group[IMPORTANT_FEATURES].copy()

    augmented = pd.concat(
        [df_mean_imp, df_mice_imp, df_age_imp], ignore_index=True
    )
    print(f"Before removing duplicates: {len(augmented)}")

    augmented = augmented.drop_duplicates()
    print(f"After removing duplicates: {len(augmented)}")
    print(f"Augmented dataset shape: {augmented.shape}")

    return augmented


def apply_smote(x_train, y_train):
    """Apply BorderlineSMOTE to balance the training dataset.

    Args:
        x_train: Training features.
        y_train: Training labels.

    Returns:
        Tuple of (resampled_features, resampled_labels).
    """
    smote = BorderlineSMOTE(random_state=SEED)
    x_resampled, y_resampled = smote.fit_resample(x_train, y_train)

    print(f"Before SMOTE: {x_train.shape}")
    print(f"After SMOTE: {x_resampled.shape}")
    print("Class distribution after SMOTE:")
    print(pd.Series(y_resampled).value_counts())

    return x_resampled, y_resampled


def prepare_train_test_split(df, test_size=TEST_SIZE):
    """Split data into stratified train and test sets.

    Args:
        df: Dataframe with features and 'stroke' target column.
        test_size: Fraction of data for testing.

    Returns:
        Tuple of (X_train, X_test, y_train, y_test).
    """
    x = df.drop("stroke", axis=1)
    y = df["stroke"]

    return train_test_split(
        x, y,
        test_size=test_size,
        random_state=SEED,
        stratify=y,
    )
