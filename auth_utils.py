import streamlit as st
import hashlib
import json
import os
from datetime import datetime
from database import init_database, save_user_to_db, get_user_from_db

# Simple file-based user storage (in production, use a proper database)
USERS_FILE = "users.json"
USER_DATA_DIR = "user_data"

def init_auth():
    """Initialize authentication system"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.user_type = None
    
    # Create directories if they don't exist
    if not os.path.exists(USER_DATA_DIR):
        os.makedirs(USER_DATA_DIR)

def hash_password(password):
    """Hash password for secure storage"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load users from file"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    """Save users to file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def register_user(username, password, email, user_type, location="", farm_size=""):
    """Register a new user"""
    return save_user_to_db(username, hash_password(password), email, user_type, location, farm_size)

def login_user(username, password):
    """Login user"""
    user = get_user_from_db(username)
    
    if not user:
        return False, "User not found"
    
    if user["password_hash"] != hash_password(password):
        return False, "Invalid password"
    
    # Set session state
    st.session_state.authenticated = True
    st.session_state.username = username
    st.session_state.user_type = user["user_type"]
    st.session_state.user_id = user["id"]
    
    return True, "Login successful"

def logout_user():
    """Logout user"""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.user_type = None

def get_user_data_path(username, filename):
    """Get path for user data file"""
    return os.path.join(USER_DATA_DIR, username, filename)

def save_user_plants(username, plants, logs):
    """Save user's plant data"""
    data = {
        "plants": plants,
        "logs": logs,
        "last_updated": datetime.now().isoformat()
    }
    
    filepath = get_user_data_path(username, "plants.json")
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def load_user_plants(username):
    """Load user's plant data"""
    filepath = get_user_data_path(username, "plants.json")
    
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                return data.get("plants", []), data.get("logs", [])
        except:
            return [], []
    
    return [], []

def get_user_profile(username):
    """Get user profile information"""
    user = get_user_from_db(username)
    return user if user else {}

def update_user_profile(username, updates):
    """Update user profile"""
    users = load_users()
    if username in users:
        users[username].update(updates)
        save_users(users)
        return True
    return False