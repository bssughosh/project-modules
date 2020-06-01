# -*- coding: utf-8 -*-
"""
Created on Tue May 26, 2020

Author: Sughosh Sudhanvan
"""

import pandas as pd
import numpy as np
import copy
from sklearn.linear_model import LinearRegression

from settings import *

pd.options.mode.chained_assignment = None

file = os.path.join(DATA_URL, 'manali.csv')
df = pd.read_csv(file)

df['date_time'] = pd.to_datetime(df['date_time'])

cols_s = [['date_time', 'maxtempC', 'mintempC', 'humidity', 'FeelsLikeC'],
          ['date_time', 'maxtempC', 'mintempC', 'humidity', 'FeelsLikeC', 'DewPointC'],
          ['date_time', 'maxtempC', 'mintempC', 'humidity', 'FeelsLikeC', 'pressure'],
          ['date_time', 'maxtempC', 'mintempC', 'humidity', 'FeelsLikeC', 'tempC'],
          ['date_time', 'maxtempC', 'mintempC', 'humidity', 'FeelsLikeC', 'DewPointC', 'pressure'],
          ['date_time', 'maxtempC', 'mintempC', 'humidity', 'FeelsLikeC', 'DewPointC', 'tempC'],
          ['date_time', 'maxtempC', 'mintempC', 'humidity', 'FeelsLikeC', 'DewPointC', 'pressure', 'tempC'],
          ['date_time', 'maxtempC', 'mintempC', 'humidity', 'DewPointC'],
          ['date_time', 'maxtempC', 'mintempC', 'humidity', 'pressure'],
          ['date_time', 'maxtempC', 'mintempC', 'humidity', 'tempC'],
          ['date_time', 'maxtempC', 'mintempC', 'humidity', 'DewPointC', 'pressure'],
          ['date_time', 'maxtempC', 'mintempC', 'humidity', 'DewPointC', 'tempC'],
          ['date_time', 'maxtempC', 'mintempC', 'humidity', 'DewPointC', 'tempC', 'pressure'],
          ['date_time', 'maxtempC', 'mintempC', 'humidity', 'FeelsLikeC', 'tempC', 'pressure'],
          ['date_time', 'maxtempC', 'mintempC', 'humidity', 'tempC', 'pressure'],
          ['date_time', 'tempC', 'humidity', 'maxtempC', 'mintempC'],
          ['date_time', 'tempC', 'humidity', 'FeelsLikeC'],
          ['date_time', 'tempC', 'humidity', 'DewPointC'],
          ['date_time', 'tempC', 'humidity', 'pressure'],
          ['date_time', 'tempC', 'humidity', 'maxtempC', 'mintempC', 'FeelsLikeC'],
          ['date_time', 'tempC', 'humidity', 'maxtempC', 'mintempC', 'DewPointC'],
          ['date_time', 'tempC', 'humidity', 'maxtempC', 'mintempC', 'pressure'],
          ['date_time', 'tempC', 'humidity', 'maxtempC', 'mintempC', 'pressure', 'FeelsLikeC'],
          ['date_time', 'tempC', 'humidity', 'maxtempC', 'mintempC', 'FeelsLikeC', 'DewPointC'],
          ['date_time', 'tempC', 'humidity', 'maxtempC', 'mintempC', 'DewPointC', 'pressure'],
          ['date_time', 'tempC', 'humidity', 'maxtempC', 'mintempC', 'FeelsLikeC', 'DewPointC', 'pressure'],
          ['date_time', 'tempC', 'humidity', 'DewPointC', 'pressure'],
          ['date_time', 'tempC', 'humidity', 'DewPointC', 'pressure', 'FeelsLikeC'],
          ['date_time', 'tempC', 'humidity', 'FeelsLikeC', 'DewPointC'],
          ['date_time', 'tempC', 'humidity', 'FeelsLikeC', 'pressure']]

cols1 = copy.deepcopy(cols_s)

for k in cols1:
    del k[0]

cols2 = copy.deepcopy(cols1)
for k in cols2:
    k.insert(0, 'year')
    k.insert(1, 'month')

statistical_values = []

for test_loc, cols in enumerate(cols_s):
    df1 = df[cols]

    df1['month'] = df1['date_time'].apply(lambda mon: mon.strftime('%m'))
    df1['year'] = df1['date_time'].apply(lambda year: year.strftime('%Y'))

    df1.drop(['date_time'], 1, inplace=True)

    g = df1.groupby(['year', 'month'], as_index=False)

    monthly_averages = g.aggregate(np.mean)
    monthly_averages[cols1[test_loc]] = monthly_averages[cols1[test_loc]].astype('int8')

    df2 = monthly_averages

    x = []
    t = []
    for i, j in df2.iterrows():
        if j[0] != '2020':
            x.append(j)
        else:
            t.append(j)

    x1 = pd.DataFrame(x, columns=cols2[test_loc])
    x2 = pd.DataFrame(t, columns=cols2[test_loc])

    forecast_out = 5

    x1['prediction'] = x1[['humidity']].shift(-forecast_out)

    X = np.array(x1.drop(['prediction', 'year', 'month'], 1))
    X = X[:-forecast_out]

    y = np.array(x1['prediction'])
    y = y[:-forecast_out]

    lr = LinearRegression()
    lr.fit(X, y)

    x_forecast = np.array(x1.drop(['prediction', 'year', 'month'], 1))[-forecast_out:]
    lr_prediction = lr.predict(x_forecast)

    lr_prediction = lr_prediction.astype('int8')
    lr_prediction = pd.DataFrame(lr_prediction, columns=['Predicted'])
    x2.index = lr_prediction.index
    lr_prediction['Original'] = x2['humidity']

    lr_prediction['diff'] = lr_prediction['Predicted'] - lr_prediction['Original']
    lr_prediction['diff'] = abs(lr_prediction['diff'])

    average_error = lr_prediction['diff'].sum()
    average_error = average_error / forecast_out
    max_difference = lr_prediction['diff'].max()

    print('Average Error =', average_error)
    print('Max Difference =', max_difference)
