# -*- coding: utf-8 -*-
"""
Created on Tue Jun 2, 2020

Author: Sughosh Sudhanvan
"""

import pandas as pd
import numpy as np
from sklearn.svm import SVR

from settings import *

pd.options.mode.chained_assignment = None


def name_preprocessing(name):
    name = name.lower()
    name = name.replace('&', 'and')
    name = name.strip()
    return name


file = os.path.join(DATA_URL, 'rainfall_data.csv')
df = pd.read_csv(file)

df.replace('N.A.', np.nan, inplace=True)

months = ['Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May']
df[months] = df[months].astype(float)
df[['Year']] = df[['Year']].round(0).astype(str)

df['Year'] = df['Year'].apply(lambda year: year.split('.')[0])
df['State'] = df['State'].apply(lambda state: name_preprocessing(state))
df['District'] = df['District'].apply(lambda district: name_preprocessing(district))


def rain_call_g100(state, district):
    selected_state = state
    selected_district = district
    vals = []
    for month_loc, selected_month in enumerate(months):
        df1 = df[df['State'] == selected_state]
        df2 = df1[df1['District'] == selected_district]
        df3 = df2[['Year', selected_month]]
        df3 = pd.DataFrame(df3, columns=['Year', selected_month])

        x = []
        for i, j in df3.iterrows():
            x.append(j)

        x1 = pd.DataFrame(x, columns=['Year', selected_month])
        if month_loc <= 6:
            forecast_out = 2020 - int(x1.iloc[-1, 0])
        else:
            forecast_out = 2021 - int(x1.iloc[-1, 0])
        x1['prediction'] = x1[['Jul']].shift(-forecast_out)

        X = np.array(x1.drop(['Year', 'prediction'], 1))
        X = X[:-forecast_out]

        y = np.array(x1['prediction'])
        y = y[:-forecast_out]

        svm = SVR(kernel='rbf', C=1000)
        svm.fit(X, y)

        x_forecast = np.array(x1.drop(['Year', 'prediction'], 1))[-forecast_out:]
        svm_prediction = svm.predict(x_forecast)
        vals.append(svm_prediction[-1])

    vals = pd.DataFrame(vals, columns=['Predicted'])
    new_file = os.path.join(DATA_URL, 'rain_pred', '{},{}.csv'.format(selected_district, selected_state))
    vals.to_csv(new_file, index=False, header=True)
