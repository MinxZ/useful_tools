chmod 400 *.pem
ssh -i *.pem ec2-user@

sudo docker ps
sudo docker ps -a
sudo docker container prune

sudo docker image -a
sudo docker rmi Image Image

sudo docker system prune -a

# with share memory mount
sudo docker pull ufoym/deepo
sudo nvidia-docker run -it --ipc=host -v ~/data:/data -v ~/config:/config ufoym/deepo bash

# with share memory mount and jupyter notebook support
sudo docker pull ufoym/deepo:all-py36-jupyter
sudo nvidia-docker run -it -p 8888:8888 --ipc=host -v ~/data:/data -v ~/config:/config  ufoym/deepo:all-py36-jupyter jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token= --notebook-dir='/root'

sudo docker ps
sudo docker exec -it 8b65380dfaf4 /bin/bash
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
