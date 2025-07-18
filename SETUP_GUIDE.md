# Real-time Audio Translation Setup Guide

This guide will help you set up a real-time English to Farsi translation system that works with VB-Cable and OBS Studio.

## 🎯 Overview

The system consists of:
1. **Real-time audio capture** from VB-Cable
2. **Speech recognition** using Whisper
3. **Translation** using Helsinki-NLP model
4. **Subtitle display** in OBS Studio

## 📋 Prerequisites

### 1. Install VB-Cable
- Download VB-Cable from: https://vb-audio.com/Cable/
- Install and restart your computer
- VB-Cable creates virtual audio devices: "CABLE Input" and "CABLE Output"

### 2. Install OBS Studio
- Download from: https://obsproject.com/
- Install and set up your scenes

### 3. Python Dependencies
```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

### Step 1: Test Audio Devices
First, let's see what audio devices are available:

```bash
python subtitle_stream.py --list-devices
```

Look for "CABLE Output" in the list. If it's not there, make sure VB-Cable is properly installed.

### Step 2: Start Real-time Translation

**Option A - Command Line:**
```bash
python subtitle_stream.py --whisper-model tiny --chunk-duration 5.0 --device "CABLE Output"
```

**Option B - Web Interface:**
```bash
python subtitle_stream.py --web
```

### Step 3: Configure OBS Studio

1. **Load the OBS Script:**
   - Open OBS Studio
   - Go to Tools → Scripts
   - Click the + button
   - Select `obs_integration.py`

2. **Configure the Script:**
   - Set "Subtitle File" to `subtitle.txt`
   - Set "Scene Name" to your scene name
   - Click "Setup Scene"
   - Click "Test Subtitle" to verify it works

## 🎙️ Audio Setup

### Windows Audio Configuration

1. **Set VB-Cable as Default:**
   - Right-click speaker icon → Sound settings
   - Set "CABLE Input" as default input device

2. **Route Audio to VB-Cable:**
   - In your application (Zoom, Discord, etc.)
   - Set microphone to "CABLE Input"
   - Or use Windows Stereo Mix to route system audio

### Alternative Audio Routing

**Using Windows Stereo Mix:**
1. Enable Stereo Mix in Windows sound settings
2. Set Stereo Mix to "CABLE Input"
3. This routes all system audio to the translator

**Using VoiceMeeter (Advanced):**
1. Install VoiceMeeter Banana
2. Route your microphone → VoiceMeeter → CABLE Input
3. More control over audio routing

## ⚙️ Configuration Options

### Whisper Model Sizes
- **tiny**: Fastest, ~39MB, good for real-time
- **base**: Balanced, ~74MB
- **small**: Better accuracy, ~244MB
- **medium**: Best accuracy, ~769MB

### Chunk Duration
- **2-3 seconds**: Very responsive, may miss context
- **5 seconds**: Good balance (recommended)
- **7-10 seconds**: More context, slower response

### Performance Tuning

**For Low-end PCs:**
```bash
python subtitle_stream.py --whisper-model tiny --chunk-duration 3.0
```

**For High-end PCs:**
```bash
python subtitle_stream.py --whisper-model base --chunk-duration 7.0
```

## 🎬 OBS Studio Integration

### Manual Setup (Alternative)

If the script doesn't work, you can set up manually:

1. **Create Text Source:**
   - Add → Text (GDI+)
   - Name it "Farsi_Subtitles"
   - Set font size to 48
   - Enable outline for better visibility

2. **Position the Text:**
   - Position at bottom center
   - Set alignment to center
   - Add background color if needed

3. **Use File Source (Alternative):**
   - Add → Text (FreeType 2)
   - Check "Read from file"
   - Set file path to `subtitle.txt`

### Advanced OBS Features

**Multiple Subtitle Styles:**
- Create different text sources for different styles
- Use different fonts, colors, and positions
- Switch between them based on content

**Subtitle Timing:**
- The system writes to `subtitle.txt` and `subtitle.json`
- JSON file includes timing information
- OBS script automatically handles timing

## 🔧 Troubleshooting

### Common Issues

**1. "Device not found" error:**
- Make sure VB-Cable is installed
- Check device name in Windows sound settings
- Try different device names: "CABLE Output", "CABLE Input", "VB-Audio Virtual Cable"

**2. No audio being captured:**
- Check Windows sound settings
- Ensure application is routing audio to VB-Cable
- Test with Windows Stereo Mix

**3. Poor translation quality:**
- Try larger Whisper model (base/small)
- Increase chunk duration for more context
- Check microphone quality and background noise

**4. OBS not showing subtitles:**
- Check file permissions
- Verify subtitle file is being created
- Try manual text source setup

**5. High CPU usage:**
- Use smaller Whisper model (tiny)
- Reduce chunk duration
- Close other applications

### Performance Optimization

**For Streaming:**
- Use "tiny" Whisper model
- Set chunk duration to 3-5 seconds
- Close unnecessary applications
- Use dedicated GPU if available

**For Recording:**
- Use "base" or "small" Whisper model
- Set chunk duration to 5-7 seconds
- Higher quality for post-processing

## 📁 File Structure

```
farsi-translator/
├── farsi_translator.py      # Main translator
├── subtitle_stream.py        # Real-time audio processing
├── obs_integration.py       # OBS Studio script
├── web_interface.py         # Web control interface
├── requirements.txt         # Dependencies
├── subtitle.txt            # Generated subtitles
├── subtitle.json           # Subtitle with timing
├── translation_config.json  # Configuration file
└── SETUP_GUIDE.md         # This guide
```

## 🎯 Usage Examples

### Live Streaming
1. Start the translator: `python subtitle_stream.py`
2. Open OBS Studio and load the script
3. Start your stream - subtitles appear automatically

### Recording
1. Start the translator with higher quality settings
2. Record your content
3. Subtitles are saved in real-time

### Conference Calls
1. Set VB-Cable as microphone in your meeting app
2. Start the translator
3. Speak in English, see Farsi subtitles

## 🔄 Advanced Features

### Custom Configuration
Edit `translation_config.json`:
```json
{
  "whisper_model_size": "tiny",
  "chunk_duration": 5.0,
  "sample_rate": 16000,
  "device_name": "CABLE Output",
  "enable_translation": true,
  "enable_subtitles": true,
  "subtitle_duration": 3.0,
  "min_confidence": 0.5,
  "language": "en"
}
```

### Multiple Language Support
The system can be extended to support other languages by:
1. Changing the Helsinki-NLP model
2. Modifying the language parameter in Whisper
3. Updating the translation pipeline

### Web Control Interface
Access the web interface at `http://localhost:7861` to:
- Start/stop translation remotely
- Monitor statistics
- Adjust settings in real-time

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all dependencies are installed
3. Test with the command-line version first
4. Check Windows sound settings and VB-Cable installation

## 🎉 Success Indicators

You'll know it's working when:
- ✅ Audio is being captured (no "Device not found" errors)
- ✅ Speech is being recognized (text appears in console)
- ✅ Translations are generated (Farsi text appears)
- ✅ Subtitles appear in OBS Studio
- ✅ File `subtitle.txt` is being updated

Happy translating! 🚀 