#!/usr/bin/env python3
"""
ESP32 Human Detection Analysis Script
=====================================

This script provides advanced real-time analysis of human detection data
from ESP32 sensors. It processes serial data and performs statistical analysis,
machine learning predictions, and anomaly detection.

Features:
- Real-time data processing from serial input
- Statistical analysis (correlation, trends, patterns)
- Machine learning-based human detection confidence
- Anomaly detection for unusual sensor readings
- Data logging and visualization preparation
- REST API for dashboard integration

Usage:
    python human_analysis.py --port COM3 --baud 115200

Requirements:
    pip install pyserial pandas scikit-learn matplotlib seaborn numpy flask
"""

import serial
import time
import threading
import json
import logging
from datetime import datetime, timedelta
from collections import deque
import statistics
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, jsonify, request
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HumanDetectionAnalyzer:
    def __init__(self, port='COM3', baudrate=115200, max_history=1000):
        self.port = port
        self.baudrate = baudrate
        self.max_history = max_history
        self.serial_conn = None
        self.is_running = False

        # Data storage
        self.motion_data = deque(maxlen=max_history)
        self.heat_data = deque(maxlen=max_history)
        self.temperature_data = deque(maxlen=max_history)
        self.detection_data = deque(maxlen=max_history)
        self.timestamps = deque(maxlen=max_history)

        # Analysis results
        self.analysis_results = {
            'detection_confidence': 0.0,
            'motion_heat_correlation': 0.0,
            'temperature_trend': 'stable',
            'anomaly_score': 0.0,
            'prediction_accuracy': 0.0,
            'last_update': None
        }

        # ML components
        self.ml_model = None
        self.scaler = StandardScaler()
        self.is_trained = False

        # Flask app for API
        self.app = Flask(__name__)
        self.setup_routes()

        logger.info(f"Human Detection Analyzer initialized on {port}:{baudrate}")

    def setup_routes(self):
        @self.app.route('/api/analysis', methods=['GET'])
        def get_analysis():
            return jsonify(self.analysis_results)

        @self.app.route('/api/data', methods=['GET'])
        def get_recent_data():
            limit = int(request.args.get('limit', 100))
            data = {
                'timestamps': list(self.timestamps)[-limit:],
                'motion': list(self.motion_data)[-limit:],
                'heat': list(self.heat_data)[-limit:],
                'temperature': list(self.temperature_data)[-limit:],
                'detection': list(self.detection_data)[-limit:]
            }
            return jsonify(data)

        @self.app.route('/api/stats', methods=['GET'])
        def get_stats():
            if len(self.motion_data) < 10:
                return jsonify({'error': 'Insufficient data for statistics'})

            stats = {
                'motion_rate': self.calculate_motion_rate(),
                'heat_detection_rate': self.calculate_heat_detection_rate(),
                'avg_temperature': statistics.mean([t for t in self.temperature_data if t != '--']),
                'temperature_variance': statistics.variance([t for t in self.temperature_data if t != '--']) if len([t for t in self.temperature_data if t != '--']) > 1 else 0,
                'detection_accuracy': self.calculate_detection_accuracy(),
                'data_points': len(self.motion_data)
            }
            return jsonify(stats)

    def connect_serial(self):
        try:
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=1)
            logger.info(f"Connected to {self.port} at {self.baudrate} baud")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to serial port: {e}")
            return False

    def parse_sensor_data(self, line):
        """Parse incoming sensor data from ESP32"""
        line = line.strip()
        if not line:
            return None

        data = {
            'motion': None,
            'heat': None,
            'temperature': None,
            'timestamp': datetime.now()
        }

        # Parse motion
        import re
        motion_match = re.search(r'motion\s*[:=]\s*(on|off|1|0)', line, re.IGNORECASE)
        if motion_match:
            data['motion'] = 1 if motion_match.group(1).lower() in ['on', '1'] else 0

        # Parse heat
        heat_match = re.search(r'heat[^a-zA-Z0-9]*[:=][^a-zA-Z0-9]*([0|1|true|false|detected|not[_ ]*detected|yes|no])', line, re.IGNORECASE)
        if heat_match:
            heat_val = heat_match.group(1).lower().replace('_', '').replace(' ', '')
            data['heat'] = 1 if heat_val in ['1', 'true', 'detected', 'yes'] else 0

        # Parse temperature
        temp_match = re.search(r'temp(?:erature)?\s*[:=]\s*(-?\d+(?:\.\d+)?)', line, re.IGNORECASE)
        if temp_match:
            data['temperature'] = float(temp_match.group(1))

        return data if any(data.values()) else None

    def add_data_point(self, data):
        """Add a new data point and update analysis"""
        if not data:
            return

        timestamp = data['timestamp']

        # Add to deques
        self.timestamps.append(timestamp.isoformat())
        self.motion_data.append(data['motion'] if data['motion'] is not None else 0)
        self.heat_data.append(data['heat'] if data['heat'] is not None else 0)
        self.temperature_data.append(data['temperature'] if data['temperature'] is not None else 25.0)

        # Calculate human detection (motion AND heat)
        detection = 1 if (data['motion'] == 1 and data['heat'] == 1) else 0
        self.detection_data.append(detection)

        # Update analysis
        self.update_analysis()

        logger.debug(f"Added data point: Motion={data['motion']}, Heat={data['heat']}, Temp={data['temperature']}, Detection={detection}")

    def update_analysis(self):
        """Update all analysis metrics"""
        if len(self.motion_data) < 5:
            return

        # Detection confidence (correlation between motion and heat)
        if len(self.motion_data) >= 10:
            motion_heat_corr = np.corrcoef(list(self.motion_data), list(self.heat_data))[0, 1]
            self.analysis_results['motion_heat_correlation'] = round(motion_heat_corr, 3)

            # Detection confidence based on correlation and recent detections
            recent_detections = list(self.detection_data)[-10:]
            detection_rate = sum(recent_detections) / len(recent_detections)
            confidence = (detection_rate + abs(motion_heat_corr)) / 2
            self.analysis_results['detection_confidence'] = round(confidence * 100, 1)

        # Temperature trend analysis
        if len(self.temperature_data) >= 20:
            temps = list(self.temperature_data)[-20:]
            trend = np.polyfit(range(len(temps)), temps, 1)[0]
            if trend > 0.1:
                self.analysis_results['temperature_trend'] = 'rising'
            elif trend < -0.1:
                self.analysis_results['temperature_trend'] = 'falling'
            else:
                self.analysis_results['temperature_trend'] = 'stable'

        # Anomaly detection (simple z-score based)
        if len(self.temperature_data) >= 50:
            temps = np.array(list(self.temperature_data))
            mean_temp = np.mean(temps)
            std_temp = np.std(temps)
            current_temp = temps[-1]
            z_score = abs(current_temp - mean_temp) / std_temp if std_temp > 0 else 0
            self.analysis_results['anomaly_score'] = round(z_score, 2)

        # Train/update ML model periodically
        if len(self.motion_data) >= 100 and len(self.motion_data) % 50 == 0:
            self.train_ml_model()

        self.analysis_results['last_update'] = datetime.now().isoformat()

    def train_ml_model(self):
        """Train ML model for human detection prediction"""
        if len(self.motion_data) < 50:
            return

        # Prepare training data
        X = []
        y = []

        for i in range(10, len(self.motion_data)):
            # Use last 10 readings as features
            features = []
            features.extend(list(self.motion_data)[i-10:i])
            features.extend(list(self.heat_data)[i-10:i])
            features.extend([t if t != '--' else 25.0 for t in list(self.temperature_data)[i-10:i]])

            X.append(features)
            y.append(list(self.detection_data)[i])

        if len(X) < 20:
            return

        # Train model
        self.ml_model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.ml_model.fit(X, y)
        self.is_trained = True

        # Calculate prediction accuracy
        predictions = self.ml_model.predict(X)
        accuracy = np.mean(predictions == y)
        self.analysis_results['prediction_accuracy'] = round(accuracy * 100, 1)

        logger.info(f"ML model trained with {len(X)} samples, accuracy: {accuracy:.3f}")

    def calculate_motion_rate(self):
        """Calculate motion events per minute"""
        if len(self.motion_data) < 2:
            return 0

        recent_motion = [i for i, m in enumerate(self.motion_data) if m == 1]
        if not recent_motion:
            return 0

        time_span_minutes = len(self.motion_data) / 60  # Assuming 1 reading per second
        return len(recent_motion) / time_span_minutes if time_span_minutes > 0 else 0

    def calculate_heat_detection_rate(self):
        """Calculate heat detection rate"""
        if not self.heat_data:
            return 0
        return sum(self.heat_data) / len(self.heat_data) * 100

    def calculate_detection_accuracy(self):
        """Calculate detection accuracy based on motion-heat correlation"""
        if len(self.motion_data) < 10:
            return 0

        # Simple accuracy: how often detection matches expected pattern
        detections = list(self.detection_data)
        expected = [1 if m and h else 0 for m, h in zip(self.motion_data, self.heat_data)]

        correct = sum(1 for d, e in zip(detections, expected) if d == e)
        return correct / len(detections) * 100 if detections else 0

    def read_serial_data(self):
        """Main serial reading loop"""
        buffer = ""
        while self.is_running and self.serial_conn:
            try:
                if self.serial_conn.in_waiting:
                    char = self.serial_conn.read().decode('utf-8', errors='ignore')
                    buffer += char

                    if '\n' in buffer:
                        lines = buffer.split('\n')
                        buffer = lines[-1]  # Keep incomplete line

                        for line in lines[:-1]:
                            if line.strip():
                                logger.info(f"Raw serial line received: {line.strip()}")
                                data = self.parse_sensor_data(line)
                                if data:
                                    logger.info(f"Parsed data: Motion={data['motion']}, Heat={data['heat']}, Temp={data['temperature']}")
                                    self.add_data_point(data)

                time.sleep(0.01)  # Small delay to prevent CPU hogging

            except Exception as e:
                logger.error(f"Error reading serial data: {e}")
                time.sleep(1)

    def start_analysis(self):
        """Start the analysis system"""
        if not self.connect_serial():
            return False

        self.is_running = True

        # Start serial reading thread
        serial_thread = threading.Thread(target=self.read_serial_data, daemon=True)
        serial_thread.start()

        # Start Flask API in separate thread
        api_thread = threading.Thread(target=lambda: self.app.run(host='0.0.0.0', port=5000, debug=False), daemon=True)
        api_thread.start()

        logger.info("Human Detection Analysis started")
        logger.info("API available at http://localhost:5000")
        logger.info("Press Ctrl+C to stop")

        try:
            while self.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_analysis()

        return True

    def stop_analysis(self):
        """Stop the analysis system"""
        self.is_running = False
        if self.serial_conn:
            self.serial_conn.close()
        logger.info("Human Detection Analysis stopped")

    def save_data(self, filename="human_detection_data.json"):
        """Save collected data to file"""
        data = {
            'timestamps': list(self.timestamps),
            'motion': list(self.motion_data),
            'heat': list(self.heat_data),
            'temperature': list(self.temperature_data),
            'detection': list(self.detection_data),
            'analysis': self.analysis_results
        }

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

        logger.info(f"Data saved to {filename}")

def main():
    import argparse

    parser = argparse.ArgumentParser(description='ESP32 Human Detection Analysis')
    parser.add_argument('--port', default='COM3', help='Serial port (default: COM3)')
    parser.add_argument('--baud', type=int, default=115200, help='Baud rate (default: 115200)')
    parser.add_argument('--save', action='store_true', help='Save data on exit')

    args = parser.parse_args()

    analyzer = HumanDetectionAnalyzer(port=args.port, baudrate=args.baud)

    try:
        if analyzer.start_analysis():
            if args.save:
                analyzer.save_data()
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
    finally:
        analyzer.stop_analysis()

if __name__ == "__main__":
    main()