import pandas as pd
from datetime import datetime

# Ieejas fails, kas satur darījumus
file1 = 'pieriga_bez_sez1/datu_apstrade/2024_fin.csv'
# Izvades fails, kas saturēs datus, ar pievienoto gadu un sezonu
file2 = 'pieriga_bez_sez1/2024_gg.csv'

df = pd.read_csv(file1, sep=';')

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
