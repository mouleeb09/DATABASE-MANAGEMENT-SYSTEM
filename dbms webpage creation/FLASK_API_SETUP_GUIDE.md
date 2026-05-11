# ESP32 Advanced Motion Detection Dashboard - Complete Setup Guide
========================================================================

This guide provides step-by-step instructions to set up the complete Flask backend server for your ESP32 motion detection system.

## 📋 Prerequisites

- Python 3.8 or higher installed
- XAMPP installed and running (MySQL service)
- ESP32 with PIR and radar sensors (optional for testing)
- Web browser for testing APIs

## 🗄️ Step 1: Database Setup

### 1.1 Start XAMPP
1. Open XAMPP Control Panel
2. Start **Apache** and **MySQL** services
3. Click **Admin** button next to MySQL (opens phpMyAdmin)

### 1.2 Create Database and Table
1. In phpMyAdmin, click **New** in the left sidebar
2. Database name: `human_detection`
3. Collation: `utf8mb4_unicode_ci`
4. Click **Create**

### 1.3 Create Table
Copy and paste the following SQL in the SQL tab:

```sql
CREATE TABLE IF NOT EXISTS detection (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    motion_status VARCHAR(255) NOT NULL,
    radar_status VARCHAR(255) NOT NULL,
    temperature FLOAT NOT NULL,
    person_detected VARCHAR(255) NOT NULL,
    detection_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_detection_time ON detection(detection_time);
CREATE INDEX idx_motion_status ON detection(motion_status);
CREATE INDEX idx_person_detected ON detection(person_detected);
```

### 1.4 Insert Sample Data (Optional)
```sql
INSERT INTO detection (motion_status, radar_status, temperature, person_detected) VALUES
('MOTION DETECTED', 'RADAR ACTIVE', 25.5, 'YES'),
('NO MOTION', 'RADAR STANDBY', 24.2, 'NO');
```

## 🐍 Step 2: Python Environment Setup

### 2.1 Install Dependencies
Open Command Prompt/Terminal in your project folder and run:

```bash
pip install flask==2.3.3
pip install flask-cors==4.0.0
pip install pymysql==1.1.0
pip install python-dotenv==1.0.0
```

Or install all at once:
```bash
pip install -r requirements.txt
```

### 2.2 Verify Installation
```bash
python -c "import flask, flask_cors, pymysql; print('All dependencies installed successfully!')"
```

## 🚀 Step 3: Run the Flask Server

### 3.1 Start the Server
```bash
python api_server.py
```

You should see output like:
```
🚀 ESP32 Motion Detection Dashboard API Server
==================================================
📊 Database: human_detection (MySQL via XAMPP)
📋 Table: detection
🌐 Server: http://127.0.0.1:5000

📍 Endpoints:
   POST /save_data  - Save sensor data from ESP32
   GET  /get_data   - Get latest detection records
   GET  /health     - Health check

⚠️  Make sure XAMPP MySQL is running!
Press Ctrl+C to stop the server
```

### 3.2 Verify Server is Running
Open browser and go to: `http://127.0.0.1:5000/health`

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-01-XX..."
}
```

## 🧪 Step 4: Test the APIs

### 4.1 Test POST /save_data

#### Using Browser (Simple Test)
Open browser and go to: `http://127.0.0.1:5000/save_data`

**Note:** Browsers can't send POST requests directly. Use one of the methods below.

#### Using curl (Command Line)
```bash
curl -X POST http://127.0.0.1:5000/save_data \
  -H "Content-Type: application/json" \
  -d '{
    "motion_status": "MOTION DETECTED",
    "radar_status": "RADAR ACTIVE",
    "temperature": "32.5",
    "person_detected": "YES"
  }'
```

#### Using Postman
1. Open Postman
2. Create new request: POST `http://127.0.0.1:5000/save_data`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
```json
{
  "motion_status": "MOTION DETECTED",
  "radar_status": "RADAR ACTIVE",
  "temperature": "32.5",
  "person_detected": "YES"
}
```
5. Click **Send**

**Expected Response:**
```json
{
  "success": true,
  "message": "Data saved successfully",
  "record_id": 1,
  "timestamp": "2024-01-XX..."
}
```

### 4.2 Test GET /get_data

#### Using Browser
Open: `http://127.0.0.1:5000/get_data`

Or with limit: `http://127.0.0.1:5000/get_data?limit=5`

#### Using curl
```bash
curl http://127.0.0.1:5000/get_data
```

**Expected Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "motion_status": "MOTION DETECTED",
      "radar_status": "RADAR ACTIVE",
      "temperature": 32.5,
      "person_detected": "YES",
      "detection_time": "2024-01-XX..."
    }
  ],
  "count": 1,
  "timestamp": "2024-01-XX..."
}
```

## 🌐 Step 5: Frontend Integration

### 5.1 JavaScript fetch() Example

Add this code to your dashboard's JavaScript to send data:

```javascript
// Function to send sensor data to Flask API
async function sendSensorData(motionStatus, radarStatus, temperature, personDetected) {
    try {
        const response = await fetch('http://127.0.0.1:5000/save_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                motion_status: motionStatus,
                radar_status: radarStatus,
                temperature: temperature.toString(),
                person_detected: personDetected
            })
        });

        const result = await response.json();

        if (result.success) {
            console.log('Data saved successfully:', result.record_id);
            return true;
        } else {
            console.error('Failed to save data:', result.message);
            return false;
        }
    } catch (error) {
        console.error('Error sending data:', error);
        return false;
    }
}

// Function to get latest detection data
async function getDetectionData(limit = 10) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/get_data?limit=${limit}`);
        const result = await response.json();

        if (result.success) {
            console.log(`Retrieved ${result.count} records`);
            return result.data;
        } else {
            console.error('Failed to get data:', result.message);
            return [];
        }
    } catch (error) {
        console.error('Error fetching data:', error);
        return [];
    }
}

// Example usage:
// Send data from ESP32
// sendSensorData('MOTION DETECTED', 'RADAR ACTIVE', 32.5, 'YES');

// Get latest 5 records
// const data = await getDetectionData(5);
```

### 5.2 ESP32 Integration

Your ESP32 should send HTTP POST requests to the Flask server. Example Arduino code:

```cpp
#include <WiFi.h>
#include <HTTPClient.h>

// WiFi credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Flask server URL
const char* serverUrl = "http://192.168.1.100:5000/save_data"; // Use your computer's IP

void sendDataToServer(String motionStatus, String radarStatus, float temperature, String personDetected) {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(serverUrl);
        http.addHeader("Content-Type", "application/json");

        String jsonData = "{";
        jsonData += "\"motion_status\":\"" + motionStatus + "\",";
        jsonData += "\"radar_status\":\"" + radarStatus + "\",";
        jsonData += "\"temperature\":\"" + String(temperature) + "\",";
        jsonData += "\"person_detected\":\"" + personDetected + "\"";
        jsonData += "}";

        int httpResponseCode = http.POST(jsonData);

        if (httpResponseCode > 0) {
            String response = http.getString();
            Serial.println("Data sent successfully: " + response);
        } else {
            Serial.println("Error sending data: " + String(httpResponseCode));
        }

        http.end();
    }
}
```

## 🔧 Troubleshooting

### Database Connection Issues
- Ensure XAMPP MySQL is running
- Check database name: `human_detection`
- Check table name: `detection`
- Default MySQL credentials: user=`root`, password=`` (empty)

### Port Already in Use
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace XXXX with PID)
taskkill /PID XXXX /F
```

### CORS Issues
- Flask-CORS is enabled by default
- If issues persist, check browser console for CORS errors

### Import Errors
```bash
# Reinstall dependencies
pip uninstall flask flask-cors pymysql
pip install -r requirements.txt
```

## 📁 Project Structure

```
your-project/
├── api_server.py              # Flask API server (main file)
├── requirements.txt            # Python dependencies
├── database_setup_human_detection.sql  # Database setup script
├── index_simple.html          # Your dashboard (frontend)
├── chart.js                   # Chart library
└── README.md                  # Project documentation
```

## 🎯 API Reference

### POST /save_data
**Save sensor data from ESP32**

**Request Body:**
```json
{
  "motion_status": "MOTION DETECTED",
  "radar_status": "RADAR ACTIVE",
  "temperature": "32.5",
  "person_detected": "YES"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Data saved successfully",
  "record_id": 1,
  "timestamp": "2024-01-XX..."
}
```

### GET /get_data
**Retrieve latest detection records**

**Query Parameters:**
- `limit` (optional): Number of records (1-100, default: 10)

**Response:**
```json
{
  "success": true,
  "data": [...],
  "count": 10,
  "timestamp": "2024-01-XX..."
}
```

### GET /health
**Health check**

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-01-XX..."
}
```

## 🚀 Next Steps

1. **Test the APIs** using Postman or browser
2. **Integrate with your ESP32** code
3. **Update your dashboard** to use the new API endpoints
4. **Add error handling** in your frontend code
5. **Deploy to production** when ready

## 📞 Support

If you encounter issues:
1. Check the server console for error messages
2. Verify XAMPP MySQL is running
3. Test database connection manually in phpMyAdmin
4. Check firewall settings if accessing from ESP32

Happy coding! 🎉</content>
<parameter name="filePath">c:\Users\Lenovo\Documents\dbms webpage creation\FLASK_API_SETUP_GUIDE.md