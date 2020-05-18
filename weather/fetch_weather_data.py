# -*- coding: utf-8 -*-
"""
Created on Wed, Apr 15 2020

Author: Sughosh Sudhanvan
"""

from wwo_hist import retrieve_hist_data

frequency = 24
start_date = '1-JAN-2020'
end_date = '1-MAR-2020'
api_key = 'f825978565ab431e8de135522201404'
location_list = ['mumbai']
hist_weather_data = retrieve_hist_data(api_key,
                                       location_list,
                                       start_date,
                                       end_date,
                                       frequency,
                                       location_label=False,
                                       export_csv=True,
                                       store_df=True)
