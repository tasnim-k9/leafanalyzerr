import requests
import streamlit as st
from datetime import datetime, timedelta

def get_weather_recommendations(location=None):
    """Get weather-based plant care recommendations"""
    
    # Mock weather data for demonstration (in production, you'd use a real weather API)
    weather_conditions = {
        "temperature": 22,  # Celsius
        "humidity": 65,     # Percentage
        "rainfall": 2.5,    # mm in last 24h
        "wind_speed": 12,   # km/h
        "uv_index": 6,
        "forecast": "Partly cloudy with chance of rain"
    }
    
    recommendations = []
    
    # Temperature-based recommendations
    if weather_conditions["temperature"] > 30:
        recommendations.append({
            "type": "warning",
            "icon": "🌡️",
            "title": "High Temperature Alert",
            "message": "Increase watering frequency and provide shade for sensitive plants. Monitor for heat stress."
        })
    elif weather_conditions["temperature"] < 5:
        recommendations.append({
            "type": "warning", 
            "icon": "❄️",
            "title": "Cold Weather Alert",
            "message": "Protect plants from frost. Move potted plants indoors if possible."
        })
    
    # Humidity recommendations
    if weather_conditions["humidity"] > 80:
        recommendations.append({
            "type": "info",
            "icon": "💧",
            "title": "High Humidity",
            "message": "Watch for fungal diseases. Ensure good air circulation around plants."
        })
    elif weather_conditions["humidity"] < 30:
        recommendations.append({
            "type": "info",
            "icon": "🏜️", 
            "title": "Low Humidity",
            "message": "Consider misting plants or using humidity trays for moisture-loving species."
        })
    
    # Rainfall recommendations
    if weather_conditions["rainfall"] > 20:
        recommendations.append({
            "type": "warning",
            "icon": "☔",
            "title": "Heavy Rainfall",
            "message": "Check for waterlogged soil and ensure proper drainage. Watch for root rot signs."
        })
    elif weather_conditions["rainfall"] < 0.5:
        recommendations.append({
            "type": "info",
            "icon": "☀️",
            "title": "Dry Conditions", 
            "message": "Increase watering frequency. Check soil moisture regularly."
        })
    
    return weather_conditions, recommendations

def get_seasonal_tips():
    """Get seasonal plant care tips"""
    
    current_month = datetime.now().month
    
    seasonal_tips = {
        "spring": {
            "months": [3, 4, 5],
            "title": "🌱 Spring Care Tips",
            "tips": [
                "Start fertilizing as growth begins",
                "Begin pruning dormant plants",
                "Watch for early pest activity",
                "Gradually increase watering",
                "Plant new seedlings after last frost"
            ]
        },
        "summer": {
            "months": [6, 7, 8],
            "title": "☀️ Summer Care Tips", 
            "tips": [
                "Water early morning or late evening",
                "Provide shade during extreme heat",
                "Monitor for spider mites and aphids",
                "Deadhead flowers to encourage blooming",
                "Mulch to retain soil moisture"
            ]
        },
        "autumn": {
            "months": [9, 10, 11],
            "title": "🍂 Autumn Care Tips",
            "tips": [
                "Reduce watering frequency",
                "Collect and destroy fallen diseased leaves",
                "Apply dormant season treatments",
                "Prepare plants for winter",
                "Plant cover crops or bulbs"
            ]
        },
        "winter": {
            "months": [12, 1, 2],
            "title": "❄️ Winter Care Tips",
            "tips": [
                "Reduce watering significantly",
                "Protect plants from frost", 
                "Plan next year's garden",
                "Clean and maintain garden tools",
                "Order seeds for spring planting"
            ]
        }
    }
    
    for season, data in seasonal_tips.items():
        if current_month in data["months"]:
            return data
    
    return seasonal_tips["spring"]  # Default fallback