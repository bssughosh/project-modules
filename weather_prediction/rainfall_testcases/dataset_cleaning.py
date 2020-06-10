# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 12:36:09 2020

Author: Sughosh Sudhanvan
"""

import pandas as pd
import numpy as np

from settings import *


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

file = os.path.join(os.getcwd(), 'naming.xlsx')
naming = pd.read_excel(file, sheet_name='Sheet1')

states = naming[:]['State'].to_list()
old = naming[:]['Old'].to_list()
new = naming[:]['New'].to_list()

not_performed_changes = []

for i, j in enumerate(old):
    if len(set(df.loc[df.District == j, 'State'].to_list())) == 1:
        df['District'].replace(j, new[i], inplace=True)
    else:
        not_performed_changes.append(j)

df['State'].replace('uttaranchal', 'uttarakhand', inplace=True)
df['State'].replace('chattisgarh', 'chhattisgarh', inplace=True)
df['State'].replace('nct of delhi', 'delhi', inplace=True)

df.to_csv('rainfall_data.csv', index=False)
