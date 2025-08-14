# To restart, you need to make this an executable. chmod +x ./restart.sh
docker-compose down          # Takes down the running containers (allowing refreshing). -v to delete volumes
docker-compose up --build -d # Runs containers, initializing them. -d is detach
sleep 1                      # if it runs instantly it can't tell if it will crash or not
docker ps -a
# docker-compose logs {name of container (api / db)} # Debugging purposes
