import shutil
import pandas as pd
import numpy as np
y_train = pd.read_csv('train_labels.csv')

y_train = np.array(y_train)

#print(y_train)
#shutil.move("path/to/current/file.foo", "path/to/new/destination/for/file.foo")

for x in range(len(y_train)):
    if y_train[x,1] == 1:
        y = x + 1
        if y <= 1600:
            y = str(y)
            shutil.move('train/'+y+'.jpg', 'train/1/'+y+'.jpg')
        else:
            y = str(y)
            shutil.move('validation/'+y+'.jpg', 'validation/1/'+y+'.jpg')
