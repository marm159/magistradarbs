import pandas as pd

# Ieejas fails, kas satur darījumus
file1 = 'valstspilsetas_ar/datu_apstrade/2024.csv'
# Izejas fails, kas saturēs datus bez izlēcējiem
file2 = 'valstspilsetas_ar/datu_apstrade/2024_fin.csv'
# Izejas fails, kas saturēs izlēcēju
file3 = 'valstspilsetas_ar/datu_apstrade/2024_izl.csv'

df = pd.read_csv(file1, sep=';')

# Pilsētu saraksts
pilsetas = ['Daugavpils', 'Jēkabpils', 'Jelgava', 'Liepāja', 'Ogre', 'Rēzekne', 'Valmiera', 'Ventspils']

# Izmet tās rindas, kur 'Darījuma summa, EUR' ir mazāka par 1000 EUR
df = df[df['Darījuma summa, EUR'] >= 1000]

# Aprēķina EUR/m^2
df['EUR/m^2'] = df['Darījuma summa, EUR'] / df['Dzīvokļa kopplatība, m2']

# Saraksti, kur glabās filtrētos datus un izlēcējus
filtretie = []
izleceji = []

# Apstrādā katru pilsētu atsevišķi
for pilseta in pilsetas:
    df_pils = df[df['Pilsēta'] == pilseta]
    
    Q1 = df_pils['EUR/m^2'].quantile(0.25) # 1. kvartile
    Q3 = df_pils['EUR/m^2'].quantile(0.75) # 3. kvartile
    IQR = Q3 - Q1                          # Starpkvartilu intervals
    lower = Q1 - 1.5 * IQR                 # Apakšējā robeža
    upper = Q3 + 1.5 * IQR                 # Augšējā robeža
    
    # Atlasa rindas, kur EUR/m^2 ir mazāks nekā lower (apakšējā robeža)
    # vai EUR/m^2 ir lielāks nekā upper (augšējā robeža)
    pils_izl = df_pils[(df_pils['EUR/m^2'] < lower) | (df_pils['EUR/m^2'] > upper)]
    
    # Izņem no datiem tās rindas, kuru indeksi sakrīt ar izlēcēju datu indeksiem
    pils_fil = df_pils[~df_pils.index.isin(pils_izl.index)]
    
    # Saglabā filtrētos datus un izlēcēju sarakstos
    filtretie.append(pils_fil)
    izleceji.append(pils_izl)

# Apvieno visus filtrētos datus
df_fil = pd.concat(filtretie)
# Apvieno visus izlēcēju datus
outliers = pd.concat(izleceji)

# Izmet kolonnu EUR/m^2 un 'Pilsēta', jo tās vairs nevajag
df_fil = df_fil.drop(columns=['EUR/m^2', 'Pilsēta'])

# Saglabā filtrētos datus jaunā CSV failā
df_fil.to_csv(file2, sep=';', index=False)

# Saglabā izlēcēju datus atsevišķā CSV failā
outliers.to_csv(file3, sep=';', index=False)
