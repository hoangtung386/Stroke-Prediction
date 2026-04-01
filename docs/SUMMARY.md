# Project Architecture Summary

## Project Structure

```
Stroke-Prediction/
├── frontend/                        # React + TypeScript + Vite
│   ├── src/
│   │   ├── components/             # UI components
│   │   ├── types/                  # TypeScript interfaces
│   │   ├── constants/              # Form options
│   │   ├── services/               # API integration (mlModelService.ts)
│   │   └── App.tsx                 # Main application
│   ├── package.json
│   └── vite.config.ts              # Proxy /api -> localhost:5000
│
├── backend/                         # Python ML pipeline + Flask API
│   ├── config.py                   # All constants & hyperparameters
│   ├── data_preprocessing.py       # Data loading, imputation, SMOTE
│   ├── model_utils.py              # Model training, evaluation, DSE
│   ├── training/
│   │   └── train.py                # Unified training script (all 10 variants)
│   ├── api/
│   │   ├── server.py               # Flask REST API
│   │   └── predict_service.py      # Prediction service
│   ├── tests/                      # Unit tests
│   ├── pyproject.toml              # Project config (uv/pip)
│   └── requirements.txt
│
└── docs/                            # Documentation
```

## ML Architecture: Dense Stacking Ensemble (DSE)

```
Base Models (8):
├── Logistic Regression (AGD)
├── Neural Network (5 layers)
├── Random Forest
├── Gradient Boosting
├── CatBoost
├── LightGBM
├── XGBoost
└── Balanced Bagging

    ↓ Fine-tune top 3

Ensemble Layers:
├── Voting Ensemble (soft voting)
├── Blending Ensemble (stacking + meta-classifier)
└── Fusion Ensemble (stacking + passthrough)

    ↓

Final DSE Model (stacking of 3 ensembles)
```

## 10 Model Variants

5 imputation methods x 2 balancing strategies:

| Imputation | Imbalanced | SMOTE |
|---|---|---|
| Drop missing values | drop_imbalanced | drop_smote |
| Mean imputation | mean_imbalanced | mean_smote |
| MICE imputation | mice_imbalanced | mice_smote |
| Age group imputation | agegroup_imbalanced | agegroup_smote |
| Augmented (3 combined) | augmented_imbalanced | augmented_smote |

## Quick Reference

```bash
# Train
cd backend
python -m training.train --imputation drop --balancing imbalanced
python -m training.train --all

# API
python -m api.server

# Frontend
cd frontend
npm run dev
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/models` | GET | List available models |
| `/api/predict` | POST | Single prediction |
| `/api/predict-batch` | POST | Batch predictions |
| `/api/compare` | POST | Compare multiple models |

## Key Design Decisions

- **Unified training script**: 1 file (`train.py`) replaces 10 near-identical scripts
- **Configurable thresholds**: Risk levels defined in `config.py`, not hardcoded
- **Environment-based debug**: `FLASK_DEBUG` env var instead of `debug=True`
- **Request logging**: All API requests logged via Python `logging` module
- **Type safety**: Frontend types aligned with backend API responses
