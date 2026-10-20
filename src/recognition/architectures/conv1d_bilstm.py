"""Local temporal patterns + bidirectional context."""
import keras
from keras import layers

def build(input_shape, n_classes):
    x_in = keras.Input(shape=input_shape, name='hand_sequence')
    x = layers.Conv1D(32, 5, padding='same', activation='relu')(x_in)
    x = layers.MaxPooling1D(pool_size=2)(x)
    x = layers.Bidirectional(layers.LSTM(24))(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(32, activation='relu')(x)
    out = layers.Dense(n_classes, activation='softmax', name='class_probabilities')(x)
    return keras.Model(x_in, out, name='Conv1D_BiLSTM')
