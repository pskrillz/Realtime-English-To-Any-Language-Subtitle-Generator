import time
import os
import json

print("🔍 Monitoring subtitle files for changes...")
print("Press Ctrl+C to stop monitoring")
print("=" * 50)

last_txt_content = ""
last_json_content = ""

try:
    while True:
        # Check JSON file first (contains both languages)
        if os.path.exists("subtitle.json"):
            try:
                with open("subtitle.json", "r", encoding="utf-8") as f:
                    json_content = f.read().strip()
                    if json_content != last_json_content and json_content:
                        try:
                            data = json.loads(json_content)
                            translated_text = data.get('text', '')
                            english_text = data.get('english', '')
                            
                            if translated_text:
                                print("🎯 NEW TRANSLATION:")
                                if english_text:
                                    print(f"   🇺🇸 English:  {english_text}")
                                print(f"   🌐 Translation: {translated_text}")
                                print("-" * 50)
                                
                        except json.JSONDecodeError:
                            print("📊 JSON UPDATE: File modified (parsing error)")
                        
                        last_json_content = json_content
            except Exception as e:
                pass  # Ignore file read errors
        
        # Also check TXT file as backup
        if os.path.exists("subtitle.txt"):
            with open("subtitle.txt", "r", encoding="utf-8") as f:
                txt_content = f.read().strip()
                if txt_content != last_txt_content and txt_content:
                    # Only show TXT if JSON didn't already show it
                    if not last_json_content or txt_content not in last_json_content:
                        print(f"📝 TXT ONLY: {txt_content}")
                    last_txt_content = txt_content
        
        time.sleep(1)  # Check every second
        
except KeyboardInterrupt:
    print("\n👋 Monitoring stopped") 