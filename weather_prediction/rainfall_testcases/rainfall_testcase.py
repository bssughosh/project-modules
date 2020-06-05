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
t = []
for i, j in df3.iterrows():
    # if j[0] == '2008':
    #     t.append(j)
    # elif j[0] == '2010' or j[0] == '2009':
    #     pass
    x.append(j)

del x[0]
x1 = pd.DataFrame(x, columns=['Year', selected_month])
# x2 = pd.DataFrame(t, columns=['Year',selected_month])

forecast_out = 10
x1['prediction'] = x1[[selected_month]].shift(-forecast_out)

X = np.array(x1.drop(['Year', 'prediction'], 1))
X = X[:-forecast_out]

y = np.array(x1['prediction'])
y = y[:-forecast_out]

svm = SVR(kernel='rbf', C=1000)
svm.fit(X, y)

x_forecast = np.array(x1.drop(['Year', 'prediction'], 1))[-forecast_out:]
svm_prediction = svm.predict(x_forecast)

# i = 300
# mini = [np.inf, np.inf, 0]
# ind = i
# while i<=3000:
#     svm = SVR(kernel='rbf', C=i)
#     svm.fit(X, y)

#     x_forecast = np.array(x1.drop(['Year','prediction'], 1))[-forecast_out:]
#     svm_prediction = svm.predict(x_forecast)

#     svm_prediction = pd.DataFrame(svm_prediction, columns=['Predicted'])
#     x2.index = svm_prediction.index

#     svm_prediction['Original'] = x2[selected_month]
#     svm_prediction['diff'] = abs(svm_prediction['Predicted'] - svm_prediction['Original'])

#     average_error = svm_prediction['diff'].sum()
#     max_difference = svm_prediction['diff'].max()
#     average_error = average_error / forecast_out
#     if average_error < mini[0]:
#         mini[0] = average_error
#         mini[1] = max_difference
#         mini[2] = svm_prediction.iloc[0,0]
#         ind = i
#     elif average_error == mini[0] and max_difference < mini[1]:
#         mini[0] = average_error
#         mini[1] = max_difference
#         mini[2] = svm_prediction.iloc[0,0]
#         ind = i

#     i += 1


# g = df.groupby(['State', 'District', 'Year'], as_index=False)

# x = []
# y = np.array(g)
# for i,j in g:
#     x.append(np.array(j))

# x = np.array(x)
