#!/bin/sh

script_path=$(dirname "$0")

if [ -z "$1" ]; then
  output_path=$script_path/../../k8s/deploy/base/argo-cd
else
  output_path=$script_path/$1
fi


helm template argo-cd argo/argo-cd \
  --namespace argocd \
  --version 7.1.0 \
  --include-crds \
  -f $script_path/argo-cd-helm-values.yaml \
  > $output_path/argo-cd.yaml

helm template argo-cd argo/argocd-image-updater \
  --namespace argocd \
  --version 0.10.1 \
  --include-crds \
  -f $script_path/argocd-image-updater-helm-values.yaml \
  > $output_path/argocd-image-updater.yaml
