pip install kaggle
mkdir ~/.kaggle
cd ~/.kaggle
vim kaggle.json
chmod 600 ~/.kaggle/kaggle.json

cd /data
kaggle datasets download -d camnugent/sandp500
