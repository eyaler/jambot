from keras.layers import LSTM, GRU, Input, TimeDistributed, Dense, Activation, Reshape, merge
from keras.models import Model

octave_len = 12
embedding_size = 12
lstm_size = 128
states = 3

def get_train_model(max_len):
    input = Input(shape=(max_len, octave_len, states))
    a = Reshape([max_len, octave_len*states])(input)
    a = TimeDistributed(Dense(embedding_size))(a)
    a = LSTM(lstm_size, return_sequences=True)(a)
    a = TimeDistributed(Dense(octave_len*states))(a)
    a = Reshape([max_len, octave_len, states])(a)
    output = TimeDistributed(Activation('softmax'))(a)
    return Model(input, output)

def get_test_model():
    input = Input(batch_shape=(1, 1, octave_len, states))
    a = Reshape([1, octave_len*states])(input)
    a = TimeDistributed(Dense(embedding_size))(a)
    a = LSTM(lstm_size, stateful=True)(a)
    a = Dense(octave_len*states)(a)
    a = Reshape([octave_len, states])(a)
    output = Activation('softmax')(a)
    return Model(input, output)

def get_train_model1(max_len):
    input1 = Input(shape=(max_len, octave_len, states))
    a1 = Reshape([max_len, octave_len*states])(input1)
    a1 = TimeDistributed(Dense(embedding_size))(a1)

    input2 = Input(shape=(max_len, octave_len, states))
    a2 = Reshape([max_len, octave_len*states])(input2)
    a2 = TimeDistributed(Dense(embedding_size))(a2)

    a = merge([a1,a2], mode='concat')

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

    a = LSTM(lstm_size, stateful=True)(a)
    a = Dense(octave_len*states)(a)
    a = Reshape([octave_len, states])(a)
    output = Activation('softmax')(a)
    return Model([input1, input2], output)
