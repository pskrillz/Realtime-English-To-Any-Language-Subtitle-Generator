#!/usr/bin/env python3
"""
Test script for the real-time Farsi translation system
This script tests all components to ensure everything is working correctly.
"""

import os
import sys
import time
import json
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import torch
        print(f"✅ PyTorch: {torch.__version__}")
    except ImportError as e:
        print(f"❌ PyTorch import failed: {e}")
        return False
    
    try:
        from transformers import MarianMTModel, MarianTokenizer
        print("✅ Transformers")
    except ImportError as e:
        print(f"❌ Transformers import failed: {e}")
        return False
    
    try:
        import sounddevice as sd
        print("✅ SoundDevice")
    except ImportError as e:
        print(f"❌ SoundDevice import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ NumPy")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    try:
        from faster_whisper import WhisperModel
        print("✅ Faster Whisper")
    except ImportError as e:
        print(f"❌ Faster Whisper import failed: {e}")
        return False
    
    try:
        import gradio as gr
        print("✅ Gradio")
    except ImportError as e:
        print(f"❌ Gradio import failed: {e}")
        return False
    
    return True

def test_audio_devices():
    """Test audio device detection"""
    print("\n🎙️ Testing audio devices...")
    
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        
        print(f"Found {len(devices)} audio devices:")
        for i, device in enumerate(devices):
            print(f"  {i}: {device['name']}")
        
        # Look for VB-Cable devices
        cable_devices = [d for d in devices if 'CABLE' in d['name'].upper()]
        if cable_devices:
            print("✅ VB-Cable devices found:")
            for device in cable_devices:
                print(f"  - {device['name']}")
        else:
            print("⚠️  No VB-Cable devices found. Make sure VB-Cable is installed.")
        
        return len(cable_devices) > 0
        
    except Exception as e:
        print(f"❌ Audio device test failed: {e}")
        return False

def test_farsi_translator():
    """Test the Farsi translator"""
    print("\n🇮🇷 Testing Farsi translator...")
    
    try:
        from farsi_translator import FarsiTranslator
        
        translator = FarsiTranslator()
        print("✅ FarsiTranslator class created")
        
        # Test translation
        test_text = "Hello, how are you?"
        print(f"Testing translation: '{test_text}'")
        
        # This will download the model on first run
        success = translator.load_model()
        if success:
            result = translator.translate_text(test_text)
            print(f"✅ Translation result: {result}")
            return True
        else:
            print("❌ Failed to load translation model")
            return False
            
    except Exception as e:
        print(f"❌ Farsi translator test failed: {e}")
        return False

def test_whisper_model():
    """Test Whisper speech recognition"""
    print("\n🎤 Testing Whisper model...")
    
    try:
        from faster_whisper import WhisperModel
        
        print("Loading Whisper model (tiny)...")
        model = WhisperModel("tiny")
        print("✅ Whisper model loaded successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Whisper model test failed: {e}")
        return False

def test_file_permissions():
    """Test file write permissions for subtitle files"""
    print("\n📁 Testing file permissions...")
    
    test_files = ["subtitle.txt", "subtitle.json", "translation_config.json"]
    
    for filename in test_files:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("test")
            
            if os.path.exists(filename):
                os.remove(filename)
                print(f"✅ {filename}: Write permission OK")
            else:
                print(f"❌ {filename}: Write failed")
                return False
                
        except Exception as e:
            print(f"❌ {filename}: Permission error - {e}")
            return False
    
    return True

def test_obs_integration():
    """Test OBS integration script"""
    print("\n🎬 Testing OBS integration...")
    
    try:
        # Check if OBS script file exists
        if os.path.exists("obs_integration.py"):
            print("✅ OBS integration script found")
            
            # Try to import (this will fail if OBS is not running, which is OK)
            try:
                import obs_integration
                print("✅ OBS integration script is valid")
                return True
            except ImportError:
                print("⚠️  OBS integration script exists but OBS is not running (this is normal)")
                return True
        else:
            print("❌ OBS integration script not found")
            return False
            
    except Exception as e:
        print(f"❌ OBS integration test failed: {e}")
        return False

def test_web_interface():
    """Test web interface components"""
    print("\n🌐 Testing web interface...")
    
    try:
        from web_interface import create_web_interface
        print("✅ Web interface module imported")
        return True
        
    except Exception as e:
        print(f"❌ Web interface test failed: {e}")
        return False

def create_test_config():
    """Create a test configuration file"""
    print("\n⚙️ Creating test configuration...")
    
    test_config = {
        "whisper_model_size": "tiny",
        "chunk_duration": 3.0,
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
            json.dump(test_config, f, indent=2)
        print("✅ Test configuration created")
        return True
    except Exception as e:
        print(f"❌ Failed to create test configuration: {e}")
        return False

def run_comprehensive_test():
    """Run all tests"""
    print("🚀 Starting comprehensive system test...")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Audio Devices", test_audio_devices),
        ("Farsi Translator", test_farsi_translator),
        ("Whisper Model", test_whisper_model),
        ("File Permissions", test_file_permissions),
        ("OBS Integration", test_obs_integration),
        ("Web Interface", test_web_interface),
        ("Configuration", create_test_config)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("1. Install VB-Cable if not already installed")
        print("2. Configure your audio routing")
        print("3. Run: python subtitle_stream.py --web")
        print("4. Load obs_integration.py in OBS Studio")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nCommon fixes:")
        print("- Install missing dependencies: pip install -r requirements.txt")
        print("- Install VB-Cable for audio routing")
        print("- Check file permissions in the current directory")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1) 