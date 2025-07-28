try:
    import obspython as obs
except ImportError:
    # This script is designed to be run from within OBS Studio.
    # The 'obspython' module is provided by the OBS environment.
    # If you see this error, it means you are trying to run the script
    # directly with a standard Python interpreter.
    #
    # To fix:
    # 1. Open OBS Studio.
    # 2. Go to Tools -> Scripts.
    # 3. Click the '+' button and add this file.
    #
    # The Pylance/Linter error "Import 'obspython' could not be resolved"
    # is expected in editors like VSCode and can be safely ignored.
    raise ImportError("This script must be run from within OBS Studio. Please see the comments in obs_integration.py for setup instructions.")
import os
import json
import time
from datetime import datetime

class OBSSubtitleDisplay:
    def __init__(self):
        self.subtitle_file = "subtitle.txt"
        self.json_file = "subtitle.json"
        self.subtitle_source_name = "Translated_Subtitles"
        self.last_text = ""
        self.last_update = 0
        self.subtitle_duration = 3.0  # seconds
        self.font_size = 48
        self.font_color = 0xFFFFFFFF  # White
        self.background_color = 0x80000000  # Semi-transparent black
        self.position_x = 50
        self.position_y = 80  # Percentage from top
        
    def create_subtitle_source(self):
        """Create or get the subtitle text source in OBS"""
        # Check if source already exists
        source = obs.obs_get_source_by_name(self.subtitle_source_name)
        if source:
            obs.obs_source_release(source)
            return True
        
        # Create new text source
        source = obs.obs_source_create("text_ft2_source", self.subtitle_source_name, None, None)
        if source:
            settings = obs.obs_data_create()
            obs.obs_data_set_string(settings, "text", "")
            obs.obs_data_set_int(settings, "font", 0)
            obs.obs_data_set_int(settings, "font_size", self.font_size)
            obs.obs_data_set_int(settings, "color", self.font_color)
            obs.obs_data_set_bool(settings, "outline", True)
            obs.obs_data_set_int(settings, "outline_color", self.background_color)
            obs.obs_data_set_int(settings, "outline_size", 2)
            obs.obs_data_set_bool(settings, "word_wrap", True)
            obs.obs_data_set_int(settings, "align", 1)  # Center align
            
            obs.obs_source_update(source, settings)
            obs.obs_data_release(settings)
            obs.obs_source_release(source)
            return True
        
        return False
    
    def add_subtitle_to_scene(self, scene_name="Scene"):
        """Add subtitle source to the specified scene"""
        scene = obs.obs_get_scene_by_name(scene_name)
        if not scene:
            print(f"Scene '{scene_name}' not found")
            return False
        
        # Create subtitle source if it doesn't exist
        if not self.create_subtitle_source():
            print("Failed to create subtitle source")
            obs.obs_scene_release(scene)
            return False
        
        # Get the subtitle source
        source = obs.obs_get_source_by_name(self.subtitle_source_name)
        if not source:
            print("Subtitle source not found")
            obs.obs_scene_release(scene)
            return False
        
        # Add source to scene
        scene_item = obs.obs_scene_add(scene, source)
        if scene_item:
            # Position the subtitle (bottom center)
            pos = obs.vec2()
            pos.x = self.position_x
            pos.y = self.position_y
            obs.obs_sceneitem_set_pos(scene_item, pos)
            
            # Set alignment to center
            obs.obs_sceneitem_set_alignment(scene_item, 5)  # Center
            
            print(f"Added subtitle source to scene '{scene_name}'")
        
        obs.obs_source_release(source)
        obs.obs_scene_release(scene)
        return True
    
    def update_subtitle_text(self, text):
        """Update the subtitle text in OBS"""
        source = obs.obs_get_source_by_name(self.subtitle_source_name)
        if not source:
            print("Subtitle source not found")
            return False
        
        settings = obs.obs_data_create()
        obs.obs_data_set_string(settings, "text", text)
        obs.obs_source_update(source, settings)
        obs.obs_data_release(settings)
        obs.obs_source_release(source)
        
        self.last_text = text
        self.last_update = time.time()
        return True
    
    def read_subtitle_file(self):
        """Read subtitle from file and update OBS"""
        print(f"DEBUG: Checking files - JSON exists: {os.path.exists(self.json_file)}, TXT exists: {os.path.exists(self.subtitle_file)}")
        try:
            subtitle_text = ""
            found_valid_subtitle = False
            
            # Try reading JSON file first (more detailed with timing)
            if os.path.exists(self.json_file):
                try:
                    with open(self.json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        text = data.get('text', '')
                        timestamp = data.get('timestamp', 0)
                        
                        # Check if subtitle is still valid (not too old)
                        if text and (time.time() - timestamp < self.subtitle_duration):
                            subtitle_text = text
                            found_valid_subtitle = True
                            print(f"DEBUG: Valid JSON subtitle: {text}")
                except Exception as e:
                    print(f"Error reading JSON file: {e}")
            
            # If no valid JSON subtitle, try text file
            if not found_valid_subtitle and os.path.exists(self.subtitle_file):
                try:
                    with open(self.subtitle_file, 'r', encoding='utf-8') as f:
                        text = f.read().strip()
                        if text:
                            subtitle_text = text
                            found_valid_subtitle = True
                            print(f"DEBUG: Valid TXT subtitle: {text}")
                except Exception as e:
                    print(f"Error reading TXT file: {e}")
            
            # Update subtitle if we have new text
            if found_valid_subtitle and subtitle_text != self.last_text:
                print(f"DEBUG: Updating subtitle: {subtitle_text}")
                self.update_subtitle_text(subtitle_text)
                return True
            
            # Clear subtitle if it's expired and we have old text showing
            elif not found_valid_subtitle and self.last_text and time.time() - self.last_update > self.subtitle_duration:
                print("DEBUG: Clearing expired subtitle")
                self.update_subtitle_text("")
                return True
                
        except Exception as e:
            print(f"Error in read_subtitle_file: {e}")
        
        return False
    
    def setup_scene(self, scene_name="Scene"):
        """Setup subtitle display for a scene"""
        print(f"Setting up subtitle display for scene: {scene_name}")
        
        # Create subtitle source
        if not self.create_subtitle_source():
            print("Failed to create subtitle source")
            return False
        
        # Add to scene
        if not self.add_subtitle_to_scene(scene_name):
            print("Failed to add subtitle to scene")
            return False
        
        print("Subtitle setup completed successfully")
        return True

# Global instance
subtitle_display = OBSSubtitleDisplay()

def script_description():
    return "Subtitle Display for OBS Studio\n\nThis script reads subtitle files generated by the real-time translator and displays them as text overlays in OBS."

def script_properties():
    props = obs.obs_properties_create()
    
    obs.obs_properties_add_text(props, "subtitle_file", "Subtitle File", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "scene_name", "Scene Name", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_int(props, "font_size", "Font Size", 24, 72, 1)
    obs.obs_properties_add_int_slider(props, "subtitle_duration", "Subtitle Duration (seconds)", 1, 10, 1)
    obs.obs_properties_add_int(props, "position_y", "Position Y (%)", 50, 90, 5)
    
    obs.obs_properties_add_button(props, "setup_scene", "Setup Scene", setup_scene_clicked)
    obs.obs_properties_add_button(props, "test_subtitle", "Test Subtitle", test_subtitle_clicked)
    
    return props

def script_update(settings):
    subtitle_display.subtitle_file = obs.obs_data_get_string(settings, "subtitle_file")
    subtitle_display.font_size = obs.obs_data_get_int(settings, "font_size")
    
    # Get subtitle duration as integer and convert to float
    duration_int = obs.obs_data_get_int(settings, "subtitle_duration")
    if duration_int > 0:
        subtitle_display.subtitle_duration = float(duration_int)
    else:
        subtitle_display.subtitle_duration = 3.0  # Default to 3 seconds
    
    subtitle_display.position_y = obs.obs_data_get_int(settings, "position_y")
    
    scene_name = obs.obs_data_get_string(settings, "scene_name")
    if scene_name:
        subtitle_display.setup_scene(scene_name)

def script_tick(seconds):
    """Called every frame - check for subtitle updates"""
    subtitle_display.read_subtitle_file()

def setup_scene_clicked(props, prop):
    scene_name = obs.obs_data_get_string(obs.obs_properties_get_settings(props), "scene_name")
    if scene_name:
        subtitle_display.setup_scene(scene_name)
    else:
        subtitle_display.setup_scene("Scene")

def test_subtitle_clicked(props, prop):
    """Test subtitle display with sample text"""
    test_text = "سلام، این یک تست است"
    subtitle_display.update_subtitle_text(test_text)

def script_load(settings):
    """Script loaded - setup initial configuration"""
    print("=== SUBTITLE DISPLAY SCRIPT LOADED ===")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Looking for subtitle files in: {os.path.abspath('.')}")
    
    # Check if subtitle files exist
    if os.path.exists("subtitle.txt"):
        print("✅ subtitle.txt found")
    else:
        print("❌ subtitle.txt NOT found")
    
    if os.path.exists("subtitle.json"):
        print("✅ subtitle.json found")
    else:
        print("❌ subtitle.json NOT found")
    
    # Set default values
    if not obs.obs_data_get_string(settings, "subtitle_file"):
        obs.obs_data_set_string(settings, "subtitle_file", "subtitle.txt")
    if not obs.obs_data_get_string(settings, "scene_name"):
        obs.obs_data_set_string(settings, "scene_name", "Scene")
    
    # Setup scene automatically
    scene_name = obs.obs_data_get_string(settings, "scene_name")
    if scene_name:
        print(f"Setting up scene: {scene_name}")
        subtitle_display.setup_scene(scene_name)
    
    print("=== SCRIPT INITIALIZATION COMPLETE ===")

def script_unload():
    """Script unloaded - cleanup"""
    print("Subtitle Display script unloaded")