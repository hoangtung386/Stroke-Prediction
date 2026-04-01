"""Flask API server for stroke prediction with auto model loading.

Usage:
    cd backend
    python -m api.server
"""

import logging
import os
import sys

from flask import Flask, request, jsonify
from flask_cors import CORS

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from api.predict_service import StrokePredictionService
from config import MODEL_DIRS, MODEL_CONFIGS, REQUIRED_PATIENT_FIELDS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

MODELS = {}


def auto_discover_models():
    """Automatically discover and load all trained models.

    Returns:
        Number of successfully loaded models.
    """
    print(f"\n{'=' * 70}")
    print(" AUTO-DISCOVERING TRAINED MODELS")
    print(f"{'=' * 70}")

    loaded_count = 0
    failed_count = 0

    for config in MODEL_CONFIGS:
        model_dir = MODEL_DIRS[config["id"]]

        if not os.path.exists(model_dir):
            logger.info("Skipping %s: directory not found", config["name"])
            failed_count += 1
            continue

        try:
            service = StrokePredictionService(
                model_dir=model_dir,
                model_suffix=config["suffix"],
            )
            MODELS[config["id"]] = {
                "service": service,
                "name": config["name"],
                "description": config["description"],
                "dir": model_dir,
            }
            logger.info("Loaded: %s", config["name"])
            loaded_count += 1

        except FileNotFoundError:
            logger.info(
                "Skipping %s: model files not found", config["name"]
            )
            failed_count += 1
        except Exception as e:
            logger.error("Failed to load %s: %s", config["name"], e)
            failed_count += 1

    print(f"\n{'=' * 70}")
    print(f"Successfully loaded: {loaded_count} models")
    print(f"Skipped/Failed: {failed_count} models")
    print(f"{'=' * 70}")

    return loaded_count


@app.before_request
def log_request():
    """Log each incoming request."""
    logger.info("%s %s", request.method, request.path)


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "models_loaded": len(MODELS),
        "available_models": list(MODELS.keys()),
    })


@app.route("/api/models", methods=["GET"])
def list_models():
    """List all available models with their details."""
    models_list = [
        {
            "id": model_id,
            "name": info["name"],
            "description": info["description"],
        }
        for model_id, info in MODELS.items()
    ]
    return jsonify({"count": len(models_list), "models": models_list})


def _get_model_or_error(model_id):
    """Validate model_id and return model info or error response.

    Args:
        model_id: ID of the model to look up.

    Returns:
        Tuple of (model_info, None) on success,
        or (None, error_response) on failure.
    """
    if not MODELS:
        return None, (
            jsonify({"error": "No models available. Train models first."}),
            503,
        )
    if model_id not in MODELS:
        return None, (
            jsonify({
                "error": f"Model not found: {model_id}",
                "available_models": list(MODELS.keys()),
            }),
            400,
        )
    return MODELS[model_id], None


def _default_model_id():
    """Return the first available model ID, or None."""
    return next(iter(MODELS), None)


@app.route("/api/predict", methods=["POST"])
def predict():
    """Predict stroke risk for a single patient.

    Request body (JSON):
        Patient data fields + optional "model_id".
    """
    try:
        data = request.get_json()
        model_id = data.pop("model_id", _default_model_id())

        model_info, error = _get_model_or_error(model_id)
        if error:
            return error

        missing = [f for f in REQUIRED_PATIENT_FIELDS if f not in data]
        if missing:
            return jsonify({
                "error": "Missing required fields",
                "missing_fields": missing,
            }), 400

        result = model_info["service"].predict(data)
        result["model_id"] = model_id
        result["model_name"] = model_info["name"]
        result["model_description"] = model_info["description"]

        return jsonify(result)

    except Exception as e:
        logger.exception("Prediction error")
        return jsonify({"error": str(e)}), 500


@app.route("/api/predict-batch", methods=["POST"])
def predict_batch():
    """Predict stroke risk for multiple patients.

    Request body (JSON):
        {"patients": [...], "model_id": "optional"}
    """
    try:
        data = request.get_json()
        patients = data.get("patients", [])
        model_id = data.get("model_id", _default_model_id())

        model_info, error = _get_model_or_error(model_id)
        if error:
            return error

        if not patients:
            return jsonify({"error": "No patients provided"}), 400

        results = model_info["service"].predict_batch(patients)

        return jsonify({
            "model_id": model_id,
            "model_name": model_info["name"],
            "count": len(results),
            "results": results,
        })

    except Exception as e:
        logger.exception("Batch prediction error")
        return jsonify({"error": str(e)}), 500


@app.route("/api/compare", methods=["POST"])
def compare_models():
    """Compare predictions from multiple models.

    Request body (JSON):
        {"patient_data": {...}, "model_ids": [...]}
    """
    try:
        data = request.get_json()
        patient_data = data.get("patient_data")
        model_ids = data.get("model_ids", list(MODELS.keys()))

        if not patient_data:
            return jsonify({"error": "No patient data provided"}), 400

        model_ids = [m for m in model_ids if m in MODELS]
        if not model_ids:
            return jsonify({"error": "No valid models specified"}), 400

        comparisons = []
        for model_id in model_ids:
            info = MODELS[model_id]
            result = info["service"].predict(patient_data)
            comparisons.append({
                "model_id": model_id,
                "model_name": info["name"],
                "prediction": result["prediction"],
                "probability": result["probability"],
                "risk_level": result["risk_level"],
                "confidence": result["confidence"],
            })

        avg_probability = (
            sum(c["probability"] for c in comparisons) / len(comparisons)
        )
        consensus_prediction = 1 if avg_probability >= 0.5 else 0
        agreement_rate = (
            sum(
                1
                for c in comparisons
                if c["prediction"] == consensus_prediction
            )
            / len(comparisons)
        )

        return jsonify({
            "patient_data": patient_data,
            "models_compared": len(comparisons),
            "comparisons": comparisons,
            "consensus": {
                "prediction": consensus_prediction,
                "avg_probability": avg_probability,
                "agreement_rate": agreement_rate,
            },
        })

    except Exception as e:
        logger.exception("Model comparison error")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print(f"{'=' * 70}")
    print(" STROKE PREDICTION API SERVER")
    print(f"{'=' * 70}")

    print("\nAuto-discovering models...")
    loaded_count = auto_discover_models()

    if loaded_count == 0:
        print("\nNo models loaded!")
        print("\nPlease train models first:")
        print("   cd backend")
        print("   python -m training.train --imputation drop --balancing imbalanced")
        print("\nOr train all models:")
        print("   python -m training.train --all")
        sys.exit(1)

    print(f"\nLoaded {loaded_count} models successfully!")
    print("\nStarting Flask server...")
    print("API will be available at: http://localhost:5000")
    print("\nAvailable Endpoints:")
    print("  GET  /api/health          - Health check")
    print("  GET  /api/models          - List available models")
    print("  POST /api/predict         - Single prediction")
    print("  POST /api/predict-batch   - Batch predictions")
    print("  POST /api/compare         - Compare multiple models")
    print(f"\n{'=' * 70}")

    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=debug, host="0.0.0.0", port=port)
