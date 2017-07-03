#!/usr/bin/env python
# encoding: utf-8

import pandas as pd

df = pd.read_csv("/Users/JRLetelier/perso/sonification/data/sources/audiens/effectifis.csv",
                 sep=";", engine='python')
df = df[["country", "indicator", "time", "value"]].drop(0).dropna()

df.columns = ['country', 'indicator', 'time', 'value']

df = df[df.indicator != '0']

df['time'] = df['time'].apply(int)

# df['indicator'] = df['indicator'].apply(lambda x: x.decode('ascii', errors='replace'))
df['indicator'] = df['indicator'].apply(lambda x: "Art workers "+x)
df['indicator'] = df['indicator'].apply(lambda x: x.replace('   ', ' '))
df['indicator'] = df['indicator'].apply(lambda x: x.replace(' ', '_'))
df['indicator'] = df['indicator'].apply(lambda x: x.replace('(*)', ''))

df['value'] = df['value'].apply(lambda x: x.replace(',', '.')).apply(float)


df.to_csv("/Users/JRLetelier/perso/sonification/data/m4l/audiens/audiens_effectifis_2010.tsv",
          header=False, index=False, sep='\t')

print df.head(3)