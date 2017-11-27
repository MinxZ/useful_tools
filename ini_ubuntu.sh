# Update ubuntu

sudo apt-get update
sudo apt-get upgrade

# install terminal tools
sudo apt install \
  ncdu\
  gdebi-core\
  tmux\
  openssh-server\
  ssh\
  htop\

sudo apt autoremove

# install Nvidia drive 375
sudo add-apt-repository ppa:graphics-drivers/ppa

sudo apt-get update
sudo apt-get install nvidia-<driver_number>

# install CUDA cuDNN
# install nvidia-docker


sudo pip install \
  opencv-python\
  keras\
  tqdm


# install Anaconda3
# wget 'https://repo.continuum.io/archive/Anaconda3-5.0.1-Linux-x86_64.sh'
# bash Anaconda3-5.0.1-Linux-x86_64.sh

# install tf keras opencv tqdm

# sudo pip install \
#   tensorflow-gpu\
#   opencv-python\
#   keras\
#   tqdm
