import sounddevice as sd
import numpy as np
import threading
import time
import queue
import os
from faster_whisper import WhisperModel
from farsi_translator import FarsiTranslator
import torch
from collections import deque
import json

class RealtimeAudioTranslator:
    def __init__(self, 
                 whisper_model_size="tiny",
                 chunk_duration=5.0,
                 sample_rate=16000,
                 device_name="CABLE Output",
                 subtitle_file="subtitle.txt",
                 config_file="translation_config.json"):
        
        self.whisper_model_size = whisper_model_size
        self.chunk_duration = chunk_duration
        self.sample_rate = sample_rate
        self.device_name = device_name
        self.subtitle_file = subtitle_file
        self.config_file = config_file
        
        # Audio processing
        self.audio_buffer = deque(maxlen=int(sample_rate * chunk_duration))
        self.audio_queue = queue.Queue()
        self.is_recording = False
        
        # Models
        self.asr_model = None
        self.translator = None
        
        # Translation settings
        self.load_config()
        
        # Performance tracking
        self.translation_count = 0
        self.last_translation_time = time.time()
        
    def load_config(self):
        """Load configuration from file or create default"""
        default_config = {
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
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = default_config
                self.save_config()
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = default_config
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def initialize_models(self):
        """Initialize ASR and translation models"""
        print("Initializing models...")
        
        # Initialize Whisper ASR
        try:
            print(f"Loading Whisper model: {self.whisper_model_size}")
            self.asr_model = WhisperModel(
                self.config["whisper_model_size"],
                device="cuda" if torch.cuda.is_available() else "cpu",
                compute_type="float16" if torch.cuda.is_available() else "float32"
            )
            print("Whisper model loaded successfully")
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            return False
        
        # Initialize Farsi translator
        try:
            print("Loading Farsi translator...")
            self.translator = FarsiTranslator()
            if not self.translator.load_model():
                print("Failed to load Farsi translator")
                return False
            print("Farsi translator loaded successfully")
        except Exception as e:
            print(f"Error loading Farsi translator: {e}")
            return False
        
        return True
    
    def audio_callback(self, indata, frames, time, status):
        """Audio callback for real-time processing"""
        if status:
            print(f"Audio status: {status}")
        
        # Convert to mono and normalize (optimized for real-time)
        audio = np.copy(indata[:,0]) if indata.ndim > 1 else np.copy(indata)
        audio = audio.astype(np.float32)
        
        # Add to buffer
        self.audio_buffer.extend(audio)
        
        # Check if we have enough audio for processing
        if len(self.audio_buffer) >= self.sample_rate * self.chunk_duration:
            # Get the chunk and clear buffer
            chunk = np.array(list(self.audio_buffer))
            self.audio_buffer.clear()
            
            # Add to processing queue (non-blocking)
            try:
                self.audio_queue.put_nowait(chunk)
            except queue.Full:
                # Drop oldest chunk if queue is full
                try:
                    self.audio_queue.get_nowait()
                    self.audio_queue.put_nowait(chunk)
                except queue.Empty:
                    pass
    
    def process_audio_chunk(self, audio_chunk):
        """Process audio chunk for speech recognition and translation"""
        try:
            # Speech recognition
            segments, info = self.asr_model.transcribe(
                audio_chunk,
                language=self.config["language"],
                beam_size=5,
                best_of=5,
                temperature=0.0,
                compression_ratio_threshold=2.4,
                log_prob_threshold=-1.0,
                no_speech_threshold=0.6,
                condition_on_previous_text=False,
                initial_prompt=None
            )
            
            # Extract text from segments
            text = " ".join([seg.text.strip() for seg in segments if seg.text.strip()])
            
            if text and len(text) > 3:  # Minimum text length
                print(f"Recognized: {text}")
                
                # Translate if enabled
                if self.config["enable_translation"]:
                    farsi_text = self.translator.translate_text(text)
                    print(f"Translated: {farsi_text}")
                    
                    # Write subtitle if enabled
                    if self.config["enable_subtitles"]:
                        self.write_subtitle(farsi_text, text)  # Pass both Farsi and English
                    
                    self.translation_count += 1
                    self.last_translation_time = time.time()
                    
                    return farsi_text
            
        except Exception as e:
            print(f"Error processing audio chunk: {e}")
        
        return None
    
    def write_subtitle(self, farsi_text, english_text=None):
        """Write subtitle text to file for OBS"""
        try:
            # Create subtitle data with timing and both languages
            subtitle_data = {
                "text": farsi_text,
                "english": english_text if english_text else "",
                "timestamp": time.time(),
                "duration": self.config["subtitle_duration"]
            }
            
            # Write only Farsi to TXT file (for OBS)
            with open(self.subtitle_file, 'w', encoding='utf-8') as f:
                f.write(farsi_text)
            
            # Write JSON format with both languages for monitoring
            json_file = self.subtitle_file.replace('.txt', '.json')
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(subtitle_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Error writing subtitle: {e}")
    
    def get_audio_devices(self):
        """List available audio devices"""
        devices = sd.query_devices()
        print("\nAvailable audio devices:")
        for i, device in enumerate(devices):
            print(f"{i}: {device['name']} (inputs: {device['max_input_channels']}, outputs: {device['max_output_channels']})")
        return devices
    
    def find_device_index(self, device_name):
        """Find device index by name"""
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            if device_name.lower() in device['name'].lower():
                return i
        return None
    
    def start_streaming(self):
        """Start the real-time audio translation stream"""
        if not self.initialize_models():
            print("Failed to initialize models")
            return
        
        # Find audio device
        device_index = self.find_device_index(self.device_name)
        if device_index is None:
            print(f"Device '{self.device_name}' not found. Available devices:")
            self.get_audio_devices()
            return
        
        print(f"Using audio device: {self.device_name} (index: {device_index})")
        
        # Set up audio stream with optimized settings
        try:
            with sd.InputStream(
                device=device_index,
                channels=1,
                samplerate=self.sample_rate,
                callback=self.audio_callback,
                dtype=np.float32,
                blocksize=int(self.sample_rate * 0.1),  # 100ms blocks for lower latency
                latency='low'
            ):
                print(f"Started listening on {self.device_name}")
                print("Press Ctrl+C to stop")
                print("-" * 50)
                
                self.is_recording = True
                
                # Process audio chunks in background
                while self.is_recording:
                    try:
                        # Get audio chunk from queue (non-blocking)
                        audio_chunk = self.audio_queue.get(timeout=1.0)
                        self.process_audio_chunk(audio_chunk)
                    except queue.Empty:
                        continue
                    except KeyboardInterrupt:
                        print("\nStopping audio stream...")
                        break
                    except Exception as e:
                        print(f"Error in processing loop: {e}")
                        
        except Exception as e:
            print(f"Error starting audio stream: {e}")
    
    def stop_streaming(self):
        """Stop the audio stream"""
        self.is_recording = False
        print("Audio stream stopped")
    
    def get_stats(self):
        """Get translation statistics"""
        current_time = time.time()
        elapsed = current_time - self.last_translation_time
        return {
            "translation_count": self.translation_count,
            "last_translation": elapsed,
            "is_recording": self.is_recording
        }

def create_web_control_interface():
    """Create a web interface for controlling the real-time translator"""
    import gradio as gr
    
    translator_instance = None
    
    def start_translation(whisper_model, chunk_duration, device_name):
        global translator_instance
        try:
            translator_instance = RealtimeAudioTranslator(
                whisper_model_size=whisper_model,
                chunk_duration=float(chunk_duration),
                device_name=device_name
            )
            # Start in a separate thread
            thread = threading.Thread(target=translator_instance.start_streaming)
            thread.daemon = True
            thread.start()
            return "Translation started successfully!"
        except Exception as e:
            return f"Error starting translation: {e}"
    
    def stop_translation():
        global translator_instance
        if translator_instance:
            translator_instance.stop_streaming()
            return "Translation stopped"
        return "No active translation"
    
    def get_stats():
        global translator_instance
        if translator_instance:
            stats = translator_instance.get_stats()
            return f"Translations: {stats['translation_count']}, Last: {stats['last_translation']:.1f}s ago"
        return "No active translation"
    
    # Create interface
    with gr.Blocks(title="Real-time Audio Translator Control") as interface:
        gr.Markdown("# 🎤 Real-time Audio Translator")
        gr.Markdown("Control panel for VB-Cable + OBS integration")
        
        with gr.Row():
            with gr.Column():
                whisper_model = gr.Dropdown(
                    choices=["tiny", "base", "small", "medium"],
                    value="tiny",
                    label="Whisper Model Size"
                )
                chunk_duration = gr.Slider(
                    minimum=2.0,
                    maximum=10.0,
                    value=5.0,
                    step=0.5,
                    label="Chunk Duration (seconds)"
                )
                device_name = gr.Textbox(
                    value="CABLE Output",
                    label="Audio Device Name"
                )
                
                start_btn = gr.Button("Start Translation", variant="primary")
                stop_btn = gr.Button("Stop Translation", variant="secondary")
                
            with gr.Column():
                status_output = gr.Textbox(label="Status", interactive=False)
                stats_output = gr.Textbox(label="Statistics", interactive=False)
                
                # Auto-refresh stats every 2 seconds.
        
        start_btn.click(
            fn=start_translation,
            inputs=[whisper_model, chunk_duration, device_name],
            outputs=status_output
        )
        
        stop_btn.click(
            fn=stop_translation,
            outputs=status_output
        )
        
        interface.load(fn=get_stats, outputs=stats_output, every=2)
    
    return interface

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Real-time Audio Translator")
    parser.add_argument("--web", action="store_true", help="Launch web control interface")
    parser.add_argument("--whisper-model", default="tiny", choices=["tiny", "base", "small", "medium"], help="Whisper model size")
    parser.add_argument("--chunk-duration", type=float, default=5.0, help="Audio chunk duration in seconds")
    parser.add_argument("--device", default="CABLE Output", help="Audio device name")
    parser.add_argument("--list-devices", action="store_true", help="List available audio devices")
    
    args = parser.parse_args()
    
    if args.list_devices:
        translator = RealtimeAudioTranslator()
        translator.get_audio_devices()
    elif args.web:
        interface = create_web_control_interface()
        interface.launch(
            share=True, 
            server_name="127.0.0.1", 
            server_port=7861,
            show_error=True,
            quiet=False
        )
    else:
        # Command line mode
        translator = RealtimeAudioTranslator(
            whisper_model_size=args.whisper_model,
            chunk_duration=args.chunk_duration,
            device_name=args.device
        )
        translator.start_streaming()
