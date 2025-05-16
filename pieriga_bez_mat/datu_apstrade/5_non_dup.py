import pandas as pd

# Ieejas fails, kas būves ārsienu materiāla nosaukuma kodus no apmācības un testa datu kopām
file1 = 'pieriga_bez_mat/datu_apstrade/dati_uni.csv'
# Izejas fails, kas būves ārsienu materiāla nosaukuma kodus bez dublikātiem
file2 = 'pieriga_bez_mat/datu_apstrade/kodi.csv'

df = pd.read_csv(file1)

# Izņem kodus, kas atkārtojās
df_bez_dub = df.drop_duplicates()

df_bez_dub.to_csv(file2, index=False)
