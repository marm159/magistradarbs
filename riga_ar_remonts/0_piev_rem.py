import pandas as pd
from datetime import datetime

# Ielādē sākotnējo datu kopu, kas satur darījumu datus
file1 = pd.read_csv('riga_ar_remonts/datu_apstrade/dati_fin.csv', sep=';')
# Ielādē datu kopu, kas satur vienādos dzīvokļus un informāciju par remontu
file2 = pd.read_csv('riga_ar_remonts/dati_eka.csv', sep=';')

# Atlasa visas kolonas, izņemot kolonu 'Remonts'
apv_col = [col for col in file2.columns if col != 'Remonts']

# Apvieno abas datu kopas pēc atbilstošajām kolonnām un pievieno 'Remonts' kolonnu
df_rem = pd.merge(file1, file2.drop_duplicates(subset=apv_col), on=apv_col, how='left')

# Pārvērš kolonas 'Remonts' vērtības par int tipa, ja ir tukša vērtība, ievieto 'NULL'
df_rem['Remonts'] = df_rem['Remonts'].apply(lambda x: int(x) if pd.notnull(x) else 'NULL')

df_rem['Telpu grupas vidējais stāvs'] = (df_rem['Telpu grupas zemākais stāvs'] + df_rem['Telpu grupas augstākais stāvs']) / 2

del_col = ['Būves apbūves laukums, m2', 'Būves būvtilpums, m3', 'Telpu grupas augstākais stāvs', 'Telpu grupas zemākais stāvs', 'Dzīvokļa kopplatība, m2']

df_rem = df_rem.drop(columns=del_col)  # No datu kopas noņem nevajadzīgās kolonas


# Iegūst gadu un mēnesi no 'Darījuma datums' kolonas
df_rem['Gads'] = df_rem['Darījuma datums'].apply(lambda x: datetime.strptime(x, '%d.%m.%Y').year)
df_rem['Mēnesis'] = df_rem['Darījuma datums'].apply(lambda x: datetime.strptime(x, '%d.%m.%Y').month)

# Mēnesim piešķir sezonu
sezonas = []
for menesis in df_rem['Mēnesis']:
    if menesis in [12, 1, 2]:
        sezonas.append('Ziema')
    elif menesis in [3, 4, 5]:
        sezonas.append('Pavasaris')
    elif menesis in [6, 7, 8]:
        sezonas.append('Vasara')
    elif menesis in [9, 10, 11]:
        sezonas.append('Rudens')

# Pievieno jaunu kolonu 'Sezona'
df_rem['Sezona'] = sezonas

# Veic one-hot encoding kolonai 'Sezona', izveidojot atsevišķu kolonu katrai sezonai
df_rem = pd.get_dummies(df_rem, columns=['Sezona'], prefix='sezona', dtype=int)

# Izdzēš nevajadzīgās kolonnas
df_rem = df_rem.drop(columns=['Darījuma datums', 'Mēnesis'])

df_rem.to_csv('riga_ar_remonts/dati_remonts.csv', sep=';', index=False)

