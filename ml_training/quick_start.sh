#!/bin/bash
# Quick Start Script - Train your first model and start the app

echo "======================================================================"
echo " 🚀 STROKE PREDICTION - QUICK START"
echo "======================================================================"
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python found: $(python --version)"
echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -q -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Train first model
echo "🎯 Training your first model (Drop + Imbalanced)..."
echo "⏱️  This will take approximately 30-60 minutes..."
echo "☕ Grab a coffee and relax!"
echo ""

python train_drop_imbalanced.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Training failed. Please check the error messages above."
    exit 1
fi

echo ""
echo "======================================================================"
echo " ✅ MODEL TRAINED SUCCESSFULLY!"
echo "======================================================================"
echo ""
echo "🎉 Your first model is ready!"
echo ""
echo "📁 Model saved in: Model for Drop Missing Value Imbalanced/"
echo ""
echo "🚀 Next steps:"
echo "   1. Start the API server:"
echo "      python api_server.py"
echo ""
echo "   2. In another terminal, start the React app:"
echo "      cd .. && npm start"
echo ""
echo "   3. Open your browser and test the app!"
echo ""
echo "💡 Want to train more models? Run:"
echo "   python main.py --variant mean_smote"
echo ""
echo "   Or train all models at once:"
echo "   python main.py"
echo ""
echo "======================================================================"
