#!/bin/bash

# 🚀 Deployment Script for Multilingual Learning Path Generator
# This script automates the deployment process

set -e  # Exit on any error

echo "🎓 Starting deployment of Multilingual Learning Path Generator..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Step 1: Local Testing
print_status "Step 1: Running local tests..."

# Check if test script exists
if [ -f "test_local.py" ]; then
    print_status "Running local testing script..."
    if python test_local.py; then
        print_success "Local tests passed!"
    else
        print_error "Local tests failed! Please fix issues before deploying."
        print_error "Run 'python test_local.py' to see detailed error messages."
        exit 1
    fi
else
    print_warning "test_local.py not found. Skipping local tests."
    print_warning "It's recommended to test locally before deploying."
fi

# Step 2: Environment Setup
print_status "Step 2: Setting up environment..."

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from template..."
    cp env_template.txt .env
    print_warning "Please edit .env file and add your OpenAI API key before continuing."
    print_warning "Press Enter when ready to continue..."
    read
fi

# Check if OpenAI API key is set
if ! grep -q "OPENAI_API_KEY=sk-" .env; then
    print_error "OpenAI API key not found in .env file!"
    print_error "Please add your OpenAI API key to the .env file."
    exit 1
fi

# Step 3: Prerequisites Check
print_status "Step 3: Checking prerequisites..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    print_status "Installing Vercel CLI..."
    npm install -g vercel
fi

# Step 4: Install Python Dependencies
print_status "Step 4: Installing Python dependencies..."
if pip install -r requirements.txt; then
    print_success "Python dependencies installed!"
else
    print_error "Failed to install Python dependencies!"
    exit 1
fi

# Step 5: Deploy Backend
print_status "Step 5: Deploying backend to Vercel..."

# Deploy to Vercel
if vercel --prod --yes; then
    print_success "Backend deployed successfully!"
    
    # Get the deployment URL
    DEPLOYMENT_URL=$(vercel ls | grep -o 'https://[^[:space:]]*' | head -1)
    print_success "Backend URL: $DEPLOYMENT_URL"
    
    # Step 6: Update Frontend Configuration
    print_status "Step 6: Updating frontend configuration..."
    
    # Create a temporary file with the new backend URL
    sed "s|http://localhost:8000|$DEPLOYMENT_URL|g" frontend/app.py > frontend/app_temp.py
    mv frontend/app_temp.py frontend/app.py
    
    print_success "Frontend configuration updated!"
    
    # Step 7: Commit Changes
    print_status "Step 7: Committing changes..."
    git add .
    git commit -m "Update backend URL for deployment" || true
    
    print_success "Deployment completed successfully!"
    echo ""
    echo "🎉 Your application is now ready for frontend deployment!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Go to https://share.streamlit.io"
    echo "2. Sign in with GitHub"
    echo "3. Create a new app with:"
    echo "   - Repository: Your GitHub repo"
    echo "   - Branch: main"
    echo "   - Main file path: frontend/app.py"
    echo ""
    echo "🔗 Your backend is available at: $DEPLOYMENT_URL"
    echo "📚 API documentation: $DEPLOYMENT_URL/docs"
    echo ""
    echo "💡 Don't forget to set environment variables in Streamlit Cloud!"
    echo ""
    echo "🧪 Test your backend:"
    echo "   curl $DEPLOYMENT_URL/"
    echo "   curl $DEPLOYMENT_URL/courses?query=python"
    
else
    print_error "Backend deployment failed!"
    exit 1
fi 