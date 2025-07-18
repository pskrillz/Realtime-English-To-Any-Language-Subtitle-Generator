#!/usr/bin/env python3
"""
Flask-based web interface for real-time audio translation
This should work without any permission issues
"""

from flask import Flask, render_template_string, request, jsonify
import threading
import time
from subtitle_stream import RealtimeAudioTranslator

app = Flask(__name__)

# Global translator instance
translator_instance = None

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Real-time Audio Translator</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .button { background: #007bff; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; margin: 10px; font-size: 16px; }
        .button:hover { background: #0056b3; }
        .button.stop { background: #dc3545; }
        .button.stop:hover { background: #c82333; }
        .status { padding: 15px; margin: 15px 0; border-radius: 5px; background: #f8f9fa; border-left: 4px solid #007bff; }
        .stats { padding: 15px; margin: 15px 0; border-radius: 5px; background: #e9ecef; }
        .instructions { background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎤 Real-time Audio Translator</h1>
        <p style="text-align: center; color: #666;">English to Farsi Translation</p>
        
        <div style="text-align: center; margin: 30px 0;">
            <button class="button" onclick="startTranslation()">🚀 Start Translation</button>
            <button class="button stop" onclick="stopTranslation()">⏹️ Stop Translation</button>
        </div>
        
        <div class="status" id="status">
            <strong>Status:</strong> <span id="statusText">Ready to start</span>
        </div>
        
        <div class="stats" id="stats">
            <strong>Statistics:</strong> <span id="statsText">No active translation</span>
        </div>
        
        <div class="instructions">
            <h3>📋 Instructions:</h3>
            <ol>
                <li>Click "Start Translation"</li>
                <li>Configure audio routing (Stereo Mix → CABLE Input)</li>
                <li>Play web video (Netflix, YouTube, etc.)</li>
                <li>Watch Farsi subtitles appear in real-time</li>
                <li>Use OBS Studio for subtitle display</li>
            </ol>
        </div>
        
        <div style="text-align: center; margin-top: 30px; color: #666;">
            <p>🌐 Web Interface for Real-time Farsi Translation</p>
        </div>
    </div>
    
    <script>
        function startTranslation() {
            fetch('/start', {method: 'POST'})
                .then(response => response.json())
                .then(data => {
                    document.getElementById('statusText').textContent = data.message;
                });
        }
        
        function stopTranslation() {
            fetch('/stop', {method: 'POST'})
                .then(response => response.json())
                .then(data => {
                    document.getElementById('statusText').textContent = data.message;
                });
        }
        
        function updateStats() {
            fetch('/stats')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('statsText').textContent = data.message;
                });
        }
        
        // Update stats every 3 seconds
        setInterval(updateStats, 3000);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/start', methods=['POST'])
def start_translation():
    global translator_instance
    try:
        translator_instance = RealtimeAudioTranslator(
            whisper_model_size="tiny",
            chunk_duration=3.0,
            device_name="CABLE Output"
        )
        # Start in a separate thread
        thread = threading.Thread(target=translator_instance.start_streaming)
        thread.daemon = True
        thread.start()
        return jsonify({"message": "✅ Translation started successfully!"})
    except Exception as e:
        return jsonify({"message": f"❌ Error: {e}"})

@app.route('/stop', methods=['POST'])
def stop_translation():
    global translator_instance
    if translator_instance:
        translator_instance.stop_streaming()
        return jsonify({"message": "⏹️ Translation stopped"})
    return jsonify({"message": "⚠️ No active translation"})

@app.route('/stats')
def get_stats():
    global translator_instance
    if translator_instance:
        stats = translator_instance.get_stats()
        return jsonify({"message": f"📊 Translations: {stats['translation_count']}, Last: {stats['last_translation']:.1f}s ago"})
    return jsonify({"message": "📊 No active translation"})

if __name__ == '__main__':
    print("🚀 Starting Flask web interface...")
    print("🌐 Opening at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False) 