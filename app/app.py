import gradio as gr
from transformers import pipeline
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize sentiment pipeline
sentiment_pipeline = None

def load_model():
    """Load the sentiment analysis model"""
    global sentiment_pipeline
    try:
        logger.info("Loading DistilBERT model...")
        sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=-1  # Use CPU
        )
        logger.info("Model loaded successfully!")
        return True
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        sentiment_pipeline = None
        return False

def analyze_sentiment(text):
    """Analyze sentiment of the input text"""
    if not text.strip():
        return "⚠️ Please enter some text to analyze"
    
    if sentiment_pipeline is None:
        return "❌ Model not loaded"
    
    try:
        result = sentiment_pipeline(text)[0]
        label = result['label']
        score = result['score']
        
        # Add emoji based on sentiment
        emoji = "😊" if label == "POSITIVE" else "😞"
        confidence = f"{score:.2%}"
        
        return f"{emoji} **{label}** (Confidence: {confidence})"
    
    except Exception as e:
        logger.error(f"Error during inference: {e}")
        return f"❌ Error: {str(e)}"

# Load model on startup
model_loaded = load_model()

# Create the Gradio interface
with gr.Blocks(title="Sentiment Analysis with DistilBERT", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🎭 Sentiment Analysis Demo
        
        Analyze the sentiment of any text using **DistilBERT**, a state-of-the-art transformer model.
        
        Simply enter your text below and click **Analyze** to get the sentiment prediction!
        """
    )
    
    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(
                lines=3,
                placeholder="Enter your text here... (e.g., 'I love this amazing project!')",
                label="Text to Analyze",
                info="Enter any text in English"
            )
            analyze_btn = gr.Button("🔍 Analyze Sentiment", variant="primary", size="lg")
        
        with gr.Column():
            output = gr.Markdown(label="Analysis Result")
    
    # Examples for users to try
    gr.Examples(
        examples=[
            ["I absolutely love this new technology!"],
            ["This movie was terrible and boring."],
            ["The weather is okay today."],
            ["I'm so excited about this project!"],
            ["This service was disappointing."],
            ["The book was interesting and well-written."]
        ],
        inputs=text_input,
        label="Try these examples:"
    )
    
    # Connect the button to the function
    analyze_btn.click(
        fn=analyze_sentiment,
        inputs=text_input,
        outputs=output
    )
    
    # Also trigger on Enter key
    text_input.submit(
        fn=analyze_sentiment,
        inputs=text_input,
        outputs=output
    )
    
    gr.Markdown(
        """
        ---
        **Model**: DistilBERT fine-tuned on SST-2 dataset  
        **Framework**: Hugging Face Transformers + Gradio  
        **Deployment**: Docker on Hugging Face Spaces
        """
    )

# Launch the app
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",  # Important for Docker
        server_port=7860,       # Hugging Face Spaces port
        share=False
    )