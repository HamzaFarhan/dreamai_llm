echo "Stopping Ray"
serve shutdown -y
ray stop
echo "Ray Stopped. Sleeping 10 seconds."
sleep 10