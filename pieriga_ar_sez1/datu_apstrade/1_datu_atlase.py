import pandas as pd
import numpy as np

# Ieejas fails, kas satur visus darījumus
file1 = 'dati/TG_CSV_2023.csv'
# Izejas fails, kas saturēs tikai atlasītos darījumus
file2 = 'pieriga_ar_sez1/datu_apstrade/2023.csv'
# Ieejas fails, kas satur pilsētu koordinātes
file_k = 'dati/koordinates.csv'

df = pd.read_csv(file1, sep=';')

df_k = pd.read_csv(file_k)

# Noņem atstarpes no kolonnu nosaukuma sākuma un beigām
df.columns = df.columns.str.strip()

# Atlasa tikai darījumus, kas atbilst konkrētiem kritērijiem
df = df[
    (df['Būves lietošanas veida kods'] == 1122) &  # Triju vai vairāku dzīvokļu mājas
    (df['Telpu grupas lietošanas veida kods'] == 1122) &  # Dzīvojamo telpu grupa
    (df['Dzīvokļu skaits (viena darījuma ietvaros)'] == 1) &  # Darījuma ietvaros pārdots viens dzīvoklis
    (df['Istabu skaits dzīvoklī'] != 0) &  # Vismaz viena istaba
    (df['Pilsēta'].isin([
        'Ādaži', 'Baldone', 'Baloži', 'Ikšķile', 'Ķegums', 'Ķekava', 
        'Lielvārde', 'Mārupe', 'Olaine', 'Salaspils', 
        'Saulkrasti', 'Sigulda', 'Vangaži'
    ]))  &  # Atrodas kādā no Pierīgas pilsētām
    (df['Pārdotā zemes kopplatība, m2'] != 'NULL')  # Ar pārdoto zemi
]

# No kolonnas 'Būves ekspluatācijas uzsākšanas gads' paņem tikai pirmo gadu, ja ir doti divi gadi, piemēram, 1999, 2000 -> 1999
df['Būves ekspluatācijas uzsākšanas gads'] = df['Būves ekspluatācijas uzsākšanas gads'].astype(str).str.split(',').str[0]

# Pārveido kolonnu 'Būves ekspluatācijas uzsākšanas gads' par skaitlisku (ja nav būves gada, atstāj tukšu vērtību)
df['Būves ekspluatācijas uzsākšanas gads'] = pd.to_numeric(df['Būves ekspluatācijas uzsākšanas gads'], errors='coerce')

# Aizvieto visus komatus (,) ar punktiem (.)
df = df.astype(str).replace(',', '.', regex=True)

# Izdzēš nevajadzīgās kolonnas
rem_columns = [
    'Darījumu skaits atlasē', 'Darījuma ID', 'Objekts', 'Īpašuma kadastra numurs',
    'Adreses pieraksts', 'Novads', 'Pagasts',
    'Zemes vienību kadastra apzīmējumi(saraksts) (viena darījuma ietvaros)',
    'Zemes daļas(skaitītājs)', 'Zemes daļas(saucējs)', 'NĪLM grupas kods (lielākais pēc platības)',
    'NĪLM kodi(saraksts)', 'Būves kadastra apzīmējums', 'Būves daļas(skaitītājs)', 'Būves daļas(saucējs)',
    'Būves lietošanas veida nosaukums', 'Būves lietošanas veida kods', 'Būves ārsienu materiāla nosaukums',
    'Būves kadastra apzīmējumu saraksts (viena darījuma ietvaros)', 'Telpu grupu skaits (viena darījuma ietvaros)',
    'Dzīvokļu skaits (viena darījuma ietvaros)', 'Telpu grupas kadastra apzīmējums', 'Telpu grupas daļas(skaitītājs)',
    'Telpu grupas daļas(saucējs)', 'Telpu grupas lietošanas veida kods'
]
df = df.drop(columns=rem_columns)

# Pievieno pilsētu koordinātu kolonas
df = df.merge(df_k, left_on='Pilsēta', right_on='Pilseta', how='left')

# Izdzēš nevajadzīgās kolonnas
df = df.drop(columns=['Pilseta', 'Pilsēta'])

# Aizvieto teksta 'nan' ar NaN
df.replace('nan', np.nan, inplace=True)

# Izdzēš visas rindas, kurās ir vismaz viena NaN vērtība
df = df.dropna()

# Kolonas, kuru vērtības jāpārveido par veselu skaitli
conv_columns = [
    'Būves ekspluatācijas uzsākšanas gads',
    'Būvju skaits',
    'Būves virszemes stāvu skaits',
    'Telpu grupas zemākais stāvs',
    'Telpu grupas augstākais stāvs',
    'Telpu skaits telpu grupā',
    'Istabu skaits dzīvoklī',
    'Telpu skaits telpu grupā'
]

# Katras norādītās kolonas vērtību vispirms pārvērš par float, tad par int
for column in conv_columns:
    df[column] = df[column].astype('float').astype('int64')

df.to_csv(file2, sep=';', index=False)
