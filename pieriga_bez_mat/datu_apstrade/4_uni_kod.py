import pandas as pd

# Ieejas fails, kas satur darījumus
file1 = 'pieriga_bez_mat/datu_apstrade/2024_kodi.csv'
# Izejas fails, kurā būs visi būves ārsienu materiālu kodi
file2 = 'pieriga_bez_mat/datu_apstrade/2024_uni.csv'

df = pd.read_csv(file1, sep=';')

# Pārveido kolonnas 'Būves ārsienu materiāla nosaukums' vērtības par sarakstu
visi_kodi = df['Būves ārsienu materiāla nosaukums'].dropna().str.split(',').explode().str.strip()

# Iegūst unikālos kodus
uni_kodi = visi_kodi.unique()

# Izveido datu kopu ar visiem unikālajiem kodiem
uni_kodi_df = pd.DataFrame(uni_kodi, columns=['uni_kods'])

uni_kodi_df.to_csv(file2, index=False)
