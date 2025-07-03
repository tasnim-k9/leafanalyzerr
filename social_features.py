import streamlit as st
import json
import os
from datetime import datetime, timedelta
from auth_utils import load_users, get_user_data_path

def get_community_stats():
    """Get community statistics"""
    users = load_users()
    
    stats = {
        "total_users": len(users),
        "farmers": len([u for u in users.values() if u.get("user_type") == "Farmer"]),
        "gardeners": len([u for u in users.values() if u.get("user_type") == "Home Gardener"]),
        "total_plants": 0,
        "healthy_plants": 0,
        "plants_needing_help": 0
    }
    
    # Count plants across all users
    for username in users.keys():
        try:
            plants, _ = load_user_plants_data(username)
            stats["total_plants"] += len(plants)
            for plant in plants:
                if plant.get("health_status") == "Healthy":
                    stats["healthy_plants"] += 1
                elif plant.get("health_status") in ["Needs Attention", "Sick"]:
                    stats["plants_needing_help"] += 1
        except:
            continue
    
    return stats

def load_user_plants_data(username):
    """Load user plants data (helper function)"""
    filepath = get_user_data_path(username, "plants.json")
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                return data.get("plants", []), data.get("logs", [])
        except:
            return [], []
    return [], []

def get_farmer_insights():
    """Get insights specifically for farmers"""
    users = load_users()
    farmers = {k: v for k, v in users.items() if v.get("user_type") == "Farmer"}
    
    insights = {
        "total_farmers": len(farmers),
        "total_farm_area": 0,
        "most_common_diseases": {},
        "crop_distribution": {},
        "regions": {}
    }
    
    for username, user_info in farmers.items():
        # Add farm size (extract number from farm_size string)
        farm_size = user_info.get("farm_size", "0")
        try:
            size_num = float(''.join(filter(str.isdigit, farm_size.split()[0]))) if farm_size else 0
            insights["total_farm_area"] += size_num
        except:
            pass
        
        # Track locations
        location = user_info.get("location", "Unknown")
        insights["regions"][location] = insights["regions"].get(location, 0) + 1
        
        # Analyze farmer's plants
        try:
            plants, logs = load_user_plants_data(username)
            for plant in plants:
                species = plant.get("species", "Unknown")
                insights["crop_distribution"][species] = insights["crop_distribution"].get(species, 0) + 1
        except:
            continue
    
    return insights

def get_disease_alerts():
    """Get disease alerts based on community data"""
    users = load_users()
    recent_diseases = {}
    
    # Look at disease detections from the last 7 days
    cutoff_date = datetime.now() - timedelta(days=7)
    
    for username in users.keys():
        try:
            _, logs = load_user_plants_data(username)
            for log in logs:
                if log.get("activity") == "disease_detected":
                    log_date = datetime.fromisoformat(log.get("date", ""))
                    if log_date > cutoff_date:
                        disease = log.get("notes", "Unknown Disease")
                        location = users[username].get("location", "Unknown")
                        
                        if disease not in recent_diseases:
                            recent_diseases[disease] = {"count": 0, "locations": set()}
                        
                        recent_diseases[disease]["count"] += 1
                        recent_diseases[disease]["locations"].add(location)
        except:
            continue
    
    # Convert sets to lists for JSON serialization
    for disease in recent_diseases:
        recent_diseases[disease]["locations"] = list(recent_diseases[disease]["locations"])
    
    return recent_diseases

def get_success_stories():
    """Get success stories from the community"""
    stories = [
        {
            "farmer": "Rajesh K.",
            "location": "Punjab, India",
            "story": "Used the AI detection to identify early blight in tomatoes. Early intervention saved 80% of my crop!",
            "crop": "Tomatoes",
            "impact": "Saved $2,000 in potential losses"
        },
        {
            "farmer": "Maria S.",
            "location": "California, USA", 
            "story": "The plant tracker helped me optimize watering schedules. Increased my pepper yield by 25%.",
            "crop": "Peppers",
            "impact": "25% yield increase"
        },
        {
            "farmer": "Ahmed H.",
            "location": "Morocco",
            "story": "Weather recommendations prevented fungal diseases during humid season.",
            "crop": "Vegetables",
            "impact": "Zero crop loss during challenging weather"
        }
    ]
    return stories

def log_disease_detection(username, disease_name, confidence, plant_name):
    """Log disease detection for community tracking"""
    try:
        plants, logs = load_user_plants_data(username)
        
        # Add disease detection log
        new_log = {
            "plant_id": None,  # Find plant ID if needed
            "activity": "disease_detected",
            "date": datetime.now().isoformat(),
            "notes": f"{disease_name} (Confidence: {confidence:.1%})",
            "disease": disease_name,
            "confidence": confidence,
            "plant_name": plant_name
        }
        
        logs.append(new_log)
        
        # Save updated data
        from auth_utils import save_user_plants
        save_user_plants(username, plants, logs)
        
    except Exception as e:
        st.error(f"Error logging disease detection: {e}")

def get_regional_tips(user_location):
    """Get location-specific agricultural tips"""
    regional_tips = {
        "India": [
            "Monsoon season: Ensure proper drainage to prevent waterlogging",
            "Summer: Use shade nets for heat-sensitive crops",
            "Winter: Protect from frost with mulching"
        ],
        "USA": [
            "Spring: Watch for late frost warnings",
            "Summer: Implement drip irrigation for water conservation", 
            "Fall: Plan cover crops for soil health"
        ],
        "Europe": [
            "Prepare for climate change impacts on traditional crops",
            "Consider drought-resistant varieties",
            "Monitor for new pest species due to warming temperatures"
        ],
        "Default": [
            "Monitor local weather patterns",
            "Practice crop rotation",
            "Use integrated pest management techniques"
        ]
    }
    
    # Simple matching - in production, use more sophisticated location matching
    for region in regional_tips:
        if region.lower() in user_location.lower():
            return regional_tips[region]
    
    return regional_tips["Default"]