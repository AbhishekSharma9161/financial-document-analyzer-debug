#!/usr/bin/env python3
"""
Setup script for Financial Document Analyzer
"""

import os
import sys
import subprocess

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def check_env_file():
    """Check if .env file exists"""
    if os.path.exists(".env"):
        print("✅ .env file found")
        return True
    else:
        print("⚠️  .env file not found")
        print("   Please copy .env.template to .env and add your API keys")
        return False

def check_sample_data():
    """Check if sample data exists"""
    sample_file = "data/TSLA-Q2-2025-Update.pdf"
    if os.path.exists(sample_file):
        print("✅ Sample financial document found")
        return True
    else:
        print("⚠️  Sample financial document not found")
        print(f"   Expected: {sample_file}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Financial Document Analyzer")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Check environment file
    env_ok = check_env_file()
    
    # Check sample data
    data_ok = check_sample_data()
    
    print("\n" + "=" * 50)
    print("📋 Setup Summary:")
    print(f"   Requirements: ✅ INSTALLED")
    print(f"   Environment: {'✅ CONFIGURED' if env_ok else '⚠️  NEEDS SETUP'}")
    print(f"   Sample Data: {'✅ AVAILABLE' if data_ok else '⚠️  MISSING'}")
    
    if env_ok and data_ok:
        print("\n🎉 Setup complete! You can now run:")
        print("   python main.py")
    else:
        print("\n⚠️  Please complete the setup steps above before running the application.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())