bash ray_start.sh
serve deploy ../configs/ray_config.yaml
echo "Ray App Deployed."
sleep 2
tail -f /tmp/ray/session_latest/logs/serve/*