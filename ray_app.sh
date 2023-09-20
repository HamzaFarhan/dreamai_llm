serve shutdown -y
ray stop
sleep 10
ray start --num-cpus 12 --head --port=6380 --dashboard-host=0.0.0.0 --dashboard-port=8890
sleep 2
serve run deploy:deployment_handle --host 0.0.0.0 --port=8889  >> ray_logs.log 2>&1 &
tail -f ray_logs.log