"""Stroke prediction service for loading models and making predictions."""

import os

import joblib
import pandas as pd

import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config import NUMERICAL_COLS, CATEGORICAL_COLS, RISK_THRESHOLDS


class StrokePredictionService:
    """Service class for stroke prediction using trained DSE models."""

    def __init__(self, model_dir, model_suffix):
        """Initialize the prediction service by loading model artifacts.

        Args:
            model_dir: Directory containing model artifacts.
            model_suffix: Suffix used when saving model (e.g., 'imbalanced_drop').
        """
        self.model_dir = model_dir
        self.model_suffix = model_suffix

        self.model = self._load_artifact(
            f"dse_stroke_prediction_{model_suffix}.pkl"
        )
        self.scaler = self._load_artifact(f"scaler_{model_suffix}.pkl")
        self.encoder = self._load_artifact(f"encoder_{model_suffix}.pkl")
        self.model_columns = self._load_artifact(
            f"model_columns_{model_suffix}.pkl"
        )

    def _load_artifact(self, filename):
        """Load a pickled artifact from the model directory.

        Args:
            filename: Name of the pickle file.

        Returns:
            Deserialized Python object.

        Raises:
            FileNotFoundError: If the artifact file does not exist.
        """
        filepath = os.path.join(self.model_dir, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Artifact not found: {filepath}")
        return joblib.load(filepath)

    def preprocess(self, data):
        """Preprocess raw patient data for model prediction.

        Args:
            data: Dictionary containing patient data fields.

        Returns:
            DataFrame ready for model prediction.
        """
        df = pd.DataFrame([data])

        df["ever_married"] = df["ever_married"].map({"Yes": 1, "No": 0})

        df[NUMERICAL_COLS] = self.scaler.transform(df[NUMERICAL_COLS].copy())

        encoded = self.encoder.transform(df[CATEGORICAL_COLS].copy())
        encoded_cols = self.encoder.get_feature_names_out(CATEGORICAL_COLS)
        encoded_df = pd.DataFrame(
            encoded, columns=encoded_cols, index=df.index
        )

        df = df.drop(columns=CATEGORICAL_COLS)
        df = pd.concat([df, encoded_df], axis=1)

        for col in self.model_columns:
            if col not in df.columns:
                df[col] = 0

        return df[self.model_columns]

    def predict(self, data):
        """Make a stroke risk prediction for a single patient.

        Args:
            data: Dictionary containing patient data fields.

        Returns:
            Dictionary with prediction, probability, risk_level,
            confidence, and interpretation.
        """
        processed = self.preprocess(data)

        prediction = self.model.predict(processed)[0]
        probability = self.model.predict_proba(processed)[0]

        stroke_prob = probability[1]
        risk_level = self._get_risk_level(stroke_prob)
        confidence = abs(stroke_prob - 0.5) * 2

        return {
            "prediction": int(prediction),
            "probability": float(stroke_prob),
            "no_stroke_probability": float(probability[0]),
            "risk_level": risk_level,
            "confidence": float(confidence),
            "interpretation": self._interpret_result(
                prediction, stroke_prob, risk_level
            ),
        }

    def predict_batch(self, patients):
        """Make predictions for multiple patients.

        Args:
            patients: List of patient data dictionaries.

        Returns:
            List of prediction result dictionaries.
        """
        results = []
        for patient in patients:
            try:
                results.append(self.predict(patient))
            except Exception as e:
                results.append({"error": str(e)})
        return results

    @staticmethod
    def _get_risk_level(probability):
        """Classify stroke probability into a risk level.

        Args:
            probability: Stroke probability (0.0 to 1.0).

        Returns:
            Risk level string: 'Low', 'Medium', or 'High'.
        """
        if probability < RISK_THRESHOLDS["low"]:
            return "Low"
        elif probability < RISK_THRESHOLDS["medium"]:
            return "Medium"
        return "High"

    @staticmethod
    def _interpret_result(prediction, probability, risk_level):
        """Generate a human-readable interpretation of the prediction.

        Args:
            prediction: Binary prediction (0 or 1).
            probability: Stroke probability.
            risk_level: Classified risk level string.

        Returns:
            Interpretation string.
        """
        if prediction == 1:
            return (
                f"High stroke risk detected ({probability:.1%} probability). "
                f"Risk level: {risk_level}. "
                "Recommend immediate consultation with a healthcare "
                "professional."
            )
        if risk_level == "Medium":
            return (
                f"Moderate stroke risk ({probability:.1%} probability). "
                "Monitor health factors and consider lifestyle modifications."
            )
        return (
            f"Low stroke risk ({probability:.1%} probability). "
            "Continue maintaining a healthy lifestyle."
        )
