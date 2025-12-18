"""
Enhanced Flask API server with auto model loading
Run this file to start the prediction API server with all trained models
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import glob

# Add ml_training to path
sys.path.append(os.path.dirname(__file__))

from predict_service import StrokePredictionService
from config import MODEL_DIRS

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Global models dictionary
MODELS = {}

def auto_discover_models():
    """
    Automatically discover and load all trained models
    """
    print("\n" + "="*70)
    print(" AUTO-DISCOVERING TRAINED MODELS")
    print("="*70)
    
    # Model configurations with human-readable names
    model_configs = [
        {
            'id': 'drop_imbalanced',
            'name': 'Drop + Imbalanced',
            'description': 'Drop missing values, imbalanced dataset',
            'dir': MODEL_DIRS['drop_imbalanced'],
            'suffix': 'imbalanced_drop'
        },
        {
            'id': 'mean_imbalanced',
            'name': 'Mean + Imbalanced',
            'description': 'Mean imputation, imbalanced dataset',
            'dir': MODEL_DIRS['mean_imbalanced'],
            'suffix': 'imbalanced_mean'
        },
        {
            'id': 'mice_imbalanced',
            'name': 'MICE + Imbalanced',
            'description': 'MICE imputation, imbalanced dataset',
            'dir': MODEL_DIRS['mice_imbalanced'],
            'suffix': 'imbalanced_mice'
        },
        {
            'id': 'agegroup_imbalanced',
            'name': 'Age Group + Imbalanced',
            'description': 'Age group imputation, imbalanced dataset',
            'dir': MODEL_DIRS['agegroup_imbalanced'],
            'suffix': 'imbalanced_agegroup'
        },
        {
            'id': 'augmented_imbalanced',
            'name': 'Augmented + Imbalanced',
            'description': 'Augmented dataset (3 methods), imbalanced',
            'dir': MODEL_DIRS['augmented_imbalanced'],
            'suffix': 'imbalanced_augmented'
        },
        {
            'id': 'drop_smote',
            'name': 'Drop + SMOTE',
            'description': 'Drop missing values, SMOTE balanced',
            'dir': MODEL_DIRS['drop_smote'],
            'suffix': 'smote_drop'
        },
        {
            'id': 'mean_smote',
            'name': 'Mean + SMOTE',
            'description': 'Mean imputation, SMOTE balanced',
            'dir': MODEL_DIRS['mean_smote'],
            'suffix': 'smote_mean'
        },
        {
            'id': 'mice_smote',
            'name': 'MICE + SMOTE',
            'description': 'MICE imputation, SMOTE balanced',
            'dir': MODEL_DIRS['mice_smote'],
            'suffix': 'smote_mice'
        },
        {
            'id': 'agegroup_smote',
            'name': 'Age Group + SMOTE',
            'description': 'Age group imputation, SMOTE balanced',
            'dir': MODEL_DIRS['agegroup_smote'],
            'suffix': 'smote_agegroup'
        },
        {
            'id': 'augmented_smote',
            'name': 'Augmented + SMOTE',
            'description': 'Augmented dataset (3 methods), SMOTE balanced',
            'dir': MODEL_DIRS['augmented_smote'],
            'suffix': 'smote_augmented'
        }
    ]
    
    loaded_count = 0
    failed_count = 0
    
    for config in model_configs:
        # Check if model directory exists
        if not os.path.exists(config['dir']):
            print(f"⏭️  Skipping {config['name']}: Directory not found")
            failed_count += 1
            continue
        
        try:
            service = StrokePredictionService(
                model_dir=config['dir'],
                model_suffix=config['suffix']
            )
            
            MODELS[config['id']] = {
                'service': service,
                'name': config['name'],
                'description': config['description'],
                'dir': config['dir']
            }
            
            print(f"✅ Loaded: {config['name']}")
            loaded_count += 1
            
        except FileNotFoundError as e:
            print(f"⏭️  Skipping {config['name']}: Model files not found")
            failed_count += 1
        except Exception as e:
            print(f"❌ Failed to load {config['name']}: {e}")
            failed_count += 1
    
    print("\n" + "="*70)
    print(f"✅ Successfully loaded: {loaded_count} models")
    print(f"⏭️  Skipped/Failed: {failed_count} models")
    print("="*70)
    
    return loaded_count


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': len(MODELS),
        'available_models': list(MODELS.keys())
    })


@app.route('/api/models', methods=['GET'])
def list_models():
    """
    List all available models with their details
    """
    models_list = []
    
    for model_id, model_info in MODELS.items():
        models_list.append({
            'id': model_id,
            'name': model_info['name'],
            'description': model_info['description']
        })
    
    return jsonify({
        'count': len(models_list),
        'models': models_list
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
        "model_id": "drop_imbalanced"  // optional, defaults to first available
    }
    """
    try:
        data = request.json
        
        # Get model ID (default to first available)
        model_id = data.pop('model_id', list(MODELS.keys())[0] if MODELS else None)
        
        if not MODELS:
            return jsonify({
                'error': 'No models available. Please train models first.'
            }), 503
        
        if model_id not in MODELS:
            return jsonify({
                'error': f'Model not found: {model_id}',
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
        model_info = MODELS[model_id]
        service = model_info['service']
        result = service.predict(data)
        
        # Add model info to result
        result['model_id'] = model_id
        result['model_name'] = model_info['name']
        result['model_description'] = model_info['description']
        
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
        "model_id": "drop_imbalanced"  // optional
    }
    """
    try:
        data = request.json
        patients = data.get('patients', [])
        model_id = data.get('model_id', list(MODELS.keys())[0] if MODELS else None)
        
        if not MODELS:
            return jsonify({
                'error': 'No models available'
            }), 503
        
        if model_id not in MODELS:
            return jsonify({
                'error': f'Model not found: {model_id}'
            }), 400
        
        if not patients:
            return jsonify({'error': 'No patients provided'}), 400
        
        # Make predictions
        model_info = MODELS[model_id]
        service = model_info['service']
        results = service.predict_batch(patients)
        
        return jsonify({
            'model_id': model_id,
            'model_name': model_info['name'],
            'count': len(results),
            'results': results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/compare', methods=['POST'])
def compare_models():
    """
    Compare predictions from multiple models
    
    Request body (JSON):
    {
        "patient_data": {patient info},
        "model_ids": ["drop_imbalanced", "mean_smote", ...]  // optional, defaults to all
    }
    """
    try:
        data = request.json
        patient_data = data.get('patient_data')
        model_ids = data.get('model_ids', list(MODELS.keys()))
        
        if not patient_data:
            return jsonify({'error': 'No patient data provided'}), 400
        
        # Filter to only available models
        model_ids = [m for m in model_ids if m in MODELS]
        
        if not model_ids:
            return jsonify({'error': 'No valid models specified'}), 400
        
        # Get predictions from each model
        comparisons = []
        for model_id in model_ids:
            model_info = MODELS[model_id]
            service = model_info['service']
            result = service.predict(patient_data)
            
            comparisons.append({
                'model_id': model_id,
                'model_name': model_info['name'],
                'prediction': result['prediction'],
                'probability': result['probability'],
                'risk_level': result['risk_level'],
                'confidence': result['confidence']
            })
        
        # Calculate consensus
        avg_probability = sum(c['probability'] for c in comparisons) / len(comparisons)
        consensus_prediction = 1 if avg_probability >= 0.5 else 0
        
        return jsonify({
            'patient_data': patient_data,
            'models_compared': len(comparisons),
            'comparisons': comparisons,
            'consensus': {
                'prediction': consensus_prediction,
                'avg_probability': avg_probability,
                'agreement_rate': sum(1 for c in comparisons if c['prediction'] == consensus_prediction) / len(comparisons)
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("="*70)
    print(" STROKE PREDICTION API SERVER - ENHANCED VERSION")
    print("="*70)
    
    print("\nAuto-discovering models...")
    loaded_count = auto_discover_models()
    
    if loaded_count == 0:
        print("\n❌ No models loaded!")
        print("\n💡 Please train models first:")
        print("   cd ml_training")
        print("   python main.py --variant drop_imbalanced")
        print("\nOr train all models:")
        print("   python main.py")
        sys.exit(1)
    
    print(f"\n✅ Loaded {loaded_count} models successfully!")
    print("\nStarting Flask server...")
    print("API will be available at: http://localhost:5000")
    print("\n📚 Available Endpoints:")
    print("  GET  /api/health          - Health check")
    print("  GET  /api/models          - List available models")
    print("  POST /api/predict         - Single prediction")
    print("  POST /api/predict-batch   - Batch predictions")
    print("  POST /api/compare         - Compare multiple models")
    print("\n" + "="*70)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
