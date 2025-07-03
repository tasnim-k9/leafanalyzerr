import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

def init_plant_tracker():
    """Initialize plant tracker in session state"""
    if 'plants' not in st.session_state:
        st.session_state.plants = []
    if 'plant_logs' not in st.session_state:
        st.session_state.plant_logs = []

def add_plant(name, species, location, health_status, notes=""):
    """Add a new plant to tracker"""
    plant = {
        "id": len(st.session_state.plants) + 1,
        "name": name,
        "species": species,
        "location": location,
        "health_status": health_status,
        "notes": notes,
        "date_added": datetime.now().strftime("%Y-%m-%d"),
        "last_watered": None,
        "last_fertilized": None,
        "last_checked": datetime.now().strftime("%Y-%m-%d")
    }
    st.session_state.plants.append(plant)
    return plant

def log_plant_activity(plant_id, activity_type, notes=""):
    """Log an activity for a plant"""
    log_entry = {
        "plant_id": plant_id,
        "activity": activity_type,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "notes": notes
    }
    st.session_state.plant_logs.append(log_entry)
    
    # Update plant's last activity dates
    for plant in st.session_state.plants:
        if plant["id"] == plant_id:
            if activity_type == "watering":
                plant["last_watered"] = datetime.now().strftime("%Y-%m-%d")
            elif activity_type == "fertilizing":
                plant["last_fertilized"] = datetime.now().strftime("%Y-%m-%d")
            plant["last_checked"] = datetime.now().strftime("%Y-%m-%d")
            break

def get_plant_care_schedule():
    """Generate care schedule based on tracked plants"""
    schedule = []
    
    for plant in st.session_state.plants:
        # Check if watering is due (example: every 3 days)
        if plant["last_watered"]:
            last_watered = datetime.strptime(plant["last_watered"], "%Y-%m-%d")
            if datetime.now() - last_watered > timedelta(days=3):
                schedule.append({
                    "plant": plant["name"],
                    "task": "Watering Due",
                    "priority": "high",
                    "overdue_days": (datetime.now() - last_watered).days - 3
                })
        
        # Check if fertilizing is due (example: every 30 days)
        if plant["last_fertilized"]:
            last_fertilized = datetime.strptime(plant["last_fertilized"], "%Y-%m-%d")
            if datetime.now() - last_fertilized > timedelta(days=30):
                schedule.append({
                    "plant": plant["name"],
                    "task": "Fertilizing Due",
                    "priority": "medium",
                    "overdue_days": (datetime.now() - last_fertilized).days - 30
                })
    
    return sorted(schedule, key=lambda x: x["overdue_days"], reverse=True)

def export_plant_data():
    """Export plant data as JSON"""
    data = {
        "plants": st.session_state.plants,
        "logs": st.session_state.plant_logs,
        "export_date": datetime.now().isoformat()
    }
    return json.dumps(data, indent=2)

def import_plant_data(json_data):
    """Import plant data from JSON"""
    try:
        data = json.loads(json_data)
        st.session_state.plants = data.get("plants", [])
        st.session_state.plant_logs = data.get("logs", [])
        return True
    except:
        return False