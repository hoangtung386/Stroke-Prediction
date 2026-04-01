"""Tests for config module."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config import (
    SEED,
    K_FOLD,
    TEST_SIZE,
    RISK_THRESHOLDS,
    NUMERICAL_COLS,
    CATEGORICAL_COLS,
    REQUIRED_PATIENT_FIELDS,
    MODEL_DIRS,
    MODEL_CONFIGS,
    PARAM_GRIDS,
    IMPORTANT_FEATURES,
)


class TestConfigConstants:
    def test_seed_is_int(self):
        assert isinstance(SEED, int)

    def test_kfold_positive(self):
        assert K_FOLD > 0

    def test_test_size_range(self):
        assert 0 < TEST_SIZE < 1

    def test_risk_thresholds_ordered(self):
        assert RISK_THRESHOLDS["low"] < RISK_THRESHOLDS["medium"]
        assert RISK_THRESHOLDS["low"] > 0
        assert RISK_THRESHOLDS["medium"] < 1

    def test_numerical_cols_not_empty(self):
        assert len(NUMERICAL_COLS) > 0
        assert "age" in NUMERICAL_COLS
        assert "bmi" in NUMERICAL_COLS

    def test_categorical_cols_not_empty(self):
        assert len(CATEGORICAL_COLS) > 0
        assert "gender" in CATEGORICAL_COLS

    def test_required_patient_fields_complete(self):
        all_cols = NUMERICAL_COLS + CATEGORICAL_COLS
        for col in all_cols:
            assert col in REQUIRED_PATIENT_FIELDS
        assert "hypertension" in REQUIRED_PATIENT_FIELDS
        assert "heart_disease" in REQUIRED_PATIENT_FIELDS
        assert "ever_married" in REQUIRED_PATIENT_FIELDS

    def test_model_dirs_10_variants(self):
        assert len(MODEL_DIRS) == 10

    def test_model_configs_match_dirs(self):
        config_ids = {c["id"] for c in MODEL_CONFIGS}
        dir_keys = set(MODEL_DIRS.keys())
        assert config_ids == dir_keys

    def test_model_configs_have_required_keys(self):
        for config in MODEL_CONFIGS:
            assert "id" in config
            assert "name" in config
            assert "description" in config
            assert "suffix" in config

    def test_param_grids_not_empty(self):
        assert len(PARAM_GRIDS) > 0
        for name, grid in PARAM_GRIDS.items():
            assert isinstance(grid, dict)
            assert len(grid) > 0

    def test_important_features_include_target(self):
        assert "stroke" in IMPORTANT_FEATURES
        assert "age" in IMPORTANT_FEATURES
        assert "bmi" in IMPORTANT_FEATURES
