import requests
import json
import pandas as pd

key = 'f825978565ab431e8de135522201404'
place = 'bengaluru'
start_d = '10-JAN-2010'
end_d = '10-MAY-2010'
url = 'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key={}&q={}&format=json&date={}&enddate={}&tp=24'.format(
    key, place, start_d, end_d)
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
op['month'] = op['date_time'].apply(lambda mon: mon.strftime('%m'))
print(op)
