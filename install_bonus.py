#!/usr/bin/env python3
"""
Install bonus feature dependencies
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a Python package"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🎖️ Installing Bonus Feature Dependencies")
    print("=" * 50)
    
    bonus_packages = [
        "sqlalchemy",
        "redis", 
        "rq",
        "python-dateutil"
    ]
    
    success_count = 0
    
    for package in bonus_packages:
        print(f"📦 Installing {package}...")
        if install_package(package):
            print(f"✅ {package} installed successfully")
            success_count += 1
        else:
            print(f"❌ Failed to install {package}")
    
    print("\n" + "=" * 50)
    print(f"📊 Installation Summary: {success_count}/{len(bonus_packages)} packages installed")
    
    if success_count == len(bonus_packages):
        print("🎉 All bonus dependencies installed successfully!")
        print("\n🚀 You can now use:")
        print("   - Enhanced API: python enhanced_main.py")
        print("   - Background worker: python start_worker.py")
        print("   - Docker deployment: docker-compose up")
    else:
        print("⚠️  Some packages failed to install. Check the errors above.")
    
    print("\n💡 Note: Redis server is required for queue features")
    print("   Install Redis: https://redis.io/download")

if __name__ == "__main__":
    main()