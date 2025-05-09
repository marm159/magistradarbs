import pandas as pd
from datetime import datetime

# Ieejas fails, kas satur darījumus
file1 = 'vert_pilsetas_ar/datu_apstrade/2024_fin.csv'
# Izvades fails, kas saturēs datus, ar pievienoto gadu un sezonu
file2 = 'vert_pilsetas_ar/2024_gg.csv'

df = pd.read_csv(file1, sep=';')

df['Telpu grupas vidējais stāvs'] = (df['Telpu grupas zemākais stāvs'] + df['Telpu grupas augstākais stāvs']) / 2

del_col = ['Būves apbūves laukums, m2', 'Būves būvtilpums, m3', 'Telpu grupas augstākais stāvs', 'Telpu grupas zemākais stāvs', 'Dzīvokļa kopplatība, m2']

df = df.drop(columns=del_col)  # No apmācību kopas noņem darījuma summu un pārējās nevajadzīgās kolonas

# Iegūst gadu un mēnesi no 'Darījuma datums' kolonas
df['Gads'] = df['Darījuma datums'].apply(lambda x: datetime.strptime(x, "%d.%m.%Y").year if pd.notna(x) else "")
df['Mēnesis'] = df['Darījuma datums'].apply(lambda x: datetime.strptime(x, "%d.%m.%Y").month if pd.notna(x) else "")

# Mēnesim piešķir sezonu
sezonas = []
for mēnesis in df['Mēnesis']:
    if mēnesis in [12, 1, 2]:
        sezonas.append("Ziema")
    elif mēnesis in [3, 4, 5]:
        sezonas.append("Pavasaris")
    elif mēnesis in [6, 7, 8]:
        sezonas.append("Vasara")
    elif mēnesis in [9, 10, 11]:
        sezonas.append("Rudens")
    else:
        sezonas.append("")

# Pievieno jaunu kolonu 'Sezona'
df['Sezona'] = sezonas

# Veic one-hot encoding kolonai 'Sezona', izveidojot atsevišķu kolonu katrai sezonai
df = pd.get_dummies(df, columns=['Sezona'], prefix='sezona', dtype=int)

# Izdzēš nevajadzīgās kolonnas
df = df.drop(columns=['Darījuma datums', 'Mēnesis'])

# Saglabā rezultātu jaunā CSV failā
df.to_csv(file2, index=False, sep=';')
