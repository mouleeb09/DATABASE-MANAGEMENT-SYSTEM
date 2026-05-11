#!/usr/bin/env python3
"""
Test script for ESP32 Motion Detection Flask API
===============================================

This script tests the API endpoints without requiring a database connection.
Run this to verify the Flask server is working correctly.

Usage:
    python test_api.py
"""

import requests
import json
import time

# Server URL
BASE_URL = "http://127.0.0.1:5000"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed")
            print(f"   Status: {data.get('status')}")
            print(f"   Database: {data.get('database')}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is the Flask server running?")
        return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_save_data():
    """Test the POST /save_data endpoint"""
    print("\n💾 Testing POST /save_data endpoint...")

    test_data = {
        "motion_status": "MOTION DETECTED",
        "radar_status": "RADAR ACTIVE",
        "temperature": "32.5",
        "person_detected": "YES"
    }

    try:
        response = requests.post(
            f"{BASE_URL}/save_data",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )

        print(f"   Status Code: {response.status_code}")
        data = response.json()
        print(f"   Response: {json.dumps(data, indent=2)}")

        if response.status_code == 201 and data.get('success'):
            print("✅ Save data test passed")
            return True
        else:
            print("❌ Save data test failed")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is the Flask server running?")
        return False
    except Exception as e:
        print(f"❌ Save data test error: {e}")
        return False

def test_get_data():
    """Test the GET /get_data endpoint"""
    print("\n📊 Testing GET /get_data endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/get_data?limit=5")

        print(f"   Status Code: {response.status_code}")
        data = response.json()
        print(f"   Response: {json.dumps(data, indent=2)}")

        if response.status_code == 200 and data.get('success'):
            print("✅ Get data test passed")
            return True
        else:
            print("❌ Get data test failed")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is the Flask server running?")
        return False
    except Exception as e:
        print(f"❌ Get data test error: {e}")
        return False

def test_invalid_data():
    """Test error handling with invalid data"""
    print("\n🚫 Testing error handling...")

    # Test missing fields
    invalid_data = {
        "motion_status": "MOTION DETECTED"
        # Missing other required fields
    }

    try:
        response = requests.post(
            f"{BASE_URL}/save_data",
            json=invalid_data,
            headers={'Content-Type': 'application/json'}
        )

        print(f"   Status Code: {response.status_code}")
        data = response.json()
        print(f"   Response: {json.dumps(data, indent=2)}")

        if response.status_code == 400 and not data.get('success'):
            print("✅ Error handling test passed")
            return True
        else:
            print("❌ Error handling test failed")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is the Flask server running?")
        return False
    except Exception as e:
        print(f"❌ Error handling test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 ESP32 Motion Detection API Test Suite")
    print("=" * 50)
    print("⚠️  Make sure the Flask server is running first!")
    print("   Run: python api_server.py")
    print()

    # Wait a moment for server to start if needed
    time.sleep(1)

    tests = [
        test_health_check,
        test_save_data,
        test_get_data,
        test_invalid_data
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Your API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        print("   Make sure XAMPP MySQL is running and database is set up.")

    print("\n💡 Next steps:")
    print("   1. Set up your MySQL database using database_setup_human_detection.sql")
    print("   2. Start XAMPP MySQL service")
    print("   3. Run the Flask server: python api_server.py")
    print("   4. Test with your ESP32 or dashboard")

if __name__ == "__main__":
    main()