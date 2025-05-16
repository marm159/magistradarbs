import pandas as pd

# Ievades fails, kas satur darījumus
file1 = 'riga_ar_remonts/datu_apstrade/dati_fin.csv'  
# Izvades fails, kas saturēs darījumu grupas, kur katrā grupā darījums noticis vienā ēkā un ir vienāda izmēra dzīvoklis
file2 = 'riga_ar_remonts/dati_eka.csv'

df = pd.read_csv(file1, sep=';')

# Izvēlas kolonnas, lai grupētu datus (izņemot 'Darījuma summa, EUR', 'Darījuma datums')
lidz_kolon = df.columns.difference(['Darījuma summa, EUR', 'Darījuma datums'])

# Grupē datus pēc visām kolonnām, izņemot 'Darījuma summa, EUR' un 'Darījuma datums'
grupas = df.groupby(list(lidz_kolon))

# Saraksts, lai saglabātu apstrādātās rindas (visas rindas, kur grupā ir vismaz 2 rindas)
sagl_rind = []
# Saraksts, lai saglabātu 'Remonts' kolonnas vērtības
remonts_dar = []

# Apstrādā katru grupu
for _, grupa in grupas:
    if len(grupa) > 1:  # Ņem vērā tikai grupas, kuru izmērs ir lielāks par 1
        # Pārbauda, vai visām rindām grupā ir tāda pati darījuma summa
        if grupa['Darījuma summa, EUR'].nunique() == 1:
            # Ja visām rindām ir vienāda darījuma summa, šo grupu izlaiž
            continue
        
        # Aprēķina vidējo summu grupai
        avg_sum = grupa['Darījuma summa, EUR'].mean()
        
        # Pārbauda katru rindu grupā, vai cena ir augstāka vai zemāka par vidējo cenu
        for idx, row in grupa.iterrows():
            if row['Darījuma summa, EUR'] >= avg_sum:
                remonts_dar.append(1)  # Ja cena ir augstāka vai vienāda ar vidējo, pievieno 1
            else:
                remonts_dar.append(0)  # Ja cena ir zemāka par vidējo, pievieno 0
        
        # Pievieno visas rindas no grupas gala sarakstam
        sagl_rind.extend(grupa.to_dict(orient='records'))

# Izveido datu kopu ar visām rindām no grupām, kuru izmērs ir lielāks par 1
df_res = pd.DataFrame(sagl_rind)

# Pievieno jauno kolonu 'Remonts'
df_res['Remonts'] = remonts_dar

df_res.to_csv(file2, sep=';', index=False)