# ESP32 Motion Detection Dashboard - Complete Implementation Guide

## 📋 Overview

Your ESP32 Motion Detection Dashboard is now fully integrated with a MySQL database using XAMPP. This solution provides:

- **Frontend**: Modern dark-themed HTML/CSS/JavaScript dashboard
- **Backend**: Python Flask API with MySQL connectivity
- **Database**: MySQL with XAMPP (local development)
- **Data Flow**: ESP32 → Dashboard → Flask API → MySQL

---

## 📁 Project Structure

```
dbms webpage creation/
│
├── 🌐 Frontend Files
│   ├── index_simple.html          ← Updated dashboard with API integration
│   ├── chart.js                   ← Chart library
│   └── test_chart.html            ← Chart testing page
│
├── 🐍 Python API Files
│   ├── app_mysql.py               ← NEW: Flask API with MySQL (USE THIS!)
│   ├── api_server.py              ← Old mock API (for reference)
│   ├── test_api.py                ← NEW: Test script without ESP32
│   └── requirements.txt             ← NEW: Python dependencies
│
├── 💾 Database Files
│   ├── database_setup.sql          ← NEW: Database creation script
│   └── (XAMPP MySQL data)
│
├── 📚 Documentation Files
│   ├── MYSQL_SETUP_GUIDE.md        ← NEW: Detailed setup guide
│   ├── IMPLEMENTATION_GUIDE.md     ← This file
│   ├── QUICK_START.md              ← Updated: Quick start guide
│   ├── README.md                   ← Project overview
│   └── SETUP_GUIDE.md              ← Original setup guide
│
├── 🔧 Hardware Files
│   ├── ESP32_PIR_Sketch.ino        ← ESP32 Arduino code
│   ├── PINOUT_REFERENCE.md         ← Hardware connections
│   └── PROJECT_SUMMARY.md          ← Project overview
│
└── 📊 Analysis Files
    ├── human_analysis.py           ← Data analysis script
    ├── INDEX.md                    ← File index
    ├── TODO.md                     ← Task list
    └── COMPLETION_SUMMARY.md       ← Previous completion notes
```

---

## 🚀 Complete Setup Workflow

### Phase 1: Environment Setup (5 minutes)

#### 1.1 Install XAMPP
- Download: https://www.apachefriends.org/
- Install with MySQL, PHP, Apache components
- Default location: `C:\xampp`

#### 1.2 Start MySQL Service
```
XAMPP Control Panel → Click "Start" next to MySQL → Should turn GREEN
```

#### 1.3 Install Python Packages
```bash
cd "c:\Users\Lenovo\Documents\dbms webpage creation"
pip install -r requirements.txt
```

### Phase 2: Database Setup (3 minutes)

#### 2.1 Access PhpMyAdmin
```
Browser → http://localhost/phpmyadmin
```

#### 2.2 Create Database and Tables
```
1. Click "Databases" tab
2. Create database "esp32_project"
3. Go to "SQL" tab
4. Copy contents of database_setup.sql
5. Paste and click "Go"
```

### Phase 3: Start Services (2 minutes)

#### 3.1 Start Flask API Server
```bash
python app_mysql.py
```

**Expected Output:**
```
✅ Database connection successful!
Server running at http://localhost:5000
Available API Endpoints:
  GET  /api/health
  POST /api/sensor-data
  GET  /api/sensor-data
  ... and more
Press Ctrl+C to stop
```

**Keep this terminal open!**

#### 3.2 Open Dashboard
```
File → Open → c:\Users\Lenovo\Documents\dbms webpage creation\index_simple.html
Or drag file into browser
```

### Phase 4: Test & Verify (5 minutes)

#### 4.1 Check API Connection
- Look at "Debug Output" section in dashboard
- Should show: ✅ "MySQL API connected"

#### 4.2 Test Motion Detection
- Option A: Connect real ESP32 (click "Connect ESP32")
- Option B: Run test script: `python test_api.py`
- Option C: Send manual POST request to API

#### 4.3 Verify Data in Database
- PhpMyAdmin → esp32_project → sensor_data
- Should see motion records with timestamps

---

## 🔌 API Reference

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Health Check
```
GET /api/health

Response:
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-04-09T10:30:45.123456"
}
```

#### 2. Add Sensor Data ⭐
```
POST /api/sensor-data
Content-Type: application/json

{
  "motion_status": "detected",      (required: "detected" or "not_detected")
  "temperature": 25.5,              (optional: float)
  "latitude": 40.7128,              (optional: decimal)
  "longitude": -74.0060             (optional: decimal)
}

Response (201 Created):
{
  "success": true,
  "message": "Sensor data saved successfully",
  "id": 42,
  "timestamp": "2024-04-09T10:30:45.123456"
}
```

#### 3. Get All Sensor Data
```
GET /api/sensor-data?limit=50&offset=0&motion=detected&hours=24

Query Parameters:
  limit:  Number of records (1-1000, default 100)
  offset: Pagination offset (default 0)
  motion: Filter "detected" or "not_detected" (optional)
  hours:  Get data from last N hours (optional)

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

#### 4. Get Specific Record
```
GET /api/sensor-data/42

Response:
{
  "success": true,
  "data": {
    "id": 42,
    "motion_status": "detected",
    "temperature": 25.5,
    "latitude": 40.7128,
    "longitude": -74.0060,
    "timestamp": "2024-04-09T10:30:45.123456"
  }
}
```

#### 5. Get Statistics
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

#### 6. Delete Record
```
DELETE /api/sensor-data-delete/42

Response:
{
  "success": true,
  "message": "Record 42 deleted successfully"
}
```

---

## 💻 How to Send Data

### Method 1: Using Dashboard (Automatic)
```
1. Open index_simple.html
2. Click "Connect ESP32"
3. Select COM port
4. Motion is auto-detected and saved to MySQL
```

### Method 2: Using Test Script
```bash
python test_api.py
# Interactive menu with options to:
# - Add motion events
# - Simulate multiple events
# - View all data
# - Get statistics
```

### Method 3: Using Python Requests
```python
import requests

response = requests.post(
    'http://localhost:5000/api/sensor-data',
    json={
        'motion_status': 'detected',
        'temperature': 25.5,
        'latitude': 40.7128,
        'longitude': -74.0060
    }
)
print(response.json())
```

### Method 4: Using cURL (PowerShell)
```powershell
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

### Method 5: Using JavaScript (Fetch)
```javascript
fetch('http://localhost:5000/api/sensor-data', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        motion_status: 'detected',
        temperature: 25.5,
        latitude: 40.7128,
        longitude: -74.0060
    })
})
.then(r => r.json())
.then(data => console.log(data));
```

---

## 📊 Database Schema

### sensor_data Table
```sql
CREATE TABLE sensor_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    motion_status VARCHAR(50) NOT NULL,        -- "detected" or "not_detected"
    temperature FLOAT DEFAULT NULL,             -- Temperature in Celsius
    latitude DECIMAL(10, 6) DEFAULT NULL,       -- GPS latitude coordinate
    longitude DECIMAL(10, 6) DEFAULT NULL,      -- GPS longitude coordinate
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, -- Auto-set to current time
    
    INDEX idx_timestamp (timestamp),
    INDEX idx_motion_status (motion_status)
);
```

### Useful SQL Queries
```sql
-- Get all data
SELECT * FROM sensor_data ORDER BY timestamp DESC;

-- Count motion detections
SELECT COUNT(*) FROM sensor_data WHERE motion_status = 'detected';

-- Get data from last 24 hours
SELECT * FROM sensor_data 
WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
ORDER BY timestamp DESC;

-- Get average temperature
SELECT AVG(temperature) as avg_temp FROM sensor_data;

-- Get motion events by hour
SELECT 
    DATE_FORMAT(timestamp, '%Y-%m-%d %H:00:00') as hour,
    COUNT(*) as count
FROM sensor_data
WHERE motion_status = 'detected'
GROUP BY hour
ORDER BY hour DESC;

-- Get motion events with location
SELECT motion_status, latitude, longitude, timestamp
FROM sensor_data
WHERE latitude IS NOT NULL AND longitude IS NOT NULL
ORDER BY timestamp DESC LIMIT 100;
```

---

## 🔧 Configuration

### Flask API Settings (app_mysql.py)
```python
DB_CONFIG = {
    'host': 'localhost',        # MySQL host
    'user': 'root',             # MySQL username (XAMPP default)
    'password': '',             # MySQL password (empty in XAMPP)
    'database': 'esp32_project',# Database name
    'port': 3306                # MySQL port
}
```

### Dashboard Settings (index_simple.html)
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
// Change this if running Flask on different host/port
```

---

## ⚠️ Troubleshooting

### Problem: "MySQL API unavailable" in Dashboard

**Causes:**
- Flask server not running
- XAMPP MySQL not running
- Firewall blocking port 5000

**Solution:**
```bash
# 1. Check Flask is running
python app_mysql.py

# 2. Check XAMPP MySQL is running (should be GREEN)

# 3. Test API health
curl http://localhost:5000/api/health

# 4. Check firewall settings
# Windows Defender Firewall → Allow app through firewall → Add Python
```

### Problem: "Database connection failed"

**Causes:**
- MySQL not running
- Database doesn't exist
- Wrong credentials

**Solution:**
```bash
# 1. Start MySQL in XAMPP Control Panel

# 2. Verify database exists
# Open http://localhost/phpmyadmin
# Look for "esp32_project" in database list

# 3. Run database setup script again
# Copy contents of database_setup.sql into PhpMyAdmin SQL tab
```

### Problem: "Cannot connect to ESP32"

**Causes:**
- USB cable not connected
- Drivers not installed
- Port already in use

**Solution:**
```bash
# 1. Install CH340 drivers (Google: "CH340 driver windows")

# 2. Check Device Manager for COM ports
# Device Manager → Ports (COM & LPT) → Look for ESP32

# 3. Close other serial programs (Arduino IDE, etc.)

# 4. Try different USB port or cable

# 5. Test ESP32 in Arduino IDE Serial Monitor first
```

### Problem: Data not saving to database

**Causes:**
- API not running
- Invalid motion_status value
- Database tables not created

**Solution:**
```bash
# 1. Check Flask server output for error messages
python app_mysql.py

# 2. Test API manually
python test_api.py

# 3. Check database tables exist
# PhpMyAdmin → esp32_project → Should show sensor_data, motion_history, api_logs

# 4. Check browser console for JavaScript errors
# F12 → Console tab → Look for errors
```

### Problem: "python: command not found"

**Causes:**
- Python not installed
- Python not in PATH

**Solution:**
```bash
# 1. Check Python installation
python --version

# 2. If not found, install Python from python.org

# 3. During installation, check "Add Python to PATH"

# 4. Restart command prompt after installation
```

---

## 🎯 Next Steps

1. **Monitor Data**
   - View all data: `http://localhost:5000/api/sensor-data`
   - Get statistics: `http://localhost:5000/api/statistics`
   - Browse in PhpMyAdmin

2. **Create Reports**
   - Generate daily motion reports
   - Track temperature trends
   - Analyze location data

3. **Set Up Alerts**
   - Email notifications on motion
   - SMS alerts
   - Slack/Discord messages

4. **Scale Up**
   - Deploy to cloud (Azure, AWS, Google Cloud)
   - Use remote MySQL database
   - Add authentication
   - Enable HTTPS

5. **Data Export**
   - Export to CSV
   - Generate PDF reports
   - Integrate with analytics tools

---

## 📝 Important Files

| File | Purpose | Status |
|------|---------|--------|
| `index_simple.html` | Dashboard UI | ✅ UPDATED with API integration |
| `app_mysql.py` | Flask API | ✅ NEW - Use this! |
| `database_setup.sql` | Database creation | ✅ NEW |
| `requirements.txt` | Python dependencies | ✅ NEW |
| `test_api.py` | API testing tool | ✅ NEW |
| `MYSQL_SETUP_GUIDE.md` | Detailed instructions | ✅ NEW |
| `QUICK_START.md` | Quick reference | ✅ UPDATED |
| `api_server.py` | Old mock API | ⚠️ For reference only |

---

## 📞 Quick Reference

**Start Sequence:**
```bash
1. XAMPP Control Panel → Start MySQL
2. Open http://localhost/phpmyadmin (verify database)
3. Command Prompt: python app_mysql.py (keep open)
4. Browser: Open index_simple.html
5. Check Debug Output: Should say "✅ MySQL API connected"
```

**Test Sequence:**
```bash
1. In separate Command Prompt: python test_api.py
2. Select option 8 (Run Full Test Suite)
3. Check PhpMyAdmin for new records
```

**Files to Keep Open:**
```
1. XAMPP Control Panel (MySQL running)
2. Command Prompt with Flask (python app_mysql.py)
3. Browser with Dashboard (index_simple.html)
```

---

## 📚 Documentation Files

- **MYSQL_SETUP_GUIDE.md** - Step-by-step setup instructions
- **QUICK_START.md** - 5-minute quick start
- **IMPLEMENTATION_GUIDE.md** - This file (complete reference)
- **README.md** - Project overview
- **SETUP_GUIDE.md** - Original setup guide
- **PROJECT_SUMMARY.md** - Project details
- **PINOUT_REFERENCE.md** - Hardware pinout

---

## 🎉 You're Ready!

Your ESP32 Motion Detection Dashboard with MySQL integration is now complete!

**Next Action:**
1. Start XAMPP MySQL
2. Run `python app_mysql.py`
3. Open `index_simple.html`
4. Test with `python test_api.py`

For any issues, check the **MYSQL_SETUP_GUIDE.md** troubleshooting section.

---

**Last Updated:** April 9, 2024  
**Project:** ESP32 Motion Detection Dashboard with MySQL Integration  
**Status:** ✅ Complete and Ready to Use
