from __future__ import division
from keras.layers import LSTM, GRU, Input, TimeDistributed, Dense, Activation, Reshape, merge
from keras.models import Model
from config import *

embedding_size = 12
lstm_size = 512
lstm_layers = 1

def get_train_model(max_len):
    input = Input(shape=(max_len, octave_len, states))
    a = Reshape([max_len, octave_len*states])(input)
    a = TimeDistributed(Dense(embedding_size))(a)
    for l in lstm_layers:
        a = LSTM(lstm_size, return_sequences=True)(a)
    a = TimeDistributed(Dense(octave_len*states))(a)
    a = Reshape([max_len, octave_len, states])(a)
    output = TimeDistributed(Activation('softmax'))(a)
    return Model(input, output)

def get_test_model():
    input = Input(batch_shape=(1, 1, octave_len, states))
    a = Reshape([1, octave_len*states])(input)
    a = TimeDistributed(Dense(embedding_size))(a)
    for l in lstm_layers:
        a = LSTM(lstm_size, stateful=True)(a)
    a = Dense(octave_len*states, name='timedistributed_3')(a)
    a = Reshape([octave_len, states])(a)
    output = Activation('softmax', name='timedistributed_4')(a)
    return Model(input, output)

def get_train_model1(max_len):
    input1 = Input(shape=(max_len, octave_len, states))
    a1 = Reshape([max_len, octave_len*states])(input1)
    a1 = TimeDistributed(Dense(embedding_size))(a1)

    input2 = Input(shape=(max_len, octave_len, states))
    a2 = Reshape([max_len, octave_len*states])(input2)
    a2 = TimeDistributed(Dense(embedding_size))(a2)

    a = merge([a1,a2], mode='concat')

    for l in lstm_layers:
        a = LSTM(lstm_size, return_sequences=True)(a)
    a = TimeDistributed(Dense(octave_len*states))(a)
    a = Reshape([max_len, octave_len, states])(a)
    output = TimeDistributed(Activation('softmax'))(a)
    return Model([input1, input2], output)

def get_test_model1():
    input1 = Input(batch_shape=(1, 1, octave_len, states))
    a1 = Reshape([1, octave_len*states])(input1)
    a1 = TimeDistributed(Dense(embedding_size))(a1)

    input2 = Input(batch_shape=(1, 1, octave_len, states))
    a2 = Reshape([1, octave_len*states])(input2)
    a2 = TimeDistributed(Dense(embedding_size))(a2)

    a = merge([a1, a2], mode='concat')

    for l in lstm_layers:
        a = LSTM(lstm_size, stateful=True)(a)
    a = Dense(octave_len*states, name='timedistributed_3')(a)
    a = Reshape([octave_len, states])(a)
    output = Activation('softmax', name='timedistributed_4')(a)
    return Model([input1, input2], output)
