# Run this cell and select the kaggle.json file downloaded
# from the Kaggle account settings page.
from google.colab import files

files.upload()

# Let's make sure the kaggle.json file is present.
!ls -lha kaggle.json
!pip install -q kaggle
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets list
!cd ~
!kaggle competitions download -c quickdraw-doodle-recognition
