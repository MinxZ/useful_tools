
chmod 400 *.pem
ssh -i *.pem ec2-user@

sudo docker ps
sudo docker ps -a
sudo docker container prune

sudo docker image ls -a

sudo docker system prune -a

sudo docker pull ufoym/deepo:keras-py36-cu90
# with share memory mount and jupyter notebook support
sudo docker pull ufoym/deepo:all-jupyter-py36-cu90
sudo nvidia-docker run -it -p 8888:8888 --ipc=host -v ~/data:/data -v ~/config:/config  ufoym/deepo:all-jupyter-py36-cu90 jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token= --notebook-dir='/root'

sudo docker ps -a
sudo docker start zen_keller
sudo docker exec -it zen_keller /bin/bash

sudo docker exec -it quirky_curran /bin/bash
pip install tqdm


# sudo docker exec -it <container name> /bin/bash

apt update -y
apt upgrade -y
apt install -y ncdu htop python3-tk
apt autoremove

# install keras opencv tqdm

git config --global user.email "z670172581@icloud.com"
git config --global user.name "MinxZ"

git clone https://github.com/MinxZ/*********.git
# git clone -b cyou https://github.com/Liaro/similar_search.git


cd Dog-Breed-Identification

git pull
git add *
git commit -m "add something"
git push origin master


docker aws
sudo yum install -y docker
sudo service docker start

# If you have nvidia-docker 1.0 installed: we need to remove it and all existing GPU containers
docker volume ls -q -f driver=nvidia-docker | xargs -r -I{} -n1 docker ps -q -a -f volume={} | xargs -r docker rm -f
sudo yum remove nvidia-docker

# Add the package repositories
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.repo | \
  sudo tee /etc/yum.repos.d/nvidia-docker.repo

# Install nvidia-docker2 and reload the Docker daemon configuration
sudo yum install -y nvidia-docker2
sudo pkill -SIGHUP dockerd

# Test nvidia-smi with the latest official CUDA image
docker run --runtime=nvidia --rm nvidia/cuda nvidia-smi
