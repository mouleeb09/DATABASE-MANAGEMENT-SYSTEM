ESP32 Motion Detection Dashboard - MongoDB Integration Guide
============================================================

## Complete Setup Instructions

### System Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                    WEB DASHBOARD                                │
│                    (index_simple.html)                          │
│              - Motion Detection Display                         │
│              - Location Tracking                                │
│              - Real-time Charts                                 │
│              - Sends data via fetch() POST                      │
└────────────────────────────────┬────────────────────────────────┘
                                 │ (JSON over HTTP)
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PYTHON FLASK API                             │
│                    (app_mysql.py)                               │
│              - Localhost:5000                                   │
│              - REST API Endpoints                               │
│              - Data Validation                                  │
│              - Connects to MySQL                                │
└────────────────────────────────┬────────────────────────────────┘
                                 │ (SQL Queries)
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MYSQL DATABASE                               │
│                    (XAMPP/PhpMyAdmin)                           │
│              - Database: esp32_project                          │
│              - Table: sensor_data                               │
│              - Stores: Motion, Temp, Location, Timestamp       │
└─────────────────────────────────────────────────────────────────┘
```

### Files in This Project
```
dbms webpage creation/
├── index_simple.html          # Dashboard UI with MySQL integration
├── app_mysql.py               # Python Flask API with MySQL
├── database_setup.sql         # SQL script to create database
├── requirements.txt           # Python dependencies
├── chart.js                   # Chart library
├── README.md                  # Project documentation
└── api_server.py              # Original mock API (optional)
```

---

## STEP 1: Install XAMPP and Start MySQL

### Windows Installation Steps:

1. **Download XAMPP**
   - Go to https://www.apachefriends.org/
   - Download the Windows version
   - File size: ~150MB

2. **Install XAMPP**
   - Run the installer
   - Select components: Apache, MySQL, PHP, PhpMyAdmin
   - Default installation path: `C:\xampp`
   - Complete the installation

3. **Start MySQL Service**
   - Open XAMPP Control Panel
   - Click "Start" button next to MySQL
   - Wait for it to show "Running" status
   - Status should turn GREEN

4. **Verify Installation**
   - Open browser and go to: http://localhost/phpmyadmin
   - You should see PhpMyAdmin dashboard
   - Take screenshot for reference

---

## STEP 2: Create Database and Tables

### Using PhpMyAdmin (Easiest Method):

1. **Open PhpMyAdmin**
   - Go to http://localhost/phpmyadmin
   - Login with default credentials (no username/password required)

2. **Create Database**
   - Click "Databases" tab
   - Enter "esp32_project" in "Create database" field
   - Click "Create"
   - You should see the database created

3. **Create Tables**
   - Click on "esp32_project" database
   - Go to "SQL" tab
   - Copy the entire contents of `database_setup.sql` file
   - Paste into the SQL editor
   - Click "Go" to execute
   - You should see success messages for table creation

4. **Verify Tables**
   - Refresh the page
   - You should see three tables:
     - sensor_data
     - motion_history
     - api_logs

### Alternative: Using Command Line

```bash
# Open MySQL Command Prompt from XAMPP
cd C:\xampp\mysql\bin
mysql -u root -p

# Paste password: (leave blank, just press Enter)

# Then run:
CREATE DATABASE esp32_project;
USE esp32_project;

# Copy and paste the SQL from database_setup.sql here
```

---

## STEP 3: Install Python Dependencies

### Windows Command Prompt:

```bash
# Navigate to your project folder
cd "c:\Users\Lenovo\Documents\dbms webpage creation"

# Install required packages
pip install -r requirements.txt

# Or install individually:
pip install flask
pip install flask-cors
pip install mysql-connector-python
pip install python-dotenv
```

### Troubleshooting Installation:

If you get permission errors, use:
```bash
pip install --user -r requirements.txt
```

If mysql-connector-python fails:
```bash
pip install --upgrade setuptools
pip install mysql-connector-python
```

---

## STEP 4: Run the Flask API Server

### Start the Server:

```bash
# Navigate to project folder
cd "c:\Users\Lenovo\Documents\dbms webpage creation"

# Run the Flask app
python app_mysql.py

# You should see:
# ✅ Database connection successful!
#    Server running at http://localhost:5000
#    Press Ctrl+C to stop
```

### Keep This Terminal Open!
Do NOT close this terminal window. The Flask server must be running for the dashboard to work.

### Test the API:

Open a new browser tab and go to:
- http://localhost:5000/api/health

You should see:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-04-09T10:30:45.123456"
}
```

---

## STEP 5: Open the Dashboard

### Open in Web Browser:

1. **Navigate to Dashboard**
   - Open your browser
   - Go to: `file:///c:/Users/Lenovo/Documents/dbms%20webpage%20creation/index_simple.html`
   - Or drag index_simple.html into browser

2. **Check API Connection**
   - Look at the "Debug Output" section
   - You should see: "✅ MySQL API connected"
   - If NOT, check that Flask server is running

3. **Test Motion Detection**
   - Click "Connect ESP32" button
   - Simulate motion events by entering data at serial port
   - When motion is detected, dashboard shows "MOTION DETECTED"
   - Data is automatically sent to MySQL

---

## STEP 6: Simulate Data (Without ESP32)

### Option 1: Using API Directly

Open a terminal and send data to the API:

```bash
# Using curl (Windows PowerShell)
$body = @{
    motion_status = "detected"
    temperature = 25.5
    latitude = 40.7128
    longitude = -74.0060
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/sensor-data" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body
```

### Option 2: Using Python Script

Create `test_api.py`:

```python
import requests
import json
from datetime import datetime

API_URL = "http://localhost:5000/api/sensor-data"

# Add motion detected
response = requests.post(API_URL, json={
    "motion_status": "detected",
    "temperature": 25.5,
    "latitude": 40.7128,
    "longitude": -74.0060
})

print(f"Response: {response.json()}")

# Add no motion
response = requests.post(API_URL, json={
    "motion_status": "not_detected",
    "temperature": 24.2,
    "latitude": 40.7128,
    "longitude": -74.0060
})

print(f"Response: {response.json()}")

# Get all data
response = requests.get(API_URL)
print(f"\nAll data: {json.dumps(response.json(), indent=2)}")

# Get statistics
response = requests.get("http://localhost:5000/api/statistics")
print(f"\nStatistics: {json.dumps(response.json(), indent=2)}")
```

Run with:
```bash
python test_api.py
```

---

## STEP 7: Verify Data in MySQL

### Check Data in PhpMyAdmin:

1. **Open PhpMyAdmin**
   - Go to http://localhost/phpmyadmin

2. **Browse Data**
   - Click esp32_project database
   - Click sensor_data table
   - You should see all motion detection records

3. **View SQL Queries**
   - Get all records: `SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 100;`
   - Count motions: `SELECT COUNT(*) FROM sensor_data WHERE motion_status = 'detected';`
   - Recent data: `SELECT * FROM sensor_data WHERE timestamp > DATE_SUB(NOW(), INTERVAL 1 HOUR);`

---

## STEP 8: Connect with ESP32 (Optional)

### ESP32 Arduino Code:

```cpp
char motionStatus;

void setup() {
  Serial.begin(115200);
  pinMode(PIR_PIN, INPUT);
}

void loop() {
  motionStatus = digitalRead(PIR_PIN);
  
  if (motionStatus == HIGH) {
    Serial.println("motion detected");
  } else {
    Serial.println("no motion");
  }
  
  delay(1000);
}
```

The dashboard will automatically:
1. Detect serial data from ESP32
2. Parse "motion detected" or "no motion"
3. Update the UI display
4. Send to MySQL API
5. Store in database

---

## API ENDPOINTS REFERENCE

### 1. Health Check
```
GET /api/health

Response:
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-04-09T10:30:45.123456"
}
```

### 2. Add Sensor Data
```
POST /api/sensor-data

Payload:
{
  "motion_status": "detected",      // Required: "detected" or "not_detected"
  "temperature": 25.5,              // Optional: Temperature in Celsius
  "latitude": 40.7128,              // Optional: GPS latitude
  "longitude": -74.0060             // Optional: GPS longitude
}

Response:
{
  "success": true,
  "message": "Sensor data saved successfully",
  "id": 1,
  "timestamp": "2024-04-09T10:30:45.123456"
}
```

### 3. Get All Sensor Data
```
GET /api/sensor-data?limit=50&offset=0&motion=detected&hours=24

Parameters:
  limit: Number of records (default 100, max 1000)
  offset: Pagination offset (default 0)
  motion: Filter by "detected" or "not_detected"
  hours: Get data from last N hours

Response:
{
  "success": true,
  "data": [
    {
      "id": 1,
      "motion_status": "detected",
      "temperature": 25.5,
      "latitude": 40.7128,
      "longitude": -74.0060,
      "timestamp": "2024-04-09T10:30:45.123456"
    }
  ],
  "total": 42,
  "limit": 50,
  "offset": 0
}
```

### 4. Get Statistics
```
GET /api/statistics

Response:
{
  "success": true,
  "statistics": {
    "total_events": 100,
    "motion_detected": 35,
    "no_motion": 65,
    "detection_rate": 35.0,
    "average_temperature": 25.3,
    "last_24h_detections": 12,
    "latest_event": "2024-04-09T10:30:45.123456"
  }
}
```

---

## TROUBLESHOOTING

### Dashboard shows "MySQL API unavailable"

**Problem**: Cannot connect to the Flask API
**Solutions**:
1. Make sure Flask server is running (python app_mysql.py)
2. Check Flask terminal for errors
3. Try accessing http://localhost:5000/api/health directly
4. Firewall might be blocking - add exception for port 5000

### "Database connection failed"

**Problem**: Flask cannot connect to MySQL
**Solutions**:
1. Check XAMPP MySQL is running (should be GREEN in Control Panel)
2. Verify database "esp32_project" exists in PhpMyAdmin
3. Check database credentials in app_mysql.py:
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'user': 'root',
       'password': '',  # XAMPP default is empty
       'database': 'esp32_project'
   }
   ```

### Data not saving to database

**Problem**: Motion events detected but not in database
**Solutions**:
1. Check Flask terminal for error messages
2. Click "Get Location" button first to authorize geolocation
3. Try sending test data directly:
   ```bash
   curl -X POST http://localhost:5000/api/sensor-data 
        -H "Content-Type: application/json" 
        -d '{"motion_status":"detected"}'
   ```

### ESP32 Serial Connection Issues

**Problem**: Chrome/Browser can't find ESP32
**Solutions**:
1. Install CH340 drivers (Google "CH340 driver windows")
2. Open Device Manager and check for unknown devices
3. Try different USB cable
4. Try different USB port
5. Use Arduino IDE to verify ESP32 works first

### Permission Denied Errors

**Problem**: Python can't write to database
**Solutions**:
1. Run Command Prompt as Administrator
2. Check folder permissions
3. Try running Flask with: `python -u app_mysql.py`

---

## NEXT STEPS

### 1. Monitor Data
- Check PhpMyAdmin regularly to verify data is being saved
- Use API endpoints to query statistics

### 2. Visualize Data
- Create charts from sensor_data table
- Generate motion detection reports

### 3. Set Up Alerts
- Add email notifications for motion detection
- Create automated response system

### 4. Deploy to Production
- Move to Raspberry Pi or Linux server
- Use production database (AWS RDS, Google Cloud SQL)
- Add authentication and API keys
- Enable HTTPS/SSL

### 5. Database Backup
```bash
# Backup database
mysqldump -u root -p esp32_project > backup.sql

# Restore database
mysql -u root -p esp32_project < backup.sql
```

---

## ADDITIONAL NOTES

- Dashboard works without ESP32 (you can simulate events)
- API runs on localhost:5000 (change in app_mysql.py if needed)
- MySQL default user is "root" with no password in XAMPP
- Browser geolocation requires HTTPS in production
- Sensor data is stored indefinitely in MySQL

---

## SUPPORT & DOCUMENTATION

- Flask Documentation: https://flask.palletsprojects.com/
- MySQL Documentation: https://dev.mysql.com/doc/
- MySQL-Connector-Python: https://dev.mysql.com/doc/connector-python/en/
- ES6 Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API

---

Last Updated: April 9, 2024
Project: ESP32 Motion Detection Dashboard with MySQL Integration
