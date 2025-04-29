# CloudNativePG (CNPG) Template

## Overview

This template provides a standardized way to deploy PostgreSQL databases in Kubernetes using the CloudNativePG operator. It generates all the necessary Kubernetes manifests based on the parameters provided through cookiecutter.

## Features

- **PostgreSQL Cluster Deployment**: Creates a CNPG Cluster with configurable resources, storage, and image version
- **Database Creation**: Generates Database custom resources for each database specified
- **Role Management**: Creates appropriate PostgreSQL roles with configurable permissions
- **Backup Integration**: Optional S3-compatible backup configuration with MinIO
- **Monitoring**: Optional Prometheus integration for PostgreSQL metrics
- **Jobs**: Grant and cleanup jobs for database permissions, backups , point-in-time-recovery ....

## Structure

- `k8s/deploy/base/`: Main Kubernetes manifests
  - `cluster.yaml`: CNPG Cluster definition
  - `database.yaml`: Database custom resources
  - `roles.yaml`: PostgreSQL role definitions
  - `backup/`: Backup and recovery configurations
  - `jobs/`: Database permission and cleanup jobs (grant: k8s/deploy/base/cnpg/jobs/grant-job.yaml)
  - `secret/`: Secret configurations for credentials

## Usage

1. Create new database or add new cluster replication of the existing one:

  <img width="484" alt="image" src="https://github.com/user-attachments/assets/30813662-d113-44ad-9c7f-219ebdc41626" />


2. : choose the backup ID and the PSQL Version image (if you want to upgrade)
   
   <img width="452" alt="image" src="https://github.com/user-attachments/assets/aea317a4-892a-4dc7-b840-ad59cb75c3a5" />


4. create the point-in-time-recovery cluster 

kubectl apply -f k8s/deploy/base/cnpg/backup/point-in-time-recovery.yaml 

## Debug 

```
## Validate backup ID ###
 mc ls myminio/web/cluster-cnpg/base --insecure
 mc ls myminio/web/cluster-cnpg/base/20250408T083611
 mc ls myminio/web/cluster-cnpg/base/20250408T083611 --insecure
[2025-04-08 10:36:18 CEST] 1.3KiB STANDARD backup.info
[2025-04-08 10:36:18 CEST]  46MiB STANDARD data.tar
 
## connect to db ###
kubectl run psql-doclib \
  --image=ghcr.io/cloudnative-pg/postgresql:15.3 \
  -n cnpg \
  -it --rm --restart=Never \
  --env="PGPASSWORD=default_pass1" \
  -- psql -h cluster-cnpg-rw.cnpg.svc.cluster.local -p 5432 -U doclib -d doclib
```

### Backup

Back up templates
```
k8s/deploy/base/cnpg/backup
├── cluster-restore.yaml
├── manual-backup.yaml
├── point-in-time-recovery.yaml
└── schedule-backup.yaml  
```
Individual db backup and restore via minio

<img width="399" alt="image" src="https://github.com/user-attachments/assets/832758f2-4da3-49b3-b4ac-9a336eec4135" />

```
k8s/deploy/base/minio/jobs/
├── backup-cnpg.yaml
├── backup-mongodb.yaml
├── backup-reldb.yaml
├── restore-cnpg.yaml
├── restore-mongodb.yaml
└── restore-reldb.yaml
```

### Commands
```
kubectl get database -A
NAMESPACE   NAME     AGE   CLUSTER        PG NAME   APPLIED   MESSAGE
cnpg        db3      23h   cluster-cnpg   db3       true      
cnpg        docai    23h   cluster-cnpg   docai     true      
cnpg        doclib   23h   cluster-cnpg   doclib    true      
```

