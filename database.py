import sqlite3
import json
import os
from datetime import datetime

DB_FILE = "agricare.db"

def init_database():
    """Initialize the SQLite database with all necessary tables"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT NOT NULL,
            user_type TEXT NOT NULL,
            location TEXT,
            farm_size TEXT,
            created_date TEXT,
            last_login TEXT
        )
    ''')
    
    # Plants table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            species TEXT NOT NULL,
            location TEXT,
            health_status TEXT,
            notes TEXT,
            date_added TEXT,
            last_watered TEXT,
            last_fertilized TEXT,
            last_checked TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Plant activity logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plant_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            plant_id INTEGER,
            activity TEXT,
            date TEXT,
            notes TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (plant_id) REFERENCES plants (id)
        )
    ''')
    
    # Disease detections table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS disease_detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            plant_name TEXT,
            disease_name TEXT,
            confidence REAL,
            detection_date TEXT,
            location TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Plant images table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plant_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plant_name TEXT NOT NULL,
            disease_name TEXT,
            image_url TEXT,
            description TEXT,
            category TEXT
        )
    ''')
    
    # Insert sample plant images
    sample_images = [
        ("Tomato", "Healthy", "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=400", "Healthy tomato plant with vibrant green leaves", "healthy"),
        ("Tomato", "Early Blight", "https://images.unsplash.com/photo-1574482620911-95c8c2d34044?w=400", "Tomato leaf showing early blight symptoms", "diseased"),
        ("Apple", "Healthy", "https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=400", "Healthy apple tree with green foliage", "healthy"),
        ("Apple", "Apple Scab", "https://images.unsplash.com/photo-1584306670957-acf935f5033c?w=400", "Apple leaves affected by scab disease", "diseased"),
        ("Potato", "Healthy", "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400", "Healthy potato plant in field", "healthy"),
        ("Potato", "Late Blight", "https://images.unsplash.com/photo-1582284540020-8acbb4541044?w=400", "Potato plant showing late blight damage", "diseased"),
        ("Pepper", "Healthy", "https://images.unsplash.com/photo-1583663848850-46af132dc3ae?w=400", "Healthy pepper plant with fruits", "healthy"),
        ("Corn", "Healthy", "https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=400", "Healthy corn field", "healthy"),
        ("Grape", "Healthy", "https://images.unsplash.com/photo-1537640538966-79f369143f8f?w=400", "Healthy grape vines", "healthy"),
        ("Lettuce", "Healthy", "https://images.unsplash.com/photo-1556075798-4825dfaaf498?w=400", "Fresh lettuce in garden", "healthy")
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO plant_images (plant_name, disease_name, image_url, description, category)
        VALUES (?, ?, ?, ?, ?)
    ''', sample_images)
    
    # Insert sample success stories
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS success_stories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_name TEXT,
            location TEXT,
            crop TEXT,
            story TEXT,
            impact TEXT,
            date_added TEXT
        )
    ''')
    
    sample_stories = [
        ("Rajesh K.", "Punjab, India", "Tomatoes", "Used the AI detection to identify early blight in tomatoes. Early intervention saved 80% of my crop!", "Saved $2,000 in potential losses", datetime.now().isoformat()),
        ("Maria S.", "California, USA", "Peppers", "The plant tracker helped me optimize watering schedules. Increased my pepper yield by 25%.", "25% yield increase", datetime.now().isoformat()),
        ("Ahmed H.", "Morocco", "Mixed Vegetables", "Weather recommendations prevented fungal diseases during humid season.", "Zero crop loss during challenging weather", datetime.now().isoformat()),
        ("Lin W.", "China", "Rice", "Community disease alerts helped me prepare preventive treatments before problems spread to my fields.", "Prevented disease outbreak", datetime.now().isoformat()),
        ("Carlos M.", "Brazil", "Coffee", "The plant encyclopedia guided me through organic pest management, improving coffee quality.", "30% improvement in bean quality", datetime.now().isoformat())
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO success_stories (farmer_name, location, crop, story, impact, date_added)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', sample_stories)
    
    conn.commit()
    conn.close()

def get_plant_images(plant_name=None, category=None):
    """Get plant images from database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    query = "SELECT * FROM plant_images WHERE 1=1"
    params = []
    
    if plant_name:
        query += " AND plant_name = ?"
        params.append(plant_name)
    
    if category:
        query += " AND category = ?"
        params.append(category)
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    
    return [
        {
            "id": row[0],
            "plant_name": row[1],
            "disease_name": row[2],
            "image_url": row[3],
            "description": row[4],
            "category": row[5]
        }
        for row in results
    ]

def get_success_stories():
    """Get success stories from database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM success_stories ORDER BY date_added DESC")
    results = cursor.fetchall()
    conn.close()
    
    return [
        {
            "farmer": row[1],
            "location": row[2],
            "crop": row[3],
            "story": row[4],
            "impact": row[5]
        }
        for row in results
    ]

def save_user_to_db(username, password_hash, email, user_type, location="", farm_size=""):
    """Save user to database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO users (username, password_hash, email, user_type, location, farm_size, created_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (username, password_hash, email, user_type, location, farm_size, datetime.now().isoformat()))
        
        conn.commit()
        return True, "User registered successfully"
    except sqlite3.IntegrityError:
        return False, "Username already exists"
    finally:
        conn.close()

def get_user_from_db(username):
    """Get user from database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            "id": result[0],
            "username": result[1],
            "password_hash": result[2],
            "email": result[3],
            "user_type": result[4],
            "location": result[5],
            "farm_size": result[6],
            "created_date": result[7],
            "last_login": result[8]
        }
    return None

def save_plant_to_db(user_id, name, species, location, health_status, notes):
    """Save plant to database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO plants (user_id, name, species, location, health_status, notes, date_added, last_checked)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, name, species, location, health_status, notes, datetime.now().isoformat(), datetime.now().isoformat()))
    
    plant_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return plant_id

def get_user_plants(user_id):
    """Get user's plants from database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM plants WHERE user_id = ?", (user_id,))
    results = cursor.fetchall()
    conn.close()
    
    return [
        {
            "id": row[0],
            "name": row[2],
            "species": row[3],
            "location": row[4],
            "health_status": row[5],
            "notes": row[6],
            "date_added": row[7],
            "last_watered": row[8],
            "last_fertilized": row[9],
            "last_checked": row[10]
        }
        for row in results
    ]

def log_disease_detection_db(user_id, plant_name, disease_name, confidence, location=""):
    """Log disease detection to database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO disease_detections (user_id, plant_name, disease_name, confidence, detection_date, location)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, plant_name, disease_name, confidence, datetime.now().isoformat(), location))
    
    conn.commit()
    conn.close()

def get_community_disease_stats():
    """Get community disease statistics"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Get recent disease detections (last 30 days)
    cursor.execute('''
        SELECT disease_name, location, COUNT(*) as count
        FROM disease_detections 
        WHERE detection_date > datetime('now', '-30 days')
        GROUP BY disease_name, location
        ORDER BY count DESC
        LIMIT 10
    ''')
    
    results = cursor.fetchall()
    conn.close()
    
    disease_alerts = {}
    for row in results:
        disease = row[0]
        location = row[1]
        count = row[2]
        
        if disease not in disease_alerts:
            disease_alerts[disease] = {"count": 0, "locations": []}
        
        disease_alerts[disease]["count"] += count
        if location and location not in disease_alerts[disease]["locations"]:
            disease_alerts[disease]["locations"].append(location)
    
    return disease_alerts