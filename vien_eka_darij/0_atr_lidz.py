import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Ievades fails, kas satur darījumus
file1 = 'vien_eka_darij/datu_apstrade/2024_fin.csv'  
# Izvades fails, kas saturēs darījumu grupas, kur katrā grupā darījums noticis vienā ēkā un ir vienāda izmēra dzīvoklis
file2 = 'vien_eka_darij/2024_eka.csv'

# Ielasa datus no ievades faila
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

# Saglabā rezultātus jaunā CSV failā
df_res.to_csv(file2, sep=';', index=False)

# Izveido grafiku
plt.figure(figsize=(12, 6))

paru_nos = []  # Saraksts pāru nosaukumiem, ko izmantos grafika izveidē
zemas_cenas = []  # Saraksts ar zemākajām cenām katrā grupā
augst_cenas = []  # Saraksts ar augstākajām cenām katrā grupā

# Izveido pāru nosakumus un cenu sarakstus vizualizācijai
for _, grupa in grupas:
    if len(grupa) > 1:  # Ņem vērā tikai grupas, kuru izmērs ir lielāks par 1
        # Pārbauda, vai visām rindām grupā ir tāda pati cena
        if grupa['Darījuma summa, EUR'].nunique() == 1:
            continue  # Izlaiž šo grupu, ja visām rindām ir vienāda cena
        
        # Atrod zemāko un augstāko cenu šajā grupā
        min_cena = grupa['Darījuma summa, EUR'].min()
        max_cena = grupa['Darījuma summa, EUR'].max()
        
        # Pievieno grupas detaļas uz grafika
        nosauk = f"Pāris {len(paru_nos) + 1}"  # Izveido pāri
        paru_nos.append(nosauk)  # Pievieno pāri sarakstam
        zemas_cenas.append(min_cena)  # Pievieno zemāko cenu sarakstam
        augst_cenas.append(max_cena)  # Pievieno augstāko cenu sarakstam

# Izveido grafiku ar visu dzīvokļu pāru datiem
for i in range(len(paru_nos)):
    plt.plot([paru_nos[i], paru_nos[i]], [zemas_cenas[i], augst_cenas[i]], marker='o', color='blue', linewidth=2)

plt.xticks(rotation=90)  # Pagriež X ass uzrakstus pa 90 grādiem, lai tie būtu salasāmi
plt.ylabel('Darījuma summa, EUR')
plt.title('2024. gads. Zemākā un augstākā darījuma summa diviem vienāda izmēra dzīvokļiem vienā ēkā un vienā stāvā')

# Sadala Y asi pa katriem 10,000 EUR
min_sum = int(min(zemas_cenas) // 10000 * 10000)
max_sum = int(max(augst_cenas) // 10000 * 10000 + 10000)
plt.yticks(np.arange(min_sum, max_sum + 10000, 10000))

plt.tight_layout()
plt.grid(True)
plt.show()
