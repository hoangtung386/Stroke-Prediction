#!/bin/bash
# Quick Start Script - Train your first model and start the app
# Run from: backend/ directory

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"

echo "======================================================================"
echo " STROKE PREDICTION - QUICK START"
echo "======================================================================"
echo ""

cd "$BACKEND_DIR"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed. Please install Python 3.10+ first."
    exit 1
fi

echo "Python found: $(python3 --version)"
echo ""

# Install dependencies (prefer uv, fallback to pip)
if command -v uv &> /dev/null; then
    echo "Installing dependencies with uv..."
    uv sync
    RUN_CMD="uv run python"
else
    echo "Installing dependencies with pip..."
    pip install -q -r requirements.txt
    RUN_CMD="python3"
fi

echo "Dependencies installed"
echo ""

# Train first model
echo "Training your first model (Drop + Imbalanced)..."
echo "This will take approximately 30-60 minutes..."
echo ""

$RUN_CMD -m training.train --imputation drop --balancing imbalanced

echo ""
echo "======================================================================"
echo " MODEL TRAINED SUCCESSFULLY!"
echo "======================================================================"
echo ""
echo "Model saved in: models/drop_imbalanced/"
echo ""
echo "Next steps:"
echo "   1. Start the API server:"
echo "      $RUN_CMD -m api.server"
echo ""
echo "   2. In another terminal, start the React app:"
echo "      cd ../frontend && npm run dev"
echo ""
echo "   3. Open http://localhost:3000 in your browser"
echo ""
echo "Want to train more models?"
echo "   $RUN_CMD -m training.train --imputation mean --balancing smote"
echo ""
echo "Or train all 10 models at once:"
echo "   $RUN_CMD -m training.train --all"
echo ""
echo "======================================================================"
