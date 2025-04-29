#!/bin/bash

script_path=$(dirname "$0")

/bin/bash $script_path/../llama/validate.sh
/bin/bash $script_path/../qdrant/validate.sh
/bin/bash $script_path/../flowise/validate.sh
/bin/bash $script_path/../apisix/validate.sh
/bin/bash $script_path/../minio/validate.sh
/bin/bash $script_path/../cnpg/validate.sh
/bin/bash $script_path/../redis/validate.sh
