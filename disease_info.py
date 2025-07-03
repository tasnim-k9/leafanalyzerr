"""
Disease information database containing descriptions, symptoms, and treatments
"""

DISEASE_INFO = {
    'Apple - Apple Scab': {
        'description': 'A fungal disease that affects apple trees, causing dark, scaly lesions on leaves and fruit.',
        'symptoms': [
            'Dark, circular spots on leaves',
            'Olive-green to black lesions',
            'Premature leaf drop',
            'Fruit cracking and deformation'
        ],
        'treatments': [
            'Apply fungicide sprays during growing season',
            'Remove fallen leaves and infected debris',
            'Prune for better air circulation',
            'Choose resistant apple varieties'
        ],
        'severity': 'Medium'
    },
    
    'Apple - Black Rot': {
        'description': 'A serious fungal disease causing leaf spots and fruit rot in apple trees.',
        'symptoms': [
            'Brown leaf spots with purple borders',
            'Black, sunken cankers on fruit',
            'Premature fruit drop',
            'Branch cankers in severe cases'
        ],
        'treatments': [
            'Apply copper-based fungicides',
            'Remove infected fruits and leaves',
            'Prune infected branches',
            'Improve orchard sanitation'
        ],
        'severity': 'High'
    },
    
    'Apple - Cedar Apple Rust': {
        'description': 'A fungal disease requiring both apple and cedar trees to complete its life cycle.',
        'symptoms': [
            'Yellow-orange spots on upper leaf surface',
            'Horn-like projections on spots',
            'Premature defoliation',
            'Reduced fruit quality'
        ],
        'treatments': [
            'Apply preventive fungicide sprays',
            'Remove nearby cedar trees if possible',
            'Plant resistant apple varieties',
            'Improve air circulation around trees'
        ],
        'severity': 'Medium'
    },
    
    'Tomato - Early Blight': {
        'description': 'A common fungal disease affecting tomatoes, causing leaf spots and fruit rot.',
        'symptoms': [
            'Dark spots with concentric rings on lower leaves',
            'Yellow halos around spots',
            'Progressive leaf yellowing and death',
            'Fruit lesions near stem end'
        ],
        'treatments': [
            'Apply fungicide treatments',
            'Improve air circulation',
            'Avoid overhead watering',
            'Remove infected plant debris'
        ],
        'severity': 'Medium'
    },
    
    'Tomato - Late Blight': {
        'description': 'A devastating disease that can rapidly destroy tomato plants and spread quickly.',
        'symptoms': [
            'Water-soaked lesions on leaves',
            'White fuzzy growth on leaf undersides',
            'Brown to black lesions on stems',
            'Rapid plant collapse in humid conditions'
        ],
        'treatments': [
            'Apply copper-based fungicides immediately',
            'Remove infected plants completely',
            'Improve air circulation and drainage',
            'Avoid overhead irrigation'
        ],
        'severity': 'High'
    },
    
    'Tomato - Leaf Mold': {
        'description': 'A fungal disease that thrives in high humidity, affecting tomato leaves.',
        'symptoms': [
            'Yellow spots on upper leaf surface',
            'Fuzzy olive-green growth on leaf undersides',
            'Progressive yellowing and browning',
            'Reduced fruit production'
        ],
        'treatments': [
            'Reduce humidity levels',
            'Improve ventilation',
            'Apply appropriate fungicides',
            'Remove infected leaves promptly'
        ],
        'severity': 'Medium'
    },
    
    'Tomato - Septoria Leaf Spot': {
        'description': 'A fungal disease causing numerous small spots on tomato leaves.',
        'symptoms': [
            'Small, circular spots with dark borders',
            'Gray centers with tiny black specks',
            'Lower leaves affected first',
            'Progressive defoliation from bottom up'
        ],
        'treatments': [
            'Apply fungicide sprays',
            'Mulch around plants',
            'Water at soil level',
            'Remove infected lower leaves'
        ],
        'severity': 'Medium'
    },
    
    'Tomato - Spider Mites': {
        'description': 'Tiny pests that feed on plant sap, causing stippling and webbing on leaves.',
        'symptoms': [
            'Fine stippling on leaf surface',
            'Webbing on undersides of leaves',
            'Yellow or bronze discoloration',
            'Premature leaf drop in severe cases'
        ],
        'treatments': [
            'Increase humidity around plants',
            'Apply miticide or insecticidal soap',
            'Introduce beneficial predatory mites',
            'Regular monitoring and early intervention'
        ],
        'severity': 'Medium'
    },
    
    'Tomato - Target Spot': {
        'description': 'A fungal disease causing distinctive target-like spots on tomato leaves.',
        'symptoms': [
            'Brown spots with concentric rings',
            'Target-like appearance on leaves',
            'Yellowing around spots',
            'Fruit lesions in advanced stages'
        ],
        'treatments': [
            'Apply fungicide treatments',
            'Improve air circulation',
            'Practice crop rotation',
            'Remove infected plant material'
        ],
        'severity': 'Medium'
    },
    
    'Tomato - Tomato Yellow Leaf Curl Virus': {
        'description': 'A viral disease transmitted by whiteflies, causing severe stunting and yield loss.',
        'symptoms': [
            'Upward curling of leaves',
            'Yellow leaf margins',
            'Stunted plant growth',
            'Reduced fruit set and size'
        ],
        'treatments': [
            'Control whitefly populations',
            'Use reflective mulches',
            'Plant resistant varieties',
            'Remove infected plants immediately'
        ],
        'severity': 'High'
    },
    
    'Tomato - Tomato Mosaic Virus': {
        'description': 'A viral disease causing mottled patterns on leaves and affecting fruit quality.',
        'symptoms': [
            'Mottled light and dark green patterns',
            'Distorted leaf growth',
            'Stunted plant development',
            'Poor fruit quality and yield'
        ],
        'treatments': [
            'Remove infected plants',
            'Disinfect tools between plants',
            'Control aphid vectors',
            'Plant virus-resistant varieties'
        ],
        'severity': 'High'
    },
    
    'Potato - Early Blight': {
        'description': 'A fungal disease affecting potato plants, causing yield reduction.',
        'symptoms': [
            'Dark spots with concentric rings on leaves',
            'Yellow halos around lesions',
            'Progressive defoliation',
            'Tuber lesions during storage'
        ],
        'treatments': [
            'Apply fungicide sprays',
            'Practice crop rotation',
            'Avoid overhead irrigation',
            'Maintain proper plant spacing'
        ],
        'severity': 'Medium'
    },
    
    'Potato - Late Blight': {
        'description': 'The same pathogen that caused the Irish Potato Famine, very destructive.',
        'symptoms': [
            'Water-soaked lesions on leaves',
            'White sporulation on leaf undersides',
            'Rapid tissue collapse',
            'Brown rot in tubers'
        ],
        'treatments': [
            'Apply preventive fungicide treatments',
            'Destroy infected plants immediately',
            'Improve field drainage',
            'Use certified disease-free seed potatoes'
        ],
        'severity': 'High'
    },
    
    'Healthy': {
        'description': 'The leaf appears healthy with no signs of disease.',
        'symptoms': [
            'Vibrant green coloration',
            'No spots or lesions',
            'Normal leaf structure',
            'No signs of pest damage'
        ],
        'treatments': [
            'Continue regular monitoring',
            'Maintain proper nutrition',
            'Ensure adequate watering',
            'Practice preventive care measures'
        ],
        'severity': 'Low'
    }
}

def get_disease_info(disease_name):
    """Get information about a specific disease"""
    # Handle variations in disease names
    disease_key = disease_name
    
    # Try exact match first
    if disease_key in DISEASE_INFO:
        return DISEASE_INFO[disease_key]
    
    # Try to find partial matches
    for key in DISEASE_INFO.keys():
        if disease_name.lower() in key.lower() or key.lower() in disease_name.lower():
            return DISEASE_INFO[key]
    
    # Return default info if no match found
    return {
        'description': f'Information about {disease_name} is not available in our database.',
        'symptoms': ['Consult with a plant pathologist for accurate diagnosis'],
        'treatments': ['Seek professional advice for treatment options'],
        'severity': 'Unknown'
    }

def get_all_diseases():
    """Get list of all diseases in the database"""
    return list(DISEASE_INFO.keys())

def search_diseases(query):
    """Search for diseases matching a query"""
    query = query.lower()
    matches = []
    
    for disease_name, info in DISEASE_INFO.items():
        if (query in disease_name.lower() or 
            query in info['description'].lower() or
            any(query in symptom.lower() for symptom in info['symptoms'])):
            matches.append(disease_name)
    
    return matches
