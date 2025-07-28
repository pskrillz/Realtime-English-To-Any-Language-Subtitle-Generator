# 🌐 Real-time English Translator

A powerful real-time English translation system that captures audio from any source (YouTube, Netflix, etc.) and provides live subtitles with OBS Studio integration.

The translator uses **Google Translate** under the hood. The default output
language is Persian (`fa`), but you can change it by editing the
`target_language` value in `translation_config.json`.

## ✨ Features

- **🎙️ Real-time Audio Capture**: Captures audio from any application (YouTube, Netflix, etc.)
- **🧠 AI-Powered Translation**: Uses Whisper for speech recognition + Google Translate for translation
- **🌐 Web Interface**: Clean Flask-based control interface
- **🎥 OBS Integration**: Automatic subtitle overlay for streaming/recording
- **📊 Live Monitoring**: Real-time display of English → translated text (language configurable)
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
 - Play English content and watch translated subtitles appear!

## 📁 Core Files

### **Main Components**
- `flask_web_interface.py` - Web control interface
- `subtitle_stream.py` - Real-time audio processing engine  
- `translator.py` - Translation core
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
4. **Record/Stream**: Translated subtitles will appear automatically

## 🛠️ Advanced Usage

### **Custom Configuration**
Edit `translation_config.json` to adjust:
- Whisper model size (tiny/base/small/medium)
- Audio chunk duration
- Subtitle display duration
- Audio device selection
- Target subtitle language (`target_language`)

### **Monitoring Translations**
```bash
python monitor_subtitles.py
```
Shows both English and the translated text in real-time:
```
🎯 NEW TRANSLATION:
   🇺🇸 English:  Hello, how are you?
   🌐 Translation: سلام، چطور هستید؟
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

- **YouTube Videos**: Real-time translated subtitles for English videos
- **Netflix/Streaming**: Live translation of movies and shows
- **Live Streams**: Translated subtitles for English live content
- **OBS Recording**: Burn-in translated subtitles to recorded videos
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

**🎉 Enjoy real-time translations! Perfect for enjoying English content with subtitles in your preferred language.**