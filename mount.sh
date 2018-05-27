sudo /usr/local/bin/s3fs liaro-ai-data /mnt/s3 -o rw,allow_other,uid=500,gid=500,default_acl=public-read,iam_role=crawler-s3
cd /mnt/s3/keras
