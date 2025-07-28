from googletrans import Translator as GoogleTranslator

try:
    import gradio as gr
except ImportError:
    gr = None

class Translator:
    """Wrapper around Google Translate for English → target language translation.

    Parameters
    ----------
    target_lang : str, optional
        Two-letter language code used by Google Translate. Defaults to "fa"
        (Persian). Change this to translate into another language.
    """

    def __init__(self, target_lang: str = "fa"):
        self.model_name = "Google Translate"
        self.translator = None
        self.model = None  # kept for backward compatibility
        self.target_lang = target_lang

    def load_model(self):
        """Initialize the Google Translate client."""
        try:
            print("Initializing Google Translate client")
            self.translator = GoogleTranslator()
            self.model = self.translator  # attribute used by other modules
            print("Translator ready")
            return True
        except Exception as e:
            print(f"Error initializing translator: {e}")
            return False

    def translate_text(self, english_text):
        """Translate a single English string to the target language."""
        if not self.model:
            return "Error: Translator not initialized."
        try:
            result = self.translator.translate(english_text, src="en", dest=self.target_lang)
            return result.text
        except Exception as e:
            return f"Translation error: {e}"

    def translate_batch(self, english_texts):
        """Translate a list of English strings to the target language."""
        if not self.model:
            return ["Error: Translator not initialized"] * len(english_texts)
        try:
            results = self.translator.translate(english_texts, src="en", dest=self.target_lang)
            if not isinstance(results, list):
                results = [results]
            return [res.text for res in results]
        except Exception as e:
            return [f"Translation error: {e}"] * len(english_texts)


def create_gradio_interface():
    """Create a Gradio web interface for the translator."""
    if gr is None:
        raise ImportError("gradio is required for the web interface. Install it with: pip install gradio")
    
    translator = Translator()

    def translate_interface(text):
        if not translator.model:
            translator.load_model()
        return translator.translate_text(text)

    interface = gr.Interface(
        fn=translate_interface,
        inputs=gr.Textbox(label="English Text", placeholder="Enter English text to translate..."),
        outputs=gr.Textbox(label="Translation", placeholder="Translation will appear here..."),
        title="English Translator",
        description="Translate English text using Google Translate",
        examples=[
            ["Hello, how are you?"],
            ["I love learning new languages."],
            ["The weather is beautiful today."],
            ["Thank you for your help."],
            ["What time is the meeting?"],
        ],
        theme=gr.themes.Soft(),
    )

    return interface


if __name__ == "__main__":
    translator = Translator()

    print("Loading Translator...")
    if translator.load_model():
        print("Translator ready! Type 'quit' to exit")
        print("-" * 50)

        while True:
            english_text = input("Enter English text to translate: ")
            if english_text.lower() == "quit":
                break

            if english_text.strip():
                translated_text = translator.translate_text(english_text)
                print(f"Translation: {translated_text}")
                print("-" * 50)
    else:
        print("Failed to initialize translator. Please check your internet connection and try again.")