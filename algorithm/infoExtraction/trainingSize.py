from keras.applications.inception_v3 import InceptionV3
from keras.layers import Conv2D, Dense, Dropout, InputLayer, Flatten
from keras.models import Sequential, Model
#from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras import optimizers
#from data import get_dategen_from_dir
from ImageFeeder import ImageFeeder
#import matplotlib as plt
#import pickle

#default input size for inception is 299x299
WIDTH = 299
HEIGHT = 299

#freeze first NUM_FREEZE_LAYERS layers or freeze all
FREEZE_ALL = True
NUM_FREEZE_LAYERS = 25

#training parameters
LR = 0.0001         #learning rate
MOMENTUM = 0.9      #momentum
BATCH_SIZE = 32     #batch size
EPOCHS = 1          #epochs

#path where the model will be stored
MODEL_PATH = "Model/Test/modelSize.h5"
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
top_model.add(Dense(1, activation="relu"))

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
model.compile(loss = "mean_squared_error", optimizer = optimizers.SGD(lr=LR, momentum=MOMENTUM), metrics=["accuracy"])

image_feeder = ImageFeeder("C:/Users/Thomas/Documents/Studium/Vorlesung/Maschbau/Master/3. Semester/TMS/solAI/Code/Image", (0.75,0.25,0), output_dims=(WIDTH, HEIGHT), batchsize=BATCH_SIZE, expand_trainset=1, expand_validationset=1)

train_acc_total = []
train_loss_total = []
val_acc_total = []
val_loss_total = []

best_val_acc = 0.0

#Train the network
for epoch in range(EPOCHS):
    image_feeder.shuffle_data()
    train_acc = 0
    train_loss = 0
    val_acc = 0
    val_loss = 0

    #perform training steps
    for step in range(image_feeder.steps["train"]):
        X_batch, Y_batch = image_feeder.get_next_train_batch()

        model.train_on_batch(X_batch, Y_batch)

        #.test_on_batch returns the loss and every metric that is given in the .compile statement
        loss_acc_train = model.test_on_batch(X_batch, Y_batch)
        train_loss += loss_acc_train[0]
        train_acc += loss_acc_train[1]

    #perform validation steps after each epoch
    for step in range(image_feeder.steps["val"]):
        X_batch, Y_batch = image_feeder.get_next_val_batch()

        loss_acc_train = model.test_on_batch(X_batch, Y_batch)
        val_loss += loss_acc_train[0]
        val_acc += loss_acc_train[1]

    train_acc /= image_feeder.steps["train"]
    train_loss /= image_feeder.steps["train"]
    val_acc /= image_feeder.steps["val"]
    val_loss /= image_feeder.steps["val"]

    #update metrics
    train_acc_total += train_acc
    train_loss_total += train_loss
    val_acc_total += val_acc
    val_loss_total += val_loss



    print("Epoch {0} of {1}: Train loss: {2} - Train acc {3} - Val loss: {4} - Val acc: {5}".format(epoch, EPOCHS, train_loss, train_acc, val_loss, val_acc))
    if val_acc > best_val_acc:
        print("___________________________________________________________New best val acc: ", val_acc)
        model.save(MODEL_PATH+".h5")
        best_val_acc = val_acc
"""
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
"""