# ESP32 + PIR Sensor Pinout Reference

## 🔌 Hardware Connection Diagram

```
┌─────────────────────────────────────────────────────────┐
│                   LAPTOP (USB PORT)                     │
└────────────────────────┬────────────────────────────────┘
                         │ USB Cable
                    ┌────▼─────┐
                    │           │
                ┌───┤  ESP32    ├───┐
                │   │  Dev Mod. │   │
                │   └───────────┘   │
                │                   │
          ┌─────┴───────────────────┴──────┐
          │                                │
          │  ┌──────────┐   ┌──────────┐   │
          │  │  5V      │   │   GND    │   │  Pins
          │  │  GPIO 5  │   │   GPIO X │   │  Labels
          └──┼──────────┼───┼──────────┼───┘
             │          │   │          │
        ┌────▼──┐  ┌────▼───▼──────┐
        │  5V   │  │   PIR Sensor  │
        │  GND  │  │   (HC-SR501) │
        │  GPIO5│  │               │
        └───┬───┘  └───────┬───────┘
            │              │
            │    ┌─────────┐
            │    │  OUT    │
            │    │ (yellow)│
            │    └────┬────┘
            │         │
    ┌───────┴─────────┴──────┐
    │   PIR Connections:     │
    │   • VCC → 5V (red)     │
    │   • GND → GND (black)  │
    │   • OUT → GPIO 5 (pin) │
    └────────────────────────┘
```

## 📍 Pin Mapping Table

| PIR Pin | Color  | ESP32 Pin | Description |
|---------|--------|-----------|------------|
| VCC     | Red    | 5V        | Power supply |
| GND     | Black  | GND       | Ground |
| OUT     | Yellow | GPIO 5    | Signal output (motion detection) |

## 🖥️ ESP32 Dev Module Pinout

```
┌─────────────────────────────────┐
│  ESP32 DEV MODULE (TOP VIEW)    │
│                                 │
│  USB ▣▣▣▣▣                     │
│  PORT                           │
│                                 │
│  GND  3V3  D35  D34  D33 D32   │ ← Left side
│         D25  D26  D27  D14 D12  │
│   5V  D23  D22  D21  D19 D18  │
│  GND   D5  D17  D16  D4   D0  │
│   EN  D35  D34  D33 D32  TX  │
│      RX   PD  PC  PA  GND  GND│
│                                 │
│  ◆ = GPIO 5 PIN                │
│                                 │
│  GND = Ground (multiple)        │
│  5V  = Power (multiple)         │
│  3V3 = 3.3V Power              │
│                                 │
└─────────────────────────────────┘
```

## 🔋 Wiring Checklist

```
✅ PIR VCC (red)    → ESP32 5V pin
✅ PIR GND (black)  → ESP32 GND pin
✅ PIR OUT (yellow) → ESP32 GPIO 5 pin
✅ USB Cable → Laptop USB port
✅ All connections secure (no loose wires)
✅ No solder bridges or bad connections
```

## ⚡ Power Supply Requirements

| Component | Voltage | Current | Notes |
|-----------|---------|---------|-------|
| ESP32 | 5V USB or 3.3V | 200mA idle | Powers from USB |
| PIR Sensor | 5V | 65mA | Needs good 5V supply |
| Total | 5V | ~250-300mA | Use USB 2A+ port |

**⚠️ Important**: Use a **quality USB cable** and a **5V/2A+ power source**. Cheap USB cables cause connection issues!

## 🔍 Pin Function Reference

### GPIO 5 (Used by PIR)
- **Input/Output**: INPUT (reads from PIR)
- **Voltage**: 3.3V logic (ESP32 can handle 5V input)
- **Protection**: Internal pull-up available
- **Debouncing**: Done in software

### GND Pins (Ground)
- Multiple ground pins available (use any)
- Must connect PIR GND to ESP32 GND
- Common ground reference for entire circuit

### 5V Pin (Power)
- Directly from USB
- Can supply up to 500mA
- Powers both ESP32 and PIR sensor

## 🛠️ Troubleshooting Pin Issues

### No motion detected?
- [ ] Check wire from PIR OUT → GPIO 5 is solid
- [ ] Try a different GPIO (change code):
  - GPIO 4, 12, 13, 14, 15, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33
- [ ] Use multimeter to test PIR output voltage

### Intermittent detection?
- [ ] Check for loose wires
- [ ] Add small capacitor (0.1µF) between PIR OUT and GND
- [ ] Improve USB power supply

### USB Port Not Found?
- [ ] Try different USB port on computer
- [ ] Try different USB cable
- [ ] Restart Arduino IDE
- [ ] Restart computer

## 🔌 Alternative GPIO Pins

If GPIO 5 doesn't work, try these alternatives:

**Safe GPIOs**: 4, 12, 13, 14, 15, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33

To use different GPIO:
1. Edit `ESP32_PIR_Sketch.ino`
2. Change: `#define PIR_PIN 5` → `#define PIR_PIN 4` (etc.)
3. Save and Upload

**Avoid these**: 0, 1, 2, 3, 5 (UART), 6-11 (Flash), 34-37 (Input-only)

## 📐 PCB Layout Reference

```
Breadboard Connection Example:

ESP32 POWER RAIL:
5V  ────────────────── (red wire) ──→ PIR VCC
GND ────────────────── (black wire) → PIR GND

ESP32 GPIO RAIL:
GPIO 5 ─ (yellow wire) → PIR OUT

Legend:
─ = Breadboard row/column
→ = Wire direction
```

## 🧪 Testing Connections

### Using Multimeter

1. **Power On**: 
   - Put meter on DC Voltage
   - Measure 5V: Should read 4.8-5.2V
   - Measure GND: Should read 0V

2. **Motion Detection**:
   - Set meter to DC Voltage
   - Connect to GPIO 5 and GND
   - No motion: ~0V
   - Motion: ~3.3V (or 5V from PIR)

3. **PIR Output**:
   - Measure directly on PIR OUT pin
   - No motion: ~0V
   - Motion: ~5V

## 🚨 Safety Notes

⚠️ **DO NOT**:
- Connect PIR VCC to 3.3V (PIR needs 5V)
- Connect PIR to wrong GPIO (software can still read, code needs update)
- Use wet/damaged USB cables
- Leave exposed solder connections
- Power multiple devices from single USB

✅ **DO**:
- Use quality USB cables (shielded preferred)
- Securely connect all wires (no loose connections)
- Test connections with multimeter
- Use 5V power supply rated for 2A+
- Keep wires away from moving parts

## 📱 Serial Communication

**Baud Rate**: 115200  
**Data Bits**: 8  
**Stop Bits**: 1  
**Parity**: None  
**Flow Control**: None  

This is set in:
- **Arduino Code**: `Serial.begin(115200);`
- **Dashboard**: `baudRate: 115200`
- **Arduino IDE Tools**: "Upload Speed" → 115200

---

## 🎓 Quick Reference Card (Print This!)

```
╔═══════════════════════════════════════╗
║  ESP32 PIR SENSOR CONNECTION GUIDE   ║
╠═══════════════════════════════════════╣
║                                       ║
║  PIR VCC   (red)   →  ESP32 5V       ║
║  PIR GND   (black) →  ESP32 GND      ║
║  PIR OUT   (yel)   →  ESP32 GPIO 5   ║
║                                       ║
║  Baud Rate: 115200                   ║
║  USB Cable: Quality USB-A to Micro-B ║
║                                       ║
║  Upload Board: ESP32 Dev Module      ║
║  Select Port: COMx (your port)       ║
║                                       ║
║  Open: index.html in Chrome/Edge     ║
║  Click: Connect ESP32 button         ║
║                                       ║
╚═══════════════════════════════════════╝
```

---

**Last Updated**: April 2026  
**Tested**: ESP32 Dev Module + HC-SR501 PIR  
**Status**: ✅ Verified Working
