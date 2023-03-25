# build name container_name
echo docker build --build-arg NB_UID=`id -u $1` --build-arg USER=$1  --build-arg USE_GPU=1 -f Dockerfile -t assistant/elleanor:1.0 .
docker build --build-arg NB_UID=`id -u $1` --build-arg USER=$1  --build-arg USE_GPU=1 -f Dockerfile -t assistant/elleanor:1.0 .  