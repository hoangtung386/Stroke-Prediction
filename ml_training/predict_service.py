"""
Prediction service for web integration
This module loads trained models and provides prediction interface
"""
import joblib
import pandas as pd
import numpy as np
import os


class StrokePredictionService:
    """
    Service class to load and use trained stroke prediction models
    """
    
    def __init__(self, model_dir, model_suffix):
        """
        Initialize the service with a trained model
        
        Args:
            model_dir: Directory containing the model artifacts
            model_suffix: Suffix of the model files (e.g., 'imbalanced_drop', 'smote_mean')
        """
        self.model_dir = model_dir
        self.model_suffix = model_suffix
        
        # Load model artifacts
        self.model = self._load_artifact(f'dse_stroke_prediction_{model_suffix}.pkl')
        self.scaler = self._load_artifact(f'scaler_{model_suffix}.pkl')
        self.encoder = self._load_artifact(f'encoder_{model_suffix}.pkl')
        self.model_columns = self._load_artifact(f'model_columns_{model_suffix}.pkl')
        
        print(f"✅ Model loaded from: {model_dir}")
        print(f"📊 Model expects {len(self.model_columns)} features")
    
    def _load_artifact(self, filename):
        """Load a model artifact file"""
        filepath = os.path.join(self.model_dir, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model artifact not found: {filepath}")
        return joblib.load(filepath)
    
    def preprocess_input(self, patient_data):
        """
        Preprocess patient data for prediction
        
        Args:
            patient_data: dict with patient information
                Required keys: age, gender, hypertension, heart_disease, 
                              ever_married, work_type, Residence_type, 
                              avg_glucose_level, bmi, smoking_status
        
        Returns:
            Preprocessed DataFrame ready for prediction
        """
        # Create DataFrame from patient data
        df = pd.DataFrame([patient_data])
        
        # Encode categorical variables
        categorical_cols = ['gender', 'work_type', 'Residence_type', 'smoking_status']
        
        # One-Hot Encoding
        encoded_features = self.encoder.transform(df[categorical_cols])
        feature_names = self.encoder.get_feature_names_out(categorical_cols)
        encoded_df = pd.DataFrame(encoded_features, columns=feature_names, index=df.index)
        
        # Drop original categorical columns
        df = df.drop(columns=categorical_cols)
        
        # Concatenate encoded features
        df = pd.concat([df, encoded_df], axis=1)
        
        # Scale numerical features
        numerical_cols = ['age', 'avg_glucose_level', 'bmi']
        df[numerical_cols] = self.scaler.transform(df[numerical_cols])
        
        # Ensure all required columns are present
        for col in self.model_columns:
            if col not in df.columns:
                df[col] = 0
        
        # Reorder columns to match training data
        df = df[self.model_columns]
        
        return df
    
    def predict(self, patient_data):
        """
        Predict stroke risk for a patient
        
        Args:
            patient_data: dict with patient information
        
        Returns:
            dict with prediction results:
                - prediction: 0 (no stroke) or 1 (stroke)
                - probability: float, probability of stroke (0-1)
                - risk_level: str, risk category
                - confidence: float, model confidence
        """
        # Preprocess input
        processed_data = self.preprocess_input(patient_data)
        
        # Make prediction
        prediction = self.model.predict(processed_data)[0]
        probabilities = self.model.predict_proba(processed_data)[0]
        
        stroke_probability = probabilities[1]  # Probability of stroke (class 1)
        
        # Determine risk level
        if stroke_probability < 0.3:
            risk_level = "Low"
        elif stroke_probability < 0.6:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        # Calculate confidence
        confidence = max(probabilities)
        
        return {
            'prediction': int(prediction),
            'probability': float(stroke_probability),
            'risk_level': risk_level,
            'confidence': float(confidence),
            'probability_no_stroke': float(probabilities[0]),
            'probability_stroke': float(probabilities[1])
        }
    
    def predict_batch(self, patients_list):
        """
        Predict stroke risk for multiple patients
        
        Args:
            patients_list: list of patient data dicts
        
        Returns:
            list of prediction results
        """
        results = []
        for patient_data in patients_list:
            result = self.predict(patient_data)
            results.append(result)
        return results
    
    def get_feature_importance(self):
        """
        Get feature importance if available
        (Only works if final estimator has feature_importances_ attribute)
        """
        if hasattr(self.model.final_estimator_, 'feature_importances_'):
            importances = self.model.final_estimator_.feature_importances_
            feature_importance_df = pd.DataFrame({
                'feature': self.model_columns,
                'importance': importances
            }).sort_values('importance', ascending=False)
            return feature_importance_df
        else:
            return None


# Example usage function
def example_usage():
    """Example of how to use the prediction service"""
    
    # Initialize service with a trained model
    service = StrokePredictionService(
        model_dir='Model for Drop Missing Value Imbalanced',
        model_suffix='imbalanced_drop'
    )
    
    # Example patient data
    patient_data = {
        'age': 67,
        'gender': 'Male',
        'hypertension': 0,
        'heart_disease': 1,
        'ever_married': 'Yes',
        'work_type': 'Private',
        'Residence_type': 'Urban',
        'avg_glucose_level': 228.69,
        'bmi': 36.6,
        'smoking_status': 'formerly smoked'
    }
    
    # Make prediction
    result = service.predict(patient_data)
    
    print("="*50)
    print("PREDICTION RESULT")
    print("="*50)
    print(f"Prediction: {'Stroke' if result['prediction'] == 1 else 'No Stroke'}")
    print(f"Stroke Probability: {result['probability']:.2%}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Confidence: {result['confidence']:.2%}")
    print("="*50)
    
    return result


if __name__ == "__main__":
    # Run example
    example_usage()
