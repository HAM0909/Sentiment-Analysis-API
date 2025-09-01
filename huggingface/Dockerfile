# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Set environment variables for Hugging Face
ENV HF_HOME=/app/.cache/huggingface
ENV TRANSFORMERS_CACHE=/app/.cache/huggingface/transformers

# Create cache directory with proper permissions
RUN mkdir -p /app/.cache/huggingface && chmod -R 777 /app/.cache/huggingface

# Expose Gradio's default port
EXPOSE 7860

# Run the application
CMD ["python", "app.py"]