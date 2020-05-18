# -*- coding: utf-8 -*-
"""
Created on Sun, May 17 2020

Author: Sughosh Sudhanvan
"""

import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression

df = pd.read_csv('mumbai.csv')

df['date_time'] = pd.to_datetime(df['date_time'])

df1 = df[['date_time', 'maxtempC', 'mintempC', 'FeelsLikeC', 'cloudcover', 'visibility', 'tempC']]
x = []
t = []
for i, j in df1.iterrows():
    if j[0].strftime("%Y") != '2020':
        x.append(j)
    else:
        t.append(j)

x = np.array(x)
x1 = pd.DataFrame(x, columns=['date_time', 'maxtempC', 'mintempC', 'FeelsLikeC', 'cloudcover', 'visibility', 'tempC'])
forecast_out = 61
x1['prediction'] = x1[['tempC']].shift(-forecast_out)

X = np.array(x1.drop(['prediction', 'date_time'], 1))
X = X[:-forecast_out]

y = np.array(x1['prediction'])
y = y[:-forecast_out]

lr = LinearRegression()
lr.fit(X, y)

x_forecast = np.array(x1.drop(['prediction', 'date_time'], 1))[-forecast_out:]
lr_prediction = lr.predict(x_forecast)

x2 = pd.DataFrame(t, columns=['date_time', 'maxtempC', 'mintempC', 'FeelsLikeC', 'cloudcover', 'visibility', 'tempC'])

lr_prediction = lr_prediction.astype('int8')
lr_prediction = pd.DataFrame(lr_prediction, columns=['Predicted'])
x2.index = lr_prediction.index
lr_prediction['Original'] = x2['tempC']

lr_prediction['diff'] = lr_prediction['Predicted'] - lr_prediction['Original']
lr_prediction['diff'] = abs(lr_prediction['diff'])

a = lr_prediction['diff'].sum()
a = a / forecast_out

print('Average error =', a)
