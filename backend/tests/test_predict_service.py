"""Tests for predict_service module."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from api.predict_service import StrokePredictionService


class TestGetRiskLevel:
    def test_low_risk(self):
        assert StrokePredictionService._get_risk_level(0.1) == "Low"
        assert StrokePredictionService._get_risk_level(0.0) == "Low"
        assert StrokePredictionService._get_risk_level(0.29) == "Low"

    def test_medium_risk(self):
        assert StrokePredictionService._get_risk_level(0.3) == "Medium"
        assert StrokePredictionService._get_risk_level(0.45) == "Medium"
        assert StrokePredictionService._get_risk_level(0.59) == "Medium"

    def test_high_risk(self):
        assert StrokePredictionService._get_risk_level(0.6) == "High"
        assert StrokePredictionService._get_risk_level(0.9) == "High"
        assert StrokePredictionService._get_risk_level(1.0) == "High"

    def test_boundary_low_medium(self):
        assert StrokePredictionService._get_risk_level(0.3) == "Medium"

    def test_boundary_medium_high(self):
        assert StrokePredictionService._get_risk_level(0.6) == "High"


class TestInterpretResult:
    def test_stroke_detected(self):
        result = StrokePredictionService._interpret_result(1, 0.85, "High")
        assert "High stroke risk" in result
        assert "85.0%" in result
        assert "consultation" in result.lower()

    def test_medium_risk_no_stroke(self):
        result = StrokePredictionService._interpret_result(0, 0.45, "Medium")
        assert "Moderate" in result
        assert "45.0%" in result

    def test_low_risk_no_stroke(self):
        result = StrokePredictionService._interpret_result(0, 0.1, "Low")
        assert "Low stroke risk" in result
        assert "10.0%" in result
        assert "healthy" in result.lower()
