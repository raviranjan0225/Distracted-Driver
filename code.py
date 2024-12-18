# -*- coding: utf-8 -*-
"""Distracted-Driver-Detection

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PUoDtwTT6zvsfbJDpYT4DAgSP8lRqaDW
"""

import pickle

#unpacking the file
with open('/content/drive/MyDrive/Colab Notebooks/Distracted Driver Detection/images.p', 'rb') as f:
    images = pickle.load(f)

with open('/content/drive/MyDrive/Colab Notebooks/Distracted Driver Detection/labels.p', 'rb') as f:
    labels = pickle.load(f)

from google.colab import drive
drive.mount('/content/drive')

print(images.shape)
print(labels.shape)

set(labels)

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
labels = le.fit_transform(labels)

set(labels)

import numpy as np

n_persons = len(set(labels))
print("Number of persons: ", n_persons)
label_mapping = le.inverse_transform(np.arange(n_persons))
for i in range(len(label_mapping)):
  print(i, "-->", label_mapping[i])

import matplotlib.pyplot as plt

plt.imshow(images[77], cmap=plt.get_cmap("gray"))
plt.show()

import cv2

def preprocessing(img):
  img = cv2.equalizeHist(img)
  img = img.reshape(100, 100, 1)
  img = img/255
  return img

images = np.array(list(map(preprocessing, images)))
print("Shape of Input: ", images.shape)

from tensorflow.keras.utils import to_categorical

labels = to_categorical(labels)

categories = labels.shape[1]
print(categories)

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import cifar10

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
# import convolution layer
from tensorflow.keras.layers import Conv2D
# import pooling layer
from tensorflow.keras.layers import MaxPooling2D
# import faltten layer
from tensorflow.keras.layers import Flatten
from tensorflow.keras.optimizers import RMSprop

from tensorflow.keras.layers import Input, Add, Dense, Activation, ZeroPadding2D,GlobalAveragePooling2D

from keras.layers import Conv2D, MaxPooling2D, BatchNormalization

from keras.callbacks import ReduceLROnPlateau

model = Sequential()

model.add(Conv2D(32, (3, 3), padding="same",input_shape = (100,100,1)))
model.add(Activation("relu"))
model.add(BatchNormalization(axis=1))
model.add(MaxPooling2D(pool_size=(3, 3)))

model.add(Conv2D(64, (3, 3), padding="same"))
model.add(Activation("relu"))
model.add(BatchNormalization(axis=1))

model.add(Conv2D(64, (3, 3), padding="same"))
model.add(Activation("relu"))
model.add(BatchNormalization(axis=1))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(128, (3, 3), padding="same"))
model.add(Activation("relu"))
model.add(BatchNormalization(axis=1))

model.add(Conv2D(128, (3, 3), padding="same"))
model.add(Activation("relu"))
model.add(BatchNormalization(axis=1))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())

model.add(Dense(1024))
model.add(Activation("relu"))
model.add(BatchNormalization())
model.add(Dense(10))
model.add(Activation("softmax"))
#model.build((0,100,100,1))

# Print the model summary
model.summary()

learning_rate_reduction = ReduceLROnPlateau(monitor='accuracy',
                                            patience = 2,
                                            verbose=1,
                                            factor=0.1,
                                            min_lr=0.000001)

opt = tf.keras.optimizers.Adam(learning_rate=0.0001)

#compiling the model
model.compile(RMSprop(learning_rate=0.0001), loss="categorical_crossentropy", metrics=['accuracy'])

h = model.fit(images,labels,validation_split=0.01,batch_size=250,epochs=10,verbose=1)

plt.plot(h.history['accuracy'])
plt.plot(h.history['val_accuracy'])
plt.show()

from tensorflow.keras.models import Model

layer0 = Model(model.layers[0].input, model.layers[0].output)
features = layer0.predict(images[69].reshape(1,100,100,1))

features.shape

plt.figure(figsize=(10,15))
for i in range(32):
  axes = plt.subplot(8, 4, i+1)
  plt.imshow(features[0,:,:,i])

from google.colab import files
upload=files.upload()

d=list(upload.keys())[0]

import cv2
a=np.fromstring(upload[d],np.uint8)
img=cv2.imdecode(a,cv2.IMREAD_COLOR)
img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
print(a)
plt.imshow(img,cmap=plt.get_cmap("gray"))

img=np.asarray(img)
img=cv2.resize(img,(100,100))
img=preprocessing(img)

img=img.reshape(1,100,100,1)
print(model.predict(img))

prediction=model.predict(img)

p=np.argmax(prediction,axis=1)
l = p.tolist()
l

for i in l:
  if i == 0:
    print('Safe driving')
  elif i == 1:
    print('Texting - right')
  elif i == 2:
    print('Talking on the phone - right')
  elif i == 3:
    print('Texting - left')
  elif i == 4:
    print('Talking on the phone - left')
  elif i == 5:
    print('Operating the radio')
  elif i == 6:
    print('Drinking')
  elif i == 7:
    print('Reaching behind')
  elif i == 8:
    print('Hair and makeup')
  elif i == 9:
    print('Talking to passenger')

a=np.fromstring(upload[d],np.uint8)
img=cv2.imdecode(a,cv2.IMREAD_COLOR)
img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
plt.imshow(img,cmap=plt.get_cmap("gray"))

