import streamlit as st
import pandas as pd
import requests
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import json

# --- Configuration de la page ---
st.set_page_config(page_title="OpenStatsMap", page_icon="🗺️", layout="wide")

# --- Fonctions ---
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
    except requests.exceptions.RequestException as e:
        st.sidebar.error(f"Erreur réseau (géolocalisation) : {e}")
    except (KeyError, IndexError):
        st.sidebar.warning(f"Aucune donnée administrative trouvée pour {city_label}.")
    return None, None, None

@st.cache_data
def get_osm_elements_by_area(area_id, amenities_to_search):
    """Récupère TOUS les éléments OSM pour une zone en UNE SEULE requête."""
    overpass_url = "http://overpass-api.de/api/interpreter"
    query_parts = "".join([f'node["{tags["key"]}"="{tags["value"]}"](area.searchArea);' for tags in amenities_to_search.values()])
    overpass_query = f'[out:json][timeout:30];area({area_id})->.searchArea;({query_parts});out;'
    try:
        response = requests.get(overpass_url, params={'data': overpass_query}, timeout=25)
        response.raise_for_status()
        return response.json().get('elements', [])
    except Exception:
        return []

# --- Dictionnaires et Configurations ---
df_communes = load_data()

st.sidebar.title("OpenStatsMap 🗺️")
if df_communes is None:
    st.stop()

osm_amenities = {
    "🎠 Aires de jeux": {"key": "leisure", "value": "playground", "icon": "child", "color": "orange"},
    "🪑 Bancs publics": {"key": "amenity", "value": "bench", "icon": "square-o", "color": "green"},
    "📷 Caméras": {"key": "man_made", "value": "surveillance", "icon": "video-camera", "color": "red"},
    "💧 Fontaines à boire": {"key": "amenity", "value": "drinking_water", "icon": "tint", "color": "blue"},
    "🌳 Parcs & Jardins": {"key": "leisure", "value": "park", "icon": "tree", "color": "darkgreen"},
    "🚲 Parkings à vélos": {"key": "amenity", "value": "bicycle_parking", "icon": "bicycle", "color": "purple"},
    "⚕️ Pharmacies": {"key": "amenity", "value": "pharmacy", "icon": "plus-square", "color": "cadetblue"},
    "🗑️ Poubelles": {"key": "amenity", "value": "waste_basket", "icon": "trash", "color": "darkred"},
    "⚽ Terrains de sport": {"key": "leisure", "value": "pitch", "icon": "futbol-o", "color": "black"},
    "⛲ Toilettes publiques": {"key": "amenity", "value": "toilets", "icon": "toilet", "color": "blue"},
}

# --- Interface Utilisateur ---
st.sidebar.header("Configuration", divider='rainbow')
# ... (partie interface inchangée)
search_mode = st.sidebar.radio("Mode de recherche :", ["Nom de ville", "Département", "Code Postal"])

options_villes = []
if search_mode == "Nom de ville":
    options_villes = df_communes['label']
elif search_mode == "Département":
    departement = st.sidebar.selectbox("Choisissez un département :", options=sorted(df_communes['departement'].unique()))
    options_villes = df_communes[df_communes['departement'] == departement]['label']
else:
    code_postal = st.sidebar.text_input("Entrez un code postal :")
    if code_postal:
        options_villes = df_communes[df_communes['code_postal'].str.startswith(code_postal)]['label']

if 'selected_cities' not in st.session_state: st.session_state.selected_cities = []
if 'selected_amenities' not in st.session_state: st.session_state.selected_amenities = ["🪑 Bancs publics"]

st.session_state.selected_cities = st.sidebar.multiselect("1. Choisissez des villes :", options=sorted(options_villes), default=st.session_state.selected_cities)
st.session_state.selected_amenities = st.sidebar.multiselect("2. Cochez les équipements :", options=list(osm_amenities.keys()), default=st.session_state.selected_amenities)

# --- Logique principale ---
if not st.session_state.selected_cities or not st.session_state.selected_amenities:
    st.info("👋 Bienvenue ! Configurez votre recherche dans le menu de gauche pour commencer.")
else:
    all_cities_data = []
    total_elements_for_map = []
    amenities_to_search = {name: osm_amenities[name] for name in st.session_state.selected_amenities}

    for city_name in st.session_state.selected_cities:
        with st.spinner(f"Analyse de {city_name}..."):
            city_info_from_file = df_communes[df_communes['label'] == city_name].iloc[0]
            population = int(city_info_from_file.get('population', 0))
            lat, lon, area_id = get_city_info(city_name)
            
            if area_id:
                city_summary = {"Ville": city_name, "Population": population}
                all_elements = get_osm_elements_by_area(area_id, amenities_to_search)
                
                for amenity_name, tags in amenities_to_search.items():
                    elements = [el for el in all_elements if el.get('tags', {}).get(tags['key']) == tags['value']]
                    count = len(elements)
                    city_summary[f"{amenity_name}_total"] = count
                    city_summary[f"{amenity_name}_ratio1k"] = (count / population) * 1000 if population > 0 else 0
                    city_summary[f"{amenity_name}_ratio10k"] = (count / population) * 10000 if population > 0 else 0
                    for el in elements: el['amenity_name'] = amenity_name
                    total_elements_for_map.extend(elements)
                all_cities_data.append(city_summary)
            else:
                st.warning(f"Impossible de trouver les données pour {city_name}.")

    # --- Affichage des résultats ---
    if all_cities_data:
        st.header("🏆 Résultats de la comparaison")
        df_results = pd.DataFrame(all_cities_data).set_index("Ville")
        
        display_mode = st.radio("Choisir la vue :", ["Total", "Ratio / 1 000 hab.", "Ratio / 10 000 hab."], index=2, horizontal=True)

        if display_mode == "Total":
            suffix, title = "_total", "Nombre total d'équipements"
            df_view = df_results[[f"{name}_total" for name in st.session_state.selected_amenities]].astype(int)
        elif display_mode == "Ratio / 1 000 hab.":
            suffix, title = "_ratio1k", "Ratio pour 1 000 habitants"
            df_view = df_results[[f"{name}_ratio1k" for name in st.session_state.selected_amenities]].round(2)
        else:
            suffix, title = "_ratio10k", "Ratio pour 10 000 habitants"
            df_view = df_results[[f"{name}_ratio10k" for name in st.session_state.selected_amenities]].round(2)

        # **MODIFICATION ICI** : On construit le nouveau nom de colonne avec le tag
        new_columns = []
        for name in df_view.columns:
            clean_name = name.replace(suffix, '')
            tag_info = osm_amenities[clean_name]
            new_columns.append(f"{clean_name} (`{tag_info['key']}={tag_info['value']}`)")
        df_view.columns = new_columns

        df_display = df_results[['Population']].join(df_view)
        
        st.subheader(title)
        st.dataframe(df_display, use_container_width=True)
        st.bar_chart(df_view)

        # --- Carte interactive ---
        st.header("🗺️ Carte interactive des équipements")
        # ... (partie carte inchangée)
        map_center_lat, map_center_lon, _ = get_city_info(st.session_state.selected_cities[0])
        if map_center_lat and map_center_lon:
            m = folium.Map(location=[map_center_lat, map_center_lon], zoom_start=12)
            marker_clusters = {name: MarkerCluster().add_to(m) for name in st.session_state.selected_amenities}
            for el in total_elements_for_map:
                if 'lat' in el and 'lon' in el:
                    amenity_name = el['amenity_name']
                    style = osm_amenities[amenity_name]
                    folium.Marker(
                        location=[el['lat'], el['lon']],
                        tooltip=amenity_name.split(" ")[1],
                        icon=folium.Icon(color=style['color'], icon=style['icon'], prefix='fa')
                    ).add_to(marker_clusters[amenity_name])
            st_folium(m, use_container_width=True, height=500)