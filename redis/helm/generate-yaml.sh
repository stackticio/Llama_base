#!/bin/sh

script_path="$(dirname "$0")"

if [ -z "$1" ]; then
    output_path="$script_path/../../k8s/deploy/base/redis"
else
    output_path="$script_path/$1"
fi



helm template "redis" oci://registry-1.docker.io/bitnamicharts/redis  \
--namespace "redis" \
--version "19.5.5" \
-f $script_path/helm-values.yaml \
> "$output_path/redis.yaml" || exit 1


