# config.py

amenities_categories = {
    "Vie Quotidienne 🌳": {
        "🪑 Bancs publics": {"key": "amenity", "value": "bench"},
        "🗑️ Poubelles": {"key": "amenity", "value": "waste_basket"},
        "📮 Boîtes aux lettres": {"key": "amenity", "value": "post_box"},
        "💧 Fontaines à boire": {"key": "amenity", "value": "drinking_water"},
        "⛲ Toilettes publiques": {"key": "amenity", "value": "toilets"},
    },
    "Loisirs & Culture 🎭": {
        "🎠 Aires de jeux": {"key": "leisure", "value": "playground"},
        "🌳 Parcs & Jardins": {"key": "leisure", "value": "park"},
        "⚽ Terrains de sport": {"key": "leisure", "value": "pitch"},
        "🏀 Centres sportifs": {"key": "leisure", "value": "sports_centre"},
        "🎨 Centres artistiques": {"key": "amenity", "value": "arts_centre"},
        "🎬 Cinémas": {"key": "amenity", "value": "cinema"},
        "📚 Bibliothèques": {"key": "amenity", "value": "library"},
        "🏛️ Musées": {"key": "tourism", "value": "museum"},
    },
    "Commerces & Services 🛒": {
        "🏧 Distributeurs de billets": {"key": "amenity", "value": "atm"},
        "🏦 Banques": {"key": "amenity", "value": "bank"},
        "⚕️ Pharmacies": {"key": "amenity", "value": "pharmacy"},
        "🛒 Supermarchés": {"key": "shop", "value": "supermarket"},
        "🥐 Boulangeries": {"key": "shop", "value": "bakery"},
        "☕ Cafés": {"key": "amenity", "value": "cafe"},
        "🍴 Restaurants": {"key": "amenity", "value": "restaurant"},
    },
    "Transport 🚌": {
        "🚲 Parkings à vélos": {"key": "amenity", "value": "bicycle_parking"},
        "🅿️ Parkings": {"key": "amenity", "value": "parking"},
        "⛽ Stations-service": {"key": "amenity", "value": "fuel"},
        "⚡ Bornes de recharge": {"key": "amenity", "value": "charging_station"},
    },
    "Sécurité & Urgence 🛡️": {
        "📷 Caméras de surveillance": {"key": "man_made", "value": "surveillance"},
        "🚨 Postes de police": {"key": "amenity", "value": "police"},
        "🔥 Bouches d'incendie": {"key": "emergency", "value": "fire_hydrant"},
    }
}

# On crée un dictionnaire plat pour un accès facile aux détails des tags plus tard
all_amenities = {name: details for category in amenities_categories.values() for name, details in category.items()}