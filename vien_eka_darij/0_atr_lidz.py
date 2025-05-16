import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Ievades fails, kas satur darījumus
file1 = 'vien_eka_darij/datu_apstrade/2024_fin.csv'  

df = pd.read_csv(file1, sep=';')

# Izvēlas kolonnas, lai grupētu datus (izņemot 'Darījuma summa, EUR', 'Darījuma datums')
lidz_kolon = df.columns.difference(['Darījuma summa, EUR', 'Darījuma datums'])

# Grupē datus pēc visām kolonnām, izņemot 'Darījuma summa, EUR' un 'Darījuma datums'
grupas = df.groupby(list(lidz_kolon))

# Izveido grafiku
plt.figure(figsize=(12, 6))

paru_nos = []  # Saraksts ar pāriem
zemas_cenas = []  # Saraksts ar zemākajām cenām katrā grupā
augst_cenas = []  # Saraksts ar augstākajām cenām katrā grupā

for _, grupa in grupas:
    if len(grupa) > 1:  # Ņem vērā tikai grupas, kuru izmērs ir lielāks par 1
        # Pārbauda, vai visām rindām grupā ir tāda pati cena
        if grupa['Darījuma summa, EUR'].nunique() == 1:
            continue  # Izlaiž šo grupu, ja visām rindām ir vienāda cena
        
        # Atrod zemāko un augstāko cenu šajā grupā
        min_cena = grupa['Darījuma summa, EUR'].min()
        max_cena = grupa['Darījuma summa, EUR'].max()
        
        nosauk = f'Pāris {len(paru_nos) + 1}'
        paru_nos.append(nosauk)  # Pievieno pāri sarakstam
        zemas_cenas.append(min_cena)  # Pievieno zemāko cenu sarakstam
        augst_cenas.append(max_cena)  # Pievieno augstāko cenu sarakstam

# Izveido grafiku ar visu dzīvokļu pāru datiem
for i in range(len(paru_nos)):
    plt.plot([paru_nos[i], paru_nos[i]], [zemas_cenas[i], augst_cenas[i]], marker='o', color='blue', linewidth=2)

plt.xticks(rotation=90)  # Pagriež X ass uzrakstus pa 90 grādiem, lai tie būtu salasāmi
plt.ylabel('Darījuma summa, EUR')
plt.title('2024. gads. Zemākā un augstākā dzīvokļu cena diviem vienāda izmēra dzīvokļiem vienā ēkā un vienā stāvā')

# Sadala Y asi pa katriem 10,000 EUR
min_sum = int(min(zemas_cenas) // 10000 * 10000)
max_sum = int(max(augst_cenas) // 10000 * 10000 + 10000)
plt.yticks(np.arange(min_sum, max_sum + 10000, 10000))

plt.tight_layout()
plt.grid(True)
plt.show()
