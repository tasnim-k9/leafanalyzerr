import os
import re
from disease_info import get_disease_info, search_diseases, get_all_diseases

# Try to initialize Gemini client if key is available
try:
    from google import genai
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key and len(api_key) > 20:  # Basic validation
        client = genai.Client(api_key=api_key)
        GEMINI_AVAILABLE = True
    else:
        GEMINI_AVAILABLE = False
        client = None
except:
    GEMINI_AVAILABLE = False
    client = None

def get_plant_expert_response(user_message, chat_history=[]):
    """Get AI response for plant disease consultation"""
    
    # First try Gemini if available
    if GEMINI_AVAILABLE and client:
        try:
            # Create comprehensive prompt with context
            system_context = """You are a professional plant pathologist and agricultural expert specializing in plant disease diagnosis and treatment. 

Your expertise includes:
- Identifying plant diseases from symptom descriptions
- Providing accurate treatment recommendations
- Offering preventive care advice
- Understanding various plant species and their common ailments

Guidelines for responses:
1. Ask clarifying questions when symptoms are unclear
2. Provide specific, actionable treatment advice
3. Recommend when to seek professional help for severe cases
4. Use clear, non-technical language for home gardeners
5. Always emphasize safety when recommending treatments
6. Suggest both organic and chemical treatment options when appropriate

Available diseases in database: Apple Scab, Black Rot, Cedar Apple Rust, Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Mosaic Virus, Yellow Leaf Curl Virus

Format your responses with:
- Clear diagnosis or possible conditions
- Specific symptoms to confirm
- Step-by-step treatment plan
- Prevention tips
- When to seek additional help"""

            # Build conversation context
            conversation_context = system_context + "\n\nConversation history:\n"
            
            # Add recent chat history for context
            for message in chat_history[-6:]:
                role = "Human" if message["role"] == "user" else "Assistant"
                conversation_context += f"{role}: {message['content']}\n"
            
            # Add current question
            full_prompt = f"{conversation_context}\nHuman: {user_message}\nAssistant:"
            
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=full_prompt
            )
            
            return response.text or "I apologize, but I'm having trouble generating a response right now. Please try again."
            
        except Exception as e:
            # Fall back to local expert system
            return get_local_plant_expert_response(user_message, chat_history)
    else:
        # Use local expert system
        return get_local_plant_expert_response(user_message, chat_history)

def get_local_plant_expert_response(user_message, chat_history=[]):
    """Local plant expert system when OpenAI is not available"""
    
    user_message_lower = user_message.lower()
    
    # Pattern matching for common queries
    responses = {
        "greeting": [
            "Hello! I'm your plant expert assistant. I can help you diagnose plant diseases and provide care advice. What seems to be the problem with your plant?",
            "Hi there! I'm here to help with your plant health questions. Can you describe what you're seeing on your plants?"
        ],
        "tomato": [
            "Tomatoes are susceptible to several diseases. Can you describe the symptoms you're seeing? Common issues include:\n\n**Early Blight**: Brown spots with concentric rings on lower leaves\n**Late Blight**: Water-soaked lesions that spread rapidly\n**Bacterial Spot**: Small dark spots on leaves and fruit\n**Leaf Mold**: Yellow spots on top, fuzzy growth underneath\n\nFor prevention:\n- Avoid overhead watering\n- Ensure good air circulation\n- Remove affected leaves promptly\n- Apply mulch to prevent soil splash"
        ],
        "apple": [
            "Apple trees can face various diseases. Here are the most common ones:\n\n**Apple Scab**: Dark, circular spots on leaves and fruit\n**Fire Blight**: Branches look burned, leaves turn brown\n**Cedar Apple Rust**: Orange spots on leaves\n**Black Rot**: Brown leaf spots with purple borders\n\nGeneral apple care:\n- Prune for air circulation\n- Remove fallen leaves\n- Apply dormant oil in late winter\n- Choose disease-resistant varieties"
        ],
        "potato": [
            "Potato plants commonly face these diseases:\n\n**Early Blight**: Dark spots with yellow halos on leaves\n**Late Blight**: Water-soaked lesions, white fuzzy growth\n**Potato Scab**: Rough, corky patches on tubers\n\nPrevention tips:\n- Avoid overhead watering\n- Rotate crops (don't plant where tomatoes/peppers grew)\n- Hill soil around plants\n- Harvest in dry conditions"
        ],
        "yellow": [
            "Yellow leaves can indicate several issues:\n\n**Possible causes:**\n- Overwatering (most common)\n- Nutrient deficiency (nitrogen, iron)\n- Viral diseases (mosaic virus, leaf curl)\n- Natural aging of lower leaves\n\n**What to do:**\n1. Check soil moisture - allow drying between waterings\n2. Examine leaf patterns - uniform yellowing vs spots\n3. Look for pests on undersides of leaves\n4. Consider fertilizing if soil is poor\n\nCan you tell me more about the yellowing pattern?"
        ],
        "brown": [
            "Brown spots or leaves often indicate disease:\n\n**Common causes:**\n- Fungal diseases (blight, leaf spot)\n- Bacterial infections\n- Overwatering leading to root rot\n- Sunburn or heat stress\n\n**Immediate actions:**\n1. Remove affected leaves immediately\n2. Improve air circulation\n3. Avoid watering leaves directly\n4. Apply appropriate fungicide if needed\n\nWhat type of plant is affected and where are the brown spots located?"
        ],
        "spots": [
            "Spots on leaves are often signs of disease:\n\n**Spot types and causes:**\n- **Round brown spots**: Leaf spot diseases\n- **Water-soaked spots**: Bacterial or late blight\n- **Yellow spots**: Early stages of many diseases\n- **Black spots**: Advanced fungal infections\n\n**Treatment approach:**\n1. Remove affected leaves\n2. Improve drainage and air flow\n3. Apply copper-based fungicide\n4. Avoid overhead watering\n\nDescribe the spots in more detail - size, color, location on plant?"
        ],
        "watering": [
            "Proper watering is crucial for plant health:\n\n**Best practices:**\n- Water deeply but less frequently\n- Water at soil level, not on leaves\n- Morning watering is ideal\n- Check soil moisture before watering\n\n**Signs of overwatering:**\n- Yellow leaves, soft stems\n- Fungal growth, musty smell\n- Root rot\n\n**Signs of underwatering:**\n- Wilting, dry soil\n- Brown leaf edges\n- Stunted growth\n\nWhat specific watering question do you have?"
        ]
    }
    
    # Check for pattern matches
    for pattern, response_list in responses.items():
        if pattern in user_message_lower:
            if isinstance(response_list, list):
                import random
                return random.choice(response_list)
            else:
                return response_list
    
    # Disease-specific analysis
    disease_suggestions = analyze_symptoms_for_diseases(user_message)
    if disease_suggestions:
        response = "Based on your description, here are the most likely conditions:\n\n"
        for suggestion in disease_suggestions[:2]:
            disease_info = suggestion['info']
            response += f"**{suggestion['name']}**\n"
            response += f"- Description: {disease_info['description']}\n"
            response += f"- Severity: {disease_info['severity']}\n"
            response += "- Key symptoms to look for:\n"
            for symptom in disease_info['symptoms'][:3]:
                response += f"  • {symptom}\n"
            response += "- Treatment recommendations:\n"
            for treatment in disease_info['treatments'][:3]:
                response += f"  • {treatment}\n"
            response += "\n"
        
        response += "Would you like more specific information about any of these conditions, or can you provide more details about the symptoms you're seeing?"
        return response
    
    # Default response with helpful guidance
    return """I'd be happy to help with your plant health question! To provide the most accurate advice, could you please tell me:

1. **What type of plant** are you asking about?
2. **What symptoms** are you seeing? (spots, yellowing, wilting, etc.)
3. **Where on the plant** are the symptoms appearing?
4. **How long** have you noticed these issues?
5. **Recent care changes** - watering, fertilizing, location changes?

Common plant problems I can help with include:
• Disease identification and treatment
• Watering and nutrition issues
• Pest management
• General plant care advice
• Preventive measures

The more details you provide, the better I can assist you!"""

def analyze_symptoms_for_diseases(description):
    """Analyze text description to suggest possible diseases"""
    
    # Search for keywords in description
    description_lower = description.lower()
    possible_diseases = []
    
    # Common symptom keywords mapped to diseases
    symptom_keywords = {
        'spots': ['Bacterial_spot', 'Septoria', 'Apple_scab', 'Target_Spot'],
        'yellow': ['Yellow_Leaf_Curl_Virus', 'mosaic_virus'],
        'brown': ['Early_blight', 'Late_blight', 'Black_rot'],
        'wilting': ['Late_blight', 'Bacterial_spot'],
        'mold': ['Leaf_Mold'],
        'rust': ['Cedar_apple_rust'],
        'scab': ['Apple_scab'],
        'rot': ['Black_rot'],
        'blight': ['Early_blight', 'Late_blight'],
        'curl': ['Yellow_Leaf_Curl_Virus'],
        'mosaic': ['mosaic_virus'],
        'web': ['Spider_mites'],
        'mites': ['Spider_mites']
    }
    
    # Check for keywords
    for keyword, diseases in symptom_keywords.items():
        if keyword in description_lower:
            possible_diseases.extend(diseases)
    
    # Remove duplicates and get disease info
    unique_diseases = list(set(possible_diseases))
    disease_suggestions = []
    
    for disease in unique_diseases[:5]:  # Limit to top 5 suggestions
        # Try to find matching disease in our database
        all_diseases = get_all_diseases()
        matching_disease = None
        
        for db_disease in all_diseases:
            if any(d in db_disease.lower() for d in disease.lower().split('_')):
                matching_disease = db_disease
                break
        
        if matching_disease:
            disease_info = get_disease_info(matching_disease)
            disease_suggestions.append({
                'name': matching_disease,
                'info': disease_info
            })
    
    return disease_suggestions

def format_disease_suggestions(suggestions):
    """Format disease suggestions for display"""
    if not suggestions:
        return "No specific diseases found based on the description. Please provide more details about the symptoms."
    
    formatted_text = "Based on your description, here are possible diseases to consider:\n\n"
    
    for suggestion in suggestions:
        formatted_text += f"**{suggestion['name']}**\n"
        formatted_text += f"Description: {suggestion['info']['description']}\n"
        formatted_text += f"Severity: {suggestion['info']['severity']}\n\n"
    
    return formatted_text