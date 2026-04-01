@echo off
REM Quick Start Script - Train your first model and start the app (Windows)
REM Run from: backend\ directory

echo ======================================================================
echo  STROKE PREDICTION - QUICK START
echo ======================================================================
echo.

cd /d "%~dp0\.."

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.10+ first.
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Install dependencies
echo Installing Python dependencies...
pip install -q -r requirements.txt

if errorlevel 1 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

echo Dependencies installed
echo.

REM Train first model
echo Training your first model (Drop + Imbalanced)...
echo This will take approximately 30-60 minutes...
echo.

python -m training.train --imputation drop --balancing imbalanced

if errorlevel 1 (
    echo.
    echo Training failed. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo  MODEL TRAINED SUCCESSFULLY!
echo ======================================================================
echo.
echo Model saved in: models\drop_imbalanced\
echo.
echo Next steps:
echo    1. Start the API server:
echo       python -m api.server
echo.
echo    2. In another terminal, start the React app:
echo       cd ..\frontend ^&^& npm run dev
echo.
echo    3. Open http://localhost:3000 in your browser
echo.
echo Want to train more models?
echo    python -m training.train --imputation mean --balancing smote
echo.
echo Or train all 10 models at once:
echo    python -m training.train --all
echo.
echo ======================================================================
pause
