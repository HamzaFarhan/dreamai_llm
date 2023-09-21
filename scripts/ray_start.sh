bash ray_stop.sh
echo "Starting Ray"
ray start --num-cpus 12 --head --port=6380 --dashboard-host=0.0.0.0 --dashboard-port=8890
echo "Ray Started."
sleep 2
