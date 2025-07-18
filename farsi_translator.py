import torch
from transformers import MarianMTModel, MarianTokenizer
import gradio as gr

class FarsiTranslator:
    def __init__(self):
        self.model_name = "Helsinki-NLP/opus-mt-en-iir"
        self.tokenizer = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def load_model(self):
        """Load the translation model and tokenizer"""
        try:
            print(f"Loading model: {self.model_name}")
            self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
            self.model = MarianMTModel.from_pretrained(self.model_name)
            self.model.to(self.device)
            print(f"Model loaded successfully on {self.device}")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def translate_text(self, english_text):
        """Translate English text to Farsi"""
        if not self.model or not self.tokenizer:
            return "Error: Model not loaded. Please wait for the model to load."
        
        try:
            # Add language token and tokenize
            prefixed_text = f">>pes<< {english_text}"
            inputs = self.tokenizer(prefixed_text, return_tensors="pt", padding=True, truncation=True, max_length=512)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate translation
            with torch.no_grad():
                outputs = self.model.generate(**inputs, max_length=512, num_beams=5, early_stopping=True)
            
            # Decode the output
            farsi_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return farsi_text
            
        except Exception as e:
            return f"Translation error: {e}"
    
    def translate_batch(self, english_texts):
        """Translate multiple English texts to Farsi"""
        if not self.model or not self.tokenizer:
            return ["Error: Model not loaded"] * len(english_texts)
        
        try:
            # Tokenize the input texts
            # Add language token and tokenize
            prefixed_texts = [f">>pes<< {text}" for text in english_texts]
            inputs = self.tokenizer(prefixed_texts, return_tensors="pt", padding=True, truncation=True, max_length=512)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate translations
            with torch.no_grad():
                outputs = self.model.generate(**inputs, max_length=512, num_beams=5, early_stopping=True)
            
            # Decode the outputs
            farsi_texts = [self.tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
            return farsi_texts
            
        except Exception as e:
            return [f"Translation error: {e}"] * len(english_texts)

def create_gradio_interface():
    """Create a Gradio web interface for the translator"""
    translator = FarsiTranslator()
    
    def translate_interface(text):
        if not translator.model:
            translator.load_model()
        return translator.translate_text(text)
    
    # Create the interface
    interface = gr.Interface(
        fn=translate_interface,
        inputs=gr.Textbox(label="English Text", placeholder="Enter English text to translate..."),
        outputs=gr.Textbox(label="Farsi Translation", placeholder="Translation will appear here..."),
        title="English to Farsi Translator",
        description="Translate English text to Farsi using the Helsinki-NLP model",
        examples=[
            ["Hello, how are you?"],
            ["I love learning new languages."],
            ["The weather is beautiful today."],
            ["Thank you for your help."],
            ["What time is the meeting?"]
        ],
        theme=gr.themes.Soft()
    )
    
    return interface

if __name__ == "__main__":
    # Simple command-line interface
    translator = FarsiTranslator()
    
    print("Loading Farsi Translator...")
    if translator.load_model():
        print("Model loaded successfully!")
        print("Type 'quit' to exit")
        print("-" * 50)
        
        while True:
            english_text = input("Enter English text to translate: ")
            if english_text.lower() == 'quit':
                break
            
            if english_text.strip():
                farsi_text = translator.translate_text(english_text)
                print(f"Farsi: {farsi_text}")
                print("-" * 50)
    else:
        print("Failed to load model. Please check your internet connection and try again.") 