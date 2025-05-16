import numpy as np
import pandas as pd
import umap
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# Ielasa apmācības datu kopu 
file1 = pd.read_csv('salidz_apm_test/dati_fin.csv', sep=';')

# Ielasa testa datu kopu 
file2 = pd.read_csv('salidz_apm_test/2024_fin.csv', sep=';')

# Apvieno abas datu kopas
comb_data = np.vstack([file1, file2])

# Izveido masīvu, kas norāda, no kuras datu kopas nāk katrs ieraksts (0 – apmācības dati, 1 – testa dati)
coloring = np.array([0] * len(file1) + [1] * len(file2))

# Standardizē datus
scaler = StandardScaler()
dati_scal = scaler.fit_transform(comb_data)

# Izmanto UMAP, lai samazinātu datu dimensijas uz 2 dimensijām
umap_r = umap.UMAP(n_components=2, random_state=42)
transf = umap_r.fit_transform(dati_scal)

# Attēlo iegūtos rezultātus vizualizācijā
plt.figure(figsize=(10, 8))
plt.scatter(transf[coloring == 0, 0], transf[coloring == 0, 1], c='blue', label='2020-2023', alpha=0.7)
plt.scatter(transf[coloring == 1, 0], transf[coloring == 1, 1], c='red', label='2024', alpha=0.7)
plt.xlabel('Dimensija 1')
plt.ylabel('Dimensija 2')
plt.legend()
plt.title('UMAP 2D redukcija apmācības un testa datiem')
plt.show()
