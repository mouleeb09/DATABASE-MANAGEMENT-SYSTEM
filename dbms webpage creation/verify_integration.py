#!/usr/bin/env python3
"""
Complete Flask + MySQL + Dashboard Integration Verification Script
===================================================================

This script verifies that:
1. Flask server is running
2. MySQL is connected
3. Database and table exist
4. Sample data can be saved
5. Dashboard integration is ready

Run this AFTER starting the Flask server:
    python api_server.py  # (in another terminal)
    python verify_integration.py
"""

import requests
import pymysql
import json
from datetime import datetime
import time

# Configuration
FLASK_URL = 'http://127.0.0.1:5000'
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'human_detection'
}

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_success(text):
    """Print success message"""
    print(f"  ✅ {text}")

def print_error(text):
    """Print error message"""
    print(f"  ❌ {text}")

def print_info(text):
    """Print info message"""
    print(f"  ℹ️  {text}")

def print_step(num, text):
    """Print step number"""
    print(f"\n  [{num}] {text}")

def test_flask_health():
    """Test Flask server health"""
    print_step(1, "Testing Flask Server Connection")
    
    try:
        print_info(f"Connecting to {FLASK_URL}/health...")
        response = requests.get(f"{FLASK_URL}/health", timeout=5)
        
        if response.ok:
            data = response.json()
            print_success(f"Flask server is running!")
            print_info(f"Database status: {data.get('database')}")
            print_info(f"Server status: {data.get('status')}")
            return True
        else:
            print_error(f"Flask returned error: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error(f"Cannot connect to Flask server at {FLASK_URL}")
        print_info("Make sure to run: python api_server.py")
        return False
    except Exception as e:
        print_error(f"Connection error: {e}")
        return False

def test_mysql_connection():
    """Test MySQL connection"""
    print_step(2, "Testing MySQL Connection")
    
    try:
        print_info(f"Connecting to MySQL at {MYSQL_CONFIG['host']}...")
        conn = pymysql.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("SELECT DATABASE()")
        db = cursor.fetchone()[0]
        
        print_success("MySQL connection successful!")
        print_info(f"Connected to database: {db}")
        
        conn.close()
        return True
        
    except pymysql.Error as e:
        print_error(f"MySQL Error: {e}")
        print_info("Make sure:")
        print_info("  1. XAMPP MySQL is running")
        print_info("  2. Database 'human_detection' exists")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False

def test_table_structure():
    """Test table structure"""
    print_step(3, "Verifying Table Structure")
    
    try:
        conn = pymysql.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("""
            SELECT COLUMN_NAME, COLUMN_TYPE 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME='detection' AND TABLE_SCHEMA='human_detection'
        """)
        
        columns = cursor.fetchall()
        
        if not columns:
            print_error("Table 'detection' not found!")
            print_info("Run database_setup_human_detection.sql in phpMyAdmin")
            conn.close()
            return False
        
        print_success("Table 'detection' exists!")
        print_info("Columns found:")
        
        required_columns = {
            'ID': 'int',
            'motion_status': 'varchar',
            'radar_status': 'varchar',
            'temperature': 'float',
            'person_detected': 'varchar',
            'detection_time': 'timestamp'
        }
        
        for col_name, col_type in columns:
            print_info(f"  - {col_name}: {col_type}")
        
        conn.close()
        return len(columns) >= 6
        
    except Exception as e:
        print_error(f"Error checking table: {e}")
        return False

def test_save_data():
    """Test saving data to database"""
    print_step(4, "Testing Data Save (POST /save_data)")
    
    test_data = {
        "motion_status": "MOTION DETECTED",
        "radar_status": "RADAR ACTIVE",
        "temperature": "28.5",
        "person_detected": "YES"
    }
    
    try:
        print_info(f"Sending test data: {json.dumps(test_data)}")
        
        response = requests.post(
            f"{FLASK_URL}/save_data",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.ok:
            data = response.json()
            if data.get('success'):
                record_id = data.get('record_id')
                print_success(f"Data saved successfully!")
                print_info(f"Record ID: {record_id}")
                print_info(f"Timestamp: {data.get('timestamp')}")
                return record_id
            else:
                print_error(f"Save failed: {data.get('message')}")
                return None
        else:
            print_error(f"Server error: {response.status_code}")
            print_info(f"Response: {response.json()}")
            return None
            
    except Exception as e:
        print_error(f"Error saving data: {e}")
        return None

def test_get_data():
    """Test retrieving data from database"""
    print_step(5, "Testing Data Retrieval (GET /get_data)")
    
    try:
        print_info("Fetching latest 5 records...")
        
        response = requests.get(
            f"{FLASK_URL}/get_data?limit=5",
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.ok:
            data = response.json()
            if data.get('success'):
                records = data.get('data', [])
                count = data.get('count', 0)
                
                print_success(f"Retrieved {count} records!")
                
                if records:
                    print_info("Latest records:")
                    for i, record in enumerate(records[:3], 1):
                        print(f"    {i}. ID: {record['id']}, "
                              f"Motion: {record['motion_status']}, "
                              f"Temp: {record['temperature']}°C, "
                              f"Time: {record['detection_time']}")
                
                return True
            else:
                print_error(f"Retrieval failed: {data.get('message')}")
                return False
        else:
            print_error(f"Server error: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error retrieving data: {e}")
        return False

def test_dashboard_ready():
    """Test if dashboard is ready"""
    print_step(6, "Dashboard Integration Status")
    
    try:
        print_info("Checking dashboard files...")
        
        files_to_check = [
            'index_simple.html',
            'test_api_dashboard.html',
            'api_server.py'
        ]
        
        all_exist = True
        for file in files_to_check:
            try:
                with open(file, 'r'):
                    print_success(f"File found: {file}")
            except:
                print_error(f"File not found: {file}")
                all_exist = False
        
        if all_exist:
            print_success("All dashboard files are ready!")
        
        return all_exist
        
    except Exception as e:
        print_error(f"Error checking files: {e}")
        return False

def main():
    """Run all tests"""
    print_header("🚀 ESP32 Flask API Integration Verification")
    print("\nThis script will verify your complete setup:\n")
    
    results = {
        'Flask Health': test_flask_health(),
        'MySQL Connection': test_mysql_connection(),
        'Table Structure': test_table_structure(),
        'Data Save': test_save_data() is not None,
        'Data Retrieval': test_get_data(),
        'Dashboard Files': test_dashboard_ready()
    }
    
    # Summary
    print_header("📊 Verification Results")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test}")
    
    print(f"\n  Total: {passed}/{total} tests passed")
    
    # Recommendations
    print_header("📋 Next Steps")
    
    if passed == total:
        print_success("All tests passed! Your system is ready!")
        print("\n  You can now:")
        print("  1. Open index_simple.html in your browser")
        print("  2. Connect your ESP32 via USB")
        print("  3. Send motion detection data")
        print("  4. Data will be automatically saved to MySQL")
        print("\n  For testing without ESP32:")
        print("  - Open test_api_dashboard.html")
        print("  - Use preset buttons or manual entry")
        print("  - Click 'Send Data' to save")
    else:
        print_error(f"Some tests failed ({total - passed}/{total})")
        print("\n  Common fixes:")
        print("  1. Flask not running? Run: python api_server.py")
        print("  2. MySQL not running? Start XAMPP")
        print("  3. Database not created? Run database_setup_human_detection.sql")
        print("  4. Connection refused? Check firewall settings")
    
    print_header("🎯 Files to Use")
    print("  📊 Dashboard: index_simple.html")
    print("  🧪 Test Panel: test_api_dashboard.html")
    print("  🔧 API Server: api_server.py (must be running)")
    print("  📖 Guides:")
    print("     - FLASK_API_SETUP_GUIDE.md")
    print("     - DASHBOARD_INTEGRATION_GUIDE.md")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()