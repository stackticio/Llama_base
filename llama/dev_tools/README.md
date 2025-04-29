

# Development tools

This guide explains how to set up and use Tilt for developing a React application deployed on Kubernetes.
The idea is to avoid complicated environments like Minikube or Docker-Compose and instead connect and code directly from your local repository into the Kubernetes development environment

## Tilt

### Install
```
MAC
curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash
LINUX
curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash
WIN
iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.ps1'))
```
* IDE extentions:
  * https://marketplace.visualstudio.com/items?itemName=tilt-dev.tiltfile
  * https://github.com/tilt-dev/tiltfile.tmbundle
 

### Define Variables

First, define the variables for the Kubernetes context and the application folder:

```python
kubectl config current-context
gke_stacktic-423213_us-central1-c_cluster-1

k8s_context = 'gke_stacktic-423213_us-central1-c_cluster-1'
app_folder = '/app'

```

Use the specific YAML configuration for deploying the application:
```
k8s_yaml('../../k8s/deploy/base/react/react.yaml')
```

Define Live Update
Define the live update for syncing all code changes. This setup ensures that changes in your local files are reflected in the running container without rebuilding the entire image.
Stacktic template example:
```
docker_build(
    'index.docker.io/project/llama:lamma.v3.1',
    context='../../llama',
    dockerfile='../../llama/Dockerfile',
    live_update=[
        sync('../../llama/src', app_folder + '/src'),
        sync('../../llama/public', app_folder + '/public'),
        sync('../../llama/package.json', app_folder + '/package.json'),
        sync('../../llama/package-lock.json', app_folder + '/package-lock.json'),
        run('npm ci --legacy-peer-deps', trigger=['package.json', 'package-lock.json']),
        run('npm start', trigger=['src/**/*.js', 'src/**/*.jsx', 'public/**/*.html'])
    ]
)
```

## Run
```  
  Tilt up         
Tilt started on http://localhost:10350/
v0.33.17, built 2024-06-12

(space) to open the browser
(s) to stream logs (--stream=true)
(t) to open legacy terminal mode (--legacy=true)
(ctrl-c) to exit
Opening browser: http://localhost:10350/
```
<img width="1722" alt="image" src="https://github.com/user-attachments/assets/5eaec9eb-e26c-4a13-913a-2f52524c3332">


## What Tilt Does
Tilt automates the process of building and deploying your application to Kubernetes, making it easier to develop and debug. Here's a brief overview of what Tilt does in this configuration:

* Build Docker Image: Tilt builds the Docker image for your React application using the specified Dockerfile.
* Deploy to Kubernetes: Tilt uses the specified Kubernetes YAML configuration to deploy the application to your cluster.
* Live Update: Tilt syncs changes from your local files to the running container in real-time. This allows you to see changes immediately without rebuilding the entire image.
* Port Forwarding: Tilt forwards the specified port (3000) from the Kubernetes pod to your local machine, making it easy to access your application in
