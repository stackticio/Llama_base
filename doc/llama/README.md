sa# Llama Model Deployment Guide

Deploying and managing Llama models can be challenging due to their large size and version compatibility. Stacktic simplifies this by streamlining the build process, enhancing deployment security, and enabling easy model and version switching.

## How it Works

Stacktic simplifies deployment through:
- **Model Storage**: Models stored in MinIO buckets.
- **Automated Updates**: MinIO jobs handle model downloads.
- **Configurations**: Utilizes PVCs, configMaps, and secrets.
- **Environment Management**: Automatically adjusts ENV variables based on GPU mode.

## Setup Instructions

### Prerequisites
- Ensure you have an approved Hugging Face token.
- For Dev, Avoid enabling unnecessary security toggles in development environments.
- Make sure your nodes can handle the jobs / build (if not buidling locally)

### Step-by-Step Deployment

1. **Connect Llama to MinIO Bucket**
   - in the background stacktic will Update the `configMap` ENV with MinIO bucket details and Create a Kubernetes job for model downloading from Hugging Face.
   - enter the models  if there are few it should looks like 
nomic-embed-text
meta-llama/Meta-Llama-3-8B-Instruct

<img width="499" alt="image" src="https://github.com/user-attachments/assets/8a40805c-c716-4e79-9958-d03b2c9aecf8" />


   ```bash
   kubectl apply -f k8s/build/base/llama/models-job.yaml
   ```

2. **Execute Model Download Job**
   - Ensure the job completes successfully before proceeding.
```
`/work/meta-llama_Meta-Llama-3-8B-Instruct/tokenizer.json` -> `minio/models/meta-llama/Meta-Llama-3-8B-Instruct/meta-llama_Meta-Llama-3-8B-Instruct/tokenizer.json`
`/work/meta-llama_Meta-Llama-3-8B-Instruct/tokenizer_config.json` -> `minio/models/meta-llama/Meta-Llama-3-8B-Instruct/meta-llama_Meta-Llama-3-8B-Instruct/tokenizer_config.json`
┌───────────┬─────────────┬──────────┬──────────────┐
│ Total     │ Transferred │ Duration │ Speed        │
│ 29.93 GiB │ 29.93 GiB   │ 03m41s   │ 138.15 MiB/s │
└───────────┴─────────────┴──────────┴──────────────┘
Upload successful!
Completed processing meta-llama/Meta-Llama-3-8B-Instruct
All models processed successfully
assafsauer@Assafs-MacBook-Pro env_dev_2 % 
```
2. **Build docker locally**
- Run local Docker (no bucket, download and build dirctly from meta)

```
docker buildx build --platform linux/amd64,linux/arm64 -t llama:lamma.v3.1 -f llama/Dockerfile llama/ --push
```

3. **Run the Build Process with kaniko within k8s**
   Execute either of the following commands based on your setup:

   ```bash
   kubectl apply -k k8s/build/over/dev
   ```
   or
   ```bash
   kubectl apply -f k8s/build/base/llamma/kaniko.yaml
   ```

### Resource Requirements

- **Large Models** (e.g., `meta-llama/Llama-4-Maverick-17B-128E-Instruct`): Require ample node storage (100GB+).
- **Standard Models** (e.g., `meta-llama/Llama-3-8B-Instruct`): Pre-configured with ephemeral storage; adjust as needed.

## Post-Deployment

- Connect your running Llama instance to RAG using a simple Kubernetes Service (SVC).
- Deploy multiple models by using distinct namespaces for each purpose (e.g., chat, embeddings).

---

For customization and advanced configurations, adjust the Kubernetes job and resources according to your needs.
### Monitoring

```
curl http://localhost:8000/metrics
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 175.0
python_gc_objects_collected_total{generation="1"} 180.0
........
```

- **Model usage tracking:**
- ollama_model_usage_total{model="llama3:latest"} 9.0
- ollama_model_usage_total{model="nomic-embed-text:latest"} 9.0

- **Latency measurements:**
- ollama_query_latency_seconds_count 9.0
- ollama_query_latency_seconds_sum 0.01676193800085457

- **Loaded models count:**
- ollama_loaded_models 2.0

- **MRR score metrics:**
- ollama_mrr_score{model="llama3:latest"} 0.75
- ollama_mrr_score{model="nomic-embed-text:latest"} 0.75

- **Hit rate metrics:**
- ollama_hit_rate{model="llama3:latest"} 0.85
- ollama_hit_rate{model="nomic-embed-text:latest"} 0.85

