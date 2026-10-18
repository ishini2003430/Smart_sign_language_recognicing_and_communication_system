"""LSTM visual sign baseline."""
import keras
from keras import layers

def build(input_shape, n_classes):
    x_in = keras.Input(shape=input_shape, name='hand_sequence')
    x = layers.LSTM(32)(x_in)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(32, activation='relu')(x)
    out = layers.Dense(n_classes, activation='softmax', name='class_probabilities')(x)
    return keras.Model(x_in, out, name='LSTM')
