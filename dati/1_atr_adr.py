import json
import pandas as pd

# Ievades GeoJSON fails ar adresēm un to koordinātām
file1 = 'dati/Riga.osm.geojson'

# Izvades CSV fails, kur tiks ierakstītas adreses un to koordinātās
file2 = 'dati/viss_adreses.csv'

# Ielādē GeoJSON failu
with open(file1, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Saraksts, kurā glabās adreses
addreses = []

# Cikls caur visiem objektiem (features) GeoJSON failā
for feature in data.get('features', []):

    # Iegūst adreses informāciju un koordinātes 
    properties = feature.get('properties', {})
    geometry = feature.get('geometry', {})

    # Pārbuada vai adrese ir Rīgā
    if properties.get('addr:city') != 'Rīga':
        continue

    # Nosaka tipu (Point, LineString vai MultiPolygon) un iegūst koordinātas
    gtype = geometry.get('type')
    coordinates = geometry.get('coordinates')

    # Apstrādā tikai tās adreses, kur koordinātu tips ir Point vai MultiPolygon
    if gtype == 'Point':
        coord = coordinates
    elif gtype == 'MultiPolygon':
        coord = [coord1 for coord1 in coordinates]
    else:
        continue # Izlaiž LineString tipu

    # Iegūst datus par adresi, ja to nav, ieliek NULL
    new_street = properties.get('addr:street', 'NULL')
    new_housenumber = properties.get('addr:housenumber', 'NULL')
    old_street = properties.get('old_addr:street', 'NULL')
    old_housenumber = properties.get('old_addr:housenumber', 'NULL')

    # Pievieno sarakstam adresi, veco adresi (ja tāda ir) un koordinātas
    addreses.append({
        'jauna_iela': new_street,
        'jauns_nr': new_housenumber,
        'veca_iela': old_street,
        'vecs_nr': old_housenumber,
        'koordinates': coord
    })

# Pārvērš sarakstu par DataFrame un saglabā kā CSV failu
df = pd.DataFrame(addreses)
df.to_csv(file2, index=False, encoding='utf-8')
