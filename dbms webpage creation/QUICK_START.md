# ESP32 Motion Detection Dashboard - Quick Start with MySQL

## ⚡ 5-Minute Quick Start

### 1. Start XAMPP MySQL
- Open XAMPP Control Panel
- Click "Start" button next to MySQL
- Wait for it to turn GREEN

### 2. Create Database
- Open: http://localhost/phpmyadmin
- Click "Databases" tab
- Create database named "esp32_project"
- Go to "SQL" tab and paste contents from database_setup.sql
- Click "Go"

### 3. Install Python Dependencies
```bash
cd "c:\Users\Lenovo\Documents\dbms webpage creation"
pip install -r requirements.txt
```

### 4. Start Flask API Server
```bash
python app_mysql.py
```
Keep this terminal open! You'll see:
```
✅ Database connection successful!
Server running at http://localhost:5000
```

### 5. Open Dashboard
- Open: file:///c:/Users/Lenovo/Documents/dbms%20webpage%20creation/index_simple.html
- You should see "✅ MySQL API connected" in the debug output

### 6. Test Motion Detection
- Click "Connect ESP32" button (or simulate with serial data)
- When motion detected, data automatically saves to MySQL
- Check http://localhost:5000/api/sensor-data to verify

---

## 📊 Test API Manually

### Get All Data
```
http://localhost:5000/api/sensor-data
```

### Get Statistics
```
http://localhost:5000/api/statistics
```

### Add Test Data (PowerShell)
```powershell
$body = @{motion_status="detected"; temperature=25.5; latitude=40.7128; longitude=-74.0060} | ConvertTo-Json
Invoke-WebRequest -Uri "http://localhost:5000/api/sensor-data" -Method POST -Headers @{"Content-Type"="application/json"} -Body $body
```

### Check API Health
```
http://localhost:5000/api/health
```

---

## 🔍 Verify Data in Database

- Open: http://localhost/phpmyadmin
- Click esp32_project → sensor_data
- You should see motion detection records
- Each record has: id, motion_status, temperature, latitude, longitude, timestamp

---

## ⚠️ If Something Doesn't Work

**"MySQL API unavailable"**
- Check Flask server is running (python app_mysql.py)
- Check XAMPP MySQL is running (should be GREEN)
- Try: http://localhost:5000/api/health in browser

**"Database connection failed"**
- Check esp32_project database exists in PhpMyAdmin
- Check XAMPP MySQL is running
- Check tables are created (sensor_data, motion_history, api_logs)

**"Cannot connect to ESP32"**
- This is optional - dashboard works without it
- Try Arduino IDE first to verify ESP32
- Install CH340 drivers if needed

---

## 📁 New Project Files

- `index_simple.html` - Dashboard with MySQL integration (UPDATED)
- `app_mysql.py` - Flask API server (NEW)
- `database_setup.sql` - Database creation script (NEW)
- `requirements.txt` - Python dependencies (NEW)
- `MYSQL_SETUP_GUIDE.md` - Detailed setup guide (NEW)

---

## 🚀 What Happens When Motion is Detected?

```
1. Dashboard detects motion (ESP32 serial or simulation)
2. JavaScript calls: sendSensorDataToAPI('detected', lat, lon)
3. Fetch POST request to: http://localhost:5000/api/sensor-data
4. Flask API validates and inserts into MySQL
5. Record saved with timestamp
6. Response with ID confirms save
7. Dashboard displays success/fail in debug output
```

---

Ready? Start with: `python app_mysql.py`

---

## ❌ Common Issues

| Problem | Solution |
|---------|----------|
| No port in dropdown | Install CH340 drivers, reconnect USB |
| API not supported | Use Chrome/Edge (not Firefox/Safari) |
| No motion detection | Wait 60s for warmup, check wiring |
| Random detections | Increase debounce time in code |
| Serial won't upload | Check board=ESP32, port=COMx |

---

## 🎯 Features

✅ Real-time motion detection  
✅ Web Serial API (no software needed)  
✅ Beautiful responsive UI  
✅ Debug console  
✅ Auto-detection parsing  
✅ History charts  
✅ Manual override  

---

## 💡 Next Steps

- **Customize**: Edit colors/text in `index.html`
- **Extend**: Add buzzer, LED, WiFi to sketch
- **Test**: Try the "Mark Detected" button
- **Deploy**: Copy to any server (needs HTTPS)

---

**Need Help?** See `SETUP_GUIDE.md` for full troubleshooting
