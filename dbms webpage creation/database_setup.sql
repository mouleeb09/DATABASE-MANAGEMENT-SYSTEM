-- ESP32 Motion Detection Dashboard - MySQL Database Setup
-- ========================================================
-- Run this script in XAMPP phpMyAdmin to create the database and tables

-- Create Database
CREATE DATABASE IF NOT EXISTS esp32_project;
USE esp32_project;

-- Create sensor_data table
CREATE TABLE IF NOT EXISTS sensor_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    motion_status VARCHAR(50) NOT NULL,
    temperature FLOAT DEFAULT NULL,
    latitude DECIMAL(10, 6) DEFAULT NULL,
    longitude DECIMAL(10, 6) DEFAULT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_timestamp (timestamp),
    INDEX idx_motion_status (motion_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create motion_history table (optional - for trend analysis)
CREATE TABLE IF NOT EXISTS motion_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    motion_count INT DEFAULT 0,
    total_events INT DEFAULT 0,
    average_interval INT DEFAULT 0,
    accuracy_rate FLOAT DEFAULT 0,
    recording_date DATE DEFAULT CURDATE(),
    recording_time TIME DEFAULT CURTIME(),
    UNIQUE KEY unique_recording (recording_date, recording_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create API logs table (optional - for debugging)
CREATE TABLE IF NOT EXISTS api_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    method VARCHAR(10),
    endpoint VARCHAR(200),
    status_code INT,
    response_time INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert sample data (optional - for testing)
INSERT INTO sensor_data (motion_status, temperature, latitude, longitude) 
VALUES 
    ('detected', 25.5, 40.7128, -74.0060, DEFAULT),
    ('not_detected', 24.2, 40.7128, -74.0060, DEFAULT),
    ('detected', 26.1, 40.7130, -74.0062, DEFAULT);

-- Display the created tables
SHOW TABLES;

-- Display structure of sensor_data table
DESCRIBE sensor_data;
