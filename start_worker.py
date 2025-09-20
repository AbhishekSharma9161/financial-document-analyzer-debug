#!/usr/bin/env python3
"""
Start the Redis Queue Worker for background processing
"""

import sys
import os
from queue_worker import start_worker, REDIS_CONNECTED

def main():
    print("🚀 Financial Document Analyzer - Queue Worker")
    print("=" * 50)
    
    if not REDIS_CONNECTED:
        print("❌ Redis server not available!")
        print("\nTo enable queue processing:")
        print("1. Install Redis server")
        print("2. Start Redis: redis-server")
        print("3. Install Python dependencies: pip install redis rq")
        print("4. Run this script again")
        print("\n💡 The system will work in fallback mode without Redis")
        return 1
    
    print("✅ Redis connection established")
    print("🔄 Starting background worker...")
    print("📋 Listening for financial analysis tasks...")
    print("\nPress Ctrl+C to stop the worker")
    print("-" * 50)
    
    try:
        start_worker()
    except KeyboardInterrupt:
        print("\n\n🛑 Worker stopped by user")
        return 0
    except Exception as e:
        print(f"\n❌ Worker error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())