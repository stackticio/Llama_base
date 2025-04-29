###############################################################################
# Dockerfile — Llama models on Ollama for K8s with PVC - Secure Non-Root Configuration
###############################################################################

FROM ollama/ollama:0.3.5

USER root

RUN apt-get update && \
    apt-get install -y curl jq sudo python3 python3-pip && \
    curl -Lo /usr/local/bin/mc https://dl.min.io/client/mc/release/linux-amd64/mc && \
    chmod +x /usr/local/bin/mc && \
    pip3 install requests prometheus-client && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user with correct UID/GID
RUN groupadd -g 1000 ollama && \
    useradd -u 1000 -g ollama -m -s /bin/bash ollama

# Create the required directories that the application needs
RUN mkdir -p /.ollama /.mc && \
    chown -R ollama:ollama /.ollama /.mc && \
    chmod -R 755 /.ollama /.mc && \
    mkdir -p /home/ollama/.ollama /home/ollama/.mc && \
    chown -R ollama:ollama /home/ollama && \
    chmod -R 755 /home/ollama/.ollama /home/ollama/.mc

# Set environment variables
ENV OLLAMA_HOST=0.0.0.0:11434
ENV OLLAMA_MODELS=/.ollama
ENV HOME=/home/ollama

# Create startup script that pulls models from Minio
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "Starting Ollama with models from Minio bucket..."\n\
\n\
# Ensure directories are accessible\n\
mkdir -p /.ollama /.mc\n\
\n\
# Flag file to track whether models are initialized\n\
FLAG_FILE="/.ollama/.initialized"\n\
\n\
# Configure Minio client\n\
echo "Configuring Minio client..."\n\
mc config host add minio "$S3_ENDPOINT_URL" \\\n\
  "$S3_STORAGE_ACCESS_KEY_ID" \\\n\
  "$S3_STORAGE_SECRET_ACCESS_KEY" --api S3v4 || true\n\
echo "Added minio successfully."\n\
\n\
# Start Ollama server in background\n\
echo "Starting Ollama server..."\n\
ollama serve & \n\
SERVER_PID=$!\n\
\n\
# Wait for server to be ready\n\
echo "Waiting for Ollama server to start..."\n\
for i in $(seq 1 60); do\n\
  if curl -s http://localhost:11434/api/version > /dev/null; then\n\
    echo "Server is ready."\n\
    break\n\
  fi\n\
  if [ $i -eq 60 ]; then\n\
    echo "Timed out waiting for server."\n\
    exit 1\n\
  fi\n\
  echo "Waiting for server to start... attempt $i"\n\
  sleep 1\n\
done\n\
\n\
# Check if models need to be initialized\n\
if [ ! -f "$FLAG_FILE" ]; then\n\
  echo "First run - loading models..."\n\
  \n\
  # Create temporary directory for model files\n\
  TEMP_DIR=$(mktemp -d)\n\
  chmod 777 "$TEMP_DIR"\n\
  \n\
\n\
  MODEL="nomic-embed-text"\n\
  echo "Processing model: $MODEL"\n\
  \n\
  echo "Trying to copy $MODEL from Minio bucket..."\n\
  if mc cp --recursive "minio/$S3_STORAGE_BUCKET_NAME/$MODEL/" "$TEMP_DIR/$MODEL/" > /dev/null 2>&1; then\n\
    echo "Successfully copied $MODEL from bucket"\n\
    chmod -R 755 "$TEMP_DIR/$MODEL"\n\
    \n\
    # Import the model to Ollama\n\
    echo "Importing $MODEL to Ollama..."\n\
    ollama create $MODEL -f "$TEMP_DIR/$MODEL/Modelfile" 2>/dev/null || echo "Using default model settings"\n\
    ollama import $MODEL "$TEMP_DIR/$MODEL" 2>/dev/null || ollama pull $MODEL\n\
  else\n\
    echo "Failed to copy $MODEL from bucket, pulling directly..."\n\
    ollama pull $MODEL\n\
  fi\n\
  \n\
  # Clean up\n\
  rm -rf "$TEMP_DIR/$MODEL"\n\
\n\
  MODEL="llama3:8b"\n\
  echo "Processing model: $MODEL"\n\
  \n\
  echo "Trying to copy $MODEL from Minio bucket..."\n\
  if mc cp --recursive "minio/$S3_STORAGE_BUCKET_NAME/$MODEL/" "$TEMP_DIR/$MODEL/" > /dev/null 2>&1; then\n\
    echo "Successfully copied $MODEL from bucket"\n\
    chmod -R 755 "$TEMP_DIR/$MODEL"\n\
    \n\
    # Import the model to Ollama\n\
    echo "Importing $MODEL to Ollama..."\n\
    ollama create $MODEL -f "$TEMP_DIR/$MODEL/Modelfile" 2>/dev/null || echo "Using default model settings"\n\
    ollama import $MODEL "$TEMP_DIR/$MODEL" 2>/dev/null || ollama pull $MODEL\n\
  else\n\
    echo "Failed to copy $MODEL from bucket, pulling directly..."\n\
    ollama pull $MODEL\n\
  fi\n\
  \n\
  # Clean up\n\
  rm -rf "$TEMP_DIR/$MODEL"\n\
\n\
  \n\
  # Clean up temp directory\n\
  rm -rf "$TEMP_DIR"\n\
  \n\
  # Create flag file\n\
  touch "$FLAG_FILE"\n\
  echo "Models initialized."\n\
else\n\
  echo "Models already initialized."\n\
fi\n\
\n\
# Show available models\n\
echo "Available models:"\n\
ollama list\n\
\n\
# Wait for server process\n\
wait $SERVER_PID\n\
' > /usr/local/bin/start.sh && \
    chmod +x /usr/local/bin/start.sh && \
    chown ollama:ollama /usr/local/bin/start.sh

# Switch to non-root user
USER ollama
WORKDIR /home/ollama
EXPOSE 11434
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s CMD curl -sf http://localhost:11434/api/tags || exit 1
ENTRYPOINT ["/usr/local/bin/start.sh"]
