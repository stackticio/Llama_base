# Flowise on Stacktic

## Overview

Flowise on Stacktic is an end-to-end solution for building and deploying AI workflows powered by Large Language Models (LLMs). This integration combines Flowise's intuitive no-code interface for AI pipeline development with Stacktic's robust Kubernetes-based infrastructure management.

## Architecture

Stacktic manages the deployment and versioning of all components required by Flowise:

- **LLaMa Models**: Served via Ollama with Minio integration for model storage
- **Vector Database**: Qdrant for efficient similarity search and retrieval
- **Redis**: For caching and message queue capabilities
- **S3-Compatible Storage**: For document management and persistence

 <img width="690" alt="image" src="https://github.com/user-attachments/assets/b03489c4-19cf-4fb3-bbd0-ca4cf3ec3ce4" />

## Key Features

- **Visual AI Workflow Builder**: Create complex LLM-powered applications without coding
- **Automated Infrastructure**: Zero-config deployment of all required components
- **Integrated RAG (Retrieval Augmented Generation)**: Out-of-the-box solution for document processing and contextual AI responses
- **Scalable & Cloud-Ready**: Kubernetes-native design for production deployments
- **Version Control**: Track and manage changes to workflows and infrastructure

## Use Cases

- **Enterprise Chatbots**: Deploy context-aware assistants with access to company knowledge
- **Document Analysis**: Extract insights from large document collections
- **Code Analysis**: Understand and analyze code within your stack
- **Data Processing Pipelines**: Build workflows for data ingestion, transformation, and analysis
- **Automated Content Generation**: Create content with guidance from your data

## Getting Started

Flowise deployment is fully managed by Stacktic.  including the build, deploy , and version.

### Accessing Flowise

Once Stacktic has deployed the environment, access the Flowise UI through the URL provided in your Stacktic dashboard.

## Configuration

Build the flowise image:
```
kubectl apply -k  k8s/build/overlay/dev
```
if you wnat to rebuild only flowise simply run:
```
kubectl apply -f k8s/build/base/flowise/kanikoyaml
```

### Environment Variables

see: k8s/deploy/base/secret/cloud.env

```
Core Configuration
PORT=3000                      # Application port
FLOWISE_USERNAME=admin         # UI login username
FLOWISE_PASSWORD=******        # UI login password

Storage Paths
All data stored in non-root paths for better security:
DATABASE_PATH=/home/node/.flowise
APIKEY_PATH=/home/node/.flowise
LOG_PATH=/home/node/.flowise/logs

External Integrations
S3 Storage
STORAGE_TYPE=s3
S3_STORAGE_BUCKET_NAME=your-bucket
S3_ENDPOINT_URL=http://minio.namespace.svc.cluster.local:9000

PostgreSQL Database
DATABASE_TYPE=postgres
DATABASE_HOST=postgres.namespace.svc.cluster.local
DATABASE_PORT=5432
DATABASE_NAME=flowise

Redis Cache
REDIS_HOST=redis-master.namespace.svc.cluster.local
REDIS_PORT=6379
```

### Examples: Adding Custom LLaMa Models

Custom LLaMa models are automatically managed by Stacktic's infrastructure. The models are stored in MinIO buckets and are automatically detected and loaded by the Ollama container as configured in your environment.

