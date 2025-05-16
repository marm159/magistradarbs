import pandas as pd

# Ieejas fails, kas satur darījumus
file1 = 'pieriga_ar_mat/datu_apstrade/2024_kodi.csv'
# Izejas fails, kas saturēs darījumus ar materiālu kodiem veiktu multi-hot encoding
file2 = 'pieriga_ar_mat/2024_mat.csv'

df = pd.read_csv(file1, sep=';',)

# Pārvērš kolonnu 'Būves ārsienu materiāla nosaukums' uz teksta (str) tipu
df['Būves ārsienu materiāla nosaukums'] = df['Būves ārsienu materiāla nosaukums'].astype(str)

# Sadala katras rindas materiāla kodus pēc komatiem un saglabā tos kā sarakstus kolonnā 'Būves_kodi'
df['Būves_kodi'] = df['Būves ārsienu materiāla nosaukums'].str.split(',')
                           
# Saraksts ar materiālu kodiem, kurus izmantos priekš multi-hot encoding
mat_kodi = [
    223, 238, 214, 212, 215, 232, 243, 537, 213, 211, 545, 227, 216, 226, 224, 222, 231, 244, 241, 235, 234
]

# Pārvērš materiālu kodus par str tipa vērtībām
mat_kodi = [str(kods) for kods in mat_kodi]

# Veic multi-hot encoding katram materiāla kodam
for kods in mat_kodi:
    df[f'mat_{kods}'] = df['Būves_kodi'].apply(lambda x: 1 if kods in x else 0)

# Izdzēš nevajdzīgās kolonnas
df = df.drop(columns=['Būves_kodi', 'Būves ārsienu materiāla nosaukums'])

df.to_csv(file2, index=False, sep=';')