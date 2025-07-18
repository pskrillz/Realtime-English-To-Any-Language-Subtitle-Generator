import gradio as gr
from farsi_translator import FarsiTranslator

def create_web_interface():
    """Create a web interface for the Farsi translator"""
    translator = FarsiTranslator()
    
    def translate_text(english_text):
        """Translate English text to Farsi"""
        if not english_text.strip():
            return ""
        
        # Load model if not already loaded
        if not translator.model:
            success = translator.load_model()
            if not success:
                return "Error: Failed to load the translation model. Please check your internet connection."
        
        # Perform translation
        farsi_text = translator.translate_text(english_text)
        return farsi_text
    
    def translate_file(file):
        """Translate text from uploaded file"""
        if file is None:
            return "Please upload a text file."
        
        try:
            with open(file.name, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                return "The uploaded file is empty."
            
            return translate_text(content)
        except Exception as e:
            return f"Error reading file: {e}"
    
    # Create the interface
    with gr.Blocks(title="English to Farsi Translator", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 🇺🇸 → 🇮🇷 English to Farsi Translator")
        gr.Markdown("Translate English text to Farsi using the Helsinki-NLP model")
        
        with gr.Tab("Text Translation"):
            with gr.Row():
                with gr.Column():
                    text_input = gr.Textbox(
                        label="English Text",
                        placeholder="Enter English text to translate...",
                        lines=5
                    )
                    translate_btn = gr.Button("Translate", variant="primary")
                
                with gr.Column():
                    text_output = gr.Textbox(
                        label="Farsi Translation",
                        placeholder="Translation will appear here...",
                        lines=5
                    )
            
            translate_btn.click(
                fn=translate_text,
                inputs=text_input,
                outputs=text_output
            )
        
        with gr.Tab("File Translation"):
            with gr.Row():
                with gr.Column():
                    file_input = gr.File(
                        label="Upload Text File",
                        file_types=[".txt"]
                    )
                    file_translate_btn = gr.Button("Translate File", variant="primary")
                
                with gr.Column():
                    file_output = gr.Textbox(
                        label="Farsi Translation",
                        placeholder="Translation will appear here...",
                        lines=10
                    )
            
            file_translate_btn.click(
                fn=translate_file,
                inputs=file_input,
                outputs=file_output
            )
        
        with gr.Tab("Examples"):
            gr.Markdown("### Try these examples:")
            examples = [
                ["Hello, how are you today?"],
                ["I love learning new languages."],
                ["The weather is beautiful today."],
                ["Thank you for your help and support."],
                ["What time is the meeting tomorrow?"],
                ["I would like to order a coffee, please."],
                ["The food at this restaurant is delicious."],
                ["Can you help me find the nearest hospital?"]
            ]
            
            gr.Examples(
                examples=examples,
                inputs=text_input,
                outputs=text_output,
                fn=translate_text,
                cache_examples=True
            )
        
        gr.Markdown("---")
        gr.Markdown("### About")
        gr.Markdown("""
        This translator uses the **Helsinki-NLP/opus-mt-en-iir** model, which is a multilingual model capable of translating from English to several Indo-Iranian languages, including Farsi.
        
        **Features:**
        - High-quality English to Farsi translation
        - Support for both text input and file upload
        - Web-based interface for easy access
        - Example translations to get you started
        
        **Note:** The first time you use this translator, it will download the model (about 300MB), which may take a few minutes depending on your internet connection.
        """)
    
    return interface

if __name__ == "__main__":
    interface = create_web_interface()
    interface.launch(share=True, server_name="0.0.0.0", server_port=7860) 