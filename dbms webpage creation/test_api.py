#!/usr/bin/env python3
"""
Test Script for ESP32 Motion Detection API
==========================================

This script allows you to test the Flask API without needing an ESP32.
It sends test data to the MySQL database through the API.

Usage:
    python test_api.py

Make sure Flask API (app_mysql.py) is running first!
"""

import requests
import json
import time
from datetime import datetime

# API Configuration
API_BASE_URL = 'http://localhost:5000/api'

# ANSI Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    """Print colored header"""
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}{text}{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    """Print success message"""
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    """Print error message"""
    print(f"{RED}❌ {text}{RESET}")

def print_info(text):
    """Print info message"""
    print(f"{BLUE}ℹ️  {text}{RESET}")

def print_warning(text):
    """Print warning message"""
    print(f"{YELLOW}⚠️  {text}{RESET}")

def check_api_health():
    """Check if API is running"""
    print_header("Checking API Health")
    try:
        response = requests.get(f'{API_BASE_URL}/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"API is running (Status: {data['status']})")
            print_info(f"Database: {data['database']}")
            print_info(f"Timestamp: {data['timestamp']}")
            return True
        else:
            print_error(f"API returned status code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to API at http://localhost:5000")
        print_info("Make sure Flask API is running: python app_mysql.py")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def add_motion_detected():
    """Add motion detected event to database"""
    print_header("Adding Motion Detection Event")
    
    payload = {
        'motion_status': 'detected',
        'temperature': 25.5,
        'latitude': 40.7128,
        'longitude': -74.0060
    }
    
    print_info(f"Sending data: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            f'{API_BASE_URL}/sensor-data',
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        data = response.json()
        
        if response.status_code == 201:
            print_success(f"Data saved successfully!")
            print_info(f"Record ID: {data.get('id')}")
            print_info(f"Message: {data.get('message')}")
            print_info(f"Timestamp: {data.get('timestamp')}")
            return True
        else:
            print_error(f"Failed to save data: {data.get('error', 'Unknown error')}")
            return False
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def add_no_motion():
    """Add no motion event to database"""
    print_header("Adding No Motion Event")
    
    payload = {
        'motion_status': 'not_detected',
        'temperature': 24.2,
        'latitude': 40.7128,
        'longitude': -74.0060
    }
    
    print_info(f"Sending data: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            f'{API_BASE_URL}/sensor-data',
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        data = response.json()
        
        if response.status_code == 201:
            print_success(f"Data saved successfully!")
            print_info(f"Record ID: {data.get('id')}")
            return True
        else:
            print_error(f"Failed to save data: {data.get('error', 'Unknown error')}")
            return False
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def simulate_motion_events(count=5):
    """Simulate multiple motion events"""
    print_header(f"Simulating {count} Motion Events")
    
    for i in range(count):
        print_info(f"Event {i+1}/{count}")
        
        # Alternate between motion detected and no motion
        if i % 2 == 0:
            add_motion_detected()
        else:
            add_no_motion()
        
        time.sleep(1)  # Wait 1 second between events
    
    print_success(f"Finished simulating {count} events")

def get_all_data():
    """Retrieve all sensor data from database"""
    print_header("Retrieving All Sensor Data")
    
    try:
        response = requests.get(
            f'{API_BASE_URL}/sensor-data?limit=10&offset=0',
            timeout=5
        )
        
        data = response.json()
        
        if data.get('success'):
            print_info(f"Total records: {data.get('total')}")
            print_info(f"Retrieved: {len(data.get('data', []))} records\n")
            
            if data.get('data'):
                for record in data['data']:
                    print(f"  ID: {record['id']}")
                    print(f"  Motion: {record['motion_status']}")
                    print(f"  Temp: {record['temperature']}°C")
                    print(f"  Location: {record['latitude']}, {record['longitude']}")
                    print(f"  Time: {record['timestamp']}")
                    print()
            else:
                print_warning("No data found in database")
            
            return True
        else:
            print_error(f"Error: {data.get('error')}")
            return False
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def get_statistics():
    """Get motion detection statistics"""
    print_header("Getting Statistics")
    
    try:
        response = requests.get(
            f'{API_BASE_URL}/statistics',
            timeout=5
        )
        
        data = response.json()
        
        if data.get('success'):
            stats = data.get('statistics', {})
            
            print_info(f"Total Events: {stats.get('total_events')}")
            print_info(f"Motion Detected: {stats.get('motion_detected')}")
            print_info(f"No Motion: {stats.get('no_motion')}")
            print_info(f"Detection Rate: {stats.get('detection_rate')}%")
            print_info(f"Avg Temperature: {stats.get('average_temperature')}°C")
            print_info(f"Last 24h Detections: {stats.get('last_24h_detections')}")
            print_info(f"Latest Event: {stats.get('latest_event')}")
            
            return True
        else:
            print_error(f"Error: {data.get('error')}")
            return False
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def get_motion_events_only():
    """Get only motion detected events"""
    print_header("Getting Motion Detected Events")
    
    try:
        response = requests.get(
            f'{API_BASE_URL}/sensor-data?motion=detected&limit=5',
            timeout=5
        )
        
        data = response.json()
        
        if data.get('success'):
            print_info(f"Found {len(data.get('data', []))} motion events\n")
            
            for record in data['data']:
                print(f"  🚨 Motion at {record['timestamp']}")
                print(f"     Location: ({record['latitude']}, {record['longitude']})")
                print(f"     Temperature: {record['temperature']}°C\n")
            
            return True
        else:
            print_error(f"Error: {data.get('error')}")
            return False
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def main_menu():
    """Display main menu"""
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}ESP32 Motion Detection Dashboard - API Test Tool{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")
    
    print("Test Options:")
    print("  1 - Check API Health")
    print("  2 - Add Motion Detected Event")
    print("  3 - Add No Motion Event")
    print("  4 - Simulate Multiple Motion Events")
    print("  5 - Get All Sensor Data")
    print("  6 - Get Statistics")
    print("  7 - Get Motion Events Only")
    print("  8 - Run Full Test Suite")
    print("  0 - Exit")
    print()

def run_full_test():
    """Run full test suite"""
    print_header("Running Full Test Suite")
    
    print_info("1/5 - Checking API health...")
    if not check_api_health():
        print_error("API is not running. Skipping rest of tests.")
        return
    
    time.sleep(1)
    
    print_info("2/5 - Adding motion detected event...")
    add_motion_detected()
    
    time.sleep(1)
    
    print_info("3/5 - Adding no motion event...")
    add_no_motion()
    
    time.sleep(1)
    
    print_info("4/5 - Retrieving all data...")
    get_all_data()
    
    time.sleep(1)
    
    print_info("5/5 - Getting statistics...")
    get_statistics()
    
    print_success("Full test suite completed!")

if __name__ == '__main__':
    try:
        while True:
            main_menu()
            choice = input("Enter your choice (0-8): ").strip()
            
            if choice == "1":
                check_api_health()
            elif choice == "2":
                add_motion_detected()
            elif choice == "3":
                add_no_motion()
            elif choice == "4":
                count = int(input("How many events to simulate? (default 5): ") or "5")
                simulate_motion_events(count)
            elif choice == "5":
                get_all_data()
            elif choice == "6":
                get_statistics()
            elif choice == "7":
                get_motion_events_only()
            elif choice == "8":
                run_full_test()
            elif choice == "0":
                print_success("Goodbye!")
                break
            else:
                print_error("Invalid choice. Please try again.")
            
            input(f"\n{YELLOW}Press Enter to continue...{RESET}")
    
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Test interrupted by user{RESET}")
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
