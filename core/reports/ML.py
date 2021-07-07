import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import pymongo

# %matplotlib inline
plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('fast')

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from sklearn.preprocessing import MinMaxScaler

from pymongo import MongoClient


client = MongoClient('localhost', 27017)
client.database_names()
db = client['tienda_materiales_final']
collectionD = db['detsale']

df = pd.read_csv('time_series.csv', parse_dates=[0], header=None, index_col=0, squeeze=True, names=['fecha', 'unidades'])

PASOS = 7

# convert series to supervised learning
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j + 1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j + 1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j + 1, i)) for j in range(n_vars)]
    # put it all together
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg


# load dataset
values = df.values
# ensure all data is float
values = values.astype('float32')
# normalize features
scaler = MinMaxScaler(feature_range=(-1, 1))
values = values.reshape(-1, 1)  # esto lo hacemos porque tenemos 1 sola dimension
scaled = scaler.fit_transform(values)
# frame as supervised learning
reframed = series_to_supervised(scaled, PASOS, 1)


values = reframed.values
n_train_days = round(df.shape[0] * 0.8)
train = values[:n_train_days, :]
test = values[n_train_days:, :]
x_train = train[:, :-1]
y_train = train[:, -1]
x_val = test[:, :-1]
y_val = test[:, -1]
x_train = x_train.reshape((x_train.shape[0], 1, x_train.shape[1]))
x_val = x_val.reshape((x_val.shape[0], 1, x_val.shape[1]))


def crear_modeloFF():
    model = Sequential()
    model.add(Dense(PASOS, input_shape=(1, PASOS), activation='tanh'))
    model.add(Flatten())
    model.add(Dense(1, activation='tanh'))
    model.compile(loss='mean_absolute_error', optimizer='Adam', metrics=["mse"])
    model.summary()
    return model


EPOCHS = 60
model = crear_modeloFF()
history = model.fit(x_train, y_train, epochs=EPOCHS, validation_data=(x_val, y_val), batch_size=PASOS)





ultimosDias = df['2018-11-16':'2018-11-30']
ultimosDias

values = ultimosDias.values
values = values.astype('float32')
# normalize features
values = values.reshape(-1, 1)  # esto lo hacemos porque tenemos 1 sola dimension
scaled = scaler.fit_transform(values)
reframed = series_to_supervised(scaled, PASOS, 1)
reframed.drop(reframed.columns[[7]], axis=1, inplace=True)
# reframed.head(7)

values = reframed.values
x_test = values[6:, :]
x_test = x_test.reshape((x_test.shape[0], 1, x_test.shape[1]))
print(x_test.shape)
x_test


def agregarNuevoValor(x_test, nuevoValor):
    for i in range(x_test.shape[2] - 1):
        x_test[0][0][i] = x_test[0][0][i + 1]
    x_test[0][0][x_test.shape[2] - 1] = nuevoValor
    return x_test


results = []
for i in range(7):
    parcial = model.predict(x_test)
    results.append(parcial[0])
    print(x_test)
    x_test = agregarNuevoValor(x_test, parcial[0])

adimen = [x for x in results]
print(adimen)
inverted = scaler.inverse_transform(adimen)
#inverted

prediccion1SemanaDiciembre = pd.DataFrame(inverted)

i=0
for fila in prediccion1SemanaDiciembre.pronostico:
    i=i+1
    ultimosDias.loc['2018-12-0' + str(i) + ' 00:00:00'] = fila
    print(fila)
#ultimosDias.tail(14)