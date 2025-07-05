@echo off
REM 🚀 Windows Deployment Script for Multilingual Learning Path Generator

echo 🎓 Starting deployment of Multilingual Learning Path Generator...

REM Step 1: Local Testing
echo Step 1: Running local tests...
python test_local.py
if %errorlevel% neq 0 (
    echo ❌ Local tests failed! Please fix issues before deploying.
    pause
    exit /b 1
)
echo ✅ Local tests passed!

REM Step 2: Environment Setup
echo Step 2: Setting up environment...
if not exist ".env" (
    echo ⚠️ .env file not found. Creating from template...
    copy env_template.txt .env
    echo ⚠️ Please edit .env file and add your OpenAI API key before continuing.
    echo Press any key when ready to continue...
    pause
)

REM Step 3: Prerequisites Check
echo Step 3: Checking prerequisites...

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js first.
    pause
    exit /b 1
)

REM Check if Vercel CLI is installed
vercel --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Vercel CLI...
    npm install -g vercel
)

REM Step 4: Install Python Dependencies
echo Step 4: Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install Python dependencies!
    pause
    exit /b 1
)
echo ✅ Python dependencies installed!

REM Step 5: Deploy Backend
echo Step 5: Deploying backend to Vercel...
vercel --prod --yes
if %errorlevel% neq 0 (
    echo ❌ Backend deployment failed!
    pause
    exit /b 1
)

echo ✅ Backend deployed successfully!
echo.
echo 🎉 Your application is now ready for frontend deployment!
echo.
echo 📋 Next steps:
echo 1. Go to https://share.streamlit.io
echo 2. Sign in with GitHub
echo 3. Create a new app with:
echo    - Repository: Your GitHub repo
echo    - Branch: main
echo    - Main file path: frontend/app.py
echo.
echo 💡 Don't forget to set environment variables in Streamlit Cloud!
echo.
pause 