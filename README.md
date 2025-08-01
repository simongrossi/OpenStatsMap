# 🌆 CityRanker

**CityRanker** est une application interactive développée avec Streamlit permettant de **classer les villes** selon leur **nombre d’équipements publics par habitant** (toilettes, bancs, parcs, etc.).  
Les données sont extraites en temps réel depuis **OpenStreetMap** grâce à l’API **Overpass**.

---

## 🚀 Fonctionnalités principales

- 🔢 **Classement automatique** des villes selon le ratio _équipements / population_
- 🎯 **Choix du type d’équipement** à analyser : toilettes, bancs, parcs, etc.
- 🗺️ **Carte interactive** des équipements publics localisés
- 🌍 **Données en temps réel** issues d’OpenStreetMap
- 🧭 **Interface web légère** accessible via navigateur

---

## 🛠️ Technologies utilisées

- [Streamlit](https://streamlit.io/) – interface web interactive
- [Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API) – extraction des données OSM
- [Folium](https://python-visualization.github.io/folium/) – cartographie interactive
- [Pandas](https://pandas.pydata.org/) – traitement de données

---

## ▶️ Lancer l’application

```bash
# Installation des dépendances
pip install -r requirements.txt

# Lancement de l'application
streamlit run app.py


📡 Exemples de tags OpenStreetMap
Type d’équipement	Tag OSM
Toilettes	amenity=toilets
Bancs	amenity=bench
Parcs	leisure=park

🔜 Prochaines évolutions
📂 Chargement de fichiers CSV avec population personnalisée

🌍 Extension à davantage de villes françaises et internationales

📤 Export des classements (CSV, PDF)

📊 Intégration de graphes interactifs avec Plotly

📜 Licence
Code distribué sous licence MIT — libre d’utilisation, modification et distribution.
