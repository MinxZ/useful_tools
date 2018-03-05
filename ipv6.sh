want to remote
http://www.makeuseof.com/tag/connect-home-network-dyndns/
http://www.makeuseof.com/tag/beginners-guide-setting-ssh-linux-testing-setup/
ssh is good with ipv6
dyndns is not

sudo inadyn \
--period 600 \
--system default@dyndns.org \
--username xmx \
--password 425535NJi \
--alias femiko.dnsdojo.com

buy router monitor keyboard
4
try ipv6 ddns

wget ' '
tar xvjf .tra.gz

cd /usr/src
sudo wget http://sourceforge.net/projects/inadyn-mt/files/latest/download -O inadyn-latest.tar.gz
sudo tar xvf inadyn-latest.tar.gz

cd inadyn-mt.v.02.28.10
./configure
sudo make check
sudo make
sudo make install
cp bin/linux/inadyn /usr/sbin/

sudo inadyn-mt \
--update_period 6000 \
--ip_server_host ipv6.dynv6.com \
--username z08040992048@gmail.com \
--password 29k-2Mv-a2r-F6q \
--alias femiko.dynv6.net

# install cuDNN

# nvidia-docker

token=zsSjZL_sZe3-G9waCSViNd7Ke8Jjbe ./dynv6.sh femiko.dynv6.net

#install ubuntu

sudo apt-get update
sudo apt-get upgrade

sudo apt-get install \
ncdu\
gdebi-core\
tmux\

# install Nvidia drive 375
sudo add-apt-repository ppa:graphics-drivers/ppa

sudo apt-get update
sudo apt-get install nvidia-<driver_number>

# install nvidia-docker

# Update IP address
token=zsSjZL_sZe3-G9waCSViNd7Ke8Jjbe ./dynv6.sh femiko.dynv6.net

ssh z@femiko.dynv6.net
ssh -6 z@2400:2410:25c1:b500:c20:2e19:6b0a:feaf
