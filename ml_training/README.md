# Stroke Prediction Model Training Pipeline

Modular training pipeline for Dense Stacking Ensemble (DSE) stroke prediction models.

## 📁 Project Structure

```
ml_training/
├── config.py                          # Configuration and constants
├── data_preprocessing.py              # Data preprocessing utilities
├── model_utils.py                     # Model training utilities
├── predict_service.py                 # Prediction service for web integration
├── main.py                           # Main orchestrator
│
├── train_drop_imbalanced.py          # Drop + Imbalanced
├── train_mean_imbalanced.py          # Mean + Imbalanced
├── train_mice_imbalanced.py          # MICE + Imbalanced
├── train_agegroup_imbalanced.py      # Age Group + Imbalanced
├── train_augmented_imbalanced.py     # Augmented + Imbalanced
│
├── train_drop_smote.py               # Drop + SMOTE
├── train_mean_smote.py               # Mean + SMOTE
├── train_mice_smote.py               # MICE + SMOTE
├── train_agegroup_smote.py           # Age Group + SMOTE
└── train_augmented_smote.py          # Augmented + SMOTE
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Train All Models

```bash
python main.py
```

### 3. Train Specific Model

```bash
python main.py --variant drop_imbalanced
```

Available variants:
- `drop_imbalanced` - Drop missing values, imbalanced dataset
- `mean_imbalanced` - Mean imputation, imbalanced dataset
- `augmented_imbalanced` - Augmented dataset (combines 3 imputation methods)
- `drop_smote` - Drop missing values, SMOTE balanced
- And 6 more...

### 4. Train Individual Script

```bash
python train_drop_imbalanced.py
```

## 🔧 Model Variants

The pipeline trains 10 different model variants:

### Imbalanced Dataset (5 variants)
1. **Drop + Imbalanced**: Drop rows with missing BMI values
2. **Mean + Imbalanced**: Fill missing BMI with mean
3. **MICE + Imbalanced**: MICE (Multiple Imputation by Chained Equations)
4. **Age Group + Imbalanced**: Fill missing BMI with age group mean
5. **Augmented + Imbalanced**: Combine all 3 imputation methods

### SMOTE Balanced Dataset (5 variants)
6. **Drop + SMOTE**: Drop + BorderlineSMOTE
7. **Mean + SMOTE**: Mean imputation + BorderlineSMOTE
8. **MICE + SMOTE**: MICE + BorderlineSMOTE
9. **Age Group + SMOTE**: Age group + BorderlineSMOTE
10. **Augmented + SMOTE**: Augmented + BorderlineSMOTE

## 📊 Model Architecture

Each variant uses **Dense Stacking Ensemble (DSE)** which combines:

### Base Models:
- Logistic Regression (AGD)
- Neural Network (5 hidden layers)
- Random Forest
- Gradient Boosting
- CatBoost
- LightGBM
- XGBoost
- Balanced Bagging
- NGBoost

### Ensemble Layers:
1. **Voting Ensemble**: Soft voting across base models
2. **Blending Ensemble**: Stacking with meta-classifier
3. **Fusion Ensemble**: Stacking with passthrough
4. **DSE Final**: Stacks the 3 ensembles above

## 🔮 Using Trained Models for Prediction

### Python API

```python
from predict_service import StrokePredictionService

# Load trained model
service = StrokePredictionService(
    model_dir='Model for Drop Missing Value Imbalanced',
    model_suffix='imbalanced_drop'
)

# Patient data
patient = {
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

# Predict
result = service.predict(patient)

print(f"Prediction: {result['prediction']}")  # 0 or 1
print(f"Probability: {result['probability']:.2%}")
print(f"Risk Level: {result['risk_level']}")  # Low/Medium/High
```

### Batch Prediction

```python
patients_list = [patient1, patient2, patient3, ...]
results = service.predict_batch(patients_list)
```

## 🌐 Web Integration

To integrate with your React web app:

1. **Backend API** (Flask example):

```python
from flask import Flask, request, jsonify
from predict_service import StrokePredictionService

app = Flask(__name__)

# Load model on startup
service = StrokePredictionService(
    model_dir='Model for Drop Missing Value Imbalanced',
    model_suffix='imbalanced_drop'
)

@app.route('/api/predict', methods=['POST'])
def predict():
    patient_data = request.json
    result = service.predict(patient_data)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
```

2. **Frontend** (TypeScript/React):

```typescript
interface PatientData {
  age: number;
  gender: string;
  hypertension: number;
  heart_disease: number;
  ever_married: string;
  work_type: string;
  Residence_type: string;
  avg_glucose_level: number;
  bmi: number;
  smoking_status: string;
}

async function predictStroke(patientData: PatientData) {
  const response = await fetch('/api/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(patientData)
  });
  
  const result = await response.json();
  return result;
}
```

## 📦 Model Artifacts

Each trained model saves 4 files:
- `dse_stroke_prediction_*.pkl` - Trained DSE model
- `scaler_*.pkl` - StandardScaler for numerical features
- `encoder_*.pkl` - OneHotEncoder for categorical features
- `model_columns_*.pkl` - Feature column names

## 🎯 Training Pipeline Steps

Each training script follows these steps:

1. **Load Dataset** - Download from Kaggle
2. **Preprocess** - Clean, encode, scale
3. **Impute** - Handle missing BMI values
4. **Split** - Train/test split (70/30)
5. **Balance** (SMOTE variants only)
6. **Train Base Models** - 9 different algorithms
7. **Evaluate** - K-fold cross-validation
8. **Fine-tune** - Top 3 models with RandomizedSearchCV
9. **Build DSE** - Create ensemble layers
10. **Evaluate Final** - Test set performance
11. **Save** - Model artifacts

## 📈 Expected Performance

Based on the paper, DSE models achieve:
- **Accuracy**: 95-97%
- **AUC**: 95-98%
- **F1-Score**: 0.85-0.95

Best results typically from:
- Augmented + SMOTE dataset
- Drop + SMOTE dataset

## ⚙️ Configuration

Edit `config.py` to customize:
- Random seed
- K-fold splits
- Test size ratio
- Model hyperparameters
- Feature lists

## 🐛 Troubleshooting

**Issue**: Memory error during training
- **Solution**: Train models individually, not all at once

**Issue**: NGBoost compatibility errors
- **Solution**: Already excluded from ensemble (handled in code)

**Issue**: Kaggle authentication
- **Solution**: Set up Kaggle API credentials: `~/.kaggle/kaggle.json`

## 📝 Notes

- Training all 10 models takes ~2-4 hours depending on hardware
- Each model requires ~500MB-1GB disk space
- GPU acceleration available for XGBoost, LightGBM, CatBoost
- SMOTE variants generally perform better on recall

## 🤝 Contributing

To add new training variants:
1. Copy `train_drop_imbalanced.py` as template
2. Modify preprocessing in Step 3
3. Update `MODEL_DIRS` in `config.py`
4. Add import to `main.py`

## 📄 License

MIT License - Free to use for research and commercial purposes
