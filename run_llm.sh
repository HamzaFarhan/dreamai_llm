#!/bin/bash

. parse_yaml.sh
create_variables ray_config.yaml

llm_fn=${applications__deployments__user_config_llm_config_llm_fn:="null"}
model_name=${applications__deployments__user_config_llm_config_model_name:="null"}
url=${applications__deployments__user_config_llm_config_model_url:="http://localhost:8000/v1"}
# token=${applications__deployments__user_config_llm_config_model_token:="null"}

# Extract the protocol, host, and port
protocol=$(echo "$url" | awk -F '://' '{print $1}')
host_port=$(echo "$url" | awk -F '://' '{print $2}' | cut -d '/' -f 1)
host=$(echo "$host_port" | cut -d ':' -f 1)
port=$(echo "$host_port" | cut -d ':' -f 2)

# echo all the variables
echo "llm_fn: $llm_fn"
echo "model_name: $model_name"
echo "url: $url"
echo "protocol: $protocol"
echo "host_port: $host_port"
echo "host: $host"
echo "port: $port"


if [ "$llm_fn" != "vllm" ]; then
    echo "Invalid llm_fn. It must be vllm"
    echo "llm_fn: $llm_fn"
elif [ "$model_name" == "null" ]; then
    echo "Invalid model name. It must be a valid model name"
    echo "Model Name: $model_name"
else
    command="python -m vllm.entrypoints.openai.api_server --model $model_name --host $url --port $port --allow-credentials True"
    $command
fi