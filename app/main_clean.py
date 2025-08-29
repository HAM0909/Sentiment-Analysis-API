from fastapi import FastAPI, HTTPException
from transformers import pipeline
import logging
from pydantic import BaseModel
from fastapi.responses import FileResponse




logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="Sentiment Analysis API",
    description="Sentiment analysis API with DistilBERT",
    version="1.0.0"
)


class SentimentInput(BaseModel):
    text: str


try:
    logger.info("Loading DistilBERT model...")
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        device=-1 
    )
    logger.info("Model loaded successfully!")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    sentiment_pipeline = None 

@app.get("/health")
def health_check():
    """Health endpoint to check API status"""
    if sentiment_pipeline is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    return {
        "status": "ok",
        "model": "distilbert-base-uncased-finetuned-sst-2-english",
        "message": "API is working"
    }

@app.get("/test-model")
def test_model():
    """Quick model test with a predefined sentence"""
    if sentiment_pipeline is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    test_text = "I love FastAPI and Hugging Face!"
    try:
        result = sentiment_pipeline(test_text)
        return {
            "input_text": test_text,
            "prediction": result[0],
            "status": "model_working"
        }
    except Exception as e:
        logger.error(f"Inference error: {e}")
        raise HTTPException(status_code=500, detail=f"Inference error: {e}")

@app.post("/analyse_sentiment")
def analyse_sentiment(input_data: SentimentInput):
    """Sentiment analysis for provided English text."""
    if sentiment_pipeline is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    try:
        result = sentiment_pipeline(input_data.text)
        return {
            "text": input_data.text,
            "prediction": result[0]
        }
    except Exception as e:
        logger.error(f"Inference error: {e}")
        raise HTTPException(status_code=500, detail=f"Inference error: {e}")
    

@app.post("/analyze")
def analyze_sentiment(input_data: SentimentInput):
    """Analyse the sentiment of given text (English)."""
    if sentiment_pipeline is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    try:
        result = sentiment_pipeline(input_data.text)[0]
        return {
            "label": result["label"],
            "score": float(result["score"])
        }
    except Exception as e:
        logger.error(f"Inference error: {e}")
        raise HTTPException(status_code=500, detail=f"Inference error: {e}")


@app.get("/", include_in_schema=False)
def serve_index():
    return FileResponse("index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
