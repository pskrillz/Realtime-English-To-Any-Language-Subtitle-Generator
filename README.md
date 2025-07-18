# 🇮🇷 Real-time English to Farsi Translator

A powerful real-time English to Farsi translation system that captures audio from any source (YouTube, Netflix, etc.) and provides live Farsi subtitles with OBS Studio integration.

## ✨ Features

- **🎙️ Real-time Audio Capture**: Captures audio from any application (YouTube, Netflix, etc.)
- **🧠 AI-Powered Translation**: Uses Whisper for speech recognition + Helsinki-NLP for translation
- **🌐 Web Interface**: Clean Flask-based control interface
- **🎥 OBS Integration**: Automatic subtitle overlay for streaming/recording
- **📊 Live Monitoring**: Real-time display of English → Farsi translations
- **⚡ High Performance**: Optimized for low-latency real-time processing

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Audio Routing
- Install [VB-Cable](https://vb-audio.com/Cable/) (virtual audio cable)
- Configure Windows audio routing (see setup guide)

### 3. Start Translation
```bash
# Option 1: Use the startup script
start_youtube_translation.bat

# Option 2: Manual start
python flask_web_interface.py
```

### 4. Open Web Interface
- Navigate to `http://localhost:5000`
- Click "🚀 Start Translation"
- Play English content and watch Farsi subtitles appear!

## 📁 Core Files

### **Main Components**
- `flask_web_interface.py` - Web control interface
- `subtitle_stream.py` - Real-time audio processing engine  
- `farsi_translator.py` - Translation core
- `obs_integration.py` - OBS Studio script for subtitle display

### **Utilities**
- `monitor_subtitles.py` - Live translation monitoring
- `test_system.py` - System testing and verification
- `quick_start.py` - Interactive setup wizard
- `test_audio_capture.py` - Audio debugging tool

### **Configuration**
- `translation_config.json` - System settings
- `requirements.txt` - Python dependencies

## 🎬 OBS Studio Integration

1. **Load the script**: Tools → Scripts → Add `obs_integration.py`
2. **Configure**: Set subtitle file to `subtitle.txt`
3. **Setup scene**: Click "Setup Scene" in script properties
4. **Record/Stream**: Farsi subtitles will appear automatically

## 🛠️ Advanced Usage

### **Custom Configuration**
Edit `translation_config.json` to adjust:
- Whisper model size (tiny/base/small/medium)
- Audio chunk duration
- Subtitle display duration
- Audio device selection

### **Monitoring Translations**
```bash
python monitor_subtitles.py
```
Shows both English and Farsi in real-time:
```
🎯 NEW TRANSLATION:
   🇺🇸 English:  Hello, how are you?
   🇮🇷 Farsi:    سلام، چطور هستید؟
```

### **System Testing**
```bash
python test_system.py
```
Verifies all components are working correctly.

## 📖 Documentation

- `SETUP_GUIDE.md` - Comprehensive setup instructions
- `MANUAL_OBS_SETUP.md` - Manual OBS configuration guide

## 🎯 Use Cases

- **YouTube Videos**: Real-time Farsi subtitles for English videos
- **Netflix/Streaming**: Live translation of movies and shows  
- **Live Streams**: Farsi subtitles for English live content
- **OBS Recording**: Burn-in Farsi subtitles to recorded videos
- **Language Learning**: Practice with dual-language display

## 🔧 System Requirements

- **OS**: Windows 10/11 (VB-Cable required)
- **Python**: 3.8+ 
- **RAM**: 4GB+ (8GB recommended)
- **Storage**: 2GB for models (downloaded automatically)
- **Audio**: VB-Cable virtual audio driver

## 🤝 Contributing

This is an open-source project. Feel free to submit issues, feature requests, or pull requests!

## 📄 License

MIT License - Feel free to use this project for personal or commercial purposes.

---

**🎉 Enjoy real-time Farsi translations! Perfect for Persian speakers wanting to enjoy English content with native subtitles.** 