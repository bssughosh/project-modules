# -*- coding: utf-8 -*-
"""
Created on Wed Jul 09, 2020

Author: Sughosh Sudhanvan
"""

import pandas as pd
import numpy as np
from sklearn.svm import SVR

from settings import *

pd.options.mode.chained_assignment = None

file1 = os.path.join(DATA_URL, 'Master_data_1.csv')
crops = pd.read_csv(file1)
file2 = os.path.join(DATA_URL, 'rainfall_data.csv')
rain = pd.read_csv(file2)

selected_state = 'maharashtra'
selected_district = 'buldana'
selected_season = 'Rabi'

rain_filtered = rain[rain['State'] == selected_state]
rain_filtered = rain_filtered[rain_filtered['District'] == selected_district]
rain_filtered = rain_filtered.sort_values('Year')
rain_filtered.reset_index(drop=True, inplace=True)

crop_filtered = crops[crops['State_Name'] == selected_state]
crop_filtered = crop_filtered[crop_filtered['District_Name'] == selected_district]
crop_filtered['Season'] = crop_filtered['Season'].apply(lambda x: x.strip())
crop_filtered = crop_filtered[crop_filtered['Season'] == selected_season]
crop_filtered['Frac'] = crop_filtered['Production'] / crop_filtered['Area']

# u_c = list(crop_filtered['Crop'].unique())
u_c = ['Jowar']

for c in u_c:
    df1 = crop_filtered[crop_filtered['Crop'] == c]
    df2 = df1[:]
    for i, j in df1.iterrows():
        df3 = rain_filtered[rain_filtered['Year'] == j[2]]
        df4 = rain_filtered[rain_filtered['Year'] == (j[2] + 1)]

        df2.loc[i, 'Jan1'] = float(df3['Jan'])
        df2.loc[i, 'Feb1'] = float(df3['Feb'])
        df2.loc[i, 'Mar1'] = float(df3['Mar'])
        df2.loc[i, 'Apr1'] = float(df3['Apr'])
        df2.loc[i, 'May1'] = float(df3['May'])
        df2.loc[i, 'Jun1'] = float(df3['Jun'])
        df2.loc[i, 'Jul1'] = float(df3['Jul'])
        df2.loc[i, 'Aug1'] = float(df3['Aug'])
        df2.loc[i, 'Sep1'] = float(df3['Sep'])
        df2.loc[i, 'Oct1'] = float(df3['Oct'])
        df2.loc[i, 'Nov1'] = float(df3['Nov'])
        df2.loc[i, 'Dec1'] = float(df3['Dec'])

        df2.loc[i, 'Jan2'] = float(df4['Jan'])
        df2.loc[i, 'Feb2'] = float(df4['Feb'])
        df2.loc[i, 'Mar2'] = float(df4['Mar'])
        df2.loc[i, 'Apr2'] = float(df4['Apr'])
        df2.loc[i, 'May2'] = float(df4['May'])
        df2.loc[i, 'Jun2'] = float(df4['Jun'])
        df2.loc[i, 'Jul2'] = float(df4['Jul'])
        df2.loc[i, 'Aug2'] = float(df4['Aug'])
        df2.loc[i, 'Sep2'] = float(df4['Sep'])
        df2.loc[i, 'Oct2'] = float(df4['Oct'])
        df2.loc[i, 'Nov2'] = float(df4['Nov'])
        df2.loc[i, 'Dec2'] = float(df4['Dec'])

    x = []
    t = []
    for i, j in df2.iterrows():
        if j[2] == 2014:
            t.append(j)
        else:
            x.append(j)
    forecast_out = 1
    x1 = pd.DataFrame(x, columns=df2.columns)
    x2 = pd.DataFrame(t, columns=df2.columns)
    x1['prediction'] = x1[['Frac']].shift(-forecast_out)
    X = np.array(x1.drop(['State_Name', 'District_Name', 'Crop_Year', 'Season', 'Crop', 'Production', 'prediction'], 1))
    y = np.array(x1['prediction'])

    X = X[:-forecast_out]
    y = y[:-forecast_out]
    k = 300

    mini = (np.Infinity, np.Infinity)
    ind = k
    while k <= 3000:
        svm = SVR(kernel='rbf', C=k)
        svm.fit(X, y)

        x_forecast = np.array(
            x1.drop(['State_Name', 'District_Name', 'Crop_Year', 'Season', 'Crop', 'Production', 'prediction'], 1))[
                     -forecast_out:]
        s_p = svm.predict(x_forecast)

        s_p = pd.DataFrame(s_p, columns=['Predicted'])
        x2.index = s_p.index

        s_p['Original'] = x2['Frac']
        s_p['diff'] = s_p['Predicted'] - s_p['Original']
        s_p['diff'] = abs(s_p['diff'])

        average_error = s_p['diff'].sum()
        average_error = average_error / forecast_out
        max_difference = s_p['diff'].max()

        if average_error < mini[0]:
            mini = (average_error, max_difference)
            ind = k
        elif average_error == mini[0]:
            if max_difference < mini[1]:
                mini = (average_error, max_difference)
                ind = k
        k += 1

for c in u_c:
    df1 = crop_filtered[crop_filtered['Crop'] == c]
    df2 = df1[:]
    for i, j in df1.iterrows():
        df3 = rain_filtered[rain_filtered['Year'] == j[2]]
        df4 = rain_filtered[rain_filtered['Year'] == (j[2] + 1)]

        df2.loc[i, 'Jan1'] = float(df3['Jan'])
        df2.loc[i, 'Feb1'] = float(df3['Feb'])
        df2.loc[i, 'Mar1'] = float(df3['Mar'])
        df2.loc[i, 'Apr1'] = float(df3['Apr'])
        df2.loc[i, 'May1'] = float(df3['May'])
        df2.loc[i, 'Jun1'] = float(df3['Jun'])
        df2.loc[i, 'Jul1'] = float(df3['Jul'])
        df2.loc[i, 'Aug1'] = float(df3['Aug'])
        df2.loc[i, 'Sep1'] = float(df3['Sep'])
        df2.loc[i, 'Oct1'] = float(df3['Oct'])
        df2.loc[i, 'Nov1'] = float(df3['Nov'])
        df2.loc[i, 'Dec1'] = float(df3['Dec'])

        df2.loc[i, 'Jan2'] = float(df4['Jan'])
        df2.loc[i, 'Feb2'] = float(df4['Feb'])
        df2.loc[i, 'Mar2'] = float(df4['Mar'])
        df2.loc[i, 'Apr2'] = float(df4['Apr'])
        df2.loc[i, 'May2'] = float(df4['May'])
        df2.loc[i, 'Jun2'] = float(df4['Jun'])
        df2.loc[i, 'Jul2'] = float(df4['Jul'])
        df2.loc[i, 'Aug2'] = float(df4['Aug'])
        df2.loc[i, 'Sep2'] = float(df4['Sep'])
        df2.loc[i, 'Oct2'] = float(df4['Oct'])
        df2.loc[i, 'Nov2'] = float(df4['Nov'])
        df2.loc[i, 'Dec2'] = float(df4['Dec'])

    x = []
    t = []
    for i, j in df2.iterrows():
        if j[2] == 2014:
            t.append(j)
        else:
            x.append(j)
    forecast_out = 1
    x1 = pd.DataFrame(x, columns=df2.columns)
    x2 = pd.DataFrame(t, columns=df2.columns)
    x1['prediction'] = x1[['Frac']].shift(-forecast_out)
    X = np.array(x1.drop(['State_Name', 'District_Name', 'Crop_Year', 'Season', 'Crop', 'Production', 'prediction'], 1))
    y = np.array(x1['prediction'])

    X = X[:-forecast_out]
    y = y[:-forecast_out]
    svm = SVR(kernel='rbf', C=ind)
    svm.fit(X, y)

    x_forecast = np.array(
        x1.drop(['State_Name', 'District_Name', 'Crop_Year', 'Season', 'Crop', 'Production', 'prediction'], 1))[
                 -forecast_out:]
    s_p = svm.predict(x_forecast)
