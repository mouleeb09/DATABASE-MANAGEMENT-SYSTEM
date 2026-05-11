# Dashboard Integration Guide - Flask API

## ✅ Changes Made to Your Dashboard

Your `index_simple.html` dashboard has been updated to integrate with the Flask API server. Here's what was changed:

### 🔧 Key Updates:

1. **API Endpoint Configuration**
   - Updated from: `http://localhost:5000/api` 
   - To: `http://127.0.0.1:5000`
   - Endpoints: `/save_data`, `/health`, `/get_data`

2. **Sensor Data Format**
   - Now sends the correct JSON format:
   ```json
   {
     "motion_status": "MOTION DETECTED",
     "radar_status": "RADAR ACTIVE",
     "temperature": "32.5",
     "person_detected": "YES"
   }
   ```

3. **Automatic Data Sending**
   - When motion is detected: Sends motion data to Flask API
   - When no motion: Sends no motion data to Flask API
   - Temperature is extracted from ESP32 serial data
   - Proper error handling for failed saves

4. **Console Logging**
   - Detailed logs for debugging:
     ```
     ✅ [API] Flask server connected successfully!
     📤 [API] Sending data to /save_data: {...}
     ✅ [API] Data saved successfully!
        Record ID: 1
        Timestamp: ...
     ```

5. **Error Handling**
   - Shows clear error messages if:
     - Flask server is not running
     - MySQL is not connected
     - Database operations fail

## 🚀 How to Use

### Step 1: Ensure Flask Server is Running

```bash
cd "c:\Users\Lenovo\Documents\dbms webpage creation"
python api_server.py
```

Expected output:
```
🚀 ESP32 Motion Detection Dashboard API Server
==================================================
📊 Database: human_detection (MySQL via XAMPP)
📋 Table: detection
🌐 Server: http://127.0.0.1:5000

Press Ctrl+C to stop the server
```

### Step 2: Open Your Dashboard

Open `index_simple.html` in a web browser:
- File path: `c:\Users\Lenovo\Documents\dbms webpage creation\index_simple.html`
- Or: Drag and drop the file into your browser

### Step 3: Check Console Logs

1. Open browser DevTools: **F12**
2. Go to **Console** tab
3. You should see:
   ```
   ============================================================
   🚀 ESP32 Advanced Motion Detection Dashboard
   ============================================================
   📍 API Endpoint: http://127.0.0.1:5000/save_data
   🔍 Health Check: http://127.0.0.1:5000/health
   📊 Get Data: http://127.0.0.1:5000/get_data
   ============================================================
   
   [API] Testing Flask server connection...
   ✅ [API] Flask server connected successfully!
   🗄️ [API] Database status: connected
   ```

### Step 4: Test with Manual Data

Use the test panel to send data:
- Open: `test_api_dashboard.html`
- Click preset buttons or enter custom values
- Click "Send Data"
- Check browser console for success messages

## 📊 What Happens When Motion is Detected

1. **ESP32 Sends**: "motion detected" (or similar)
2. **Dashboard Receives**: Message via Web Serial API
3. **Dashboard Sends to Flask API**:
   ```json
   {
     "motion_status": "MOTION DETECTED",
     "radar_status": "RADAR ACTIVE",
     "temperature": 32.5,
     "person_detected": "YES"
   }
   ```
4. **Flask Saves to MySQL**: Record inserted into `detection` table
5. **Dashboard Shows**: Success message in console and debug panel
6. **Database Contains**: All sensor data with timestamp

## 🧪 Test Scenarios

### Test 1: Manual API Test
```
File: test_api_dashboard.html
Steps:
1. Open the file in browser
2. Click "Test API Connection"
3. Should see "✅ API Connection Successful"
4. Click preset "Motion Detected"
5. Click "Send Data"
6. Check database
```

### Test 2: Dashboard with Simulated Data
```
File: index_simple.html
Steps:
1. Open in browser
2. Press F12 to open console
3. Connect to ESP32 (if available)
4. When motion detected, check:
   - Console shows "✅ [API] Data saved successfully!"
   - Debug panel shows "💾 Data saved to database"
5. Check database for new records
```

### Test 3: Get Data from Database
```
Browser Console:
- Go to index_simple.html
- Open DevTools (F12)
- Paste this in console:

fetch('http://127.0.0.1:5000/get_data?limit=5')
  .then(r => r.json())
  .then(d => console.log(d))
```

## 🔍 Debugging

### Issue: "API not connected" message

**Solutions:**
1. Check if Flask server is running:
   ```bash
   # In terminal, check for:
   # * Running on http://127.0.0.1:5000
   ```

2. Check if XAMPP MySQL is running:
   - Start XAMPP Control Panel
   - Ensure MySQL shows "Running"

3. Check if database exists:
   - Open phpMyAdmin
   - Look for `human_detection` database

### Issue: "Failed to save data"

**Check:**
1. Database and table exist
2. Column names match exactly (case-sensitive)
3. MySQL credentials in `api_server.py` are correct:
   ```python
   'user': 'root',          # Default XAMPP user
   'password': '',          # Default XAMPP password
   ```

### Issue: CORS errors

**If you see CORS error in console:**
- Flask-CORS is already enabled
- Make sure Flask server is running
- Try different browser if problem persists

### Issue: Can't see console logs

**To enable console logging:**
1. Right-click dashboard page
2. Select "Inspect" or press F12
3. Go to "Console" tab
4. Refresh the page
5. Look for log messages

## 📈 Verify Data in Database

### Using phpMyAdmin:
1. Open XAMPP Control Panel
2. Click "Admin" next to MySQL
3. Left sidebar: Click `human_detection`
4. Click `detection` table
5. Should see inserted records with:
   - id, motion_status, radar_status, temperature, person_detected, detection_time

### Using Python:
```python
import pymysql
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='human_detection'
)
cursor = conn.cursor()
cursor.execute("SELECT * FROM detection ORDER BY detection_time DESC LIMIT 5")
records = cursor.fetchall()
for record in records:
    print(record)
```

## 📝 Expected Console Output

When motion is detected and saved successfully:

```
[PARSE] "motion detected"
✅ Motion Detected
[API] Sending data to /save_data: {
  motion_status: 'MOTION DETECTED',
  radar_status: 'RADAR ACTIVE',
  temperature: 32.5,
  person_detected: 'YES'
}
✅ [API] Data saved successfully!
   Record ID: 42
   Timestamp: 2024-05-07T15:30:45.123Z
💾 ✅ Data saved to database (Record ID: 42)
```

## 🎯 Temperature Handling

The dashboard now extracts temperature from ESP32 messages:

**ESP32 Should Send:**
- "temp:32.5" or
- "temperature:32.5" or
- "temp: 32.5"

**Dashboard Will:**
1. Parse the temperature value
2. Update `currentTemperature` variable
3. Send temperature with next motion detection

## 🔐 Security Notes

- This setup is for local development only
- Use proper authentication for production
- Don't expose Flask server to public internet without HTTPS
- Use environment variables for sensitive data

## 📞 Quick Reference

| Component | URL/Path | Status |
|-----------|----------|--------|
| Flask API | http://127.0.0.1:5000 | ✅ Running |
| Dashboard | index_simple.html | ✅ Updated |
| Test Panel | test_api_dashboard.html | ✅ Created |
| Database | human_detection | ✅ Configured |
| MySQL | XAMPP localhost | ✅ Required |

## 🎓 Example ESP32 Code

Send data from ESP32 to trigger dashboard saving:

```cpp
// Motion Detected
Serial.println("motion detected");
Serial.println("temp:32.5");

// No Motion
Serial.println("no motion");
Serial.println("temp:31.2");
```

---

**Dashboard is now ready to receive and save sensor data! 🚀**