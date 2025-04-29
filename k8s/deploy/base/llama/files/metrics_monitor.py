#!/usr/bin/env python3
"""
Ollama Metrics Monitoring Script for Kubernetes
"""

import time
import requests
import json
from prometheus_client import start_http_server, Gauge, Counter, Histogram

# Prometheus metrics
MODEL_USAGE = Counter('ollama_model_usage_total', 'Number of times each model is used', ['model'])
QUERY_LATENCY = Histogram('ollama_query_latency_seconds', 'Latency of queries to Ollama')
ACTIVE_MODELS = Gauge('ollama_loaded_models', 'Number of currently loaded models')
MRR_SCORE = Gauge('ollama_mrr_score', 'Mean Reciprocal Rank score for retrieval', ['model'])
HIT_RATE = Gauge('ollama_hit_rate', 'Hit rate score for retrieval', ['model'])

# Ollama API endpoint
API_URL = "http://localhost:11434/api"

def get_models():
    """Get list of available models from Ollama"""
    try:
        response = requests.get(f"{API_URL}/tags")
        if response.status_code == 200:
            models = response.json().get('models', [])
            return [model.get('name') for model in models]
        return []
    except Exception as e:
        print(f"Error getting models: {e}")
        return []

def update_metrics():
    """Update Prometheus metrics based on Ollama stats"""
    try:
        # Get available models
        models = get_models()
        ACTIVE_MODELS.set(len(models))
        
        # For demonstration, set some sample metrics
        # In production, you would collect real data
        for model in models:
            MODEL_USAGE.labels(model).inc(1)
            MRR_SCORE.labels(model).set(0.75)  # Example value
            HIT_RATE.labels(model).set(0.85)   # Example value
            
        # Record a sample query latency
        with QUERY_LATENCY.time():
            # Simulate a query to measure latency
            requests.get(f"{API_URL}/version")
            
        print(f"Updated metrics for {len(models)} models")
    except Exception as e:
        print(f"Error updating metrics: {e}")

def main():
    """Main function to start the metrics server"""
    # Start Prometheus metrics server
    start_http_server(8000)
    print("Metrics server started on port 8000")
    
    # Update metrics every 15 seconds
    while True:
        update_metrics()
        time.sleep(15)

if __name__ == "__main__":
    # Give Ollama time to start
    time.sleep(10)
    main()
