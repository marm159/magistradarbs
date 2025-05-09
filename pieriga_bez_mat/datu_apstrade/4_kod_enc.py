import pandas as pd

# Ieejas fails, kas satur darījumus
file1 = 'pieriga_bez_mat/datu_apstrade/2024_kodi.csv'
# Izejas fails, kas saturēs darījumus ar materiālu kodiem veiktu multi-hot encoding
file2 = 'pieriga_bez_mat/2024_mat.csv'

df = pd.read_csv(file1, sep=';',)

# Pārvērš kolonnu 'Būves ārsienu materiāla nosaukums' uz teksta (str) tipu
df['Būves ārsienu materiāla nosaukums'] = df['Būves ārsienu materiāla nosaukums'].astype(str)

# Sadala katras rindas materiāla kodus pēc komatiem un saglabā tos kā sarakstus kolonnā 'Būves_kodi'
df['Būves_kodi'] = df['Būves ārsienu materiāla nosaukums'].str.split(',')
                           
# Saraksts ar materiālu kodiem, kurus izmantos priekš multi-hot encoding
mat_kodi = [
    211, 212, 213, 214, 215, 216, 221, 222, 223, 224, 226, 227, 231, 232, 233, 234, 235, 236, 
    237, 238, 241, 242, 243, 244, 245, 111, 113, 331, 511, 521, 531, 532, 537, 541, 544, 545
]

# Pārvērš materiālu kodus par str tipa vērtībām
mat_kodi = [str(kods) for kods in mat_kodi]

# Veic multi-hot encoding katram materiāla kodam
for kods in mat_kodi:
    df[f'mat_{kods}'] = df['Būves_kodi'].apply(lambda x: 1 if kods in x else 0)

# Izdzēš nevajdzīgās kolonas
df.drop(columns=['Būves_kodi', 'Būves ārsienu materiāla nosaukums'], inplace=True)

# Saglabā apstrādātos datus jaunā CSV failā
df.to_csv(file2, index=False, sep=';')