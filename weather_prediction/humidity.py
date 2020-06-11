# -*- coding: utf-8 -*-
"""
Created on Tue May 26, 2020

Author: Sughosh Sudhanvan
"""

import pandas as pd
import numpy as np
import copy
from sklearn.svm import SVR

from settings import *

pd.options.mode.chained_assignment = None


def humidity_call(place, state):
    file = os.path.join(DATA_URL, '{}.csv'.format(place))
    df = pd.read_csv(file)

    df['date_time'] = pd.to_datetime(df['date_time'])

    cols_s = [['date_time', 'maxtempC', 'mintempC', 'humidity', 'tempC', 'pressure']]

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

        i = 1
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
            svm_prediction['Original'] = x2['humidity']

            svm_prediction['diff'] = svm_prediction['Predicted'] - svm_prediction['Original']
            svm_prediction['diff'] = abs(svm_prediction['diff'])

            average_error = svm_prediction['diff'].sum()
            average_error = average_error / forecast_out
            max_difference = svm_prediction['diff'].max()

            if average_error < mini[0]:
                mini = (average_error, max_difference)
                ind = i
            elif average_error == mini[0]:
                if max_difference < mini[1]:
                    mini = (average_error, max_difference)
                    ind = i
            i += 1

        x = []

        for i, j in df2.iterrows():
            x.append(j)

        x1 = pd.DataFrame(x, columns=cols2[test_loc])
        forecast_out = 12
        x1['prediction'] = x1[['humidity']].shift(-forecast_out)

        X = np.array(x1.drop(['prediction', 'year', 'month'], 1))
        X = X[:-forecast_out]

        y = np.array(x1['prediction'])
        y = y[:-forecast_out]
        svm = SVR(kernel='rbf', C=ind)
        svm.fit(X, y)

        x_forecast = np.array(x1.drop(['prediction', 'year', 'month'], 1))[-forecast_out:]
        svm_prediction = svm.predict(x_forecast)

        svm_prediction = svm_prediction.astype('int8')
        svm_prediction = pd.DataFrame(svm_prediction, columns=['Predicted'])

        new_file = os.path.join(DATA_URL, 'humidity_pred', '{},{}.csv'.format(place, state))
        svm_prediction.to_csv(new_file, index=False, header=True)
