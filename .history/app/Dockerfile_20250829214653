# 1. Base image
FROM python:3.10-slim

# 2. Working directory in container
WORKDIR /app

# 3. Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy application code
COPY . .

# 5. HuggingFace environment variables (local cache in container)
ENV HF_HOME=/app/.cache/huggingface
ENV TRANSFORMERS_CACHE=/app/.cache/huggingface/transformers

# 6. Prepare cache and set permissions
RUN mkdir -p /app/.cache/huggingface && chmod -R 777 /app/.cache/huggingface

# 7. Expose FastAPI port
EXPOSE 8000

# 8. Startup command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]