# -*- coding: utf-8 -*-
"""
Created on Wed, Apr 15 2020

Author: Sughosh Sudhanvan
"""

from dotenv import load_dotenv
import requests
import pandas as pd

from settings import *

load_dotenv()
# api_key = os.getenv("SECRET_KEY")
frequency = 24
api_key = '30b6a9ce351543f7b77151928202105'
start_date = '1-JAN-2010'
end_date = '20-MAY-2020'


def get_data(place):
    url = 'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key={}&q={}&format=json&date={}&enddate={}&tp=24'.format(
        api_key, place, start_date, end_date)
    res = requests.get(url).json()

    op = []
    for each in res['data']['weather']:
        row = {
            'date_time': each['date'],
            "maxtempC": each["maxtempC"],
            "mintempC": each["mintempC"],
            'tempC': each['hourly'][0]['tempC'],
            "windspeedKmph": each['hourly'][0]["windspeedKmph"],
            "winddirDegree": each['hourly'][0]["winddirDegree"],
            "precipMM": each['hourly'][0]["precipMM"],
            "humidity": each['hourly'][0]["humidity"],
            "visibility": each['hourly'][0]["visibility"],
            "pressure": each['hourly'][0]["pressure"],
            "cloudcover": each['hourly'][0]["cloudcover"],
            "FeelsLikeC": each['hourly'][0]["FeelsLikeC"],
            "DewPointC": each['hourly'][0]["DewPointC"]
        }
        op.append(row)

    op = pd.DataFrame(op)
    op['date_time'] = pd.to_datetime(op['date_time'])
    file = os.path.join(DATA_URL, '{}.csv'.format(place))
    op.to_csv(file, index=False, header=True, mode='a')


get_data('mangalore')
