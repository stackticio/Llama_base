#!/bin/sh

set -e  # optional: exit immediately on errors for easier debugging
set -x  # optional: print commands for debugging

script_path=$(dirname "$0")

if [ -z "$1" ]; then
  output_path="$script_path/../../k8s/deploy/base/cnpg"
else
  output_path="$script_path/$1"
fi

# If you want to be sure your Helm repo is registered:
helm repo add cloudnative-pg https://cloudnative-pg.io/charts/

helm template "cnpg" "cloudnative-pg/cloudnative-pg" \
  --namespace "cnpg" \
  --version "0.23.2" \
  -f "$script_path/helm-values.yaml" \
  > "$output_path/cnpg.yaml"
