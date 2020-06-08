# -*- coding: utf-8 -*-
"""
Created on Wed, Apr 15 2020

Author: Sughosh Sudhanvan
"""

from wwo_hist import retrieve_hist_data
from dotenv import load_dotenv

from settings import *

load_dotenv()

os.chdir(DATA_URL)

frequency = 24
start_date = '1-JAN-2010'
end_date = '20-MAY-2020'
api_key = os.getenv("SECRET_KEY")


def get_data(place):
    location_list = [place]
    hist_weather_data = retrieve_hist_data(api_key,
                                           location_list,
                                           start_date,
                                           end_date,
                                           frequency,
                                           location_label=False,
                                           export_csv=True,
                                           store_df=True)
