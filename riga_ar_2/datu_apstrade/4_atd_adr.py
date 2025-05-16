import pandas as pd

# Ieejas fails, kas satur darījumus
file1 = 'riga_ar_2/datu_apstrade/2024_gg.csv'
# Izejas fails, kas saturēs atsevišķas kolonas ar ielas nosaukumu un mājas numuru
file2 = 'riga_ar_2/datu_apstrade/2024_adr.csv'

df = pd.read_csv(file1, sep=';')

# Saraksti, kuros glabās ielu nosaukumus un mājas numurus
ielas = []
majas_nrs = []

# Ielas ar skaitļiem nosaukumā tiek apstrādātas atsevišķi
ielas_ar_sk = ['13. janvāra iela', '11. novembra krastmala']

# Apstrādā katru adresi no kolonas 'Adreses pieraksts'
for adrese in df['Adreses pieraksts']:
    # Inicializē mainīgos katrai adresei
    iela = ''
    majas_nr = ''

    # Pārbauda, vai adrese satur kādu no ielām ar skaitļiem nosaukumā
    for iela_sk in ielas_ar_sk:
        if iela_sk in adrese:
            iela = iela_sk  # Piešķir 13. janvāra iela vai 11. novembra krastmala
            pareja_adr = adrese[len(iela_sk):].strip().split()  # Pārējo adreses daļu pēc ielas sadala pa atstarpēm,  piemēram: '15A', 'k-1', '-', '12'

            # Meklē mājas nummuru
            for i, dala in enumerate(pareja_adr):
                if dala[0].isdigit(): # Ja adresei pēc ielas nosaukuma seko daļa, kas sākas ar ciparu, 
                    majas_nr = dala   # tā tiek uzskatīta par mājas numura sākumu
                    for j in range(i + 1, len(pareja_adr)): # Turpina meklēt, vai mājas numuram nav vēl kāda daļa, piemēram, 1A vai k-11
                        if pareja_adr[j] == '-': # Ja tiek atrasts '-'
                            break # iziet no šī cikla, jo vairs nav jāmeklē tālāk.
                        majas_nr += ' ' + pareja_adr[j] # pievieno pārējo daļu mājas numuram
                    break
            break

    # Ja adrese nesatur 13. janvāra iela vai 11. novembra krastmala
    if not iela:
        adrese_dalas = adrese.split()  # Sadala adresi pa atstarpēm, piemēram: 'Brīvības', 'iela', '15A', 'k-1', '-', '12'

        # Ja adrese satur vārdu 'līnija', piemēram, '5. šķērslīnija'
        if 'līnija' in adrese:
            for i, dala in enumerate(adrese_dalas): # Iet cauri katrai adreses daļai
                if 'līnija' in dala:
                    iela = ' '.join(adrese_dalas[:i + 1]) # Ielas nosaukums ir līdz vārdam 'līnija' ieskaitot
                # Ja atrod pirmo skaitli pēc ielas, kuras nosaukumā ir 'līnija', tad tā ir mājas numura daļa
                elif dala[0].isdigit() and 'līnija' in ' '.join(adrese_dalas[:i]):
                    majas_nr = dala
                    for j in range(i + 1, len(adrese_dalas)): # Turpina meklēt, vai mājas numuram nav vēl kāda daļa, piemēram, 1A vai k-11
                        if adrese_dalas[j] == '-':  # Ja tiek atrasts '-'
                            break # iziet no šī cikla, jo vairs nav jāmeklē tālāk.
                        majas_nr += ' ' + adrese_dalas[j] # pievieno pārējo daļu mājas numuram
                    break
        else:
            # Ja adrese nesatur vārdu 'līnija'
            for i, dala in enumerate(adrese_dalas):  # Iet cauri katrai adreses daļai
                if dala[0].isdigit():  # Pārbauda, vai daļa sākas ar ciparu
                    iela = ' '.join(adrese_dalas[:i])  # Apvieno visas daļas pirms cipara – tas ir ielas nosaukums
                    majas_nr = dala # Ja daļa sākas ar ciparu, tad tas ir mājas numurs.
                    for j in range(i + 1, len(adrese_dalas)): # Turpina meklēt, vai mājas numuram nav vēl kāda daļa, piemēram, 1A vai k-11
                        if adrese_dalas[j] == '-': # Ja tiek atrasts '-'
                            break # iziet no šī cikla, jo vairs nav jāmeklē tālāk.
                        majas_nr += ' ' + adrese_dalas[j] # pievieno pārējo daļu mājas numuram
                    break

    # Saglabā ielas nosaukumu un mājas numuru attiecīgajos sarakstos
    ielas.append(iela)
    majas_nrs.append(majas_nr)

# Pievieno jaunu kolonnu ar ielu nosaukumiem
df['Iela'] = ielas
# Pievieno jaunu kolonnu ar mājas numuriem
df['Mājas numurs'] = majas_nrs

# Regulārā izteiksme, lai no mājas numura noņemtu daļu: '. Rīga. LV-xxxx'
pasta_ind = r'. Rīga. LV-\d{4}'

# Ja pie kolonnas 'Mājas numurs' ir pielicies '. Rīga. LV-xxxx', to noņem
df['Mājas numurs'] = df['Mājas numurs'].str.replace(pasta_ind, '', regex=True)

df.to_csv(file2, index=False, sep=';')
