# 🏥 StrokeGuard AI - ML-Powered Stroke Prediction

> Advanced stroke risk prediction using Dense Stacking Ensemble (DSE) machine learning models

[![Accuracy](https://img.shields.io/badge/Accuracy-95--97%25-success)](ml_training/)
[![Models](https://img.shields.io/badge/Models-10%20Variants-blue)](ml_training/)
[![Tech](https://img.shields.io/badge/Tech-React%20%7C%20Vite%20%7C%20Python%20%7C%20ML-orange)](/)

## 🎯 Overview

StrokeGuard AI is a cutting-edge web application that predicts stroke risk using **trained machine learning models** instead of AI estimation. The system achieves **95-97% accuracy** using Dense Stacking Ensemble (DSE) architecture.

**Key Features:**
- 🎓 **10 ML Models** - Choose from different training variants
- 📊 **95-97% Accuracy** - Significantly better than AI estimation
- ⚡ **<100ms Predictions** - Lightning fast
- 🔒 **Privacy-First** - All processing on your server
- 🎨 **Beautiful UI** - Modern React + Vite interface
- 🔧 **Production-Ready** - Complete API server

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** with pip
- **Node.js 18+** with npm
- ~2GB disk space for models

### 1. Clone Repository

```bash
git clone https://github.com/hoangtung386/Stroke-Prediction.git
cd Stroke-Prediction
```

### 2. Install Python Dependencies

```bash
cd ml_training
pip install -r requirements.txt
```

### 3. Train Your First Model

> [!IMPORTANT] 
> You **MUST** train the models **BEFORE** starting the API server. 
> The API server will fail with "No models loaded" if you skip this step.

```bash
# Train a single model (fastest, ~30-60 min)
python main.py --variant agegroup_imbalanced

# Or train all 10 models (~2-4 hours)
python main.py
```

### 4. Install Frontend Dependencies

```bash
cd ..  # Back to project root
npm install
```

### 5. Start the System (2 Terminals Required)

#### Terminal 1 - Start API Server:
```bash
cd ml_training
python api_server.py
```
> API will run on http://localhost:5000

#### Terminal 2 - Start Frontend:
```bash
npm run dev
```
> Frontend will run on http://localhost:3000

### 6. Open the App! 🎉

Open http://localhost:3000 in your browser:
- Select a model from dropdown
- Fill in patient data
- Click "Analyze Risk"
- View prediction results

### Stopping the Services

Press `Ctrl + C` in each terminal to stop the servers.

---

## 🗂️ Project Structure

```
Stroke-Prediction/
├── src/                               # React Frontend (Vite)
│   ├── components/                    # UI Components
│   │   ├── Header.tsx
│   │   ├── ModelSelector.tsx
│   │   ├── PatientForm.tsx
│   │   └── AnalysisResult.tsx
│   ├── services/                      # API Services
│   │   └── mlModelService.ts
│   ├── App.tsx                        # Main App
│   ├── main.tsx                       # Entry Point
│   ├── index.css                      # Global Styles
│   └── types.ts                       # TypeScript Types
│
├── ml_training/                       # ML Training Pipeline
│   ├── config.py                      # Configuration
│   ├── data_preprocessing.py          # Data preprocessing
│   ├── model_utils.py                 # Model utilities
│   ├── predict_service.py             # Prediction service
│   ├── api_server.py                  # Flask API server
│   ├── main.py                        # Training orchestrator
│   ├── requirements.txt               # Python dependencies
│   └── train_*.py                     # Training scripts
│
├── public/                            # Static assets
├── index.html                         # HTML entry
├── package.json                       # npm config
├── vite.config.ts                     # Vite config (with API proxy)
├── tailwind.config.js                 # Tailwind CSS
└── tsconfig.json                      # TypeScript config
```

---

## 🏗️ Architecture

### ML Training Pipeline

```
Dataset → Preprocessing → Imputation → Train/Test Split
    ↓
Base Models (9 algorithms):
├── Logistic Regression (AGD)
├── Neural Network (5 hidden layers)
├── Random Forest
├── Gradient Boosting
├── CatBoost
├── LightGBM
├── XGBoost
├── Balanced Bagging
└── NGBoost
    ↓
Ensemble Layers:
├── Voting Ensemble (soft voting)
├── Blending Ensemble (stacking with meta-classifier)
└── Fusion Ensemble (stacking with passthrough)
    ↓
Dense Stacking Ensemble (DSE)
    ↓
Trained Model (95-97% accuracy)
```

### Tech Stack
- **Frontend**: React 18 + TypeScript + Vite + Tailwind CSS
- **Backend**: Python + Flask + CORS
- **ML**: Scikit-learn + XGBoost + LightGBM + CatBoost
- **Data**: Kaggle Stroke Prediction Dataset

---

## 📊 Available Models

### Imbalanced Datasets
| Variant | Description | Command |
|---------|-------------|---------|
| Drop + Imbalanced | Drop missing values | `python main.py --variant drop_imbalanced` |
| Mean + Imbalanced | Mean imputation | `python main.py --variant mean_imbalanced` |
| MICE + Imbalanced | MICE imputation | `python main.py --variant mice_imbalanced` |
| Age Group + Imbalanced | Age-based imputation | `python main.py --variant agegroup_imbalanced` |
| Augmented + Imbalanced | Combined methods | `python main.py --variant augmented_imbalanced` |

### SMOTE Balanced Datasets (Better Recall)
| Variant | Description | Command |
|---------|-------------|---------|
| Drop + SMOTE | Drop + BorderlineSMOTE | `python main.py --variant drop_smote` |
| Mean + SMOTE | Mean + BorderlineSMOTE | `python main.py --variant mean_smote` |
| MICE + SMOTE | MICE + BorderlineSMOTE | `python main.py --variant mice_smote` |
| Age Group + SMOTE | Age Group + BorderlineSMOTE | `python main.py --variant agegroup_smote` |
| Augmented + SMOTE ⭐ | Augmented + BorderlineSMOTE | `python main.py --variant augmented_smote` |

---

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/models` | GET | List available models |
| `/api/predict` | POST | Single prediction |
| `/api/predict-batch` | POST | Batch predictions |
| `/api/compare` | POST | Compare multiple models |

### Example: Single Prediction
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
    "model_id": "agegroup_imbalanced"
  }'
```

---

## 📈 Performance

| Metric | Gemini AI | ML Models |
|--------|-----------|-----------|
| **Accuracy** | ~85% | **95-97%** ✅ |
| **Speed** | 2-5 sec | **<100ms** ✅ |
| **Cost** | $$$ per request | **Free** ✅ |
| **Offline** | ❌ No | **✅ Yes** |
| **Privacy** | Cloud API | **On-premise** ✅ |

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "No models loaded" when starting API | Train models first: `python main.py --variant agegroup_imbalanced` |
| Port 3000 already in use | Kill the process: `lsof -ti:3000 \| xargs kill -9` |
| Port 5000 already in use | Kill the process: `lsof -ti:5000 \| xargs kill -9` |
| Memory error during training | Train models individually, not all at once |
| npm install fails | Ensure Node.js 18+ is installed: `node --version` |
| API connection refused | Ensure Flask API is running on port 5000 |

---

## 🚀 Development Commands

```bash
# Start frontend dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

---

## 📦 Deployment

### Option 1: Single Server (Recommended)
1. Build React: `npm run build`
2. Serve static files from Flask (configure in `api_server.py`)
3. Deploy to Heroku/Railway/Render

### Option 2: Separate Deployments
- **Backend**: Deploy Flask API to Heroku/Railway
- **Frontend**: Deploy React to Vercel/Netlify
- Update API URL in environment variables

---

## ⚠️ Medical Disclaimer

**Important**: This application is for educational and research purposes only. It is **NOT** a medical diagnostic tool and should **NOT** replace professional medical advice, diagnosis, or treatment.

Always consult qualified healthcare professionals for medical concerns.

---

## 🙏 Acknowledgments

- Dataset: [Kaggle Stroke Prediction Dataset](https://www.kaggle.com/fedesoriano/stroke-prediction-dataset)
- Based on DSE (Dense Stacking Ensemble) methodology
- Inspired by recent research in medical ML

---

**Made with ❤️ for better healthcare through AI**
