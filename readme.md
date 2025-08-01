# 🌆 OpenStatsMap

**OpenStatsMap** est une application web interactive développée avec **Streamlit** pour analyser et comparer la **densité d'équipements publics** des villes françaises.

À partir des données démographiques de l'INSEE et des données géographiques d'OpenStreetMap, l'application **calcule en temps réel des ratios d'équipements par habitant** et affiche les résultats sous forme de tableaux, graphiques et cartes interactives.

---

## 🚀 Fonctionnalités

- 📊 Classement dynamique des villes selon des critères multiples (nombre total, ratio / 1k, / 10k habitants).
- 🔎 Recherche de villes flexible par **nom**, **département** ou **code postal**.
- ✅ Sélection fine de dizaines d'équipements classés par catégories (bancs, pharmacies, bornes de recharge, etc.).
- 🗺️ Carte interactive affichant la localisation précise de chaque équipement trouvé, avec **regroupement automatique (clustering)**.
- 🔄 Données en **temps réel** via l'API Overpass d'OpenStreetMap, garantissant des informations à jour.
- 🧾 Transparence des requêtes avec un **visualiseur des appels** faits à l'API.

---

## 🛠️ Technologies

- **Frontend** : [Streamlit](https://streamlit.io/)
- **Données tabulaires** : [Pandas](https://pandas.pydata.org/)
- **Cartographie** : [Folium](https://python-visualization.github.io/folium/) & [streamlit-folium](https://github.com/randyzwitch/streamlit-folium)
- **APIs géographiques** :
  - [Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API) (données OSM)
  - [Nominatim](https://nominatim.openstreetmap.org/) (géocodage)

---

## ▶️ Installation et Lancement

### Cloner le dépôt

```bash
git clone https://github.com/votre-utilisateur/OpenStatsMap.git
cd OpenStatsMap
```

### Créer et activer un environnement virtuel (recommandé)

```bash
python -m venv venv
# Sur Mac/Linux:
source venv/bin/activate
# Sur Windows:
venv\Scripts\activate
```

### Installer les dépendances

```bash
pip install -r requirements.txt
```

### Lancer l’application

```bash
streamlit run app.py
```

L'application devrait s'ouvrir automatiquement dans votre navigateur.

---

## 📂 Structure du Projet

Il est recommandé d'ajouter un fichier `.gitignore` (depuis un modèle Python standard) pour exclure les fichiers de l'environnement virtuel.

| Fichier                        | Description |
|-------------------------------|-------------|
| `app.py`                      | Script principal de l'interface et de la logique Streamlit |
| `utils.py` *(optionnel)*      | Fonctions utilitaires (appels API, chargement des données) |
| `config.py` *(optionnel)*     | Fichier de configuration (liste des équipements) |
| `requirements.txt`            | Dépendances Python du projet |
| `communes_population...json`  | Données démographiques sur les communes françaises |
| `README.md`                   | Ce fichier de documentation |

---

## 🗺️ Roadmap

- 🧮 **Score Pondéré** : Mise en place d'un score de "qualité de vie" personnalisable en attribuant des poids aux différents équipements.
- 📤 **Export des Données** : Ajout de formats d'export (JSON, Excel) pour les résultats et la carte (HTML).
- 🌐 **Internationalisation** : Extension de l'analyse à des villes hors de France en adaptant la recherche de zone administrative.
- ➕ **Personnalisation** : Permettre à l'utilisateur d'ajouter ses propres tags OSM à la volée.

---

## 📜 Licence

Ce projet est sous **licence MIT**. Voir le fichier `LICENSE` pour plus de détails.

---

## 🤝 Contribuer

Les contributions sont les bienvenues !  
Pour toute suggestion ou rapport de bug, merci d’ouvrir une *issue*.  
Pour proposer une modification, n'hésitez pas à créer une *pull request*.
