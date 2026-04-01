"""Tests for API server endpoints."""

import json
import sys
import os

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from api.server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


SAMPLE_PATIENT = {
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
}


class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        response = client.get("/api/health")
        assert response.status_code == 200

    def test_health_returns_status(self, client):
        data = json.loads(response := client.get("/api/health").data)
        assert data["status"] == "healthy"
        assert "models_loaded" in data
        assert "available_models" in data


class TestModelsEndpoint:
    def test_models_returns_200(self, client):
        response = client.get("/api/models")
        assert response.status_code == 200

    def test_models_returns_list(self, client):
        data = json.loads(client.get("/api/models").data)
        assert "count" in data
        assert "models" in data
        assert isinstance(data["models"], list)


class TestPredictEndpoint:
    def test_predict_missing_fields(self, client):
        response = client.post(
            "/api/predict",
            data=json.dumps({"age": 50}),
            content_type="application/json",
        )
        assert response.status_code in (400, 503)

    def test_predict_empty_body(self, client):
        response = client.post(
            "/api/predict",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert response.status_code in (400, 503)


class TestPredictBatchEndpoint:
    def test_batch_no_patients(self, client):
        response = client.post(
            "/api/predict-batch",
            data=json.dumps({"patients": []}),
            content_type="application/json",
        )
        assert response.status_code in (400, 503)


class TestCompareEndpoint:
    def test_compare_no_patient_data(self, client):
        response = client.post(
            "/api/compare",
            data=json.dumps({}),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_compare_invalid_models(self, client):
        response = client.post(
            "/api/compare",
            data=json.dumps({
                "patient_data": SAMPLE_PATIENT,
                "model_ids": ["nonexistent_model"],
            }),
            content_type="application/json",
        )
        assert response.status_code == 400
