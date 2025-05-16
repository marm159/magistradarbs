import pandas as pd
import umap
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

# Ieejas fails, kas satur darījumus
file1 = 'red_klast/2024_bez.csv'
# Izejas fails, kas saturēs datus ar klasteriem
file2 = 'red_klast/2024_bez_db.csv'

df = pd.read_csv(file1, sep=';')

# Saglabā kolonnu 'Darījuma summa, EUR', lai to vēlāk varētu pievienot atpakaļ
cenas = df['Darījuma summa, EUR']

# Izmet kolonnu 'Darījuma summa, EUR'
df = df.drop(columns=['Darījuma summa, EUR'])

# Klasterizācijai nepieciešamās kolonnas
liet_kolon = [
    'Būvju skaits', 'Būves virszemes stāvu skaits', 
    'Būves apbūves laukums, m2', 'Būves kopplatība, m2', 'Būves būvtilpums, m3', 
    'Būves ekspluatācijas uzsākšanas gads', 'Būves fiziskais nolietojums, %', 
    'Telpu grupas zemākais stāvs', 'Telpu grupas augstākais stāvs', 
    'Telpu grupas platība, m2', 'Dzīvokļa kopplatība, m2', 
    'Telpu skaits telpu grupā', 'Istabu skaits dzīvoklī', 'Garums', 'Platums'
]

# Standardizē datus
scaler = StandardScaler()
dati_scal = scaler.fit_transform(df[liet_kolon])

# Izmanto UMAP, lai samazinātu datu dimensijas uz 2 dimensijām
umap_r = umap.UMAP(n_components=2, random_state=42)
transf = umap_r.fit_transform(dati_scal)

# Izmanto DBSCAN, lai atrastu klasterus 2D telpā, kas iegūta ar UMAP
dbscan = DBSCAN(eps=0.5, min_samples=10)
klasteri = dbscan.fit_predict(transf)

# Pievieno kolonnu ar klasteru numuriem kā pirmo kolonnu datu kopā
df.insert(0, 'Klasteris', klasteri)

# Pievieno kolonnu 'Darījuma summa, EUR' atpakaļ datiem
df['Darījuma summa, EUR'] = cenas

# Sakārto datus pēc klastera numura
df = df.sort_values(by='Klasteris')

# Attēlo iegūtos rezultātus vizualizācijā
plt.figure(figsize=(10, 8))
sns.scatterplot(x=transf[:, 0], y=transf[:, 1], hue=df['Klasteris'], palette='cividis', s=10)
plt.xlabel('Dimensija 1')
plt.ylabel('Dimensija 2')
plt.title('UMAP 2D redukcija un DBSCAN klasterizācija')
plt.legend(title='Klasteris')
plt.show()

df.to_csv(file2, index=False, sep=';')