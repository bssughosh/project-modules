import pandas as pd
import numpy as np

from settings import *
from weather_prediction.fetch_weather_data import get_data
from weather_prediction.temperature import temp_call
from weather_prediction.humidity import humidity_call
from weather_prediction.rainfall import rain_call_g100, rain_call_g5

pd.options.mode.chained_assignment = None

available_temp = ['bhopal', 'manali', 'ooty', 'rajkot', 'sangli']
available_humidity = ['bhopal', 'manali', 'ooty', 'rajkot', 'sangli']
available_rainfall = ['bhopal', 'manali', 'ooty', 'rajkot', 'sangli']


def temperature_prediction(place, state, s_month, e_month):
    places = available_temp

    if place in places:
        file = os.path.join(DATA_URL, 'temp_pred', '{},{}.csv'.format(place, state))
        t = pd.read_csv(file)
        s_month = s_month - 5
        e_month = e_month - 5

        req = np.array(t.iloc[s_month:e_month + 1, 0])
        print(req)
    else:
        get_data(place)
        temp_call(place, state)
        available_temp.append(place)
        temperature_prediction(place, state, s_month, e_month)


def humidity_prediction(place, state, s_month, e_month):
    places = available_humidity

    if place in places:
        file = os.path.join(DATA_URL, 'humidity_pred', '{},{}.csv'.format(place, state))
        t = pd.read_csv(file)
        s_month = s_month - 5
        e_month = e_month - 5

        req = np.array(t.iloc[s_month:e_month + 1, 0])
        print(req)
    else:
        get_data(place)
        humidity_call(place, state)
        available_humidity.append(place)
        humidity_prediction(place, state, s_month, e_month)


def rainfall_prediction(district, state, s_month, e_month):
    file = os.path.join(DATA_URL, 'g.csv')
    g = pd.read_csv(file)
    df1 = g[g['State'] == state]
    df1 = df1[df1['District'] == district]

    for i, j in df1.iterrows():
        if j[3:].min() >= 100:
            if district in available_rainfall:
                file = os.path.join(DATA_URL, '{},{}.csv'.format(district, state))
                t = pd.read_csv(file)
                s_month = s_month - 5
                e_month = e_month - 5

                req = np.array(t.iloc[s_month:e_month + 1, 0])
                print(req)
            else:
                rain_call_g100(state, district)
                available_rainfall.append(district)
                rainfall_prediction(district, state, s_month, e_month)
        elif j[3:].min() > 5:
            if district in available_rainfall:
                file = os.path.join(DATA_URL, '{},{}.csv'.format(district, state))
                t = pd.read_csv(file)
                s_month = s_month - 5
                e_month = e_month - 5

                req = np.array(t.iloc[s_month:e_month + 1, 0])
                print(req)
            else:
                rain_call_g5(state, district)
                available_rainfall.append(district)
                rainfall_prediction(district, state, s_month, e_month)
        else:
            if district in available_rainfall:
                file = os.path.join(DATA_URL, '{},{}.csv'.format(district, state))
                t = pd.read_csv(file)
                s_month = s_month - 5
                e_month = e_month - 5

                req = np.array(t.iloc[s_month:e_month + 1, 0])
                print(req)
            else:
                rain_call_g5(state, district)
                available_rainfall.append(district)
                rainfall_prediction(district, state, s_month, e_month)
