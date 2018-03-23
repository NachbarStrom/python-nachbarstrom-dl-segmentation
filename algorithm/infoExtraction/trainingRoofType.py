from keras.applications.inception_v3 import InceptionV3
from keras.layers import Conv2D, Dense, Dropout, InputLayer, Flatten
from keras.models import Sequential, Model
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras import optimizers
from data import get_dategen_from_dir
#import matplotlib as plt
import pickle

#default input size for inception is 299x299
WIDTH = 299
HEIGHT = 299

#number of classes to predict
NUM_CLASSES = 5

#freeze first NUM_FREEZE_LAYERS layers or freeze all
FREEZE_ALL = True
NUM_FREEZE_LAYERS = 25

#training parameters
LR = 0.0001         #learning rate
MOMENTUM = 0.9      #momentum
BATCH_SIZE = 32     #batch size

#path where the model will be stored
MODEL_PATH = "Model/Test/modelRoofType.h5"
#path where the training path is stored / one folder per class
TRAIN_PATH = "ImageOrientation/Training/"
#path where the validation data is stored
VAL_PATH = "ImageOrientation/Validation/"


#import the model
base_model = InceptionV3(include_top=False, weights="imagenet", input_shape=(WIDTH, HEIGHT, 3), pooling="max")

base_model.summary()

# build a classifier model to put on top of the convolutional model
top_model = Sequential()
#top_model.add(Flatten(input_shape=model.output_shape[1:]))
print(base_model.output_shape)
top_model.add(InputLayer(base_model.output_shape))
top_model.add(Dense(512, activation='relu'))
top_model.add(Dropout(0.5))
top_model.add(Dense(256, activation='relu'))
top_model.add(Dense(NUM_CLASSES, activation="softmax"))

if FREEZE_ALL:
    for layer in base_model.layers:
        layer.trainable = False
else:
    for layer in base_model.layers[:NUM_FREEZE_LAYERS]:
        layer.trainable = False

# add the model on top of the convolutional base
model = Model(inputs= base_model.input, outputs= top_model(base_model.output))

#print model summary
model.summary()

#Compile the model with optimizer
model.compile(loss = "categorical_crossentropy", optimizer = optimizers.SGD(lr=LR, momentum=MOMENTUM), metrics=["accuracy"])

# Save the model according to the conditions
checkpoint = ModelCheckpoint(MODEL_PATH, monitor='val_acc', verbose=1, save_best_only=True, save_weights_only=False, mode='auto', period=1)
#Performe early stopping, based on validation accuracy
early = EarlyStopping(monitor='val_acc', min_delta=0, patience=50, verbose=1, mode='auto')

#Create data generators
train_generator = get_dategen_from_dir(TRAIN_PATH, target_size=(WIDTH, HEIGHT), batch_size=BATCH_SIZE)
#print(train_generator.)
validation_generator = get_dategen_from_dir(VAL_PATH, target_size=(WIDTH, HEIGHT), batch_size=BATCH_SIZE)

# Train the model
history = model.fit_generator(
    train_generator,
    steps_per_epoch = 1,
    epochs = 5,
    validation_data = validation_generator,
    validation_steps = 1,
    callbacks = [checkpoint, early],
    verbose=2)

acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(len(acc))

metrics = {"acc":acc,"val_acc":val_acc,"loss":loss,"val_loss":val_loss}

with open("history.pickle", "wb") as file:
    pickle.dump(metrics, file)


#plt.plot(epochs, acc, 'b', label="training acc")
#plt.plot(epochs, val_acc, 'r', label="validation acc")
#+plt.title('Training and validation accuracy')

#plt.figure()
#plt.plot(epochs, loss, 'b', label="training loss")
#plt.plot(epochs, val_loss, 'r', label="validation loss")
#plt.title('Training and validation loss')


#plt.show()