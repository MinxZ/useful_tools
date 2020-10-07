# -*- coding: UTF-8 -*-
'''
@Author: houwx
@Date: 2019-11-20 15:28:51
@LastEditors: houwx
@LastEditTime: 2019-12-12 11:14:02
@Description: 
'''
# -*- coding: UTF-8 -*-
'''
    concatenate wavs into a single one
'''

from os import walk
import random

# words: [five stop seven forward backward yes down follow learn visual]

path = "/net/callisto/storage3/gshengzhou/datasets/fruits_20191210/for_segmentation/mp3s"
#out_path = '/net/callisto/storage3/gshengzhou/datasets/fruits_20191210/for_segmentation/wavs'
out_path = '/net/callisto/storage3/gshengzhou/fyppp/segmented_wavs_short'
file_format = "mp3"

_, _, filenames = next(walk(path), (None, None, []))

#print(filenames)
random.shuffle(filenames)

from pydub import AudioSegment

for i, filename in enumerate(filenames):
    sounds = AudioSegment.from_file(path + "/" + filename, file_format)
    sounds.export(out_path + "/" + filename, format="wav")


print('done!')
