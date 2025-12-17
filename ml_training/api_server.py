"""
Flask API server for integrating ML models with React frontend
Run this file to start the prediction API server
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add ml_training to path
sys.path.append(os.path.dirname(__file__))

from predict_service import StrokePredictionService

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize multiple models (you can choose which one to use)
MODELS = {}

def load_models():
    """Load all trained models on startup"""
    model_configs = [
        {
            'name': 'drop_imbalanced',
            'dir': 'Model for Drop Missing Value Imbalanced',
            'suffix': 'imbalanced_drop'
        },
        {
            'name': 'augmented_smote',
            'dir': 'Model for Augmented SMOTE Dataset',
            'suffix': 'smote_augmented'
        },
        # Add more models as needed
    ]
    
    for config in model_configs:
        try:
            MODELS[config['name']] = StrokePredictionService(
                model_dir=config['dir'],
                model_suffix=config['suffix']
            )
            print(f"✅ Loaded model: {config['name']}")
        except Exception as e:
            print(f"❌ Failed to load {config['name']}: {e}")


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': list(MODELS.keys())
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict stroke risk
    
    Request body (JSON):
    {
        "age": 67,
        "gender": "Male",
        "hypertension": 0,
        "heart_disease": 1,
        "ever_married": "Yes",
        "work_type": "Private",
        "Residence_type": "Urban",
        "avg_glucose_level": 228.69,
        "bmi": 36.6,
        "smoking_status": "formerly smoked",
        "model": "drop_imbalanced"  // optional, default to first model
    }
    """
    try:
        data = request.json
        
        # Get model name (default to first available)
        model_name = data.pop('model', list(MODELS.keys())[0])
        
        if model_name not in MODELS:
            return jsonify({
                'error': f'Model not found: {model_name}',
                'available_models': list(MODELS.keys())
            }), 400
        
        # Validate required fields
        required_fields = [
            'age', 'gender', 'hypertension', 'heart_disease',
            'ever_married', 'work_type', 'Residence_type',
            'avg_glucose_level', 'bmi', 'smoking_status'
        ]
        
        missing_fields = [f for f in required_fields if f not in data]
        if missing_fields:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': missing_fields
            }), 400
        
        # Make prediction
        service = MODELS[model_name]
        result = service.predict(data)
        
        # Add model info to result
        result['model_used'] = model_name
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict-batch', methods=['POST'])
def predict_batch():
    """
    Predict stroke risk for multiple patients
    
    Request body (JSON):
    {
        "patients": [
            {patient_data_1},
            {patient_data_2},
            ...
        ],
        "model": "drop_imbalanced"  // optional
    }
    """
    try:
        data = request.json
        patients = data.get('patients', [])
        model_name = data.get('model', list(MODELS.keys())[0])
        
        if model_name not in MODELS:
            return jsonify({
                'error': f'Model not found: {model_name}'
            }), 400
        
        if not patients:
            return jsonify({'error': 'No patients provided'}), 400
        
        # Make predictions
        service = MODELS[model_name]
        results = service.predict_batch(patients)
        
        return jsonify({
            'model_used': model_name,
            'count': len(results),
            'results': results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/models', methods=['GET'])
def list_models():
    """List all available models"""
    return jsonify({
        'models': list(MODELS.keys())
    })


if __name__ == '__main__':
    print("="*70)
    print(" STROKE PREDICTION API SERVER")
    print("="*70)
    
    print("\nLoading models...")
    load_models()
    
    if not MODELS:
        print("❌ No models loaded! Please train models first.")
        sys.exit(1)
    
    print(f"\n✅ Loaded {len(MODELS)} models")
    print("\nStarting Flask server...")
    print("API will be available at: http://localhost:5000")
    print("\nEndpoints:")
    print("  GET  /api/health         - Health check")
    print("  GET  /api/models         - List available models")
    print("  POST /api/predict        - Single prediction")
    print("  POST /api/predict-batch  - Batch predictions")
    print("\n" + "="*70)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
