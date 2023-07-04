import pandas as pd

df = pd.read_csv('data/11.csv')
print(df[df['DATATIME'].str.startswith('2021-11-01 01:15:00')].index[0])
start = df[df['DATATIME'].str.startswith('2021-11-01 01:15:00')].index[0]
end = df[df['DATATIME'].str.startswith('2021-11-01 03:00:00')].index[0]
print(df[start:end])
