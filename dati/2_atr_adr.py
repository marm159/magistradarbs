import pandas as pd
import ast

# Ievades fails ar adresēm un koordinātām
file1 = 'dati/viss_adreses.csv'

# Izvades fails ar pareizi noformētām adresēm un koordinātēm 
file2 = 'dati/adreses.csv'

df = pd.read_csv(file1, sep=',')

# Saraksti, kuros glabāsies garuma un platuma vērtības
garums = []
platums = []

# Iegūst koordinātes no katras datu rindas
for coordinates in df['koordinates']:
    # Pārvērš teksta formāta kordinātes par sarakstu (piemēram, no "[11.1, 22.2]" uz [11.1, 22.2])
    coord = ast.literal_eval(coordinates)

    # Iet līdz atrod pirmo koordinātu pāri, jo MultiPolygon satur vairākus sarakstus ar koordinātēm
    while isinstance(coord[0], list):
        coord = coord[0]

    # Saglabā garumu (coord[0]) un platumu (coord[1]) atsevišķos sarakstos
    garums.append(coord[0])
    platums.append(coord[1])

# Pievieno jaunas kolonnas ar garuma un platuma vērtībām
df['Garums'] = garums
df['Platums'] = platums

# Izdzēš kolonnu 'koordinates', jo tā vairs nav vajadzīga
df = df.drop(columns=['koordinates'])

# Ja adreses vecais ielas nosaukums vai mājas numurs ir tukšs, to aizvieto ar jaunās adreses ielas nosaukumu vai mājas numuru
# Tas tiek darīts, lai pēc tam ēkām, kurām ir mainījusies adrese, būtu vieglāk atrast koordinātes
df['veca_iela'] = df['veca_iela'].fillna(df['jauna_iela'])
df['vecs_nr'] = df['vecs_nr'].fillna(df['jauns_nr'])

df.to_csv(file2, index=False, sep=',')