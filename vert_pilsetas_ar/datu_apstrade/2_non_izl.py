import pandas as pd

# Ieejas fails, kas satur darījumus
file1 = 'vert_pilsetas_ar/datu_apstrade/2024.csv'
# Izejas fails, kas saturēs datus bez izlēcējiem
file2 = 'vert_pilsetas_ar/datu_apstrade/2024_fin.csv'
# Izejas fails, kas saturēs izlēcējus
file3 = 'vert_pilsetas_ar/datu_apstrade/2024_izl.csv'

df = pd.read_csv(file1, sep=';')

# Reģioni un to pilsētas
regions = {
    'Kurzeme': ['Brocēni', 'Grobiņa', 'Kandava', 'Kuldīga', 'Pāvilosta', 'Saldus', 'Talsi', 'Tukums'],
    'Latgale': ['Balvi', 'Līvāni', 'Ludza', 'Preiļi'],
    'Vidzeme': ['Ainaži', 'Alūksne', 'Cēsis', 'Gulbene', 'Limbaži', 'Madona', 'Salacgrīva', 'Smiltene'],
    'Zemgale': ['Aizkraukle', 'Bauska', 'Dobele', 'Iecava']
}

# Izmet tās rindas, kur 'Darījuma summa, EUR' ir mazāka par 1000 EUR
df = df[df['Darījuma summa, EUR'] >= 1000]

# Aprēķina EUR/m^2
df['EUR/m^2'] = df['Darījuma summa, EUR'] / df['Dzīvokļa kopplatība, m2']

# Izveido tukšu sarakstu, kurā tiks saglabāti piešķirtie reģioni katrai pilsētai
regioni = []

# Iet cauri katrai datu rindai
for ind, row in df.iterrows():
    pilseta = row['Pilsēta'] # Iegūst pilsētu no pašreizējās rindas
    reg_atr = None # Inicializē mainīgo, kas uzglabās atrasto reģionu
    for region, pilsetas in regions.items():  # Iet cauri visiem reģioniem un to pilsētām
        if pilseta in pilsetas: # Ja pilsēta ir atrodama reģiona pilsētu sarakstā, piešķir reģionu
            reg_atr = region
            break
    regioni.append(reg_atr) # Pievieno atrasto reģionu sarakstam
df['Reģions'] = regioni # Piešķir katrai rindai atbilstošo reģionu, pievienojot jaunu kolonu 'Reģions'

# Saraksti, kur glabās filtrētos datus un izlēcējus
filtretie = []
izleceji = []

# Apstrādā katru reģionu atsevišķi
for region, pilsetas in regions.items():
    # Izveido jaunu datu kopu df_reg, kurā tiek iekļautas tikai tās rindas, kuras atbilst noteiktam reģionam
    df_reg = df[df['Reģions'] == region]
    
    Q1 = df_reg['EUR/m^2'].quantile(0.25) # 1. kvartile
    Q3 = df_reg['EUR/m^2'].quantile(0.75) # 3. kvartile
    IQR = Q3 - Q1                         # Starpkvartilu intervals
    lower = Q1 - 1.5 * IQR                # Apakšējā robeža
    upper = Q3 + 1.5 * IQR                # Augšējā robeža
    
    # Atlasa rindas, kur EUR/m^2 ir mazāks nekā lower (apakšējā robeža)
    # vai EUR/m^2 ir lielāks nekā upper (augšējā robeža)
    reg_izl  = df_reg[(df_reg['EUR/m^2'] < lower) | (df_reg['EUR/m^2'] > upper)]
    
    # Izņem no datiem tās rindas, kuru indeksi sakrīt ar izlēcēju datu indeksiem
    reg_fil = df_reg[~df_reg.index.isin(reg_izl.index)]
    
    # Saglabā filtrētos datus un izlēcējus sarakstos
    filtretie.append(reg_fil)
    izleceji.append(reg_izl)

# Apvieno visus filtrētos datus
df_fil = pd.concat(filtretie)
# Apvieno visus izlēcēju datus
outliers = pd.concat(izleceji)

# Izmet kolonnas 'EUR/m^2', 'Pilsēta', 'Reģions', jo tās vairs nevajag
df_fil = df_fil.drop(columns=['EUR/m^2', 'Pilsēta', 'Reģions'])

# Saglabā filtrētos datus jaunā CSV failā
df_fil.to_csv(file2, sep=';', index=False)

# Saglabā izlēcēju datus atsevišķā CSV failā
outliers.to_csv(file3, sep=';', index=False)
