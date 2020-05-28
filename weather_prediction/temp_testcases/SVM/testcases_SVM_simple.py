# -*- coding: utf-8 -*-
"""
Created on Sun May 17, 2020

Author: Sughosh Sudhanvan
"""

import pandas as pd
import numpy as np
from sklearn.svm import SVR

from settings import *

file = os.path.join(DATA_URL, 'manali.csv')
df = pd.read_csv(file)

df['date_time'] = pd.to_datetime(df['date_time'])

cols_s = [['date_time', 'maxtempC', 'mintempC', 'cloudcover', 'windspeedKmph', 'visibility', 'tempC'],
          ['date_time', 'maxtempC', 'mintempC', 'cloudcover', 'visibility', 'windspeedKmph', 'FeelsLikeC', 'tempC'],
          ['date_time', 'maxtempC', 'mintempC', 'cloudcover', 'windspeedKmph', 'FeelsLikeC', 'tempC'],
          ['date_time', 'maxtempC', 'mintempC', 'cloudcover', 'windspeedKmph', 'tempC'],
          ['date_time', 'maxtempC', 'mintempC', 'cloudcover', 'windspeedKmph', 'humidity', 'tempC']]

for cols in cols_s:
    df1 = df[cols]
    x = []
    t = []
    for i, j in df1.iterrows():
        if j[0].strftime('%Y') == '2020':
            t.append(j)
        else:
            x.append(j)

    x = np.array(x)
    x1 = pd.DataFrame(x, columns=cols)
    x2 = pd.DataFrame(t, columns=cols)
    forecast_out = 141
    x1['prediction'] = x1[['tempC']].shift(-forecast_out)

    X = np.array(x1.drop(['prediction', 'date_time'], 1))
    X = X[:-forecast_out]

    y = np.array(x1['prediction'])
    y = y[:-forecast_out]

    svm = SVR(kernel='rbf', C=100)
    svm.fit(X, y)

    x_forecast = np.array(x1.drop(['prediction', 'date_time'], 1))[-forecast_out:]
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

    print('a =', average_error)
    print('m =', max_difference)
