# ESP32 PIR Motion Sensor - Web Dashboard

A professional-grade IoT dashboard for real-time ESP32 motion detection with Web Serial API integration. No software installation needed - works directly in your browser!

![Status](https://img.shields.io/badge/Status-Production%20Ready-green)
[![Browser Support](https://img.shields.io/badge/Browser-Chrome%2FEdge-blue)](https://caniuse.com/web-serial)
[![Baud Rate](https://img.shields.io/badge/Baud%20Rate-115200-orange)](#)

---

## 🚀 Quick Start (5 Minutes)

### 1️⃣ Hardware Setup
```
PIR Sensor → ESP32 Dev Module
VCC        → 5V Power
GND        → Ground
OUT        → GPIO 5
USB        → Laptop
```

### 2️⃣ Upload Code
1. Open `ESP32_PIR_Sketch.ino` in Arduino IDE
2. **Tools** → Set Board to "ESP32 Dev Module"
3. **Tools** → Set Port to your COM port
4. **Tools** → Set Speed to "115200"
5. Click **Upload** ✓

### 3️⃣ Open Dashboard
1. Double-click `index.html` in Chrome/Edge
2. Click **📡 Connect ESP32**
3. Select your COM port from dropdown
4. Watch motion detection in real-time! 🟢

**That's it!** Motion updates appear instantly on your dashboard.

---

## 📁 Files Included

### Main Files
| File | Purpose |
|------|---------|
| `index.html` | **Advanced Dashboard** - Full features, charts, history, Python integration |
| `index_simple.html` | **Simple Dashboard** - Minimal, beginner-friendly, just shows motion status |
| `ESP32_PIR_Sketch.ino` | **ESP32 Code** - Arduino sketch for PIR sensor (GPIO 5) |

### Documentation
| File | Purpose |
|------|---------|
| `QUICK_START.md` | 🏃 Quick reference checklist |
| `SETUP_GUIDE.md` | 📖 Detailed setup & troubleshooting guide |
| `README.md` | 📚 This file - complete documentation |

---

## 🎯 Which Dashboard to Use?

### Use `index.html` if you want:
- ✅ Complete feature set
- ✅ Real-time charts & graphs
- ✅ Historical data analysis
- ✅ Python analysis integration
- ✅ Advanced statistics
- ✅ Professional UI

**Best for**: Learning, advanced projects, professional deployments

### Use `index_simple.html` if you want:
- ✅ Simple motion indicator
- ✅ No extra features
- ✅ Fast & lightweight
- ✅ Easy to understand code
- ✅ Good for beginners
- ✅ Works on slower computers

**Best for**: Quick testing, beginners, embedded displays

---

## 📊 Features

### Real-Time Monitoring
- 📡 **Web Serial API**: Direct browser ↔ ESP32 communication
- 🎯 **Motion Detection**: Shows 🟢 DETECTED or 🔴 NO MOTION
- 🔄 **Live Updates**: Data refreshes instantly
- 📉 **Historical Charts**: Track motion patterns

### Dashboard (index.html)
- ✅ Multi-card status display
- ✅ Real-time Chart.js graphs  
- ✅ Detection confidence % scores
- ✅ Temperature tracking
- ✅ Manual override controls
- ✅ Debug console
- ✅ Data summary table
- ✅ Python API integration

### Error Handling
- ✅ Browser support check
- ✅ Port not found handling
- ✅ No data timeout detection
- ✅ USB disconnection recovery
- ✅ Graceful error messages
- ✅ Null reference protection

---

## 💻 System Requirements

### Hardware
- **ESP32 Dev Module** (other ESP32 boards may work)
- **5V PIR Motion Sensor** (HC-SR501 or similar)
- **USB Cable** (quality USB-A to Micro-USB)
- **5V Power Supply** (USB port or external 2A+ supply)

### Software
- **Browser**: Chrome 89+, Edge 89+, or Opera 76+ ([check compatibility](https://caniuse.com/web-serial))
- **Arduino IDE**: Latest version with ESP32 board support
- **USB Driver**: CH340 (most ESP32 boards use this)

---

## 📥 Serial Data Format

Your ESP32 sends messages at **115200 baud**:

### Supported Formats

#### Simple Format (Recommended)
```
Motion Detected
No Person Detected
```

#### Alternative Formats
```
motion: ON
motion: OFF
motion = 1
motion = 0
```

The dashboard automatically recognizes all formats!

---

## 🔌 Arduino IDE Setup Guide

### 1. Install ESP32 Board Support
1. **Arduino IDE** → **Preferences**
2. Paste in "Additional Boards Manager URLs":
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
3. **Tools** → **Board Manager**
4. Search "ESP32" and click **Install**

### 2. Select Board
- **Tools** → **Board** → **ESP32 Dev Module**

### 3. Select Port
- **Tools** → **Port** → **COMx** (check Device Manager)

### 4. Set Speed
- **Tools** → **Upload Speed** → **115200**

### 5. Upload Code
- Open `ESP32_PIR_Sketch.ino`
- Click **Upload** button (→ icon)
- Wait for "Upload complete"

---

## 🛠️ Troubleshooting

### ❌ "Web Serial API not supported"
**Cause**: Browser doesn't support Web Serial  
**Solution**: Use Chrome, Edge, or Opera (v76+)

### ❌ No ESP32 in port dropdown
**Cause**: USB driver not installed or device not recognized  
**Solutions**:
1. Download [CH340 Driver](https://sparks.gogo.co.nz/ch340)
2. Restart Arduino IDE
3. Try different USB cable (quality matters!)
4. Try different USB port on computer

### ❌ Upload fails / "Device not found"
**Cause**: Wrong board/port selected  
**Solutions**:
1. Check **Tools** → **Board** = "ESP32 Dev Module"
2. Check **Tools** → **Port** = COMx (not grayed out)
3. Reset ESP32: Press the RESET button
4. Try different USB port

### ❌ No motion detection / Always shows NO MOTION
**Cause**: PIR not detecting motion  
**Solutions**:
1. **Wait 30-60 seconds**: PIR sensors need warmup time
2. **Check wiring**:
   - VCC (red wire) → 5V ✅
   - GND (black wire) → GND ✅
   - OUT (yellow wire) → GPIO 5 ✅
3. **Check Serial Monitor**:
   - **Tools** → **Serial Monitor**
   - Should see: "Motion Detected" when you move
   - If nothing: Check wiring, try resetting ESP32

### ❌ Random false motion detections
**Cause**: Electrical noise or sensor sensitivity  
**Solutions**:
1. Move sensor away from heat sources (vents, AC)
2. Increase `DEBOUNCE_TIME` in sketch (500ms → 1000ms)
3. Use stable power supply (quality USB cable)
4. Some PIR sensors have potentiometer dial - adjust sensitivity

### ❌ Dashboard won't connect
**Cause**: Browser or port issues  
**Solutions**:
1. Check USB is plugged into ESP32
2. Try hard refresh: **Ctrl+Shift+Delete** (Clear everything)
3. Restart browser
4. Check browser console: **F12** → **Console** tab for errors

---

## 🖥️ Running Without Arduino IDE

### Option 1: Python HTTP Server (Recommended)
```bash
# Navigate to project folder
cd "c:\Users\Lenovo\Documents\dbms webpage creation"

# Run Python
python -m http.server 8000

# Open browser to: http://localhost:8000
```

### Option 2: Node.js
```bash
npx serve .
# Opens at http://localhost:3000
```

### Option 3: VS Code Live Server Extension
1. Install "Live Server" extension
2. Right-click `index.html` → **Open with Live Server**

---

## 🎨 Customization

### Change Colors (index.html)
Find the `<style>` section and modify:
```css
/* Main gradient - lines 13-14 */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Motion detected color - search for "detected" class */
background: #d5f4e6;  /* Light green */
color: #27ae60;       /* Dark green */
```

### Change Title/Icons
Look for `<h1>` and emoji (🟢🔴📡 etc.) in the HTML

### Change Message Format
In `ESP32_PIR_Sketch.ino`:
```cpp
Serial.println("Motion Detected");      // Change this text
Serial.println("No Person Detected");   // Change this text
```

---

## 📖 Learning Resources

### For ESP32 Programming
- [Espressif ESP32 Docs](https://docs.espressif.com/)
- [Arduino ESP32 Guide](https://docs.espressif.com/projects/arduino-esp32/)

### For Web Serial API
- [MDN Web Serial Docs](https://developer.mozilla.org/en-US/docs/Web/API/Web_Serial_API)
- [W3C Web Serial Spec](https://wicg.github.io/serial/)

### For PIR Sensors
- [HC-SR501 Datasheet](https://www.mouser.com/datasheet/2/-/608526.pdf)
- [PIR Sensor Guide](https://www.teachwithict.com/microbit-pir)

---

## 🚀 Next Steps

### Basic Enhancements
- [ ] Add LED that turns on with motion
- [ ] Add buzzer alarm on detection
- [ ] Add button to ESP32 for manual test
- [ ] Add push notifications to phone

### Advanced Projects
- [ ] WiFi connection (send data to cloud)
- [ ] Store data in local CSV file
- [ ] Email alerts on motion detection
- [ ] Add 2nd PIR sensor for zone coverage
- [ ] Add temperature/humidity sensor
- [ ] Mobile app integration

---

## 📝 Debug Console Tips

Press **F12** in browser to see logs:

```
[PARSING] Motion = ON                  → Shows motion was parsed
[PERSON DETECTION] Motion Detected => ON  → Shows the result
[CONNECTION DEBUG]                      → Connection events
❌ ERROR: ...                           → Error messages
✅ Connected to ESP32                   → Success message
```

---

## 📞 Support

### Check These First:
1. **Read**: Appropriate guide based on issue
   - Quick problems: `QUICK_START.md`
   - Complex issues: `SETUP_GUIDE.md`

2. **Test**:
   - Open Serial Monitor to see raw ESP32 output
   - Check browser console (F12) for JavaScript errors

3. **Verify**:
   - Baud rate is 115200 ✅
   - Board is "ESP32 Dev Module" ✅
   - Port is selected ✅
   - USB cable works ✅

---

## 📄 License & Credits

- **Web Serial API**: W3C Standard (browser feature)
- **Chart.js**: MIT License
- **ESP32**: Espressif Systems
- **Dashboard**: Custom built for PIR motion detection

---

## 🎓 Ver sion History

- **v1.0.0** (April 2026):
  - ✅ Web Serial API integration
  - ✅ PIR sensor support (GPIO 5)
  - ✅ Real-time motion detection
  - ✅ Simple & advanced UI options
  - ✅ Comprehensive documentation

---

**Last Updated**: April 2026  
**Status**: Production Ready ✅  
**Tested On**: Chrome 125+, Edge 125+  
**ESP32 Firmware**: Arduino IDE with ESP32 v2.0.x+


3. **Start Python analysis** (optional but recommended):
   ```bash
   pip install pyserial pandas scikit-learn matplotlib seaborn numpy flask
   python human_analysis.py --port COM3 --baud 115200
   ```

## Usage

### Basic Operation
1. Click "📡 Connect ESP32" and select your COM port
2. ESP32 data will automatically populate all cards
3. View real-time charts and analysis metrics
4. Use manual controls for testing

### Advanced Analysis
When Python analysis is running:
- **Detection Confidence**: ML-based confidence scoring
- **Statistical Metrics**: Motion rates, temperature trends
- **Anomaly Detection**: Automatic outlier identification
- **REST API**: Access data at `http://localhost:5000/api/*`

## API Endpoints (Python Analysis)

- `GET /api/analysis` - Current analysis results
- `GET /api/data?limit=100` - Recent sensor data
- `GET /api/stats` - Statistical metrics

## Troubleshooting

### Common Issues
1. **"Web Serial API not supported"**
   - Use Chrome or Edge browser
   - Serve over HTTPS or localhost

2. **Serial connection fails**
   - Check COM port number
   - Ensure ESP32 is sending data at 115200 baud
   - Close other serial monitor applications

3. **Python analysis not working**
   - Install dependencies: `pip install pyserial pandas scikit-learn matplotlib seaborn numpy flask`
   - Check if port 5000 is available

4. **Charts not updating**
   - Ensure Chart.js is loaded
   - Check browser console for errors

## ESP32 Example Code

```cpp
// Basic ESP32 code for sensor data transmission
#include <HardwareSerial.h>

void setup() {
  Serial.begin(115200);
  // Initialize your sensors here
}

void loop() {
  // Read sensors
  bool motion = digitalRead(MOTION_PIN);
  float temperature = readTemperature();
  bool heatDetected = temperature > 30.0; // Your threshold

  // Send data
  Serial.print("Motion:");
  Serial.print(motion ? "ON" : "OFF");
  Serial.print(", Heat:");
  Serial.print(heatDetected ? "DETECTED" : "NOT_DETECTED");
  Serial.print(", Temp:");
  Serial.println(temperature);

  delay(1000);
}
```

## Architecture

```
ESP32 Sensors → Serial → Web Serial API → Dashboard
                                      ↓
                            Python Analysis Server
                                      ↓
                            Advanced ML Analysis
```

## Contributing

Feel free to enhance the system with:
- Additional sensor types
- More sophisticated ML models
- Data export functionality
- Custom analysis algorithms

## License

This project is open-source. Use and modify as needed for your applications.