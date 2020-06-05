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

file = os.path.join(DATA_URL, 'rainfall_data.csv')
df = pd.read_csv(file)

df.replace('N.A.', np.nan, inplace=True)

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
selected_state = 'gujarat'
selected_district = 'rajkot'
selected_month = months[6]


def name_preprocessing(name):
    name = name.lower()
    name = name.replace('&', 'and')
    name = name.strip()
    return name


df[months] = df[months].astype(float)
df[['Year']] = df[['Year']].round(0).astype(str)

df['Year'] = df['Year'].apply(lambda year: year.split('.')[0])
df['State'] = df['State'].apply(lambda state: name_preprocessing(state))
df['District'] = df['District'].apply(lambda district: name_preprocessing(district))

df1 = df[df['State'] == selected_state]
df2 = df1[df1['District'] == selected_district]
df3 = df2[['Year', selected_month]]
df3 = pd.DataFrame(df3, columns=['Year', selected_month])

x = []
for i, j in df3.iterrows():
    x.append(j)

x1 = pd.DataFrame(x, columns=['Year', selected_month])

forecast_out = 10
x1['prediction'] = x1[['Jul']].shift(-forecast_out)

X = np.array(x1.drop(['Year', 'prediction'], 1))
X = X[:-forecast_out]

y = np.array(x1['prediction'])
y = y[:-forecast_out]

svm = SVR(kernel='rbf', C=1000)
svm.fit(X, y)

x_forecast = np.array(x1.drop(['Year', 'prediction'], 1))[-forecast_out:]
svm_prediction = svm.predict(x_forecast)
