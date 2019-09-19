import os
import pickle

from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Concatenate, Dense, BatchNormalization, Input
from tensorflow.keras.callbacks import CSVLogger, ReduceLROnPlateau, EarlyStopping
from tensorflow.keras import backend as K
from tensorflow.keras.optimizers import SGD

from create_base_model import initialize_base_model, freeze
from generators import Triplet


def model_path(name, iteration=""):
    return 'models/' + name + '.model' if not iteration else 'models/' + name + '_'+iteration+'.model'


def initialize_bitvector_model(in_dim, embedding_dim):
    print('Creating bitvector network from scratch.')
    model = initialize_base_model(in_dim)
    m_in = Input(shape=in_dim)
    x = model(m_in)
    bitvector = Dense(embedding_dim, activation='sigmoid')(x)
    return Model(inputs=m_in, outputs=bitvector)


def tripletize(in_dim, bitvector_model):
    anc_in = Input(shape=in_dim)
    pos_in = Input(shape=in_dim)
    neg_in = Input(shape=in_dim)

    anc_out = bitvector_model(anc_in)
    pos_out = bitvector_model(pos_in)
    neg_out = bitvector_model(neg_in)

    out_vector = Concatenate()([anc_out, pos_out, neg_out])
    return Model(inputs=[anc_in, pos_in, neg_in], outputs=out_vector)


def std_triplet_loss(out_dim, alpha=5):
    """
    Basic triplet loss.
    Note, due to the K.maximum, this learns nothing when dneg>dpos+alpha
    """
    def myloss(_, y_pred):
        anchor = y_pred[:, 0:out_dim]
        pos = y_pred[:, out_dim:out_dim*2]
        neg = y_pred[:, out_dim*2:out_dim*3]
        pos_dist = K.sum(K.square(anchor-pos), axis=1)
        neg_dist = K.sum(K.square(anchor-neg), axis=1)
        basic_loss = pos_dist - neg_dist + alpha
        loss = K.maximum(basic_loss, 0.0)
        return loss

    return myloss


def train_siamese_model(model, train_generator, out_dim ):
    print("Starting to train")
    model.compile(optimizer=SGD(lr=1E-3, momentum=0.9),
                  loss=std_triplet_loss(out_dim))

    history = model.fit_generator(
        train_generator,
        epochs=25)

    return history

if __name__ == "__main__":
    batch_size = 4
    train_dir = "./pointDatasets"
    in_shape = (16, 16, 16)
    embedding_shape = 64
    steps_per_epoch = 500
    train_generator = Triplet(batch_size=batch_size, directory=train_dir, steps_per_epoch=steps_per_epoch, shape=in_shape)
    bitvector_model = initialize_bitvector_model(in_shape, embedding_shape)
    siamese_model = tripletize(in_shape, bitvector_model)
    train_siamese_model(siamese_model, train_generator, embedding_shape)
    # freeze(bitvector_model).save(model_path(out_name))
