import sounddevice as sd
import numpy as np
import time

print("🎤 Testing audio capture from CABLE Output...")
print("Play some YouTube audio and you should see audio level indicators")
print("Press Ctrl+C to stop")
print("=" * 50)

try:
    # Try to find CABLE Output device
    devices = sd.query_devices()
    cable_device = None
    
    for i, device in enumerate(devices):
        if "CABLE Output" in device['name']:
            cable_device = i
            print(f"Found CABLE Output device: {device['name']} (ID: {i})")
            break
    
    if cable_device is None:
        print("❌ CABLE Output device not found!")
        print("Available devices with 'CABLE' in name:")
        for i, device in enumerate(devices):
            if "CABLE" in device['name']:
                print(f"  {i}: {device['name']}")
        exit()
    
    # Test audio capture
    def audio_callback(indata, frames, time, status):
        if status:
            print(f"Audio status: {status}")
        
        # Calculate audio level
        level = np.max(np.abs(indata))
        if level > 0.01:  # Threshold for audio detection
            bars = int(level * 50)  # Scale to 50 bars
            print(f"🔊 Audio detected: {'█' * bars} ({level:.3f})")
    
    # Start audio stream
    with sd.InputStream(device=cable_device, callback=audio_callback, channels=1, samplerate=16000):
        print("🎧 Listening for audio... (play YouTube video now)")
        while True:
            time.sleep(0.1)
            
except KeyboardInterrupt:
    print("\n👋 Audio test stopped")
except Exception as e:
    print(f"❌ Error: {e}")
    print("Try running with a different audio device or check VB-Cable installation") 