# -*- coding: utf-8 -*-
"""Model_Tuberculosis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1InEFPGhaUBHi1EhrucTUbxpg_mjdDJ7R
"""

from google.colab import drive

drive.mount('/content/drive')

import tensorflow as tf 
from keras.layers import Input, Lambda, Dense, Flatten
from keras.models import Model
#from keras.applications.resnet50 import ResNet50
from PIL import Image, ImageChops
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt

IMAGE_SIZE =[500,500]
train_path = '/content/drive/MyDrive/ColabNotebooks/TB_Chest_Radiography_Database/train'
valid_path = '/content/drive/MyDrive/ColabNotebooks/TB_Chest_Radiography_Database/test'

vgg = VGG16(input_shape=IMAGE_SIZE + [3] , weights='imagenet', include_top=False)

for layer in vgg.layers:
    layer.trainable = False

folders = glob('/content/drive/MyDrive/ColabNotebooks/TB_Chest_Radiography_Database/train/*')
print(folders)

x = Flatten()(vgg.output)

prediction = Dense(len(folders), activation='softmax')(x)
# MOdel creation
model = Model(inputs=vgg.input, outputs=prediction)

model.summary()

#cost and optimization method
run_opts = tf.compat.v1.RunOptions(report_tensor_allocations_upon_oom = True)
model.compile(
  loss='categorical_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)
val_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory('/content/drive/MyDrive/ColabNotebooks/TB_Chest_Radiography_Database/train',
                                                 target_size = (500,500),
                                                 batch_size = 5,
                                                 class_mode = 'categorical')

test_set = test_datagen.flow_from_directory('/content/drive/MyDrive/ColabNotebooks/TB_Chest_Radiography_Database/test',
                                            target_size = (500,500),
                                            batch_size = 5,
                                            class_mode = 'categorical')
print(test_set)

for _ in range(50):
    img, label = training_set.next()
    print(img.shape)   #  (1,256,256,3)
    plt.imshow(img[0])
    plt.show()

# fit the Model
r = model.fit(
  training_set,
  validation_data=test_set,
  epochs=25,
  steps_per_epoch=(len(training_set)),
  validation_steps=len(test_set),
  #batch_size=32
)

# plot the loss
plt.plot(r.history['loss'], label='train loss')
plt.plot(r.history['val_loss'], label='val loss')
plt.xlabel("epoch")
plt.ylabel("Loss")
plt.legend()
plt.show()
plt.savefig('LossVal_loss')

# plot the accuracy
plt.plot(r.history['accuracy'], label='train accuracy')
plt.plot(r.history['val_accuracy'], label='val accuracy')
plt.xlabel("epoch")
plt.ylabel("Accurracy")
plt.legend()
plt.show()
plt.savefig('AccVal_accuracy')

# save it as a h5 file

import tensorflow as tf

from keras.models import load_model

model.save('Trained_modelTB.h5')

from google.colab import drive
drive.mount('/content/drive')