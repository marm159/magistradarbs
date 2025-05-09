import pandas as pd

# Ieejas fails, kas satur darījumus
file1 = 'pieriga_bez_mat/datu_apstrade/2024_fin.csv'
# Ieejas fails, kas satur vecos un jaunos materiālu kodus
file_kodi = 'pieriga_bez_mat/datu_apstrade/jauni_kodi.csv'
# Izejas fails, kas saturēs darījumus ar jaunajiem materiālu kodiem
file2 = 'pieriga_bez_mat/datu_apstrade/2024_kodi.csv'

# Ielsa darījumu failu
df = pd.read_csv(file1, sep=';')

# Ielādē veco un jauno materiālu kodu failu
df_kodi = pd.read_csv(file_kodi, sep=';')

# Izveido vārdnīcu, kur katram vecajam kodam atbilst jaunais kods
kodi_doct = dict(zip(df_kodi['vec_kod'].astype(str), df_kodi['jaun_kod'].astype(str)))

# Saraksts, kurā tiks glabāti jaunie kodi
mat_kods = []
# Iziet cauri katrai vērtībai 'Būves ārsienu materiāla nosaukums' kolonnā
for vert in df['Būves ārsienu materiāla nosaukums']:
    if not vert or pd.isnull(vert):
        mat_kods.append('')
        continue
    
    dalas = vert.split('.') # Sadala ierkastu divās daļās, ja tas satur (.), kas norāda, ka ir vairāki materiāli
    kodi = [] # Saraksts, kur glabāsies konkrētās datu rindas materiāla kodi
    for dala in dalas: # apstrādā katru materiālu
        dala = dala.strip() # noņem atstarpes sākumā un beigās
        if ' - ' in dala: # kad atrod ' - '
            atr_kod = dala.split(' - ')[0].strip() # tas, kas ir pirms ' - ' ir materiāla kods
            if atr_kod.isdigit(): # ja šī daļa ir skaitlis
                # pārvērš to par tekstu, jo vārdnīca satur vecos materiālu kodus kā teksta vērtības
                vec_kods = str(atr_kod) 
                # meklē jauno materiāla kodu vārdnīcā
                jaun_kods = kodi_doct.get(vec_kods, str(vec_kods)) 
                kodi.append(jaun_kods) # jauno kodu pievieno sarakstam kodi 
    # Apvieno visus atrastos kodus un pievieno sarakstam mat_kods
    mat_kods.append(','.join(kodi))

# Kolonnas 'Būves ārsienu materiāla nosaukums' vērtību aivieto ar jauno materāla kodu
df['Būves ārsienu materiāla nosaukums'] = mat_kods

# Saglabā apstrādātos datus jaunā CSV failā
df.to_csv(file2, index=False, sep=';')

