import os
import pickle
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras import models
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Activation, Flatten, \
    Conv2D, MaxPooling2D, Dropout, BatchNormalization, Input
from tensorflow.keras import backend as K
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import SGD

from generators import Singlet


def freeze(model):
    """Freeze model weights in every layer."""
    for layer in model.layers:
        layer.trainable = False

        if isinstance(layer, models.Model):
            freeze(layer)
    return model


def model_path(name):
    return 'models/' + name + '.model'


def get_convolutional_model(in_dim):
    inputs_image_simple_convolutional = Input(shape=in_dim)

    x1 = BatchNormalization()(inputs_image_simple_convolutional)
    x1 = Conv2D(32, (3, 3), data_format='channels_first')(x1)
    x1 = BatchNormalization()(x1)
    x1 = Activation(activation='relu')(x1)
    x1 = MaxPooling2D(pool_size=(2, 2))(x1)

    x2 = Conv2D(48, (3, 3), padding='same', data_format='channels_first')(x1)
    x2 = BatchNormalization()(x2)
    x2 = Activation(activation='relu')(x2)
    x2 = MaxPooling2D(pool_size=(2, 2))(x2)

    x3 = Conv2D(64, (3, 3), padding='same', data_format='channels_first')(x2)
    x3 = Activation(activation='relu')(x3)
    x3 = MaxPooling2D(pool_size=(2, 2))(x3)
    x3 = Flatten()(x3)
    out = Dense(128, activation='relu')(x3)
    return Model(inputs=inputs_image_simple_convolutional, outputs=out)



def initialize_base_model(in_dim):
    return get_convolutional_model(in_dim)


def train_base_model(model, train_generator, epochs):
    inp = Input(shape=train_generator._shape)
    x = model(inp)
    predictions = Dense(train_generator.n_classes, activation='softmax', name="output")(x)
    trainable_model = Model(inputs=inp, outputs=predictions)
    trainable_model.compile(optimizer=SGD(lr=1e-3, momentum=0.9),
                            loss="sparse_categorical_crossentropy",
                            metrics=["accuracy"])

    trainable_model.fit_generator(train_generator, epochs=epochs)
    return trainable_model


def main():
    batch_size = 4
    train_dir = "./pointDatasets"
    in_shape = (16, 16, 16)
    steps_per_epoch = 100
    # save_path = "trained_base_model.h5"
    model = initialize_base_model(in_shape)
    print("Instantiating generators")
    train_generator = Singlet(
        batch_size=batch_size, directory=train_dir, steps_per_epoch=steps_per_epoch, shape=in_shape)
    print("Training model")
    _ = train_base_model(model, train_generator, 10)
    print("Finished training")
    # model.save(save_path)
    # freeze(trainable_model).save(model_path("trainable_model_trained.h5"))


if __name__ == "__main__":
    main()
