# Complete Training & Deployment Guide

## Setup Environment

```bash
cd backend

# Option A: uv (recommended)
uv sync

# Option B: pip
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Setup Kaggle API (to download dataset)
# Create ~/.kaggle/kaggle.json with API credentials from kaggle.com/account
```

## Train Models

### Option A: Train 1 Model (Quick - 30-60 minutes)

```bash
cd backend
python -m training.train --imputation drop --balancing imbalanced
# or with uv: uv run python -m training.train --imputation drop --balancing imbalanced
```

After training, you will have:
- Folder: `models/drop_imbalanced/`
- Files:
  - `dse_stroke_prediction_imbalanced_drop.pkl` (model)
  - `scaler_imbalanced_drop.pkl` (scaler)
  - `encoder_imbalanced_drop.pkl` (encoder)
  - `model_columns_imbalanced_drop.pkl` (features)

### Option B: Train All 10 Models (3-5 hours)

```bash
python -m training.train --all
```

### Option C: Train Specific Variant

```bash
python -m training.train --imputation mean --balancing smote
```

Available combinations:

| `--imputation` | `--balancing` | Variant ID |
|---|---|---|
| `drop` | `imbalanced` | drop_imbalanced |
| `mean` | `imbalanced` | mean_imbalanced |
| `mice` | `imbalanced` | mice_imbalanced |
| `agegroup` | `imbalanced` | agegroup_imbalanced |
| `augmented` | `imbalanced` | augmented_imbalanced |
| `drop` | `smote` | drop_smote |
| `mean` | `smote` | mean_smote |
| `mice` | `smote` | mice_smote |
| `agegroup` | `smote` | agegroup_smote |
| `augmented` | `smote` | augmented_smote |

## Start API Server

```bash
cd backend
python -m api.server
# or with uv: uv run python -m api.server
```

Expected output:
```
======================================================================
 AUTO-DISCOVERING TRAINED MODELS
======================================================================
Loaded: Drop + Imbalanced
...
Successfully loaded: X models
======================================================================

Starting Flask server...
API will be available at: http://localhost:5000
```

Keep the API server running in a separate terminal.

## Start React App

```bash
cd frontend
npm install   # first time only
npm run dev
```

Open: http://localhost:3000

## Test Full Integration

1. Check models loaded: `curl http://localhost:5000/api/health`
2. Open the React app
3. Verify the model selector dropdown appears
4. Select a model, fill in patient data, click "Analyze Stroke Risk"
5. Verify the prediction result displays

## API Endpoints

### GET /api/health
```bash
curl http://localhost:5000/api/health
```

### GET /api/models
```bash
curl http://localhost:5000/api/models
```

### POST /api/predict
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
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
    "model_id": "drop_imbalanced"
  }'
```

### POST /api/compare
```bash
curl -X POST http://localhost:5000/api/compare \
  -H "Content-Type: application/json" \
  -d '{
    "patient_data": { ... },
    "model_ids": ["drop_imbalanced", "mean_smote"]
  }'
```

## Production Deployment

### Using gunicorn
```bash
cd backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api.server:app
```

### Separate Deployments
- **Backend**: Deploy Flask API to Heroku/Railway/Render
- **Frontend**: Build with `npm run build`, deploy to Vercel/Netlify

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No models loaded | Train a model: `python -m training.train --imputation drop --balancing imbalanced` |
| API connection failed | Ensure API server is running: `python -m api.server` |
| Module not found | Install dependencies: `uv sync` or `pip install -r requirements.txt` |
| CORS errors | Already handled with `flask-cors` |
| Prediction errors | Check patient data field names match API (snake_case) |

## Model Performance

Expected accuracy ranges:
- **Imbalanced datasets**: 93-95%
- **SMOTE balanced**: 95-97%
- **Augmented datasets**: 95-97% (highest)
