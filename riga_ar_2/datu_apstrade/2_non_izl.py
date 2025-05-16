import pandas as pd

# Ieejas fails, kas satur darījumus
file1 = 'riga_ar_2/datu_apstrade/2024.csv'
# Izejas fails, kas saturēs datus bez izlēcējiem
file2 = 'riga_ar_2/datu_apstrade/2024_fil.csv'
# Izejas fails, kas saturēs izlēcējus
file3 = 'riga_ar_2/datu_apstrade/2024_izl.csv'

df = pd.read_csv(file1, sep=';')

# Izmet tās rindas, kur 'Darījuma summa, EUR' ir mazāka par 5000 EUR
df = df[df['Darījuma summa, EUR'] >= 5000]

# Aprēķina 'EUR/m^2' un pievieno to kā jaunu kolonnu
df['EUR/m^2'] = df['Darījuma summa, EUR'] / df['Dzīvokļa kopplatība, m2']

# Sadala datus divās grupās: būves, kas ekspluatētas pirms 2000. gada un pēc 2000. gadā
pirms_2000 = df[df['Būves ekspluatācijas uzsākšanas gads'] < 2000]
pec_2000 = df[df['Būves ekspluatācijas uzsākšanas gads'] >= 2000]

# Meklē izlēcējus datiem, kur ēka ekspluatēta pirms 2000. gada
Q1_pirms = pirms_2000['EUR/m^2'].quantile(0.25)  # 1. kvartile
Q3_pirms = pirms_2000['EUR/m^2'].quantile(0.75)  # 3. kvartile
IQR_pirms = Q3_pirms - Q1_pirms                  # Starpkvartilu intervāls
lower_pirms = Q1_pirms - 1.5 * IQR_pirms         # Apakšējā robeža
upper_pirms = Q3_pirms + 1.5 * IQR_pirms         # Augšējā robeža

# Atlasa rindas, kur EUR/m^2 ir mazāks nekā lower_pec (apakšējā robeža)
# vai EUR/m^2 ir lielāks nekā upper_pec (augšējā robeža)
outliers_pirms_2000 = pirms_2000[(pirms_2000['EUR/m^2'] < lower_pirms) | (pirms_2000['EUR/m^2'] > upper_pirms)]

# Meklē izlēcējus datiem, kur ēka ekspluatēta pēc 2000. gada
Q1_pec = pec_2000['EUR/m^2'].quantile(0.25)  # 1. kvartile
Q3_pec = pec_2000['EUR/m^2'].quantile(0.75)  # 3. kvartile
IQR_pec = Q3_pec - Q1_pec                    # Starpkvartilu intervāls
lower_pec = Q1_pec - 1.5 * IQR_pec           # Apakšējā robeža
upper_pec = Q3_pec + 1.5 * IQR_pec           # Augšējā robeža

# Atlasa rindas, kur EUR/m^2 ir mazāks nekā lower_pec (apakšējā robeža)
# vai EUR/m^2 ir lielāks nekā upper_pec (augšējā robeža)
outliers_pec_2000 = pec_2000[(pec_2000['EUR/m^2'] < lower_pec) | (pec_2000['EUR/m^2'] > upper_pec)]

# Apvieno abus izlēcēju datus
outliers = pd.concat([outliers_pirms_2000, outliers_pec_2000])

# No sākotnējās datu kopas tiek izņemtas tās datu rindas, kuru indeksi sakrīt ar indeksiem izlēcēju datu kopā
df = df[~df.index.isin(outliers.index)]

# Izdzēš kolonnu 'EUR/m^2', jo tā vairs nav nepieciešama
df = df.drop(columns=['EUR/m^2'])

# Saglabā filtrētos datus jaunā CSV failā
df.to_csv(file2, sep=';', index=False)

# Saglabā trokšņu datus atsevišķā CSV failā
outliers.to_csv(file3, sep=';', index=False)
