#!/usr/bin/env python3
"""
Simple Command-Line Interface for Real-time Audio Translation
This will work without any web interface issues
"""

import time
import threading
from subtitle_stream import RealtimeAudioTranslator

def main():
    print("🎤 Real-time Audio Translator")
    print("=" * 50)
    print("English to Farsi Translation System")
    print("=" * 50)
    
    print("\n📋 Instructions:")
    print("1. Configure audio routing (Stereo Mix → CABLE Input)")
    print("2. Start translation below")
    print("3. Play web video (Netflix, YouTube, etc.)")
    print("4. Watch Farsi subtitles appear in real-time")
    print("5. Use OBS Studio for subtitle display")
    print("=" * 50)
    
    # Configuration
    whisper_model = "tiny"
    chunk_duration = 3.0
    device_name = "CABLE Output"
    
    print(f"\n⚙️ Configuration:")
    print(f"   Whisper Model: {whisper_model}")
    print(f"   Chunk Duration: {chunk_duration} seconds")
    print(f"   Audio Device: {device_name}")
    
    input("\nPress Enter to start translation...")
    
    try:
        print("\n🚀 Starting translation system...")
        translator = RealtimeAudioTranslator(
            whisper_model_size=whisper_model,
            chunk_duration=chunk_duration,
            device_name=device_name
        )
        
        print("✅ Translation started!")
        print("🎬 Now play any web video (Netflix, YouTube, etc.)")
        print("📝 Farsi subtitles will appear in real-time")
        print("⏹️ Press Ctrl+C to stop")
        print("-" * 50)
        
        # Start translation
        translator.start_streaming()
        
    except KeyboardInterrupt:
        print("\n⏹️ Translation stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure VB-Cable is installed")
        print("2. Check audio device settings")
        print("3. Try running as administrator")
    
    print("\n👋 Goodbye!")

if __name__ == "__main__":
    main() 