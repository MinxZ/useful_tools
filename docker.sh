apt update -y
apt upgrade -y
apt install -y ncdu htop python3-tk
apt autoremove
# install keras opencv tqdm

# github setup
git config --global user.email "z670172581@icloud.com"
git config --global user.name "MinxZ"

git config --global credential.helper 'cache --timeout 72000'
git config credential.helper store
git push https://github.com/Liaro/similar_search.git

git clone https://github.com/MinxZ/*********.git
git clone -b cyou https://github.com/Liaro/similar_search.git


# docker setup
sudo docker ps
sudo docker ps -a
sudo docker system prune -a

# with share memory mount and jupyter notebook support
sudo docker pull ufoym/deepo:all-jupyter-py36-cu90
sudo nvidia-docker run -it -p 8888:8888 --ipc=host -v ~/data:/data -v ~/config:/config  ufoym/deepo:all-jupyter-py36-cu90 jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token= --notebook-dir='/root'

# for cpu
sudo docker pull ufoym/deepo:all-py36-jupyter-cpu
sudo docker run -it -p 8888:8888 --ipc=host -v ~/data:/data  ufoym/deepo:all-py36-jupyter-cpu jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token= --notebook-dir='/root'


sudo docker ps -a

# ubuntu
sudo docker start zen_keller
sudo docker exec -it zen_keller /bin/bash

# mac
sudo docker start practical_darwin
sudo docker exec -it practical_darwin /bin/bash

pip install tqdm


# aws
chmod 400 *.pem
ssh -i *.pem ec2-user@

# docker aws
# install s3fs
sudo yum install automake fuse fuse-devel gcc-c++ git libcurl-devel libxml2-devel make openssl-devel

git clone https://github.com/s3fs-fuse/s3fs-fuse.git
cd s3fs-fuse
./autogen.sh
./configure
make
sudo make install

pip install tqdm



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
