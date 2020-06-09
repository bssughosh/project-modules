# -*- coding: utf-8 -*-
"""
Created on Sat Jun 6, 2020

Author: Sughosh Sudhanvan
"""

import pandas as pd
import numpy as np

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

g = df.groupby(['State', 'District'], as_index=False).count()
file = os.path.join(DATA_URL, 'g.csv')
g.to_csv(file, index=False)

g100 = []  # Greater than 100
g5 = []  # Greater than 5 but less than 100
le5 = []  # Less than or equal to 5

for i, j in g.iterrows():
    if j[3:].min() >= 100:
        g100.append(j)
    elif j[3:].min() > 5:
        g5.append(j)
    else:
        le5.append(j)

g100 = pd.DataFrame(g100)
g5 = pd.DataFrame(g5)
le5 = pd.DataFrame(le5)

g100s = g100[:]['State'].to_list()
g100d = g100[:]['District'].to_list()
g5s = g5[:]['State'].to_list()
g5d = g5[:]['District'].to_list()
le5s = le5[:]['State'].to_list()
le5d = le5[:]['District'].to_list()

for x, y in zip(g100d, g100s):
    df1 = df[df['State'] == y]
    df1 = df1[df1['District'] == x]
    file = os.path.join(DATA_URL, 'g100.csv')
    df1.to_csv(file, mode='a', header=False, index=False)

for x, y in zip(g5d, g5s):
    df1 = df[df['State'] == y]
    df1 = df1[df1['District'] == x]
    file = os.path.join(DATA_URL, 'g5.csv')
    df1.to_csv(file, mode='a', header=False, index=False)

for x, y in zip(le5d, le5s):
    df1 = df[df['State'] == y]
    df1 = df1[df1['District'] == x]
    file = os.path.join(DATA_URL, 'le5.csv')
    df1.to_csv(file, mode='a', header=False, index=False)
