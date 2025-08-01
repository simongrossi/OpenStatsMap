# app.py
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# On importe les fonctions et les configurations depuis les autres fichiers
from utils import load_data, get_city_info, get_osm_elements_by_area
from config import amenities_categories, all_amenities

# --- Configuration de la page ---
st.set_page_config(page_title="OpenStatsMap", page_icon="🗺️", layout="wide")

# --- Chargement des données ---
df_communes = load_data()

st.sidebar.title("OpenStatsMap 🗺️")
if df_communes is None:
    st.stop()

# --- Interface Utilisateur ---
st.sidebar.header("Configuration", divider='rainbow')
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

st.session_state.selected_cities = st.sidebar.multiselect("1. Choisissez des villes :", options=sorted(options_villes), default=st.session_state.get('selected_cities', []))

st.sidebar.subheader("2. Cochez les équipements :")
selected_amenities_names = []
for category_name, amenities in amenities_categories.items():
    with st.sidebar.expander(category_name):
        for amenity_name in amenities.keys():
            if st.checkbox(amenity_name, key=f"amenity_{amenity_name}"):
                selected_amenities_names.append(amenity_name)

# --- Logique principale ---
if not st.session_state.selected_cities or not selected_amenities_names:
    st.info("👋 Bienvenue ! Configurez votre recherche dans le menu de gauche pour commencer.")
else:
    all_cities_data = []
    total_elements_for_map = []
    amenities_to_search = {name: all_amenities[name] for name in selected_amenities_names}

    for city_name in st.session_state.selected_cities:
        with st.spinner(f"Analyse de {city_name}..."):
            city_info_from_file = df_communes.loc[df_communes['label'] == city_name].iloc[0]
            population = int(city_info_from_file.get('population', 0))
            lat, lon, area_id = get_city_info(city_name)
            
            if area_id:
                # **CORRECTION** : On ajoute lat et lon au résumé de la ville
                city_summary = {"Ville": city_name, "Population": population, "lat": lat, "lon": lon}
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
            df_view_cols = [f"{name}_total" for name in selected_amenities_names]
            df_view = df_results[df_view_cols].astype(int)
        elif display_mode == "Ratio / 1 000 hab.":
            suffix, title = "_ratio1k", "Ratio pour 1 000 habitants"
            df_view_cols = [f"{name}_ratio1k" for name in selected_amenities_names]
            df_view = df_results[df_view_cols].round(2)
        else:
            suffix, title = "_ratio10k", "Ratio pour 10 000 habitants"
            df_view_cols = [f"{name}_ratio10k" for name in selected_amenities_names]
            df_view = df_results[df_view_cols].round(2)

        new_columns = []
        for name in df_view.columns:
            clean_name = name.replace(suffix, '')
            tag_info = all_amenities[clean_name]
            new_columns.append(f"{clean_name} (`{tag_info['key']}={tag_info['value']}`)")
        df_view.columns = new_columns
        
        df_display = df_results[['Population']].join(df_view)
        
        st.subheader(title)
        st.dataframe(df_display, use_container_width=True)
        st.bar_chart(df_view)

        # --- Carte ---
        st.header("🗺️ Carte interactive des équipements")
        
        # **CORRECTION** : On récupère les coordonnées depuis le DataFrame des résultats
        first_city_coords = df_results.iloc[0]
        map_center_lat = first_city_coords.get('lat')
        map_center_lon = first_city_coords.get('lon')

        if map_center_lat and map_center_lon:
            m = folium.Map(location=[map_center_lat, map_center_lon], zoom_start=12)
            marker_clusters = {name: MarkerCluster().add_to(m) for name in selected_amenities_names}
            for el in total_elements_for_map:
                if 'lat' in el and 'lon' in el:
                    amenity_name = el['amenity_name']
                    style = all_amenities[amenity_name]
                    folium.Marker(
                        location=[el['lat'], el['lon']],
                        tooltip=amenity_name.split(" ")[1],
                        icon=folium.Icon(color=style.get('color', 'blue'), icon=style.get('icon', 'info-sign'), prefix='fa')
                    ).add_to(marker_clusters[amenity_name])
            st_folium(m, use_container_width=True, height=500)
        else:
            st.warning("Impossible d'afficher la carte car aucune coordonnée n'a pu être trouvée pour la première ville sélectionnée.")