# -*- coding: utf-8 -*-
"""
Created on Mon May 25, 2020

Author: Sughosh Sudhanvan
"""

import pandas as pd
import numpy as np
from sklearn.svm import SVR

pd.options.mode.chained_assignment = None

df = pd.read_csv('../../../datasets/mumbai.csv')

df['date_time'] = pd.to_datetime(df['date_time'])

cols_s = [['date_time', 'maxtempC', 'mintempC', 'cloudcover', 'windspeedKmph', 'visibility', 'tempC'],
          ['date_time', 'maxtempC', 'mintempC', 'cloudcover', 'visibility', 'windspeedKmph', 'FeelsLikeC', 'tempC'],
          ['date_time', 'maxtempC', 'mintempC', 'cloudcover', 'windspeedKmph', 'FeelsLikeC', 'tempC'],
          ['date_time', 'maxtempC', 'mintempC', 'cloudcover', 'windspeedKmph', 'tempC'],
          ['date_time', 'maxtempC', 'mintempC', 'cloudcover', 'windspeedKmph', 'humidity', 'tempC']]
cols1 = [['maxtempC', 'mintempC', 'cloudcover', 'windspeedKmph', 'visibility', 'tempC'],
         ['maxtempC', 'mintempC', 'cloudcover', 'visibility', 'windspeedKmph', 'FeelsLikeC', 'tempC'],
         ['maxtempC', 'mintempC', 'cloudcover', 'windspeedKmph', 'FeelsLikeC', 'tempC'],
         ['maxtempC', 'mintempC', 'cloudcover', 'windspeedKmph', 'tempC'],
         ['maxtempC', 'mintempC', 'cloudcover', 'windspeedKmph', 'humidity', 'tempC']]
cols2 = [['year', 'month', 'maxtempC', 'mintempC', 'cloudcover', 'windspeedKmph', 'visibility', 'tempC'],
         ['year', 'month', 'maxtempC', 'mintempC', 'cloudcover', 'visibility', 'windspeedKmph', 'FeelsLikeC', 'tempC'],
         ['year', 'month', 'maxtempC', 'mintempC', 'cloudcover', 'windspeedKmph', 'FeelsLikeC', 'tempC'],
         ['year', 'month', 'maxtempC', 'mintempC', 'cloudcover', 'windspeedKmph', 'tempC'],
         ['year', 'month', 'maxtempC', 'mintempC', 'cloudcover', 'windspeedKmph', 'humidity', 'tempC']]
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
    x1['prediction'] = x1[['tempC']].shift(-forecast_out)

    X = np.array(x1.drop(['prediction', 'year', 'month'], 1))
    X = X[:-forecast_out]

    y = np.array(x1['prediction'])
    y = y[:-forecast_out]

    i = 300
    mini = (np.Infinity, np.Infinity)
    ind = i
    while i <= 3000:
        svm = SVR(kernel='rbf', C=i)
        svm.fit(X, y)

        x_forecast = np.array(x1.drop(['prediction', 'year', 'month'], 1))[-forecast_out:]
        svm_prediction = svm.predict(x_forecast)

        svm_prediction = svm_prediction.astype('int8')
        svm_prediction = pd.DataFrame(svm_prediction, columns=['Predicted'])
        x2.index = svm_prediction.index
        svm_prediction['Original'] = x2['tempC']

        svm_prediction['diff'] = svm_prediction['Predicted'] - svm_prediction['Original']
        svm_prediction['diff'] = abs(svm_prediction['diff'])

        average_error = svm_prediction['diff'].sum()
        max_difference = svm_prediction['diff'].max()
        average_error = average_error / forecast_out
        if average_error < mini[0]:
            mini = (average_error, max_difference)
            ind = i
        elif average_error == mini[0]:
            if max_difference < mini[1]:
                mini = (average_error, max_difference)
                ind = i
        print(i)
        i += 1
    print('Minimum Values (Average error, Max_difference) =', mini)
    print('C value for optimized result =', ind)
