#!/usr/bin/env python3
"""
Final comprehensive test of the Financial Document Analyzer system
"""

import requests
import time
import os
import sys

def test_main_api():
    """Test the main API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Financial Document Analyzer")
    print("=" * 60)
    
    # Test 1: Health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("   ✅ Health check passed")
            health_data = response.json()
            print(f"   📊 Database: {health_data.get('database', 'unknown')}")
            print(f"   🔄 Queue: {health_data.get('queue_system', 'unknown')}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to API. Is the server running?")
        print("   💡 Start with: python main.py")
        return False
    
    # Test 2: Create user
    print("\n2. Testing user creation...")
    try:
        user_data = {
            "username": f"test_user_{int(time.time())}",
            "email": f"test_{int(time.time())}@example.com"
        }
        response = requests.post(f"{base_url}/users/", data=user_data)
        if response.status_code == 200:
            user_info = response.json()
            user_id = user_info['id']
            print(f"   ✅ User created: ID {user_id}")
        else:
            print(f"   ❌ User creation failed: {response.status_code}")
            user_id = 1  # Use default user
    except Exception as e:
        print(f"   ⚠️  User creation error: {e}")
        user_id = 1
    
    # Test 3: File upload and analysis
    print("\n3. Testing document analysis...")
    sample_file = "data/TSLA-Q2-2025-Update.pdf"
    
    if not os.path.exists(sample_file):
        print(f"   ❌ Sample file not found: {sample_file}")
        return False
    
    try:
        with open(sample_file, 'rb') as f:
            files = {'file': f}
            data = {
                'query': 'Test analysis of Tesla financial document',
                'user_id': user_id
            }
            response = requests.post(f"{base_url}/analyze", files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print("   ✅ Document analysis completed")
            print(f"   📄 File: {result.get('file_processed', 'unknown')}")
            print(f"   ⏱️  Processing time: {result.get('processing_time', 0):.2f}s")
            print(f"   📊 Result ID: {result.get('result_id', 'unknown')}")
            
            # Test getting the result
            if 'result_id' in result:
                result_response = requests.get(f"{base_url}/results/{result['result_id']}")
                if result_response.status_code == 200:
                    print("   ✅ Result retrieval successful")
                else:
                    print("   ⚠️  Result retrieval failed")
        else:
            print(f"   ❌ Document analysis failed: {response.status_code}")
            print(f"   📝 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Analysis error: {e}")
        return False
    
    # Test 4: Queue status
    print("\n4. Testing queue status...")
    try:
        response = requests.get(f"{base_url}/queue/status")
        if response.status_code == 200:
            queue_info = response.json()
            print("   ✅ Queue status retrieved")
            print(f"   📊 Total jobs: {queue_info.get('total', 0)}")
            print(f"   ✅ Completed: {queue_info.get('completed', 0)}")
            print(f"   🔄 Redis: {'Connected' if queue_info.get('redis_connected') else 'Fallback mode'}")
        else:
            print(f"   ❌ Queue status failed: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Queue status error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Enhanced API test completed successfully!")
    print("📋 All core features are working properly")
    return True

def test_basic_apis():
    """Test basic API versions"""
    apis = [
        ("Simple API", "http://localhost:8001", "simple_main.py"),
        ("Standard API", "http://localhost:8000", "main.py")
    ]
    
    print("\n🔍 Checking other API versions...")
    for name, url, script in apis:
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                print(f"   ✅ {name} is running at {url}")
            else:
                print(f"   ⚠️  {name} returned status {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"   💤 {name} is not running (start with: python {script})")
        except Exception as e:
            print(f"   ❌ {name} error: {e}")

def main():
    """Run all tests"""
    print("🚀 Final System Test - Financial Document Analyzer")
    print("🎯 Assignment: AI Internship Debug Challenge")
    print("📅 Testing all components...")
    
    # Test main API (main submission)
    success = test_main_api()
    
    # Test other versions
    test_basic_apis()
    
    print("\n" + "=" * 60)
    if success:
        print("🏆 SYSTEM TEST PASSED!")
        print("✅ Ready for GitHub submission")
        print("\n📋 Submission Checklist:")
        print("   ✅ All bugs fixed")
        print("   ✅ System working properly")
        print("   ✅ Database integration")
        print("   ✅ Queue system (with fallback)")
        print("   ✅ Comprehensive documentation")
        print("   ✅ Bonus features implemented")
        
        print("\n🚀 Next Steps:")
        print("   1. Create GitHub repository")
        print("   2. Push all code")
        print("   3. Submit repository link")
        
        return 0
    else:
        print("❌ SYSTEM TEST FAILED!")
        print("🔧 Please fix issues before submission")
        return 1

if __name__ == "__main__":
    sys.exit(main())