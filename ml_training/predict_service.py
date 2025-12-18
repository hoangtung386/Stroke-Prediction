"""
Stroke Prediction Service
Handles loading trained models and making predictions
"""
import joblib
import pandas as pd
import numpy as np
import os
from config import NUMERICAL_COLS, CATEGORICAL_COLS


class StrokePredictionService:
    """
    Service class for stroke prediction using trained models
    """
    
    def __init__(self, model_dir: str, model_suffix: str):
        """
        Initialize the prediction service
        
        Args:
            model_dir: Directory containing model artifacts
            model_suffix: Suffix used when saving model (e.g., 'imbalanced_drop')
        """
        self.model_dir = model_dir
        self.model_suffix = model_suffix
        
        # Load model artifacts
        self.model = self._load_artifact(f'dse_stroke_prediction_{model_suffix}.pkl')
        self.scaler = self._load_artifact(f'scaler_{model_suffix}.pkl')
        self.encoder = self._load_artifact(f'encoder_{model_suffix}.pkl')
        self.model_columns = self._load_artifact(f'model_columns_{model_suffix}.pkl')
        
    def _load_artifact(self, filename: str):
        """Load a pickled artifact from the model directory"""
        filepath = os.path.join(self.model_dir, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Artifact not found: {filepath}")
        return joblib.load(filepath)
    
    def preprocess(self, data: dict) -> pd.DataFrame:
        """
        Preprocess input data for prediction
        
        Args:
            data: Dictionary containing patient data
            
        Returns:
            Preprocessed DataFrame ready for prediction
        """
        # Convert to DataFrame
        df = pd.DataFrame([data])
        
        # Handle binary columns
        df['ever_married'] = df['ever_married'].map({'Yes': 1, 'No': 0})
        
        # Scale numerical features
        numerical_data = df[NUMERICAL_COLS].copy()
        df[NUMERICAL_COLS] = self.scaler.transform(numerical_data)
        
        # Encode categorical features
        categorical_data = df[CATEGORICAL_COLS].copy()
        encoded = self.encoder.transform(categorical_data)
        
        # Get encoded column names from encoder
        encoded_cols = self.encoder.get_feature_names_out(CATEGORICAL_COLS)
        encoded_df = pd.DataFrame(encoded, columns=encoded_cols, index=df.index)
        
        # Drop original categorical columns and add encoded ones
        df = df.drop(columns=CATEGORICAL_COLS)
        df = pd.concat([df, encoded_df], axis=1)
        
        # Ensure all expected columns are present
        for col in self.model_columns:
            if col not in df.columns:
                df[col] = 0
        
        # Reorder columns to match training
        df = df[self.model_columns]
        
        return df
    
    def predict(self, data: dict) -> dict:
        """
        Make a prediction for a single patient
        
        Args:
            data: Dictionary containing patient data
            
        Returns:
            Dictionary with prediction results
        """
        # Preprocess data
        processed = self.preprocess(data)
        
        # Make prediction
        prediction = self.model.predict(processed)[0]
        probability = self.model.predict_proba(processed)[0]
        
        # Calculate risk level
        stroke_prob = probability[1]
        if stroke_prob < 0.3:
            risk_level = 'Low'
        elif stroke_prob < 0.6:
            risk_level = 'Medium'
        else:
            risk_level = 'High'
        
        # Calculate confidence
        confidence = abs(stroke_prob - 0.5) * 2  # 0 to 1 scale
        
        return {
            'prediction': int(prediction),
            'probability': float(stroke_prob),
            'no_stroke_probability': float(probability[0]),
            'risk_level': risk_level,
            'confidence': float(confidence),
            'interpretation': self._interpret_result(prediction, stroke_prob, risk_level)
        }
    
    def predict_batch(self, patients: list) -> list:
        """
        Make predictions for multiple patients
        
        Args:
            patients: List of patient data dictionaries
            
        Returns:
            List of prediction results
        """
        results = []
        for patient in patients:
            try:
                result = self.predict(patient)
                results.append(result)
            except Exception as e:
                results.append({'error': str(e)})
        return results
    
    def _interpret_result(self, prediction: int, probability: float, risk_level: str) -> str:
        """Generate human-readable interpretation of the prediction"""
        if prediction == 1:
            return (
                f"High stroke risk detected ({probability:.1%} probability). "
                f"Risk level: {risk_level}. "
                "Recommend immediate consultation with a healthcare professional."
            )
        else:
            if risk_level == 'Medium':
                return (
                    f"Moderate stroke risk ({probability:.1%} probability). "
                    "Monitor health factors and consider lifestyle modifications."
                )
            else:
                return (
                    f"Low stroke risk ({probability:.1%} probability). "
                    "Continue maintaining a healthy lifestyle."
                )
