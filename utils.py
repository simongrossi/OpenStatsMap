# utils.py
import streamlit as st
import pandas as pd
import requests
import json

@st.cache_data
def load_data():
    """Charge et nettoie les données des communes."""
    try:
        df = pd.read_json("communes_population_insee_extended.json")
        df.rename(columns={'Commune': 'nom_commune', 'Code Postal': 'code_postal', 'Population': 'population'}, inplace=True)
        df['code_postal'] = df['code_postal'].astype(str)
        df['departement'] = df['code_postal'].str[:2]
        df['label'] = df['nom_commune']
        df.drop_duplicates(subset='label', inplace=True)
        return df.sort_values('label')
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier des communes : {e}")
        return None

@st.cache_data
def get_city_info(city_label):
    """Récupère les coordonnées et l'ID de la zone administrative d'une ville."""
    query = f"{city_label}, France"
    url = "https://nominatim.openstreetmap.org/search"
    params = {'q': query, 'format': 'json', 'featuretype': 'city,village,town', 'limit': 1}
    headers = {'User-Agent': 'OpenStatsMap/1.0'}
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data:
            area_id = int(data[0]['osm_id']) + 3600000000
            lat, lon = float(data[0]['lat']), float(data[0]['lon'])
            return lat, lon, area_id
    except Exception:
        return None, None, None

@st.cache_data
def get_osm_elements_by_area(area_id, amenities_to_search):
    """Récupère TOUS les éléments OSM (noeuds, chemins et relations) pour une zone en UNE SEULE requête."""
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    # **MODIFICATION** : On utilise (nwr) pour chercher les noeuds (n), les chemins (w) et les relations (r)
    query_parts = "".join([f'(nwr["{tags["key"]}"="{tags["value"]}"](area.searchArea););' for tags in amenities_to_search.values()])
    
    overpass_query = f'[out:json][timeout:30];area({area_id})->.searchArea;({query_parts});out center;'
    
    try:
        response = requests.get(overpass_url, params={'data': overpass_query}, timeout=25)
        response.raise_for_status()
        # La commande "out center;" ajoute lat/lon au centre des 'ways' et 'relations' pour l'affichage sur la carte
        return response.json().get('elements', [])
    except Exception:
        return []