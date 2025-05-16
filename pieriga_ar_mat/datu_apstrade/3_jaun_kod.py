import pandas as pd

# Ieejas fails, kas satur darījumus
file1 = 'pieriga_ar_mat/datu_apstrade/2024_fin.csv'
# Ieejas fails, kas satur vecos un jaunos materiālu kodus
file_kodi = 'pieriga_ar_mat/datu_apstrade/jauni_kodi.csv'
# Izejas fails, kas saturēs darījumus ar jaunajiem materiālu kodiem
file2 = 'pieriga_ar_mat/datu_apstrade/2024_kodi.csv'

df = pd.read_csv(file1, sep=';')

df_kodi = pd.read_csv(file_kodi, sep=';')

# Izveido vārdnīcu, kur katram vecajam kodam atbilst jaunais kods
kodi_doct = dict(zip(df_kodi['vec_kod'].astype(str), df_kodi['jaun_kod'].astype(str)))

# Saraksts, kurā tiks glabāti jaunie kodi
mat_kods = []
# Iziet cauri katrai vērtībai 'Būves ārsienu materiāla nosaukums' kolonnā
for vert in df['Būves ārsienu materiāla nosaukums']:
    dalas = vert.split('.') # Sadala ierkastu vairākās daļās, ja tas satur (.), kas norāda, ka ir vairāki materiāli
    kodi = [] # Saraksts, kur glabāsies konkrētās datu rindas materiāla kodi
    for dala in dalas:
        dala = dala.strip()  # noņem atstarpes kokrētās daļas sākumā un beigās
        if ' - ' in dala: # kad atrod ' - '
            atr_kod = dala.split(' - ')[0].strip() # tas, kas ir pirms ' - ' ir materiāla kods
            if atr_kod.isdigit(): # ja šī daļa ir skaitlis
                # pārvērš to par tekstu, jo vārdnīca satur vecos materiālu kodus kā tekstu
                vec_kods = str(atr_kod) 
                # Iegūst jauno kodu no vārdnīcas
                jaun_kods = kodi_doct.get(vec_kods, str(vec_kods)) 
                kodi.append(jaun_kods) # jauno kodu pievieno sarakstam kodi 
    # Apvieno visus atrastos kodus, atdalītus ar komatu un pievieno sarakstam mat_kods
    mat_kods.append(','.join(kodi))

# Kolonnas 'Būves ārsienu materiāla nosaukums' vērtības aivieto ar jaunajiem materāla kodiem
df['Būves ārsienu materiāla nosaukums'] = mat_kods

df.to_csv(file2, index=False, sep=';')

