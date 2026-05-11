/*
 * ESP32 PIR Motion Sensor - Web Serial Compatible Sketch
 * 
 * Hardware Setup:
 * - PIR Sensor VCC → ESP32 5V
 * - PIR Sensor GND → ESP32 GND
 * - PIR Sensor OUT → ESP32 GPIO 5
 * - USB → Laptop (115200 baud)
 * 
 * Board: ESP32 Dev Module
 * Baud Rate: 115200
 * 
 * Output Examples:
 * - "Motion Detected"
 * - "No Person Detected"
 */

#define PIR_PIN 5           // GPIO 5 for PIR sensor
#define BAUD_RATE 115200    // Serial baud rate
#define FLAME_SENSOR_ANALOG_PIN 34  // GPIO 34 for IR Flame Sensor Analog Output (adjust if different)
#define DEBOUNCE_TIME 500   // Debounce time in ms
#define READ_INTERVAL 1000  // Send status every second

// State tracking
bool lastMotionState = false;
bool currentMotionState = false;
unsigned long lastStateChangeTime = 0;
unsigned long lastReadTime = 0;

void setup() {
  // Initialize Serial for Web Serial API
  Serial.begin(BAUD_RATE);
  
  // Configure GPIO
  pinMode(PIR_PIN, INPUT);
  
  // Wait for serial connection (optional - for debugging)
  delay(1000);
  
  Serial.println("=== ESP32 PIR Motion Sensor Started ===");
  Serial.println("Baud: 115200");
  Serial.println("GPIO 5: PIR Sensor");
  Serial.println("GPIO " + String(FLAME_SENSOR_ANALOG_PIN) + ": IR Flame Sensor (Analog)");
  Serial.println("Waiting for motion...");
  Serial.println("");
  
  lastMotionState = digitalRead(PIR_PIN);
  lastReadTime = millis();
}

void loop() {
  // Read PIR sensor (HIGH = motion detected, LOW = no motion)
  currentMotionState = digitalRead(PIR_PIN);
  unsigned long currentTime = millis();
  
  // Check for state change with debouncing
  if (currentMotionState != lastMotionState) {
    // Debounce: wait to confirm the state change
    delay(DEBOUNCE_TIME);
    
    // Re-read to confirm
    if (digitalRead(PIR_PIN) == currentMotionState) {
      lastMotionState = currentMotionState;
      lastStateChangeTime = currentTime;
      
      // Send state change immediately
      if (currentMotionState) {
        Serial.println("Motion Detected");
        Serial.flush();
      } else {
        Serial.println("No Person Detected");
        Serial.flush();
      }
    }
  }
  
  // Also send periodic status updates (every 1 second)
  if (currentTime - lastReadTime >= READ_INTERVAL) {
    lastReadTime = currentTime;
    
    // Send current state
    if (currentMotionState) {
      Serial.println("Motion Detected");
    } else {
      Serial.println("No Person Detected");
    }
    Serial.flush();
  }
  
  // Small delay to prevent overwhelming the serial buffer
  delay(100);
}

// Function to read IR flame sensor and approximate temperature
float readFlameSensorTemperature() {
  int analogValue = analogRead(FLAME_SENSOR_ANALOG_PIN);

  // --- IMPORTANT: CALIBRATION REQUIRED ---
  // These values are highly approximate and need to be calibrated
  // based on your specific sensor, environment, and desired 'temperature' range.
  // The flame sensor primarily detects IR presence, not precise temperature.
  // 
  // Example linear mapping:
  //  - Assume analogRead returns 0-4095 (for ESP32 default 12-bit ADC)
  //  - Map a range of analog values to a conceptual temperature range.
  //    Adjust these 'min' and 'max' values after testing your sensor.

  float minAnalog = 500;   // Analog value when 'cold' or no flame (adjust this)
  float maxAnalog = 3000;  // Analog value when 'hot' or near flame (adjust this)
  float minTemp = 20.0;    // Corresponding approximate minimum temperature
  float maxTemp = 80.0;    // Corresponding approximate maximum temperature

  // Constrain the analog value within the defined range
  analogValue = constrain(analogValue, minAnalog, maxAnalog);

  // Map the analog value linearly to the temperature range
  float temperature = map(analogValue, minAnalog, maxAnalog, minTemp, maxTemp);

  return temperature;
}

/*
 * TROUBLESHOOTING GUIDE:
 * 
 * 1. No output in Serial Monitor:
 *    - Check USB connection
 *    - Verify baud rate is 115200
 *    - Check if ESP32 board is selected in Arduino IDE
 *    - Try a different USB cable
 * 
 * 2. PIR not detecting motion:
 *    - Check GPIO 5 connection
 *    - Verify VCC (5V) and GND are connected
 *    - PIR sensors need 30-60 seconds warmup time - wait before testing
 *    - Check if motion is within PIR detection range (typically 5-7 meters)
 *    - Adjust PIR sensor's potentiometer (sensitivity dial) if available
 * 
 * 3. Random detections / false positives:
 *    - Increase DEBOUNCE_TIME to 1000 ms
 *    - Point PIR away from heat sources and direct sunlight
 *    - Ensure stable power supply (use quality USB cable)
 * 
 * 4. Dashboard not receiving data:
 *    - Click "Connect ESP32" button in dashboard
 *    - Select the correct COM port from the dropdown
 *    - Check browser console (F12) for errors
 *    - Verify baud rate matches (115200)
 * 
 * 5. Permission denied error:
 *    - On some systems, you may need to grant permissions
 *    - Try using a different browser (Chrome/Edge recommended)
 *    - Run browser as administrator if on Windows
 */
