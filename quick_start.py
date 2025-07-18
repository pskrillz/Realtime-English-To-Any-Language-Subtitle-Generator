#!/usr/bin/env python3
"""
Quick Start Script for Real-time Farsi Translation System
This script provides a simple interface to get everything running quickly.
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path

def print_banner():
    """Print the system banner"""
    print("=" * 60)
    print("🇮🇷 Real-time English to Farsi Translation System")
    print("=" * 60)
    print("🎯 Complete solution for live streaming with Farsi subtitles")
    print("📋 Includes: VB-Cable integration, OBS Studio support, Web interface")
    print("=" * 60)

def check_dependencies():
    """Check if all dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        "torch", "transformers", "sounddevice", "numpy", 
        "faster-whisper", "gradio", "sentencepiece", "protobuf"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Installing missing dependencies...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies. Please run:")
            print("   pip install -r requirements.txt")
            return False
    
    return True

def check_vb_cable():
    """Check if VB-Cable is installed"""
    print("\n🎙️ Checking VB-Cable installation...")
    
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        
        cable_devices = [d for d in devices if 'CABLE' in d['name'].upper()]
        
        if cable_devices:
            print("✅ VB-Cable devices found:")
            for device in cable_devices:
                print(f"  - {device['name']}")
            return True
        else:
            print("❌ VB-Cable not found!")
            print("\n📥 Please install VB-Cable:")
            print("   1. Download from: https://vb-audio.com/Cable/")
            print("   2. Install and restart your computer")
            print("   3. Run this script again")
            return False
            
    except Exception as e:
        print(f"❌ Error checking VB-Cable: {e}")
        return False

def setup_audio_routing():
    """Guide user through audio routing setup"""
    print("\n🎛️ Audio Routing Setup")
    print("=" * 40)
    print("To route audio to the translator, you need to:")
    print("1. Set your application's microphone to 'CABLE Input'")
    print("2. Or enable 'Stereo Mix' in Windows sound settings")
    print("3. Route Stereo Mix to 'CABLE Input'")
    print("\nAlternative: Use VoiceMeeter Banana for advanced routing")
    
    input("\nPress Enter when you've configured your audio routing...")

def test_translation():
    """Test the translation system"""
    print("\n🧪 Testing translation system...")
    
    try:
        from farsi_translator import FarsiTranslator
        
        translator = FarsiTranslator()
        print("Loading translation model (this may take a few minutes on first run)...")
        
        if translator.load_model():
            test_text = "Hello, this is a test of the translation system."
            result = translator.translate_text(test_text)
            print(f"✅ Test successful!")
            print(f"English: {test_text}")
            print(f"Farsi: {result}")
            return True
        else:
            print("❌ Failed to load translation model")
            return False
            
    except Exception as e:
        print(f"❌ Translation test failed: {e}")
        return False

def create_config():
    """Create default configuration"""
    print("\n⚙️ Creating configuration...")
    
    config = {
        "whisper_model_size": "tiny",
        "chunk_duration": 5.0,
        "sample_rate": 16000,
        "device_name": "CABLE Output",
        "subtitle_file": "subtitle.txt",
        "enable_translation": True,
        "enable_subtitles": True,
        "subtitle_duration": 3.0,
        "min_confidence": 0.5,
        "language": "en"
    }
    
    try:
        with open("translation_config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        print("✅ Configuration created")
        return True
    except Exception as e:
        print(f"❌ Failed to create configuration: {e}")
        return False

def show_menu():
    """Show the main menu"""
    print("\n" + "=" * 40)
    print("🚀 QUICK START MENU")
    print("=" * 40)
    print("1. 🧪 Run System Test")
    print("2. 🎤 Start Real-time Translation (Command Line)")
    print("3. 🌐 Start Real-time Translation (Web Interface)")
    print("4. 📋 Show OBS Studio Setup Instructions")
    print("5. 📖 Show Full Setup Guide")
    print("6. 🚪 Exit")
    print("=" * 40)

def run_system_test():
    """Run the comprehensive system test"""
    print("\n🧪 Running system test...")
    
    try:
        result = subprocess.run([sys.executable, "test_system.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ System test passed!")
            return True
        else:
            print("❌ System test failed!")
            print("Error output:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Failed to run system test: {e}")
        return False

def start_translation_cli():
    """Start translation in command line mode"""
    print("\n🎤 Starting real-time translation (Command Line)...")
    print("Press Ctrl+C to stop")
    
    try:
        subprocess.run([sys.executable, "subtitle_stream.py", "--whisper-model", "tiny"])
    except KeyboardInterrupt:
        print("\n⏹️  Translation stopped")

def start_translation_web():
    """Start translation with web interface"""
    print("\n🌐 Starting real-time translation (Web Interface)...")
    print("Web interface will be available at: http://localhost:7861")
    print("Press Ctrl+C to stop")
    
    try:
        subprocess.run([sys.executable, "subtitle_stream.py", "--web"])
    except KeyboardInterrupt:
        print("\n⏹️  Translation stopped")

def show_obs_instructions():
    """Show OBS Studio setup instructions"""
    print("\n🎬 OBS Studio Setup Instructions")
    print("=" * 50)
    print("1. Open OBS Studio")
    print("2. Go to Tools → Scripts")
    print("3. Click the + button")
    print("4. Select 'obs_integration.py'")
    print("5. Configure the script:")
    print("   - Set 'Subtitle File' to 'subtitle.txt'")
    print("   - Set 'Scene Name' to your scene name")
    print("   - Click 'Setup Scene'")
    print("   - Click 'Test Subtitle' to verify")
    print("\n6. Start your stream/recording")
    print("7. Speak in English - Farsi subtitles will appear!")

def show_setup_guide():
    """Show the full setup guide"""
    print("\n📖 Full Setup Guide")
    print("=" * 50)
    print("For detailed instructions, see: SETUP_GUIDE.md")
    print("\nQuick reference:")
    print("- Install VB-Cable: https://vb-audio.com/Cable/")
    print("- Install OBS Studio: https://obsproject.com/")
    print("- Route audio to 'CABLE Input'")
    print("- Run translation system")
    print("- Load OBS script")

def main():
    """Main function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check VB-Cable
    if not check_vb_cable():
        return
    
    # Setup audio routing
    setup_audio_routing()
    
    # Test translation
    if not test_translation():
        print("❌ Translation test failed. Please check the errors above.")
        return
    
    # Create configuration
    if not create_config():
        return
    
    print("\n✅ System is ready!")
    
    # Main menu loop
    while True:
        show_menu()
        
        try:
            choice = input("\nSelect an option (1-6): ").strip()
            
            if choice == "1":
                run_system_test()
            elif choice == "2":
                start_translation_cli()
            elif choice == "3":
                start_translation_web()
            elif choice == "4":
                show_obs_instructions()
            elif choice == "5":
                show_setup_guide()
            elif choice == "6":
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-6.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 