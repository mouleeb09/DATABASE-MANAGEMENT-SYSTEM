-- ESP32 Advanced Motion Detection Dashboard - MySQL Database Setup
-- =================================================================
-- Run this script in XAMPP phpMyAdmin to create the database and table
-- Database: human_detection
-- Table: detection

-- Create Database
CREATE DATABASE IF NOT EXISTS human_detection;
USE human_detection;

-- Create detection table
CREATE TABLE IF NOT EXISTS detection (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    motion_status VARCHAR(255) NOT NULL,
    radar_status VARCHAR(255) NOT NULL,
    temperature FLOAT NOT NULL,
    person_detected VARCHAR(255) NOT NULL,
    detection_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create indexes for better query performance
CREATE INDEX idx_detection_time ON detection(detection_time);
CREATE INDEX idx_motion_status ON detection(motion_status);
CREATE INDEX idx_person_detected ON detection(person_detected);

-- Insert sample data for testing (optional)
INSERT INTO detection (motion_status, radar_status, temperature, person_detected) VALUES
('MOTION DETECTED', 'RADAR ACTIVE', 25.5, 'YES'),
('NO MOTION', 'RADAR STANDBY', 24.2, 'NO'),
('MOTION DETECTED', 'RADAR ACTIVE', 26.1, 'YES'),
('NO MOTION', 'RADAR STANDBY', 23.8, 'NO');

-- Display success message
SELECT 'Database and table created successfully!' AS Status;</content>
<parameter name="filePath">c:\Users\Lenovo\Documents\dbms webpage creation\database_setup_human_detection.sql