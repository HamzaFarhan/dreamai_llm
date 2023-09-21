. parse_yaml.sh
create_variables ray_config.yaml

model_name=$applications__deployments__user_config_model_name
url=$applications__deployments__user_config_model_url

# Extract the protocol, host, and port
protocol=$(echo "$url" | awk -F '://' '{print $1}')
host_port=$(echo "$url" | awk -F '://' '{print $2}' | cut -d '/' -f 1)
host=$(echo "$host_port" | cut -d ':' -f 1)
port=$(echo "$host_port" | cut -d ':' -f 2)

python -m vllm.entrypoints.openai.api_server --model $model_name --host $host --port $port