# argo-cd Documentation

**Table of content**

<!-- TOC -->
* [argo-cd documentation](#-cookiecuttercomponentname--documentation)
  * [Component](#component)
    * [Overview](#overview)
    * [Component Key Features](#component-key-features)
    * [Stacktic - Ready to use](#stacktic---ready-to-use)
    * [Prerequisites](#prerequisites)
    * [Dependencies](#dependencies)
  * [Structure Overview](#structure-overview)
  * [Installation and Configuration](#installation-and-configuration)
    * [Kubernetes](#kubernetes)
      * [Deploy](#deploy)
        * [Base Configuration](#base-configuration)
        * [Overlay Configuration](#overlay-configuration)
        * [Advanced](#advanced)
        * [SOPS Plugin](#sops-plugin)
  * [Usage](#usage)
    * [GUI Access](#gui-access)
    * [Image Updater](#image-updater)
  * [Recommendations](#recommendations)
    * [Generality](#generality)
    * [Security](#security)
    * [Best Practices](#best-practices)
  * [Troubleshooting](#troubleshooting)
  * [Resources](#resources)
<!-- TOC -->

## Component

### Overview

[Argo CD](https://argo-cd.readthedocs.io/en/stable/) is a declarative, GitOps continuous delivery tool for Kubernetes. It automates the deployment of applications to multiple Kubernetes clusters by syncing them with specified Git repositories. Argo CD visualizes and manages the state of application deployments, ensuring that the deployed state matches the configurations defined in the repository.

[Argo CD Image Updater](https://argocd-image-updater.readthedocs.io/en/stable/) is an extension for Argo CD that automates the update of container images within Kubernetes applications managed by Argo CD. It monitors configured container image registries for new or updated images and automatically updates the Git repositories with these new image versions, triggering Argo CD to deploy the updates.

### Component Key Features

- **Scriptable Test Scenarios**: Enables the definition of complex user behaviors and performance tests in JavaScript, offering extensive control over testing parameters and execution.
- **Automated Performance Regression Detection**: Integrates with CI/CD pipelines to automatically detect and alert on performance regressions, ensuring high performance standards are maintained throughout the development lifecycle.
- **Scalable Load Generation**: Facilitates the simulation of millions of concurrent users with minimal resource usage, allowing for scalable and efficient load testing across various environments.
- **Real-time Feedback and Metrics**: Provides detailed performance metrics and real-time feedback on the application's behavior under load, enabling quick identification and resolution of performance bottlenecks.
- **Distributed Execution**: Supports running tests in a distributed manner across multiple machines or cloud environments, enabling large-scale performance testing without significant infrastructure.
- **Custom Metrics and Checks**: Allows the creation of custom metrics and checks within test scripts for detailed monitoring and validation of application performance and functionality.
- **Extensible and Integrable**: Offers a rich set of APIs and integrations with popular tools and services, enhancing testing capabilities and fitting seamlessly into existing development workflows.

### Stacktic - Ready to use

t0d0

### Prerequisites

- Kubernetes 1.23+
- PV provisioner support in the underlying infrastructure
- ReadWriteMany volumes for deployment scaling

[Source](https://github.com/bitnami/charts/tree/main/bitnami/argo-cd/#prerequisites)

### Dependencies


## Structure Overview

> Global structure is described [here](../../README.md#folder-structure).

The component structure is the following:

```
├── argo-cd/              
|   ├── helm/                                       
|   |   ├── argo-cd-helm-values.yaml                # Helm configuration for Argo CD
|   |   ├── argocd-image-updater-helm-values.yaml   # Helm configuration for Argo CD Image Updater
|   |   └── generate-yaml.sh                        # Script to generate the Kubernetes files of the Helm Charts
```

>You can configure your deployment by following the official Chart documentation:
>* [Argo CD](https://github.com/argoproj/argo-helm/tree/main/charts/argo-cd)
>* [Argo CD Image Updater](https://github.com/argoproj/argo-helm/tree/main/charts/argocd-image-updater)

##  Installation and Configuration

### Kubernetes

#### Deploy

##### Base Configuration

```
├── k8s/deploy/base/argo-cd
|   ├── config/
|   └── secret/                      
|   |   ├── git.env                  # Git repository configuration
|   |   ├── registry.json            # Container registry configuration
|   |   └── sops-key.txt             # SOPS Key required by Argo to decrypt secrets
|   ├── apps.yaml                    # Applications configuration to be deployed by Argo CD
|   ├── argo-cd.yaml                 # Generated template from the Chart to deploy Argo CD
|   ├── argocd-image-updater.yaml    # Generated template from the Chart to deploy Argo CD Image Updater
|   ├── kustomization.yaml           # Kustomize configuration
|   ├── namespace.yaml               # Kubernetes manifest for the Argo CD namespace
|   └── network-policy.yaml          # Kubernetes manifest for the Network Policies
```

##### Overlay Configuration

Initialized with the base.

##### Advanced

## Usage

### GUI Access

```bash
# GUI Access - At localhost:8081
kubectl -n argocd port-forward svc/argo-cd-argocd-server 8080:443


argocd login localhost:8080 \
  --username admin \
  --password default_password \
  --insecure

```

> ℹ️ The username is `admin` and the password is the one you defined in Stacktic.

### Image Updater

- The Image Updater monitors your image registry for new image pushes.
- Upon detecting a new image version, it automatically updates the `image:version` tag in the relevant Kubernetes
  manifests within your Git repository.
- Argo CD then synchronizes these changes, deploying the latest image version to your cluster.

## Recommendations

### Generality

> ⚠️ Once this chart is deployed, it is not possible to change the application's access credentials, such as usernames
> or passwords, using Helm. To change these application credentials after deployment, delete any persistent volumes (PVs)
> used by the chart and re-deploy it, or use the application's built-in administrative tools if available.

### Security

### Best Practices

## Troubleshooting

## Resources

- [Declarative Setup](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/)
- [Config Management Plugins](https://argo-cd.readthedocs.io/en/stable/operator-manual/config-management-plugins/)
- [Using Argo CDs new Config Management Plugins to Build Kustomize, Helm, and More](https://codefresh.io/blog/using-argo-cds-new-config-management-plugins-to-build-kustomize-helm-and-more/)

