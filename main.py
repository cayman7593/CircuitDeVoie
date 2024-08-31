import pandas as pd

# Fonction pour extraire les identifiants 'idGaiaSRVoie' de la structure JSON imbriquée
def extract_ids(df):
    ids = []
    for item in df['listeVoies']:
        if isinstance(item, list):  # Vérifie que 'listeVoies' est une liste
            for voie in item:
                if 'idGaiaSRVoie' in voie:  # Vérifie si 'idGaiaSRVoie' est une clé dans le dictionnaire
                    ids.append(voie['idGaiaSRVoie'].lower())  # Ajoute l'identifiant en minuscules
    return ids

# Charger les fichiers JSON
json_data1 = pd.read_json('data\\CircuitDeVoie.json5')
json_data2 = pd.read_json('data\\extremiteCvd.json5')

# Extraire les identifiants 'idGaiaSRVoie' des deux fichiers JSON
ids_json1 = extract_ids(json_data1)
ids_json2 = extract_ids(json_data2)

# Charger le fichier CSV avec le bon séparateur
data = pd.read_csv('data\\Lignes_Voies_18032024to26032024.csv', sep=';')

# Normaliser les identifiants dans le CSV
idsrvoie_list = data['IdSRVoie'].str.lower().tolist()

# Comparer les identifiants : ils sont manquants s'ils ne sont dans aucun des deux JSON
missing_ids = [id for id in idsrvoie_list if id not in ids_json1 and id not in ids_json2]

# Si certains identifiants manquent, les afficher et les exporter
if missing_ids:
    print(f"Identifiants manquants: {missing_ids}")
    pd.DataFrame(missing_ids, columns=['IdSRVoie']).to_csv('missing_ids.csv', index=False)
    print("Les identifiants manquants ont été exportés dans 'missing_ids.csv'.")
else:
    print("Tous les identifiants sont présents dans au moins un des fichiers JSON.")
