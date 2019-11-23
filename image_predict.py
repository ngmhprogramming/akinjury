from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.optimizers import Adam
from keras import backend as K
from PIL import Image
import numpy as np

categories = ["Contusion","First Degree Burn","Minor Cut","Nose Bleed", "Snake Bite"]
img_width, img_height = 978, 742
train_data_dir = 'data/train'
validation_data_dir = 'data/test'
nb_train_samples = 160
nb_validation_samples = 44
epochs = 150
learning_rate = 1e-3
batch_size = 16

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
    chanDim = 1
else:
    input_shape = (img_width, img_height, 3)
    chanDim = -1

model = Sequential()

# CONV => RELU => POOL
model.add(Conv2D(32, (3, 3), padding="same",
    input_shape=input_shape))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(3, 3)))

model.add(Conv2D(32, (3, 3), padding="same",
    input_shape=input_shape))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(3, 3)))
model.add(Dropout(0.25))

# (CONV => RELU) * 2 => POOL
model.add(Conv2D(64, (3, 3), padding="same"))
model.add(Activation("relu"))
model.add(Conv2D(64, (3, 3), padding="same"))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation("relu"))
model.add(BatchNormalization())
model.add(Dropout(0.5))

model.add(Dense(5))
model.add(Activation('softmax'))

opt = Adam(lr=learning_rate, decay=learning_rate / epochs)
model.compile(loss="categorical_crossentropy",
              optimizer=opt,
              metrics=['accuracy'])

model.load_weights('second_try.h5')
impt = (742,978)

def predict(filename):
    im = Image.open(filename)
    im = im.resize(impt)
    im = im.convert("RGB")
    x = img_to_array(im)
    x = x.reshape((1,) + x.shape)
    x = x.astype('float32')
    x /= 255
    prediction = model.predict(x)
    return categories[np.argmax(prediction)], prediction.tolist()[0]