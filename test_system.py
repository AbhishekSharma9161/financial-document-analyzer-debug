#!/usr/bin/env python3
"""
Test script to verify the financial document analyzer system works correctly
"""

import os
import sys
import requests
import time

def test_api_health():
    """Test if the API is running"""
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ API Health Check: PASSED")
            return True
        else:
            print("❌ API Health Check: FAILED")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ API Health Check: FAILED - Server not running")
        return False

def test_file_upload():
    """Test file upload and analysis"""
    try:
        # Check if sample file exists
        sample_file = "data/TSLA-Q2-2025-Update.pdf"
        if not os.path.exists(sample_file):
            print("❌ File Upload Test: FAILED - Sample file not found")
            return False
        
        # Test file upload
        with open(sample_file, 'rb') as f:
            response = requests.post(
                'http://localhost:8000/analyze',
                files={'file': f},
                data={'query': 'Test analysis of Tesla financial document'}
            )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 'success':
                print("✅ File Upload Test: PASSED")
                print(f"   Analysis length: {len(result.get('analysis', ''))}")
                return True
            else:
                print("❌ File Upload Test: FAILED - Invalid response")
                return False
        else:
            print(f"❌ File Upload Test: FAILED - Status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ File Upload Test: FAILED - {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Financial Document Analyzer System")
    print("=" * 50)
    
    # Test 1: API Health
    health_ok = test_api_health()
    
    if not health_ok:
        print("\n❌ Cannot proceed with tests - API server not running")
        print("Please start the server with: python main.py")
        sys.exit(1)
    
    # Test 2: File Upload and Analysis
    upload_ok = test_file_upload()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"   API Health: {'✅ PASSED' if health_ok else '❌ FAILED'}")
    print(f"   File Upload: {'✅ PASSED' if upload_ok else '❌ FAILED'}")
    
    if health_ok and upload_ok:
        print("\n🎉 All tests passed! System is working correctly.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())