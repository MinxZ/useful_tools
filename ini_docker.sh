docker ps
docker ps -a
docker image ls
docker image prune
docker container prune

nvidia-docker run -it gcr.io/tensorflow/tensorflow:latest-gpu bash

apt-get update
apt-get upgrade

# install terminal tools
apt install \
	  ncdu \
    tmux \
		htop \
		zip
apt autoremove


# install tf keras opencv tqdm

pip install \
	  opencv-python\
	  keras\
	  tqdm


# install Anaconda3
# wget 'https://repo.continuum.io/archive/Anaconda3-5.0.1-Linux-x86_64.sh'
# bash Anaconda3-5.0.1-Linux-x86_64.sh

git config --global user.name "MinxZ"
git clone https://github.com/MinxZ/Dog-Breed-Identification.git

git commit -a -m ‘committing all changes, equals to git add and git commit’
git push origin master
