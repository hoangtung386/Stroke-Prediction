@echo off
REM Quick Start Script - Train your first model and start the app (Windows)

echo ======================================================================
echo  🚀 STROKE PREDICTION - QUICK START
echo ======================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo ✅ Python found
python --version
echo.

REM Install dependencies
echo 📦 Installing Python dependencies...
pip install -q -r requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed
echo.

REM Train first model
echo 🎯 Training your first model (Drop + Imbalanced)...
echo ⏱️  This will take approximately 30-60 minutes...
echo ☕ Grab a coffee and relax!
echo.

python train_drop_imbalanced.py

if errorlevel 1 (
    echo.
    echo ❌ Training failed. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo  ✅ MODEL TRAINED SUCCESSFULLY!
echo ======================================================================
echo.
echo 🎉 Your first model is ready!
echo.
echo 📁 Model saved in: Model for Drop Missing Value Imbalanced/
echo.
echo 🚀 Next steps:
echo    1. Start the API server:
echo       python api_server.py
echo.
echo    2. In another terminal, start the React app:
echo       cd .. ^&^& npm start
echo.
echo    3. Open your browser and test the app!
echo.
echo 💡 Want to train more models? Run:
echo    python main.py --variant mean_smote
echo.
echo    Or train all models at once:
echo    python main.py
echo.
echo ======================================================================
pause
