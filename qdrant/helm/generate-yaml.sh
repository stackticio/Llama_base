#!/bin/sh

script_path="$(dirname "$0")"

if [ -z "$1" ]; then
    output_path="$script_path/../../k8s/deploy/base/qdrant"
else
    output_path="$script_path/$1"
fi

helm repo add qdrant https://qdrant.github.io/qdrant-helm
helm repo update


helm template "qdrant" qdrant/qdrant  \
--namespace "qdrant" \
--version "1.13.6" \
-f $script_path/helm-values.yaml \
> "$output_path/qdrant.yaml" || exit 1


