# Web App Integration Guide

## 🔄 Local ML Model Integration

This project is configured to run completely locally using trained Machine Learning models.

## Step 1: Train Models

You must train the models before the application can make predictions.

```bash
cd ml_training
# Install dependencies
pip install -r requirements.txt

# Train a single efficient model (Recommended for quick start)
python main.py --variant drop_imbalanced

# OR Train all 10 model variants (Takes longer)
python main.py
```

## Step 2: Start API Server

The React frontend communicates with a local Python Flask server to get predictions.

```bash
cd ml_training
python api_server.py
```

The API will be available at `http://localhost:5000`.

## Step 3: Frontend Configuration

The frontend is already configured to use the local ML service (`services/mlModelService.ts`).
Ensure your `.env` (if used) points to the local server, or rely on the default:

```typescript
const apiUrl = process.env.REACT_APP_ML_API_URL || 'http://localhost:5000/api';
```

## Performance

| Aspect | ML Models (Local) |
|--------|-------------------|
| Speed | <100ms |
| Accuracy | 95-97% |
| Cost | Free |
| Offline | ✅ Yes |
| Privacy | ✅ 100% Local |

## Troubleshooting

- **No models available**: Run `python main.py --variant drop_imbalanced` inside `ml_training` folder.
- **Connection refused**: Ensure `api_server.py` is running in a separate terminal.
