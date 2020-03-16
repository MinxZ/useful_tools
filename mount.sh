sudo /usr/local/bin/s3fs liaro-ai-data /mnt/s3 -o rw,allow_other,uid=500,gid=500,default_acl=public-read,iam_role=crawler-s3
cd /mnt/s3/keras

mkdir mnt_home
mkdir mnt_lab

sudo sshfs -o allow_other,defer_permissions mingxin@192.168.10.73:/net/callisto/storage4/mingxin/data/ /Users/z/mnt_lab
sudo sshfs -o allow_other,defer_permissions z@192.168.3.2:/home/z/data/ /Users/z/mnt_home
sudo umount /Users/z/mnt_lab
sudo umount /Users/z/mnt_home
