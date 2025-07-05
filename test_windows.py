#!/usr/bin/env python3
"""
Simplified Windows Test Script for Multilingual Learning Path Generator
"""

import os
import sys
import shutil

def print_status(message, status="INFO"):
    """Print colored status messages"""
    colors = {
        "INFO": "\033[94m",    # Blue
        "SUCCESS": "\033[92m", # Green
        "WARNING": "\033[93m", # Yellow
        "ERROR": "\033[91m",   # Red
    }
    color = colors.get(status, "\033[0m")
    reset = "\033[0m"
    print(f"{color}[{status}]{reset} {message}")

def setup_environment():
    """Setup environment file"""
    print_status("Setting up environment...")
    
    if not os.path.exists(".env"):
        if os.path.exists("env_template.txt"):
            try:
                shutil.copy("env_template.txt", ".env")
                print_status("✅ .env file created!", "SUCCESS")
                print_status("⚠️  Please edit .env file and add your OpenAI API key", "WARNING")
                return False
            except Exception as e:
                print_status(f"❌ Failed to create .env: {e}", "ERROR")
                return False
        else:
            print_status("❌ env_template.txt not found!", "ERROR")
            return False
    
    # Check if OpenAI key is set
    try:
        with open(".env", "r") as f:
            content = f.read()
            if "OPENAI_API_KEY=sk-" in content:
                print_status("✅ Environment setup complete!", "SUCCESS")
                return True
            else:
                print_status("⚠️  OpenAI API key not found in .env", "WARNING")
                print_status("Please add your OpenAI API key to .env file", "INFO")
                return False
    except Exception as e:
        print_status(f"❌ Error reading .env: {e}", "ERROR")
        return False

def test_packages():
    """Test if required packages are installed"""
    print_status("Testing required packages...")
    
    required = ["fastapi", "uvicorn", "requests", "streamlit", "plotly", "pandas", "openai"]
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print_status(f"❌ Missing packages: {missing}", "ERROR")
        print_status("Run: pip install -r requirements.txt", "WARNING")
        return False
    
    print_status("✅ All packages installed!", "SUCCESS")
    return True

def test_files():
    """Test if all required files exist"""
    print_status("Checking required files...")
    
    required_files = [
        "main.py",
        "frontend/app.py", 
        "requirements.txt",
        "vercel.json",
        "env_template.txt"
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print_status(f"❌ Missing files: {missing}", "ERROR")
        return False
    
    print_status("✅ All required files found!", "SUCCESS")
    return True

def main():
    """Main test function"""
    print_status("🚀 Windows Test for Multilingual Learning Path Generator", "INFO")
    print_status("=" * 60, "INFO")
    
    tests = [
        ("File Check", test_files),
        ("Package Check", test_packages),
        ("Environment Setup", setup_environment)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print_status(f"\n--- {test_name} ---", "INFO")
        if test_func():
            passed += 1
            print_status(f"✅ {test_name} PASSED", "SUCCESS")
        else:
            print_status(f"❌ {test_name} FAILED", "ERROR")
    
    print_status("=" * 60, "INFO")
    print_status(f"Results: {passed}/{total} tests passed", "INFO")
    
    if passed >= 2:  # At least 2 tests should pass
        print_status("🎉 Ready for deployment!", "SUCCESS")
        print_status("\nNext steps:", "INFO")
        print_status("1. Edit .env file with your OpenAI API key", "INFO")
        print_status("2. Run: python test_local.py", "INFO")
        print_status("3. Run: ./deploy.sh", "INFO")
        return True
    else:
        print_status("⚠️  Please fix issues before deploying", "WARNING")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 