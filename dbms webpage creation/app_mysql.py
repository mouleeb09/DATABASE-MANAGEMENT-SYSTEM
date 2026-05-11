#!/usr/bin/env python3
"""
ESP32 Motion Detection Dashboard - MySQL API Server
====================================================

Complete Flask API that connects to MySQL database and stores sensor data
from the ESP32 Motion Detection Dashboard.

Installation:
    pip install flask flask-cors mysql-connector-python

Usage:
    python app_mysql.py

The server will run on http://localhost:5000
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import json
import os
from dotenv import load_dotenv

# Load environment variables (optional - for security)
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# ==================== DATABASE CONFIGURATION ====================

# MySQL Database Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),  # XAMPP default is empty
    'database': os.getenv('DB_NAME', 'esp32_project'),
    'port': int(os.getenv('DB_PORT', '3306'))
}

# ==================== DATABASE CONNECTION HELPER ====================

def get_db_connection():
    """Create and return a MySQL database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def log_api_call(method, endpoint, status_code, response_time):
    """Log API calls to the database"""
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            query = """
                INSERT INTO api_logs (method, endpoint, status_code, response_time)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (method, endpoint, status_code, response_time))
            conn.commit()
            cursor.close()
            conn.close()
    except Error as e:
        print(f"Error logging API call: {e}")

# ==================== API ENDPOINTS ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        conn = get_db_connection()
        if conn:
            conn.close()
            return jsonify({
                'status': 'healthy',
                'database': 'connected',
                'timestamp': datetime.now().isoformat()
            }), 200
        else:
            return jsonify({
                'status': 'unhealthy',
                'database': 'disconnected',
                'timestamp': datetime.now().isoformat()
            }), 503
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sensor-data', methods=['POST'])
def add_sensor_data():
    """
    Add new sensor data to the database
    
    Expected JSON payload:
    {
        "motion_status": "detected" or "not_detected",
        "temperature": 25.5,
        "latitude": 40.7128,
        "longitude": -74.0060
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'motion_status' not in data:
            return jsonify({'error': 'motion_status is required'}), 400
        
        motion_status = data.get('motion_status', 'unknown')
        temperature = data.get('temperature')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        # Validate motion_status
        valid_statuses = ['detected', 'not_detected', 'unknown']
        if motion_status.lower() not in valid_statuses:
            return jsonify({'error': f'motion_status must be one of: {valid_statuses}'}), 400
        
        # Connect to database
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 503
        
        cursor = conn.cursor()
        
        # Insert data
        query = """
            INSERT INTO sensor_data (motion_status, temperature, latitude, longitude)
            VALUES (%s, %s, %s, %s)
        """
        
        cursor.execute(query, (motion_status, temperature, latitude, longitude))
        conn.commit()
        
        # Get the inserted record ID
        inserted_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Sensor data saved successfully',
            'id': inserted_id,
            'timestamp': datetime.now().isoformat()
        }), 201
    
    except Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sensor-data', methods=['GET'])
def get_sensor_data():
    """
    Retrieve sensor data from the database
    
    Optional query parameters:
    - limit: number of records (default: 100)
    - offset: pagination offset (default: 0)
    - motion: filter by motion_status (detected/not_detected)
    - hours: get data from last N hours
    """
    try:
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        motion_filter = request.args.get('motion', None)
        hours = request.args.get('hours', None, type=int)
        
        # Validate limit
        limit = min(limit, 1000)  # Cap at 1000
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 503
        
        cursor = conn.cursor(dictionary=True)
        
        # Build query
        query = "SELECT * FROM sensor_data WHERE 1=1"
        params = []
        
        if motion_filter:
            query += " AND motion_status = %s"
            params.append(motion_filter)
        
        if hours:
            query += " AND timestamp >= DATE_SUB(NOW(), INTERVAL %s HOUR)"
            params.append(hours)
        
        query += " ORDER BY timestamp DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        # Convert datetime objects to ISO format strings
        for record in results:
            if isinstance(record['timestamp'], datetime):
                record['timestamp'] = record['timestamp'].isoformat()
        
        # Get total count
        count_query = "SELECT COUNT(*) as total FROM sensor_data WHERE 1=1"
        count_params = []
        
        if motion_filter:
            count_query += " AND motion_status = %s"
            count_params.append(motion_filter)
        
        if hours:
            count_query += " AND timestamp >= DATE_SUB(NOW(), INTERVAL %s HOUR)"
            count_params.append(hours)
        
        cursor.execute(count_query, count_params)
        total_count = cursor.fetchone()['total']
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'data': results,
            'total': total_count,
            'limit': limit,
            'offset': offset
        }), 200
    
    except Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sensor-data/<int:record_id>', methods=['GET'])
def get_sensor_data_by_id(record_id):
    """Retrieve a specific sensor record by ID"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 503
        
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM sensor_data WHERE id = %s"
        cursor.execute(query, (record_id,))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not result:
            return jsonify({'error': 'Record not found'}), 404
        
        if isinstance(result['timestamp'], datetime):
            result['timestamp'] = result['timestamp'].isoformat()
        
        return jsonify({'success': True, 'data': result}), 200
    
    except Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sensor-data-delete/<int:record_id>', methods=['DELETE'])
def delete_sensor_data(record_id):
    """Delete a specific sensor record by ID"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 503
        
        cursor = conn.cursor()
        query = "DELETE FROM sensor_data WHERE id = %s"
        cursor.execute(query, (record_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Record not found'}), 404
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'Record {record_id} deleted successfully'
        }), 200
    
    except Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get statistics about motion detection events"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 503
        
        cursor = conn.cursor(dictionary=True)
        
        # Total events
        cursor.execute("SELECT COUNT(*) as total FROM sensor_data")
        total = cursor.fetchone()['total']
        
        # Motion detected count
        cursor.execute("SELECT COUNT(*) as count FROM sensor_data WHERE motion_status = 'detected'")
        motion_detected = cursor.fetchone()['count']
        
        # No motion count
        cursor.execute("SELECT COUNT(*) as count FROM sensor_data WHERE motion_status = 'not_detected'")
        no_motion = cursor.fetchone()['count']
        
        # Average temperature
        cursor.execute("SELECT AVG(temperature) as avg_temp FROM sensor_data WHERE temperature IS NOT NULL")
        avg_temp = cursor.fetchone()['avg_temp']
        
        # Last 24 hours motion events
        cursor.execute("""
            SELECT COUNT(*) as count FROM sensor_data 
            WHERE motion_status = 'detected' AND timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
        """)
        last_24h = cursor.fetchone()['count']
        
        # Get latest timestamp
        cursor.execute("SELECT MAX(timestamp) as latest FROM sensor_data")
        latest = cursor.fetchone()['latest']
        if isinstance(latest, datetime):
            latest = latest.isoformat()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'statistics': {
                'total_events': total,
                'motion_detected': motion_detected,
                'no_motion': no_motion,
                'detection_rate': round((motion_detected / total * 100) if total > 0 else 0, 2),
                'average_temperature': round(avg_temp, 2) if avg_temp else None,
                'last_24h_detections': last_24h,
                'latest_event': latest
            }
        }), 200
    
    except Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analysis', methods=['GET'])
def get_analysis():
    """Get analysis data (for backward compatibility with existing dashboard)"""
    try:
        conn = get_db_connection()
        if not conn:
            # Return mock data if database is unavailable
            return jsonify({
                'motion_detected': False,
                'confidence': 0.0,
                'timestamp': datetime.now().isoformat(),
                'source': 'mock'
            }), 200
        
        cursor = conn.cursor(dictionary=True)
        
        # Get latest sensor data
        query = "SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 1"
        cursor.execute(query)
        latest = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if latest:
            return jsonify({
                'motion_detected': latest['motion_status'] == 'detected',
                'temperature': latest['temperature'],
                'latitude': float(latest['latitude']) if latest['latitude'] else None,
                'longitude': float(latest['longitude']) if latest['longitude'] else None,
                'timestamp': latest['timestamp'].isoformat(),
                'source': 'database'
            }), 200
        else:
            return jsonify({
                'motion_detected': False,
                'confidence': 0.0,
                'timestamp': datetime.now().isoformat(),
                'source': 'database_empty'
            }), 200
    
    except Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  ESP32 Motion Detection Dashboard - MySQL API Server        ║
    ║  Version: 1.0                                               ║
    ║  Starting server...                                         ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    print(f"Database Configuration:")
    print(f"  Host: {DB_CONFIG['host']}")
    print(f"  Port: {DB_CONFIG['port']}")
    print(f"  Database: {DB_CONFIG['database']}")
    print(f"  User: {DB_CONFIG['user']}")
    print()
    
    # Test database connection
    test_conn = get_db_connection()
    if test_conn:
        print("✅ Database connection successful!")
        test_conn.close()
    else:
        print("❌ Database connection failed!")
        print("   Make sure XAMPP MySQL is running and the database exists.")
    
    print("\nAvailable API Endpoints:")
    print("  GET  /api/health                 - Health check")
    print("  POST /api/sensor-data            - Add new sensor data")
    print("  GET  /api/sensor-data            - Get all sensor data")
    print("  GET  /api/sensor-data/<id>       - Get specific sensor data")
    print("  DELETE /api/sensor-data-delete/<id> - Delete sensor data")
    print("  GET  /api/statistics             - Get statistics")
    print("  GET  /api/analysis               - Get analysis data")
    print("\nServer running at http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    
    # Run Flask server
    app.run(debug=True, host='localhost', port=5000, use_reloader=True)
