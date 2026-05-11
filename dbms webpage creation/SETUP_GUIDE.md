# ESP32 PIR Motion Sensor - Web Dashboard Guide

## ✅ Quick Start

### 1. Hardware Setup
```
PIR Sensor → ESP32 Dev Module
VCC → 5V
GND → GND  
OUT → GPIO 5
```

### 2. Upload ESP32 Code
1. Open Arduino IDE
2. Go to **Sketch** → **Include Library** → **Manage Libraries**
3. Search for "ESP32" and install "ESP32 by Espressif Systems"
4. Set Board: **Tools** → **Board** → **ESP32 Dev Module**
5. Set Port: **Tools** → **Port** → COMx (COM3, COM4, etc.)
6. Set Baud: **Tools** → **Upload Speed** → **115200**
7. Copy code from `ESP32_PIR_Sketch.ino` to IDE
8. Click **Upload** (arrow icon)

### 3. Open Web Dashboard
1. Open `index.html` in Chrome/Edge browser
   - Option A: Right-click → Open with → Chrome
   - Option B: Use Live Server extension (recommended)
2. Click **📡 Connect ESP32** button
3. Select your ESP32 COM port from dropdown
4. Watch for motion detection updates!

---

## 🔌 Serial Output Format

Your ESP32 sends these messages at **115200 baud**:

```
Motion Detected       → Shows "🟢 PERSON DETECTED" (motion + heat)
No Person Detected    → Shows "🔴 NO PERSON DETECTED"
```

The dashboard automatically:
- ✅ Reads messages in real-time
- ✅ Parses motion status
- ✅ Updates UI dynamically
- ✅ Logs debug info
- ✅ Stores history in charts

---

## 🛠️ Troubleshooting

### ❌ No connection to ESP32

**Problem**: "Port not found" error

**Solutions**:
1. **Check USB cable**: Try a different quality USB cable
2. **Install drivers**: 
   - Most ESP32 boards use CH340 USB chip
   - Download: https://sparks.gogo.co.nz/ch340
3. **Check port**:
   - Windows: Device Manager → Ports (COM & LPT)
   - Should see "COM3" or similar
4. **Reset ESP32**: Press RESET button on board

### ❌ No motion detection

**Problem**: Dashboard shows "NO PERSON DETECTED" always

**Solutions**:
1. **Wait for warmup**: PIR sensors need 30-60 seconds after power-on
2. **Check wiring**: 
   - VCC (red) → 5V ✅
   - GND (black) → GND ✅
   - OUT (yellow) → GPIO 5 ✅
3. **Test with Serial Monitor**:
   - Open Arduino IDE
   - Tools → Serial Monitor
   - Should see "Motion Detected" when motion occurs
4. **Check sensor range**: PIR detects ~5-7 meters away
5. **Adjust sensitivity**: Some PIR sensors have a potentiometer dial

### ❌ Browser shows "Web Serial API not supported"

**Problem**: Dashboard can't find Web Serial API

**Solutions**:
1. **Use Chrome/Edge**: Only Chromium-based browsers support Web Serial
   - NOT supported: Firefox, Safari
2. **Check HTTPS/localhost**: 
   - Local HTML files work directly
   - Hosted files need HTTPS
3. **Update browser**: Update to latest version

### ❌ Permission denied error

**Problem**: "Permission denied" when clicking Connect

**Solutions**:
1. Try a different USB port
2. Run browser as Administrator (Windows)
3. Restart browser
4. Check if another program is using the serial port

### ❌ Random false motion detections

**Problem**: Motion detected when no movement

**Solutions**:
1. Increase `DEBOUNCE_TIME` in sketch (default 500ms → try 1000ms)
2. Move PIR sensor away from:
   - Heat vents/radiators
   - Direct sunlight
   - AC units
3. Use good quality power supply (5V stable)

---

## 📊 Dashboard Features

### Connection Section
- **📡 Connect ESP32**: Opens port selection dialog
- **❌ Disconnect**: Closes connection safely
- **Status Badge**: Shows connection state (green = connected)

### Status Cards
- **🚀 Motion Status**: Real-time motion (ON/OFF)
- **👤 Living Person Detection**: Main status indicator
- **📈 Real-time Charts**: Historical sensor data
- **🧠 Analysis Section**: Detection confidence, rates, etc.
- **📊 Data Summary**: Table of all sensor values
- **📊 Debug Output**: Console logs for troubleshooting

### Manual Controls
- **🟢 Mark Detected**: Manually override to "Person Detected"
- **🔴 Mark Not Detected**: Manually override to "No Person Detected"
- **🔄 Auto Mode**: Return to automatic detection
- **🔍 Trigger Detection**: Send command to ESP32

---

## 🔍 Debug Console

The bottom panel shows real-time debug logs:

```
✅ Connected to ESP32              → Connection established
❌ Serial error: ...               → Connection failed
[HH:MM:SS] 📥 "Motion Detected"   → Data received
[HH:MM:SS] 📍 Motion = ON          → Parsed as motion ON
```

**Console Logs** (F12 → Console tab):
- `[PARSING] Motion = ON`
- `[PERSON DETECTION] ... => ON`
- `[CONNECTION DEBUG]`

---

## 📝 Serial Message Examples

### Simple format (recommended for PIR):
```
Motion Detected
No Person Detected
```

### Alternative format (also supported):
```
motion: ON
motion: OFF
motion = 1
motion = 0
```

The dashboard accepts multiple formats - pick one for your ESP32!

---

## ⚡ Power Requirements

- **ESP32**: 5V USB or 3.3V regulated
- **PIR Sensor**: 5V supply (or 3.3V with current limit)
- **Total Current**: ~200mA idle, same during motion
- **Power Supply**: Use quality USB cable/port

---

## 🎯 Production Tips

1. **Stability**:
   - Use 5V power supply rated for 2A+
   - Keep USB cable short/shielded
   - Mount PIR sensor stable (avoid vibrations)

2. **Accuracy**:
   - Position PIR to face detection area
   - Avoid pointing at walls/ceilings
   - Mount at 1-2m height for best coverage

3. **Maintenance**:
   - Avoid dust/dirt on PIR lens
   - Keep away from temperature extremes
   - Check USB connection periodically

---

## 📚 Resources

- **ESP32 Board Docs**: https://docs.espressif.com/projects/esp-idf/
- **Arduino IDE Setup**: https://docs.espressif.com/projects/arduino-esp32/
- **Web Serial API**: https://wicg.github.io/serial/
- **PIR Sensor Guide**: Check your specific sensor's datasheet

---

## 🎓 Learning More

### Understanding the Code

**ESP32 Sketch** (`ESP32_PIR_Sketch.ino`):
- Reads PIR pin every 100ms
- Applies debouncing to avoid noise
- Sends status every 1 second
- Uses Serial at 115200 baud

**Dashboard** (`index.html`):
- Web Serial API reads data
- Regex parses motion messages  
- Updates UI in real-time
- Charts store history

### Customization Ideas

1. **Add LED feedback**: Light up when motion detected
2. **Add buzzer**: Beep on motion detection
3. **Add LCD display**: Show status on display
4. **Add WiFi**: Send data to cloud database
5. **Add email alerts**: Email when motion detected

---

## ✉️ Support Debugging

If something doesn't work:

1. **Check browser console** (F12):
   ```
   [PARSING] Motion = ON
   [PERSON DETECTION] Motion Detected => ON
   ```

2. **Check Arduino Serial Monitor**:
   - Tools → Serial Monitor
   - Set baud to 115200
   - Should see: "Motion Detected" or "No Person Detected"

3. **Test ESP32 connection**:
   - Upload simple LED blink
   - Verify USB works

4. **Test PIR sensor**:
   - Check multimeter leads on PIR output
   - Should read ~5V when motion, ~0V when empty

---

**Created**: April 2026  
**ESP32 Board**: Dev Module  
**PIR Sensor**: Generic 5V  
**Baud Rate**: 115200  
**Web Serial**: Chrome/Edge required
