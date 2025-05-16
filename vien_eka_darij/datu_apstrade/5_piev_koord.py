import pandas as pd

# Ieejas fails, kas satur darījumus
file1 = 'vien_eka_darij/datu_apstrade/2024_adr.csv'
# Ieejas fails, kas satur katrai adresei atbilstošās koordinātes
file_koord = 'dati/adreses.csv'
# Izvades fails, kas saturēs datus, kur adrese ir aizvietota ar koordinātēm
file2 = 'vien_eka_darij/datu_apstrade/2024_fin.csv'

df = pd.read_csv(file1, sep=';')
df_k = pd.read_csv(file_koord)

# Izveido vārdnīcu meklēšanai pēc jaunajām adresēm
jauna_adr = {
    (row['jauna_iela'], row['jauns_nr']): (row['Platums'], row['Garums'])
    for _, row in df_k.iterrows()
}

# Izveido vēl vienu vārdnīcu meklēšanai pēc vecajām adresēm
veca_adr = {
    (row['veca_iela'], row['vecs_nr']): (row['Platums'], row['Garums'])
    for _, row in df_k.iterrows()
}

# Saraksti, kuros glabās platumu un garumu vērtības
platumi = []
garumi = []

# Iet cauri katrai datu rindai darījumu failā
for ind, row in df.iterrows():
    iela = str(row['Iela']).strip() # Iegūst ielas nosaukumu
    majas_numurs = str(row['Mājas numurs']).strip() # Iegūst mājas numuru

    # Vispirms meklē koordinātes pēc jaunās adreses
    koordinates = jauna_adr.get((iela, majas_numurs))
    if not koordinates:
        # Ja nav atrastas koordinātes pēc jaunās adreses, tad meklē pēc vecās adreses
        koordinates = veca_adr.get((iela, majas_numurs))

    # Ja koordinātes atrastas, pievieno tās sarakstiem, citādi ieraksta 'nan'
    if koordinates:
        platumi.append(koordinates[0])
        garumi.append(koordinates[1])
    else:
        platumi.append('nan')
        garumi.append('nan')

# Pievieno koordinātu kolonnas
df['Platums'] = platumi
df['Garums'] = garumi

# Noņem kolonnas, kas vairs nav vajadzīgas
df = df.drop(columns=['Adreses pieraksts', 'Iela', 'Mājas numurs'])

df.to_csv(file2, sep=';', index=False)
