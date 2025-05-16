import pandas as pd
from datetime import datetime

# Ieejas fails, kas satur darījumus
file1 = 'valstspilsetas_bez/datu_apstrade/2024_fin.csv'
# Izvades fails, kas saturēs datus, ar pievienoto gadu un sezonu
file2 = 'valstspilsetas_bez/2024_gg.csv'

df = pd.read_csv(file1, sep=';')

df['Telpu grupas vidējais stāvs'] = (df['Telpu grupas zemākais stāvs'] + df['Telpu grupas augstākais stāvs']) / 2

del_col = ['Būves apbūves laukums, m2', 'Būves būvtilpums, m3', 'Telpu grupas augstākais stāvs', 'Telpu grupas zemākais stāvs', 'Dzīvokļa kopplatība, m2']

df = df.drop(columns=del_col) # No datu kopas noņem nevajadzīgās kolonas

# Iegūst gadu un mēnesi no 'Darījuma datums' kolonas
df['Gads'] = df['Darījuma datums'].apply(lambda x: datetime.strptime(x, '%d.%m.%Y').year)
df['Mēnesis'] = df['Darījuma datums'].apply(lambda x: datetime.strptime(x, '%d.%m.%Y').month)

# Mēnesim piešķir sezonu
sezonas = []
for menesis in df['Mēnesis']:
    if menesis in [12, 1, 2]:
        sezonas.append('Ziema')
    elif menesis in [3, 4, 5]:
        sezonas.append('Pavasaris')
    elif menesis in [6, 7, 8]:
        sezonas.append('Vasara')
    elif menesis in [9, 10, 11]:
        sezonas.append('Rudens')

# Pievieno jaunu kolonu 'Sezona'
df['Sezona'] = sezonas

# Veic one-hot encoding kolonai 'Sezona', izveidojot atsevišķu kolonu katrai sezonai
df = pd.get_dummies(df, columns=['Sezona'], prefix='sezona', dtype=int)

# Izdzēš nevajadzīgās kolonnas
df = df.drop(columns=['Darījuma datums', 'Mēnesis'])

df.to_csv(file2, index=False, sep=';')
