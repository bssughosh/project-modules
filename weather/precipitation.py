# -*- coding: utf-8 -*-
"""
Created on Mon, May 18 2020

Author: Sughosh Sudhanvan
"""

import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression

df = pd.read_csv('mumbai.csv')

df['date_time'] = pd.to_datetime(df['date_time'])

df1 = df[
    ['date_time', 'maxtempC', 'mintempC', 'FeelsLikeC', 'cloudcover', 'visibility', 'precipMM', 'tempC', 'humidity']]

x = []
t = []
for i, j in df1.iterrows():
    if j[0].strftime("%Y") in ('2010', '2011', '2012', '2013'):
        x.append(j)
    if j[0].strftime("%Y") == '2014':
        t.append(j)

x = np.array(x)
x1 = pd.DataFrame(x, columns=['date_time', 'maxtempC', 'mintempC', 'FeelsLikeC', 'cloudcover', 'visibility', 'precipMM',
                              'tempC', 'humidity'])
forecast_out = 365
x1['prediction'] = x1[['precipMM']].shift(-forecast_out)

X = np.array(x1.drop(['prediction', 'date_time'], 1))
X = X[:-forecast_out]

y = np.array(x1['prediction'])
y = y[:-forecast_out]

lr = LinearRegression()
lr.fit(X, y)

x_forecast = np.array(x1.drop(['prediction', 'date_time'], 1))[-forecast_out:]
lr_prediction = lr.predict(x_forecast)

x2 = pd.DataFrame(t, columns=['date_time', 'maxtempC', 'mintempC', 'FeelsLikeC', 'cloudcover', 'visibility', 'precipMM',
                              'tempC', 'humidity'])

lr_prediction = pd.DataFrame(lr_prediction, columns=['Predicted'])
lr_prediction['Predicted'] = lr_prediction['Predicted'].abs()
x2.index = lr_prediction.index
lr_prediction['Original'] = x2['precipMM']

lr_prediction['diff'] = lr_prediction['Predicted'] - lr_prediction['Original']
lr_prediction['diff'] = abs(lr_prediction['diff'])

a = lr_prediction['diff'].sum()
a = a / forecast_out
