import matplotlib.pyplot as plt
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
from keras.layers import LSTM, Dense
from keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler


def processData(data, lb=20, delay=10):
    X, Y = [], []
    for i in range(len(data) - lb - 1 - delay):
        X.append(data[i:(i + lb), 0])
        Y.append(data[(i + lb):(i + lb + delay), 0])
    return np.array(X), np.array(Y)


def get_data(data, name, lb=20, delay=10):
    cl = data[data['Name'] == name]
    scl = MinMaxScaler()
    # Scale the data
    cl = np.array(cl)
    cl = cl[:, 2]
    cll = cl.copy()

    # for i in range(cl.shape[0] - 1):
    #     cll[i] = cl[i + 1] / cl[i]
    # cl = cll - 1
    cl = cl.reshape(cl.shape[0], 1)
    cl = scl.fit_transform(cl)

    X, y = processData(cl, lb, delay)
    X_train, X_test = X[:int(X.shape[0] * 0.80)], X[int(X.shape[0] * 0.80):]
    y_train, y_test = y[:int(y.shape[0] * 0.80)], y[int(y.shape[0] * 0.80):]
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
    print(X_train.shape[0])
    print(X_test.shape[0])
    print(y_train.shape[0])
    print(y_test.shape[0])

    return X_train, X_test, y_train, y_test


lb = 7
delay = 7
data = pd.read_csv('../data/all_stocks_5yr.csv')
x_train, x_test, y_train, y_test = get_data(data, 'MMM', lb, delay)
# X_train, X_test, y_train, y_test=get_data(data, 'ZTS', 3)

model = Sequential()
model.add(LSTM(256, input_shape=(lb, 1)))
model.add(Dense(delay))
model.compile(optimizer='adam', loss='mse')
model.summary()
# Reshape data for (Sample,Timestep,Features)
# Fit model with history to check for overfitting

model.fit(x_train, y_train, epochs=100,
          validation_data=(x_test, y_test), shuffle=False)
model.evaluate(x_train, y_train)
