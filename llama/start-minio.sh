#!/bin/bash
echo "Starting Ollama with models from Minio bucket..."

# Flag file to track whether models are initialized
FLAG_FILE="/root/.ollama/.initialized"

# Configure Minio client
echo "Configuring Minio client..."
/usr/local/bin/mc alias set minio "$S3_ENDPOINT_URL" \
  "$S3_STORAGE_ACCESS_KEY_ID" \
  "$S3_STORAGE_SECRET_ACCESS_KEY" --api S3v4

# Set environment variables for Ollama
export OLLAMA_MODELS=/root/.ollama
export OLLAMA_HOST=0.0.0.0:11434

# Start Ollama in background
echo "Starting Ollama server..."
ollama serve & 
SERVER_PID=$!

# Wait for server to be ready
echo "Waiting for Ollama server to start..."
for i in $(seq 1 30); do
  if curl -s http://localhost:11434/api/version > /dev/null; then
    echo "Server is ready."
    break
  fi
  if [ $i -eq 30 ]; then
    echo "Timed out waiting for server."
    exit 1
  fi
  sleep 1
done

# Check if models need to be initialized
if [ ! -f "$FLAG_FILE" ]; then
  echo "First run - initializing models..."
  
  # Try to get models from Minio first
  TEMP_DIR=$(mktemp -d)
  
  # Loop through models
  for MODEL in nomic-embed-text llama3; do
    echo "Processing model: $MODEL"
    
    echo "Trying to copy $MODEL from Minio bucket..."
    if /usr/local/bin/mc cp --recursive "minio/$S3_STORAGE_BUCKET_NAME/$MODEL/" "$TEMP_DIR/$MODEL/" > /dev/null 2>&1; then
      echo "Successfully copied $MODEL from bucket"
      
      # Import the model files
      echo "Importing $MODEL to Ollama..."
      ollama create $MODEL -f $TEMP_DIR/$MODEL/Modelfile 2>/dev/null || echo "Using default model settings"
      ollama import $MODEL $TEMP_DIR/$MODEL 2>/dev/null || ollama pull $MODEL
    else
      echo "Failed to copy $MODEL from bucket, pulling directly..."
      ollama pull $MODEL
    fi
    
    # Clean up temp files
    rm -rf "$TEMP_DIR/$MODEL"
  done
  
  # Clean up temp directory
  rm -rf "$TEMP_DIR"
  
  # Create flag file
  touch "$FLAG_FILE"
  echo "Models initialized."
else
  echo "Models already initialized."
fi

# Show available models
echo "Available models:"
ollama list

# Wait for server process
wait $SERVER_PID
