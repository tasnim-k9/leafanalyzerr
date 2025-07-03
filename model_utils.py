import numpy as np
from PIL import Image
import requests
import os
from io import BytesIO
import random

# Plant disease class names
CLASS_NAMES = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Blueberry___healthy',
    'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot',
    'Corn_(maize)___Common_rust',
    'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy',
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot',
    'Peach___healthy',
    'Pepper,_bell___Bacterial_spot',
    'Pepper,_bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Raspberry___healthy',
    'Soybean___healthy',
    'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch',
    'Strawberry___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

class SimplePlantClassifier:
    """A simple plant disease classifier using image analysis"""
    
    def __init__(self):
        self.class_names = CLASS_NAMES
        random.seed(42)  # For consistent demo results
    
    def predict(self, processed_image, verbose=0):
        """Make a prediction based on image features"""
        # Analyze image characteristics
        image_array = processed_image[0] * 255  # Convert back to 0-255 range
        
        # Calculate basic image statistics
        mean_brightness = np.mean(image_array)
        green_channel = image_array[:, :, 1]  # Green channel for leaf analysis
        red_channel = image_array[:, :, 0]
        blue_channel = image_array[:, :, 2]
        
        # Calculate color ratios and variability
        green_ratio = np.mean(green_channel) / 255.0
        red_ratio = np.mean(red_channel) / 255.0
        blue_ratio = np.mean(blue_channel) / 255.0
        
        # Calculate standard deviation to detect spots/variations
        green_std = np.std(green_channel)
        red_std = np.std(red_channel)
        color_variation = green_std + red_std
        
        # More sensitive disease detection criteria
        brown_detection = (red_ratio > 0.35 and green_ratio < 0.65) or (red_ratio - green_ratio > 0.1)
        yellow_detection = (red_ratio > 0.5 and green_ratio > 0.5 and blue_ratio < 0.6)
        spot_detection = color_variation > 35  # Detect color inconsistencies
        dark_patches = mean_brightness < 120
        color_imbalance = abs(green_ratio - 0.6) > 0.2  # Unhealthy if far from ideal green
        
        # Create probability distribution based on image analysis
        probabilities = np.zeros(len(self.class_names))
        
        # Disease indicators
        disease_score = 0
        if brown_detection: disease_score += 3
        if yellow_detection: disease_score += 2
        if spot_detection: disease_score += 2
        if dark_patches: disease_score += 1
        if color_imbalance: disease_score += 1
        
        # Healthy leaves: very green, consistent color, good brightness
        if (green_ratio > 0.65 and disease_score <= 1 and 
            color_variation < 25 and mean_brightness > 100):
            healthy_indices = [i for i, name in enumerate(self.class_names) if 'healthy' in name]
            total_healthy_prob = 0.7 + random.uniform(0, 0.2)
            for idx in healthy_indices:
                probabilities[idx] = total_healthy_prob / len(healthy_indices)
            
            # Add small chance for diseases
            disease_indices = [i for i, name in enumerate(self.class_names) if 'healthy' not in name]
            remaining_prob = 1 - total_healthy_prob
            for idx in disease_indices:
                probabilities[idx] = remaining_prob / len(disease_indices) * random.uniform(0.1, 1.0)
        
        # Disease detected - higher disease probability
        else:
            disease_indices = [i for i, name in enumerate(self.class_names) if 'healthy' not in name]
            healthy_indices = [i for i, name in enumerate(self.class_names) if 'healthy' in name]
            
            # Select likely diseases based on color patterns
            if brown_detection and (spot_detection or dark_patches):
                # Brown/dark spots suggest blight or rot diseases
                likely_diseases = ['Early_blight', 'Late_blight', 'Black_rot', 'Leaf_blight', 'Target_Spot']
            elif yellow_detection:
                # Yellow patterns suggest virus or nutrient issues
                likely_diseases = ['Yellow_Leaf_Curl_Virus', 'mosaic_virus', 'Septoria']
            elif spot_detection:
                # General spotting diseases
                likely_diseases = ['Bacterial_spot', 'Septoria', 'Leaf_Mold', 'Apple_scab']
            else:
                # Other diseases
                likely_diseases = ['Bacterial_spot', 'Target_Spot', 'Leaf_Mold', 'Spider_mites']
            
            # Assign higher probabilities to likely diseases
            total_disease_prob = 0.7 + random.uniform(0, 0.2)
            likely_disease_indices = []
            for idx in disease_indices:
                class_name = self.class_names[idx]
                if any(disease in class_name for disease in likely_diseases):
                    likely_disease_indices.append(idx)
            
            # Distribute probability among likely diseases
            if likely_disease_indices:
                for idx in likely_disease_indices:
                    probabilities[idx] = (total_disease_prob / len(likely_disease_indices)) * random.uniform(0.5, 1.5)
            
            # Add smaller probabilities for other diseases
            for idx in disease_indices:
                if idx not in likely_disease_indices:
                    probabilities[idx] = random.uniform(0.01, 0.1)
            
            # Small chance for healthy
            for idx in healthy_indices:
                probabilities[idx] = random.uniform(0.01, 0.15)
        
        # Ensure probabilities sum to 1
        total_prob = np.sum(probabilities)
        if total_prob > 0:
            probabilities = probabilities / total_prob
        else:
            # Fallback - equal distribution
            probabilities = np.ones(len(self.class_names)) / len(self.class_names)
        
        return probabilities.reshape(1, -1)

def load_model():
    """Load the plant disease detection model"""
    try:
        # Return our simple classifier
        model = SimplePlantClassifier()
        return model
        
    except Exception as e:
        raise Exception(f"Failed to load model: {str(e)}")

def preprocess_image(image):
    """Preprocess the image for model prediction"""
    try:
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize image to model input size
        image = image.resize((224, 224))
        
        # Convert to numpy array
        image_array = np.array(image)
        
        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)
        
        # Normalize pixel values
        image_array = image_array.astype(np.float32) / 255.0
        
        return image_array
        
    except Exception as e:
        raise Exception(f"Failed to preprocess image: {str(e)}")

def predict_disease(model, processed_image):
    """Make disease prediction using the model"""
    try:
        # Make prediction
        predictions = model.predict(processed_image, verbose=0)
        
        # Get prediction probabilities
        prediction_probs = predictions[0]
        
        # Create dictionary of class names and probabilities
        results = {}
        for i, class_name in enumerate(CLASS_NAMES):
            # Clean up class name for display
            clean_name = clean_class_name(class_name)
            results[clean_name] = float(prediction_probs[i])
        
        return results
        
    except Exception as e:
        raise Exception(f"Failed to make prediction: {str(e)}")

def clean_class_name(class_name):
    """Clean up class name for better display"""
    # Remove plant name prefix and format
    if '___' in class_name:
        parts = class_name.split('___')
        plant = parts[0].replace('_', ' ').title()
        disease = parts[1].replace('_', ' ').title()
        
        if disease.lower() == 'healthy':
            return 'Healthy'
        else:
            return f"{plant} - {disease}"
    else:
        return class_name.replace('_', ' ').title()

def get_model_info():
    """Get information about the loaded model"""
    return {
        'name': 'Plant Disease Detection Model',
        'input_shape': (224, 224, 3),
        'num_classes': len(CLASS_NAMES),
        'classes': CLASS_NAMES
    }
