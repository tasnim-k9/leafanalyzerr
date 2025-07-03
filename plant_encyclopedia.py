import streamlit as st

PLANT_ENCYCLOPEDIA = {
    "Tomato": {
        "scientific_name": "Solanum lycopersicum",
        "family": "Solanaceae",
        "care_difficulty": "Easy",
        "watering": "Regular, deep watering. Avoid overhead watering.",
        "light": "Full sun (6-8 hours daily)",
        "soil": "Well-draining, slightly acidic to neutral (pH 6.0-7.0)",
        "temperature": "65-85°F (18-29°C)",
        "humidity": "50-70%",
        "fertilizer": "Balanced fertilizer every 2-3 weeks during growing season",
        "common_diseases": ["Early Blight", "Late Blight", "Bacterial Spot", "Leaf Mold"],
        "companion_plants": ["Basil", "Carrots", "Lettuce", "Peppers"],
        "harvest_time": "70-85 days from transplant",
        "tips": [
            "Stake or cage plants for support",
            "Remove suckers for better fruit production", 
            "Mulch to retain moisture and prevent disease",
            "Rotate crops yearly to prevent soil-borne diseases"
        ]
    },
    "Apple": {
        "scientific_name": "Malus domestica",
        "family": "Rosaceae",
        "care_difficulty": "Moderate",
        "watering": "Deep, infrequent watering. About 1 inch per week.",
        "light": "Full sun (at least 6 hours daily)",
        "soil": "Well-draining, slightly acidic (pH 6.0-6.8)",
        "temperature": "Varies by variety, most need chill hours",
        "humidity": "Moderate, good air circulation important",
        "fertilizer": "Annual application of compost and balanced fertilizer",
        "common_diseases": ["Apple Scab", "Fire Blight", "Cedar Apple Rust", "Black Rot"],
        "companion_plants": ["Chives", "Nasturtiums", "Marigolds"],
        "harvest_time": "Late summer to fall, depending on variety",
        "tips": [
            "Prune during dormant season for shape and air circulation",
            "Thin fruits when young for better quality harvest",
            "Apply dormant oil in late winter for pest control",
            "Choose disease-resistant varieties when possible"
        ]
    },
    "Potato": {
        "scientific_name": "Solanum tuberosum", 
        "family": "Solanaceae",
        "care_difficulty": "Easy",
        "watering": "Consistent moisture, especially during tuber formation",
        "light": "Full sun to partial shade",
        "soil": "Loose, well-draining, slightly acidic (pH 5.8-6.2)",
        "temperature": "60-70°F (15-21°C) optimal",
        "humidity": "Moderate, avoid high humidity",
        "fertilizer": "Low nitrogen, higher phosphorus and potassium",
        "common_diseases": ["Early Blight", "Late Blight", "Potato Scab", "Black Leg"],
        "companion_plants": ["Beans", "Corn", "Cabbage", "Marigolds"],
        "harvest_time": "70-120 days depending on variety",
        "tips": [
            "Hill soil around plants as they grow",
            "Avoid overhead watering to prevent disease",
            "Harvest on dry days and cure before storage",
            "Don't plant where tomatoes grew previously"
        ]
    },
    "Pepper": {
        "scientific_name": "Capsicum spp.",
        "family": "Solanaceae", 
        "care_difficulty": "Easy",
        "watering": "Regular, consistent watering. Allow soil to dry slightly between waterings.",
        "light": "Full sun (6-8 hours daily)",
        "soil": "Well-draining, rich in organic matter (pH 6.0-6.8)",
        "temperature": "70-85°F (21-29°C)",
        "humidity": "50-60%",
        "fertilizer": "Balanced fertilizer, reduce nitrogen once flowering begins",
        "common_diseases": ["Bacterial Spot", "Anthracnose", "Phytophthora Blight"],
        "companion_plants": ["Tomatoes", "Basil", "Onions", "Carrots"],
        "harvest_time": "60-90 days from transplant",
        "tips": [
            "Support plants with stakes or cages",
            "Harvest regularly to encourage more production",
            "Avoid overhead watering",
            "Mulch to maintain consistent soil moisture"
        ]
    }
}

def search_plant_info(query):
    """Search for plant information"""
    results = []
    query_lower = query.lower()
    
    for plant_name, info in PLANT_ENCYCLOPEDIA.items():
        if (query_lower in plant_name.lower() or 
            query_lower in info["scientific_name"].lower() or
            query_lower in info["family"].lower()):
            results.append((plant_name, info))
    
    return results

def get_plant_info(plant_name):
    """Get detailed information about a specific plant"""
    return PLANT_ENCYCLOPEDIA.get(plant_name, None)

def get_all_plants():
    """Get list of all plants in encyclopedia"""
    return list(PLANT_ENCYCLOPEDIA.keys())

def get_plants_by_difficulty(difficulty):
    """Get plants filtered by care difficulty"""
    return [name for name, info in PLANT_ENCYCLOPEDIA.items() 
            if info["care_difficulty"].lower() == difficulty.lower()]

def get_disease_prone_plants(disease):
    """Get plants that are prone to a specific disease"""
    disease_lower = disease.lower()
    plants = []
    
    for plant_name, info in PLANT_ENCYCLOPEDIA.items():
        for plant_disease in info["common_diseases"]:
            if disease_lower in plant_disease.lower():
                plants.append(plant_name)
                break
    
    return plants