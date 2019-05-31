from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.optimizers import RMSprop
from keras.layers.recurrent import LSTM
from keras.callbacks import Callback


class LossHistory(Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))

def neural_net(num_sensors, params, load=''):
    model = Sequential()

    # First layer, takes parameters from learning.py for size (sensors)
    model.add(Dense(params[0], init='lecun_uniform', input_shape=(num_sensors,)))
    model.add(Activation('relu'))

    # Second layer, , takes parameters from learning.py for size
    model.add(Dense(params[1], init='lecun_uniform'))
    model.add(Activation('relu'))

    # Output layer
    model.add(Dense(3, init='lecun_uniform'))
    model.add(Activation('linear'))

    rms = RMSprop(lr=0.001)
    model.compile(loss='mse', optimizer=rms)

    if load:
        model.load_weights(load)
    return model
