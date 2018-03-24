from keras.preprocessing.image import ImageDataGenerator

#Imagegenerator with the specified augmentation
datagen = ImageDataGenerator(
    #featurewise_center=perform_featurewise_normalization,
    #samplewise_center=False,
    #featurewise_std_normalization=perform_featurewise_normalization,
    #samplewise_std_normalization=False,
    #zca_whitening=False,
    #zca_epsilon=1e-6,
    #rotation_range=180.0,
    #width_shift_range=0.1,
    #height_shift_range=0.1,
    #shear_range=0.,
    #zoom_range=0.,
    #channel_shift_range=0.,
    #fill_mode='nearest',
    #cval=0.,
    #horizontal_flip=True,
    #vertical_flip=True,
    #rescale=None,
    #preprocessing_function=None,
    #data_format=K.image_data_format()
)


def get_dategen_from_dir(dir, target_size=(299,299), batch_size=16):
    """
    Returns the specified datagenerator
    :param dir: Directory to the data
    :param target_size: Target image size
    :param batch_size: Size of one batch
    :return: The datagenerator
    """
    generator = datagen.flow_from_directory(dir,
                                target_size=target_size,
                                color_mode="rgb",
                                batch_size=batch_size,
                                shuffle=True)
    print(generator.class_indices)
    return generator