#!/usr/bin/env python3
"""
ESP32 Advanced Motion Detection Dashboard - Flask API Server
===========================================================

Complete Flask backend server for ESP32 motion detection system.
Provides REST API endpoints for saving and retrieving sensor data.

Database: MySQL (human_detection)
Table: detection
Columns: ID, motion_status, radar_status, temperature, person_detected, detection_time

Endpoints:
- POST /save_data : Save sensor data from ESP32
- GET /get_data   : Retrieve latest detection records

Author: GitHub Copilot
Date: 2024
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import pymysql.cursors
from datetime import datetime
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',          # Default XAMPP MySQL user
    'password': '',          # Default XAMPP MySQL password (empty)
    'database': 'human_detection',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    """
    Create and return a database connection.

    Returns:
        pymysql.Connection: Database connection object

    Raises:
        pymysql.Error: If connection fails
    """
    try:
        connection = pymysql.connect(**DB_CONFIG)
        logger.info("Database connection established successfully")
        return connection
    except pymysql.Error as e:
        logger.error(f"Database connection failed: {e}")
        raise

@app.route('/save_data', methods=['POST'])
def save_data():
    """
    Save sensor data from ESP32 to MySQL database.

    Expected JSON format:
    {
        "motion_status": "MOTION DETECTED",
        "radar_status": "RADAR ACTIVE",
        "temperature": "32.5",
        "person_detected": "YES"
    }

    Returns:
        JSON response with success status and message
    """
    try:
        # Get JSON data from request
        data = request.get_json()

        # Validate required fields
        required_fields = ['motion_status', 'radar_status', 'temperature', 'person_detected']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}',
                    'timestamp': datetime.now().isoformat()
                }), 400

        # Extract data
        motion_status = data['motion_status']
        radar_status = data['radar_status']
        temperature = float(data['temperature'])  # Convert to float
        person_detected = data['person_detected']

        # Validate temperature range (reasonable range for ESP32 sensor)
        if not (-50 <= temperature <= 100):
            return jsonify({
                'success': False,
                'message': 'Temperature out of valid range (-50°C to 100°C)',
                'timestamp': datetime.now().isoformat()
            }), 400

        # Connect to database
        connection = get_db_connection()

        try:
            with connection.cursor() as cursor:
                # SQL query to insert data
                sql = """
                INSERT INTO detection
                (motion_status, radar_status, temperature, person_detected)
                VALUES (%s, %s, %s, %s)
                """

                # Execute the query
                cursor.execute(sql, (motion_status, radar_status, temperature, person_detected))

                # Commit the transaction
                connection.commit()

                # Get the ID of the inserted record
                record_id = cursor.lastrowid

                logger.info(f"Data saved successfully with ID: {record_id}")

                # Return success response
                return jsonify({
                    'success': True,
                    'message': 'Data saved successfully',
                    'record_id': record_id,
                    'timestamp': datetime.now().isoformat()
                }), 201

        finally:
            connection.close()

    except ValueError as e:
        logger.error(f"Invalid data format: {e}")
        return jsonify({
            'success': False,
            'message': 'Invalid data format. Temperature must be a number.',
            'timestamp': datetime.now().isoformat()
        }), 400

    except pymysql.Error as e:
        logger.error(f"Database error: {e}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred',
            'timestamp': datetime.now().isoformat()
        }), 500

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({
            'success': False,
            'message': 'An unexpected error occurred',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/get_data', methods=['GET'])
def get_data():
    """
    Retrieve latest detection records from database.

    Query parameters:
    - limit (optional): Number of records to return (default: 10, max: 100)

    Returns:
        JSON array of detection records
    """
    try:
        # Get limit parameter (default 10, max 100)
        limit = request.args.get('limit', default=10, type=int)
        if limit > 100:
            limit = 100
        elif limit < 1:
            limit = 1

        # Connect to database
        connection = get_db_connection()

        try:
            with connection.cursor() as cursor:
                # SQL query to get latest records
                sql = """
                SELECT ID, motion_status, radar_status, temperature, person_detected, detection_time
                FROM detection
                ORDER BY detection_time DESC
                LIMIT %s
                """

                # Execute the query
                cursor.execute(sql, (limit,))

                # Fetch all records
                records = cursor.fetchall()

                # Convert records to list of dictionaries
                result = []
                for record in records:
                    result.append({
                        'id': record['ID'],
                        'motion_status': record['motion_status'],
                        'radar_status': record['radar_status'],
                        'temperature': record['temperature'],
                        'person_detected': record['person_detected'],
                        'detection_time': record['detection_time'].isoformat() if record['detection_time'] else None
                    })

                logger.info(f"Retrieved {len(result)} records")

                # Return the data
                return jsonify({
                    'success': True,
                    'data': result,
                    'count': len(result),
                    'timestamp': datetime.now().isoformat()
                }), 200

        finally:
            connection.close()

    except pymysql.Error as e:
        logger.error(f"Database error: {e}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred',
            'timestamp': datetime.now().isoformat()
        }), 500

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({
            'success': False,
            'message': 'An unexpected error occurred',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify server and database status.

    Returns:
        JSON with server status and database connection status
    """
    try:
        # Test database connection
        connection = get_db_connection()
        connection.close()

        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.now().isoformat()
        }), 200

    except pymysql.Error:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'timestamp': datetime.now().isoformat()
        }), 503

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'message': 'Endpoint not found',
        'timestamp': datetime.now().isoformat()
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        'success': False,
        'message': 'Method not allowed',
        'timestamp': datetime.now().isoformat()
    }), 405

if __name__ == '__main__':
    print("🚀 ESP32 Motion Detection Dashboard API Server")
    print("=" * 50)
    print("📊 Database: human_detection (MySQL via XAMPP)")
    print("📋 Table: detection")
    print("🌐 Server: http://127.0.0.1:5000")
    print()
    print("📍 Endpoints:")
    print("   POST /save_data  - Save sensor data from ESP32")
    print("   GET  /get_data   - Get latest detection records")
    print("   GET  /health     - Health check")
    print()
    print("📝 POST /save_data JSON format:")
    print('   {"motion_status":"MOTION DETECTED", "radar_status":"RADAR ACTIVE", "temperature":"32.5", "person_detected":"YES"}')
    print()
    print("⚠️  Make sure XAMPP MySQL is running!")
    print("⚠️  Database 'human_detection' and table 'detection' must exist!")
    print()
    print("Press Ctrl+C to stop the server")
    print()

    # Run the Flask app
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )