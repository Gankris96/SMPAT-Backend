
import pandas as pd
import pyspark as spark
import matplotlib.pyplot as plt
from math import ceil
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import keras.utils

symbol = "INFY"
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    '''
    Converts the original dataframe to a format which contains
    lag shifted values of inputs which can be used as input
    to the LSTM
    '''
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    # put it all together
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg

df1 = pd.read_csv("twitterCompanyStocks/"+symbol+'Features.csv',header=None)
df1.columns = ['DateTime','Negative','Neutral','Positive','Compound','Price']
df1.set_index('DateTime',inplace=True)
cols = df1.columns.tolist()
cols = cols[-1:] + cols[:-1]
df1 = df1[cols]
scaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(df1.values)
n_days = 3
n_features = 5
n_obs = n_days*n_features
reframed = series_to_supervised(scaled, n_days, 1)
reframed.head()
reframed = reframed.drop(reframed.columns[-4:], axis=1)
reframed.head()
values = reframed.values
n_train_hours = ceil(len(values)*0.8)
train = values[:n_train_hours, :]
test = values[n_train_hours:, :]
data_set = pd.read_csv("twitterCompanyStocks/"+symbol+'Features.csv')
data_set_dates = data_set.iloc[n_train_hours:,0]
data_set_dates_arr = []
for i in data_set_dates[:-2]:
    data_set_dates_arr.append(i.split("T")[0])
data_set_dates_arr = np.array(data_set_dates_arr)
# split into input and outputs
train_X, train_y = train[:, :n_obs], train[:, -n_features]
test_X, test_y = test[:, :n_obs], test[:, -n_features]
# reshape input to be 3D [samples, timesteps, features]
train_X = train_X.reshape((train_X.shape[0], n_days, n_features))
test_X = test_X.reshape((test_X.shape[0], n_days, n_features))











handler = open(symbol+"Features.csv_model.json","r")
json_str = handler.read()
model = keras.models.model_from_json(json_str)
print("Loaded the model successfully")

#Load the weights

model.load_weights(symbol+"Features.csv_model_weights.h5")
test_X, test_y = test[:, :n_obs], test[:, -n_features]
test_X = test_X.reshape((test_X.shape[0], n_days, n_features))


# make a prediction
yhat = model.predict(test_X)
test_X = test_X.reshape((test_X.shape[0], n_days* n_features))
# invert scaling for forecast
inv_yhat = np.concatenate((yhat, test_X[:, -4:]), axis=1)
inv_yhat = scaler.inverse_transform(inv_yhat)
inv_yhat = inv_yhat[:,0]
# invert scaling for actual
test_y = test_y.reshape((len(test_y), 1))
inv_y = np.concatenate((test_y, test_X[:, -4:]), axis=1)
inv_y = scaler.inverse_transform(inv_y)
inv_y = inv_y[:,0]
# calculate RMSE
rmse = np.sqrt(mean_squared_error(inv_y, inv_yhat))
print('Test RMSE: %.3f' % rmse)

df_sol = pd.DataFrame({'Date':data_set_dates_arr,'actual':inv_y,'Predicted':inv_yhat})
df_sol.to_csv('Predictions_Multi'+symbol+'.csv')