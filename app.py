import streamlit as st
import numpy as np
from PIL import Image
from model_utils import load_model, preprocess_image, predict_disease
from disease_info import get_disease_info
from chat_utils import get_plant_expert_response, analyze_symptoms_for_diseases
from weather_utils import get_weather_recommendations, get_seasonal_tips
from plant_tracker import init_plant_tracker, add_plant, log_plant_activity, get_plant_care_schedule, export_plant_data
from plant_encyclopedia import search_plant_info, get_plant_info, get_all_plants, get_plants_by_difficulty
from auth_utils import init_auth, register_user, login_user, logout_user, load_user_plants, save_user_plants, get_user_profile
from social_features import get_community_stats, get_farmer_insights, get_disease_alerts, get_success_stories, log_disease_detection, get_regional_tips
from database import init_database, get_plant_images, get_success_stories as get_db_success_stories, log_disease_detection_db, get_community_disease_stats
import io

# Configure page
st.set_page_config(
    page_title="Plant Disease Detector",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #4CAF50, #45a049);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .upload-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        border: 2px dashed #4CAF50;
        margin-bottom: 1rem;
    }
    
    .results-section {
        background: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #4CAF50;
    }
    
    .disease-card {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .healthy-card {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .info-box {
        background: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        margin: 0.5rem 0;
    }
    
    .warning-box {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 0.5rem 0;
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #4CAF50, #45a049);
    }
    
    .upload-text {
        text-align: center;
        color: #666;
        font-size: 1.1em;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'model' not in st.session_state:
    st.session_state.model = None
    st.session_state.model_loaded = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Initialize database, authentication and plant tracker
init_database()
init_auth()
init_plant_tracker()

# Load user-specific data if authenticated
if st.session_state.authenticated and st.session_state.username:
    plants, logs = load_user_plants(st.session_state.username)
    st.session_state.plants = plants
    st.session_state.plant_logs = logs

def main():
    # Check authentication
    if not st.session_state.authenticated:
        show_auth_page()
        return
    
    # Main header with styling
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        <div class="main-header">
            <h1>🌱 Plant Disease Detector</h1>
            <p style="font-size: 1.2em; margin: 0;">AI-Powered Plant Health Analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        user_profile = get_user_profile(st.session_state.username)
        st.markdown(f"""
        <div style="background: #f0f0f0; padding: 1rem; border-radius: 10px; text-align: center; margin-top: 1rem;">
            <strong>Welcome, {st.session_state.username}!</strong><br>
            <small>{user_profile.get('user_type', 'User')} | {user_profile.get('location', 'Location not set')}</small>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Logout", type="secondary"):
            logout_user()
            st.rerun()
    
    # Determine tabs based on user type
    if st.session_state.user_type == "Farmer":
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📸 Disease Detection", 
            "💬 AI Expert", 
            "🌾 Farmer Dashboard",
            "📊 My Crops",
            "🌿 Plant Guide",
            "🌤️ Weather & Care"
        ])
        
        with tab1:
            image_analysis_tab()
        with tab2:
            ai_chat_tab()
        with tab3:
            farmer_dashboard_tab()
        with tab4:
            plant_tracker_tab()
        with tab5:
            plant_encyclopedia_tab()
        with tab6:
            care_dashboard_tab()
    else:
        # Regular user tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📸 Image Analysis", 
            "💬 AI Plant Expert", 
            "🌿 Plant Encyclopedia", 
            "📊 Plant Tracker",
            "🌤️ Care Dashboard"
        ])
        
        with tab1:
            image_analysis_tab()
        with tab2:
            ai_chat_tab()
        with tab3:
            plant_encyclopedia_tab()
        with tab4:
            plant_tracker_tab()
        with tab5:
            care_dashboard_tab()

def show_auth_page():
    """Show login/register page"""
    st.markdown("""
    <div class="main-header">
        <h1>🌱 AgriCare Platform</h1>
        <p style="font-size: 1.2em; margin: 0;">Empowering Farmers & Gardeners with AI Technology</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show sample plant images in a gallery
    st.markdown("### Featured Plant Health Examples")
    healthy_images = get_plant_images(category="healthy")[:4]
    
    if healthy_images:
        cols = st.columns(4)
        for i, img in enumerate(healthy_images):
            with cols[i]:
                st.image(img["image_url"], caption=f"Healthy {img['plant_name']}", use_container_width=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        auth_tab1, auth_tab2 = st.tabs(["Login", "Register"])
        
        with auth_tab1:
            show_login_form()
        
        with auth_tab2:
            show_register_form()

def show_login_form():
    """Show login form"""
    st.markdown("### Login to Your Account")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login", type="primary")
        
        if submit:
            if username and password:
                success, message = login_user(username, password)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please fill in all fields")

def show_register_form():
    """Show registration form"""
    st.markdown("### Create New Account")
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username*")
            password = st.text_input("Password*", type="password")
            email = st.text_input("Email*")
        
        with col2:
            user_type = st.selectbox("I am a:", ["Home Gardener", "Farmer", "Agricultural Student", "Researcher"])
            location = st.text_input("Location (City, Country)")
            farm_size = st.text_input("Farm Size (if farmer)", placeholder="e.g., 5 acres, 2 hectares")
        
        submit = st.form_submit_button("Create Account", type="primary")
        
        if submit:
            if username and password and email:
                success, message = register_user(username, password, email, user_type, location, farm_size)
                if success:
                    st.success(message)
                    st.info("Please login with your new account")
                else:
                    st.error(message)
            else:
                st.error("Please fill in required fields (marked with *)")

def farmer_dashboard_tab():
    """Special dashboard for farmers"""
    st.markdown("### 🌾 Farmer Dashboard")
    
    # Community stats from database
    disease_stats = get_community_disease_stats()
    
    st.markdown("#### Community Disease Tracking")
    if disease_stats:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Active Disease Reports", len(disease_stats))
        with col2:
            total_cases = sum(info["count"] for info in disease_stats.values())
            st.metric("Total Cases (30 days)", total_cases)
        
        # Show top diseases
        st.markdown("#### Recent Disease Alerts")
        for disease, info in list(disease_stats.items())[:3]:
            alert_color = "#ff4444" if info["count"] > 5 else "#ff9800"
            locations_text = ", ".join(info["locations"][:3]) if info["locations"] else "Various locations"
            st.markdown(f"""
            <div style="background: {alert_color}20; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid {alert_color};">
                <strong>⚠️ {disease}</strong><br>
                {info['count']} cases reported in: {locations_text}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("No disease outbreaks reported in your area recently!")
    
    # Plant image gallery
    st.markdown("#### Plant Health Reference Gallery")
    tab1, tab2 = st.tabs(["Healthy Plants", "Disease Examples"])
    
    with tab1:
        healthy_images = get_plant_images(category="healthy")
        if healthy_images:
            cols = st.columns(3)
            for i, img in enumerate(healthy_images[:6]):
                with cols[i % 3]:
                    st.image(img["image_url"], caption=f"{img['plant_name']}", use_container_width=True)
                    st.caption(img["description"])
    
    with tab2:
        diseased_images = get_plant_images(category="diseased")
        if diseased_images:
            cols = st.columns(3)
            for i, img in enumerate(diseased_images[:6]):
                with cols[i % 3]:
                    st.image(img["image_url"], caption=f"{img['plant_name']} - {img['disease_name']}", use_container_width=True)
                    st.caption(img["description"])
    
    # Regional tips
    user_profile = get_user_profile(st.session_state.username)
    user_location = user_profile.get('location', '')
    if user_location:
        st.markdown("#### Regional Agricultural Tips")
        regional_tips = get_regional_tips(user_location)
        for tip in regional_tips:
            st.write(f"• {tip}")
    
    # Success stories from database
    st.markdown("#### Success Stories from Our Community")
    stories = get_db_success_stories()
    
    if stories:
        cols = st.columns(min(len(stories), 3))
        for i, story in enumerate(stories[:3]):
            with cols[i]:
                st.markdown(f"""
                <div style="background: #e8f5e8; padding: 1rem; border-radius: 10px; height: 200px;">
                    <strong>{story['farmer']}</strong><br>
                    <small>{story['location']}</small><br><br>
                    "{story['story']}"<br><br>
                    <strong>Impact:</strong> {story['impact']}
                </div>
                """, unsafe_allow_html=True)

def image_analysis_tab():
    """Tab for image-based disease detection"""
    st.markdown("### Upload a leaf image to get instant disease analysis and treatment recommendations")
    
    # Load model
    if not st.session_state.model_loaded:
        with st.spinner("Loading AI model... This may take a moment."):
            try:
                st.session_state.model = load_model()
                st.session_state.model_loaded = True
                st.success("AI model loaded successfully!")
            except Exception as e:
                st.error(f"Failed to load AI model: {str(e)}")
                st.stop()
    
    # Create two columns for layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="upload-section">
        """, unsafe_allow_html=True)
        
        st.markdown("### 📤 Upload Leaf Image")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose a leaf image...",
            type=['jpg', 'jpeg', 'png'],
            help="Upload a clear image of a plant leaf for disease detection"
        )
        
        if uploaded_file is not None:
            try:
                # Display uploaded image
                image = Image.open(uploaded_file)
                st.image(image, caption="📷 Uploaded Image", use_container_width=True)
                
                # Image info in a nice format
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    st.metric("Image Size", f"{image.size[0]}×{image.size[1]}")
                with col_info2:
                    st.metric("File Size", f"{len(uploaded_file.getvalue())/1024:.1f} KB")
                
                # Analyze button with custom styling
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🔍 Analyze for Diseases", type="primary", use_container_width=True):
                    analyze_image(image, col2)
                    
            except Exception as e:
                st.error(f"Error loading image: {str(e)}")
        else:
            st.markdown("""
            <div class="upload-text">
                <p>📁 Drag and drop or click to upload a leaf image</p>
                <p>Supported formats: JPG, JPEG, PNG</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        if uploaded_file is None:
            st.markdown("### 🔬 Analysis Results")
            st.markdown("""
            <div class="info-box">
                <h4>🎯 Ready for Analysis</h4>
                <p>Upload a leaf image to get instant disease detection results with detailed treatment recommendations.</p>
            </div>
            """, unsafe_allow_html=True)

def ai_chat_tab():
    """Tab for AI-powered plant expert chat"""
    st.markdown("### 💬 Describe your plant's symptoms and get expert advice")
    
    # Check API status and show appropriate message
    from chat_utils import GEMINI_AVAILABLE
    
    if GEMINI_AVAILABLE:
        st.markdown("""
        <div class="info-box">
            <h4>🤖 Enhanced AI Plant Expert (Gemini Powered)</h4>
            <p>Advanced Google AI system ready to help diagnose plant issues and provide detailed treatment recommendations.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="warning-box">
            <h4>🧑‍🌾 Local Plant Expert System</h4>
            <p>Using built-in plant knowledge base. To enable enhanced AI responses, please provide your Gemini API key in the environment.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("#### Previous Conversation")
        for message in st.session_state.chat_history[-6:]:  # Show last 6 messages
            if message["role"] == "user":
                st.markdown(f"""
                <div style="background: #e3f2fd; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #2196f3;">
                    <strong>You:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: #e8f5e8; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #4caf50;">
                    <strong>🧑‍🌾 Plant Expert:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
    
    # Input area
    st.markdown("#### Ask the Plant Expert")
    
    # Create columns for better layout
    input_col, button_col = st.columns([4, 1])
    
    with input_col:
        user_input = st.text_area(
            "Describe your plant's symptoms:",
            placeholder="For example: My tomato leaves have brown spots with yellow rings around them, and some leaves are turning yellow and dropping off...",
            height=100,
            key="plant_chat_input"
        )
    
    with button_col:
        st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
        send_button = st.button("Send", type="primary", use_container_width=True)
        clear_button = st.button("Clear Chat", use_container_width=True)
    
    # Handle button clicks
    if clear_button:
        st.session_state.chat_history = []
        st.rerun()
    
    if send_button and user_input.strip():
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Show loading indicator
        with st.spinner("Getting expert advice..."):
            try:
                # Get AI response
                ai_response = get_plant_expert_response(user_input, st.session_state.chat_history)
                
                # Add AI response to history
                st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                
                # Refresh the page to show new messages
                st.rerun()
                
            except Exception as e:
                st.error(f"Sorry, I'm having trouble connecting right now. Please try again. Error: {str(e)}")
    
    elif send_button and not user_input.strip():
        st.warning("Please describe your plant's symptoms before sending.")
    
    # Quick question suggestions
    st.markdown("#### Quick Questions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🍅 Tomato problems", use_container_width=True):
            suggested_input = "I'm having issues with my tomato plants. Can you help me identify what might be wrong?"
            st.session_state.chat_history.append({"role": "user", "content": suggested_input})
            with st.spinner("Getting expert advice..."):
                ai_response = get_plant_expert_response(suggested_input, st.session_state.chat_history)
                st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()
    
    with col2:
        if st.button("🍎 Apple tree issues", use_container_width=True):
            suggested_input = "My apple tree leaves don't look healthy. What should I look for and how can I treat it?"
            st.session_state.chat_history.append({"role": "user", "content": suggested_input})
            with st.spinner("Getting expert advice..."):
                ai_response = get_plant_expert_response(suggested_input, st.session_state.chat_history)
                st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()
    
    with col3:
        if st.button("🥔 Potato diseases", use_container_width=True):
            suggested_input = "I think my potato plants might have a disease. What are the common signs to watch for?"
            st.session_state.chat_history.append({"role": "user", "content": suggested_input})
            with st.spinner("Getting expert advice..."):
                ai_response = get_plant_expert_response(suggested_input, st.session_state.chat_history)
                st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()

def analyze_image(image, result_column):
    """Analyze the uploaded image for plant diseases"""
    
    with result_column:
        st.markdown("### 🔬 Analysis Results")
        
        # Add progress bar for better UX
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Preprocessing
            status_text.text("🔄 Preprocessing image...")
            progress_bar.progress(25)
            processed_image = preprocess_image(image)
            
            # Step 2: Analysis
            status_text.text("🧠 Analyzing with AI model...")
            progress_bar.progress(75)
            predictions = predict_disease(st.session_state.model, processed_image)
            
            # Step 3: Results
            status_text.text("✅ Analysis complete!")
            progress_bar.progress(100)
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Display results
            display_results(predictions)
            
            # Log disease detection for authenticated users
            if st.session_state.authenticated:
                top_disease = max(predictions.items(), key=lambda x: x[1])
                if top_disease[1] > 0.3 and "healthy" not in top_disease[0].lower():
                    user_profile = get_user_profile(st.session_state.username)
                    log_disease_detection_db(
                        st.session_state.user_id,
                        "Uploaded Image",
                        top_disease[0], 
                        top_disease[1],
                        user_profile.get('location', '')
                    )
            
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"Error during analysis: {str(e)}")

def display_results(predictions):
    """Display the disease prediction results"""
    
    # Get top predictions
    top_predictions = sorted(predictions.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Display top prediction
    disease_name, confidence = top_predictions[0]
    
    # Check if it's a healthy prediction or disease
    is_healthy = "healthy" in disease_name.lower() or disease_name.lower() == "healthy"
    
    if is_healthy and confidence > 0.4:
        st.markdown("""
        <div class="healthy-card">
            <h3>✅ Healthy Leaf Detected</h3>
            <p>No significant disease detected. The leaf appears healthy!</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_conf1, col_conf2 = st.columns(2)
        with col_conf1:
            st.metric("Health Status", "Healthy", delta="Good")
        with col_conf2:
            st.metric("Confidence", f"{confidence:.1%}")
        
        # Show potential concerns if any disease has moderate confidence
        disease_predictions = [(name, conf) for name, conf in top_predictions if "healthy" not in name.lower()]
        if disease_predictions and disease_predictions[0][1] > 0.2:
            st.markdown("#### 👁️ Potential Concerns to Monitor")
            st.markdown("""
            <div class="warning-box">
                <p>While the leaf appears mostly healthy, keep an eye out for:</p>
            </div>
            """, unsafe_allow_html=True)
            for disease, conf in disease_predictions[:2]:
                if conf > 0.15:
                    st.write(f"• {disease}: {conf:.1%} confidence")
    else:
        # Disease detected
        if not is_healthy:
            st.markdown(f"""
            <div class="disease-card">
                <h3>🔍 Disease Detected: {disease_name}</h3>
                <p>Analysis indicates potential plant disease requiring attention.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Find the top disease prediction
            disease_predictions = [(name, conf) for name, conf in top_predictions if "healthy" not in name.lower()]
            if disease_predictions:
                disease_name, confidence = disease_predictions[0]
                st.markdown(f"""
                <div class="warning-box">
                    <h3>⚠️ Possible Disease: {disease_name}</h3>
                    <p>Potential disease detected - please review recommendations.</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Confidence metrics
        col_conf1, col_conf2 = st.columns(2)
        with col_conf1:
            st.metric("Detection Status", "Disease Found", delta="Alert")
        with col_conf2:
            st.metric("Confidence", f"{confidence:.1%}")
        
        # Display disease information with better styling
        disease_data = get_disease_info(disease_name)
        
        st.markdown("#### 📋 Disease Information")
        st.markdown(f"""
        <div class="info-box">
            <strong>Description:</strong> {disease_data['description']}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 🔍 Symptoms to Look For")
        for i, symptom in enumerate(disease_data['symptoms'], 1):
            st.write(f"{i}. {symptom}")
        
        st.markdown("#### 🌿 Treatment Recommendations")
        for i, treatment in enumerate(disease_data['treatments'], 1):
            st.write(f"{i}. {treatment}")
        
        # Severity indicator with colors
        if disease_data['severity'] == 'High':
            st.markdown("""
            <div style="background: #ffebee; color: #c62828; padding: 1rem; border-radius: 8px; border-left: 4px solid #c62828;">
                <strong>🚨 High Severity Disease</strong><br>
                Immediate action recommended to prevent spread and plant damage.
            </div>
            """, unsafe_allow_html=True)
        elif disease_data['severity'] == 'Medium':
            st.markdown("""
            <div style="background: #fff8e1; color: #f57c00; padding: 1rem; border-radius: 8px; border-left: 4px solid #f57c00;">
                <strong>⚠️ Medium Severity Disease</strong><br>
                Monitor closely and treat as needed to prevent progression.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #e8f5e8; color: #2e7d32; padding: 1rem; border-radius: 8px; border-left: 4px solid #2e7d32;">
                <strong>ℹ️ Low Severity Disease</strong><br>
                Regular monitoring recommended with preventive measures.
            </div>
            """, unsafe_allow_html=True)
    
    # Show all predictions with better styling
    st.markdown("#### 📊 Detailed Analysis Results")
    
    for i, (disease, conf) in enumerate(top_predictions):
        if i < 3:  # Show top 3 with progress bars
            # Color coding based on confidence
            if conf > 0.6:
                color = "#4CAF50"  # Green for high confidence
            elif conf > 0.3:
                color = "#ff9800"  # Orange for medium
            else:
                color = "#f44336"  # Red for low
                
            st.markdown(f"""
            <div style="margin: 0.5rem 0;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.2rem;">
                    <span style="font-weight: bold;">{disease}</span>
                    <span style="color: {color}; font-weight: bold;">{conf:.1%}</span>
                </div>
                <div style="background: #f0f0f0; border-radius: 10px; height: 8px; overflow: hidden;">
                    <div style="background: {color}; height: 100%; width: {conf*100}%; transition: width 0.3s ease;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Show remaining as simple text
            st.write(f"• {disease}: {conf:.1%}")

# Sidebar with enhanced styling
def display_sidebar():
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, #4CAF50, #45a049); color: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
        <h2 style="margin: 0; color: white;">🌱 Plant Disease Detector</h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">AI-Powered Plant Health Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("### 🔬 About This Tool")
    st.sidebar.markdown("""
    <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; border-left: 4px solid #4CAF50;">
        This advanced AI system can detect various plant diseases from leaf images with high accuracy.
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("### 🦠 Detectable Diseases")
    diseases = [
        "Apple Scab", "Black Rot", "Cedar Apple Rust", "Bacterial Spot",
        "Early Blight", "Late Blight", "Leaf Mold", "Septoria Leaf Spot",
        "Spider Mites", "Target Spot", "Mosaic Virus", "Yellow Leaf Curl"
    ]
    
    for disease in diseases:
        st.sidebar.markdown(f"• {disease}")
    
    st.sidebar.markdown("### 📋 How to Use")
    steps = [
        "Upload a clear leaf image",
        "Click 'Analyze for Diseases'", 
        "Review the detailed results",
        "Follow treatment recommendations"
    ]
    
    for i, step in enumerate(steps, 1):
        st.sidebar.markdown(f"""
        <div style="display: flex; align-items: center; margin: 0.5rem 0;">
            <div style="background: #4CAF50; color: white; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; margin-right: 0.5rem; font-weight: bold; font-size: 0.8em;">
                {i}
            </div>
            <span>{step}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.sidebar.markdown("### 💡 Pro Tips")
    st.sidebar.markdown("""
    <div style="background: #fff3cd; padding: 1rem; border-radius: 8px; border-left: 4px solid #ffc107;">
        <strong>For Best Results:</strong><br>
        📸 Use well-lit, clear images<br>
        🎯 Focus on affected leaf areas<br>
        🚫 Avoid blurry or dark photos<br>
        🖼️ Include the whole leaf in frame
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9em;">
        <p>🌿 Helping farmers and gardeners maintain healthy plants through AI technology</p>
    </div>
    """, unsafe_allow_html=True)

def plant_encyclopedia_tab():
    """Tab for plant care encyclopedia"""
    st.markdown("### 🌿 Plant Care Encyclopedia")
    st.markdown("Search for detailed care information about different plants")
    
    # Search functionality
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("Search for a plant:", placeholder="e.g., tomato, apple, pepper")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_button = st.button("Search", type="primary")
    
    # Display search results or plant grid
    if search_button and search_query:
        results = search_plant_info(search_query)
        if results:
            st.markdown(f"#### Search Results for '{search_query}'")
            for plant_name, info in results:
                display_plant_card_with_images(plant_name, info)
        else:
            st.warning(f"No plants found matching '{search_query}'")
    else:
        # Show plant image gallery first
        st.markdown("#### Featured Plants")
        plant_images = get_plant_images(category="healthy")
        if plant_images:
            cols = st.columns(4)
            for i, img in enumerate(plant_images[:8]):
                with cols[i % 4]:
                    st.image(img["image_url"], caption=img["plant_name"], use_container_width=True)
        
        # Show all plants in a grid
        st.markdown("#### Browse All Plants")
        all_plants = get_all_plants()
        
        # Display in columns
        cols = st.columns(2)
        for i, plant_name in enumerate(all_plants):
            with cols[i % 2]:
                info = get_plant_info(plant_name)
                display_plant_card_with_images(plant_name, info)

def display_plant_card_with_images(plant_name, info):
    """Display a plant information card with images"""
    with st.expander(f"🌱 {plant_name} ({info['scientific_name']})"):
        # Get plant images
        plant_images = get_plant_images(plant_name=plant_name)
        
        if plant_images:
            st.markdown("**Plant Examples:**")
            img_cols = st.columns(min(len(plant_images), 3))
            for i, img in enumerate(plant_images[:3]):
                with img_cols[i]:
                    st.image(img["image_url"], caption=f"{img['disease_name'] or 'Healthy'}", use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Family:** {info['family']}")
            st.markdown(f"**Care Difficulty:** {info['care_difficulty']}")
            st.markdown(f"**Light:** {info['light']}")
            st.markdown(f"**Watering:** {info['watering']}")
            st.markdown(f"**Soil:** {info['soil']}")
        
        with col2:
            st.markdown(f"**Temperature:** {info['temperature']}")
            st.markdown(f"**Humidity:** {info['humidity']}")
            st.markdown(f"**Harvest Time:** {info['harvest_time']}")
        
        st.markdown("**Common Diseases:**")
        for disease in info['common_diseases']:
            st.write(f"• {disease}")
        
        st.markdown("**Care Tips:**")
        for tip in info['tips']:
            st.write(f"• {tip}")
        
        st.markdown("**Companion Plants:**")
        st.write(", ".join(info['companion_plants']))

def display_plant_card(plant_name, info):
    """Display a simple plant information card"""
    display_plant_card_with_images(plant_name, info)

def plant_tracker_tab():
    """Tab for personal plant tracking"""
    st.markdown("### 📊 My Plant Collection")
    
    # Add new plant section
    with st.expander("➕ Add New Plant"):
        col1, col2 = st.columns(2)
        with col1:
            plant_name = st.text_input("Plant Name")
            species = st.text_input("Species/Variety")
        with col2:
            location = st.text_input("Location (e.g., Garden, Window)")
            health_status = st.selectbox("Health Status", ["Healthy", "Needs Attention", "Sick", "Recovering"])
        
        notes = st.text_area("Notes", placeholder="Any additional observations...")
        
        if st.button("Add Plant", type="primary"):
            if plant_name and species:
                add_plant(plant_name, species, location, health_status, notes)
                # Save to user's account
                if st.session_state.authenticated:
                    save_user_plants(st.session_state.username, st.session_state.plants, st.session_state.plant_logs)
                st.success(f"Added {plant_name} to your collection!")
                st.rerun()
            else:
                st.error("Please fill in plant name and species")
    
    # Display existing plants
    if st.session_state.plants:
        st.markdown("#### Your Plants")
        
        for plant in st.session_state.plants:
            with st.container():
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #4CAF50;">
                    <h4>{plant['name']} ({plant['species']})</h4>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Health", plant['health_status'])
                with col2:
                    st.metric("Location", plant['location'])
                with col3:
                    last_watered = plant['last_watered'] or "Never"
                    st.metric("Last Watered", last_watered)
                with col4:
                    if st.button(f"Log Activity", key=f"log_{plant['id']}"):
                        st.session_state[f"show_log_{plant['id']}"] = True
                
                # Activity logging
                if st.session_state.get(f"show_log_{plant['id']}", False):
                    activity_col1, activity_col2 = st.columns(2)
                    with activity_col1:
                        activity = st.selectbox("Activity", ["watering", "fertilizing", "pruning", "inspection"], key=f"activity_{plant['id']}")
                    with activity_col2:
                        activity_notes = st.text_input("Notes", key=f"notes_{plant['id']}")
                    
                    log_col1, log_col2 = st.columns(2)
                    with log_col1:
                        if st.button("Save Activity", key=f"save_{plant['id']}"):
                            log_plant_activity(plant['id'], activity, activity_notes)
                            # Save to user's account
                            if st.session_state.authenticated:
                                save_user_plants(st.session_state.username, st.session_state.plants, st.session_state.plant_logs)
                            st.session_state[f"show_log_{plant['id']}"] = False
                            st.success("Activity logged!")
                            st.rerun()
                    with log_col2:
                        if st.button("Cancel", key=f"cancel_{plant['id']}"):
                            st.session_state[f"show_log_{plant['id']}"] = False
                            st.rerun()
                
                if plant['notes']:
                    st.markdown(f"**Notes:** {plant['notes']}")
                
                st.markdown("---")
        
        # Care schedule
        schedule = get_plant_care_schedule()
        if schedule:
            st.markdown("#### 📅 Care Schedule")
            for task in schedule:
                priority_color = "#ff4444" if task["priority"] == "high" else "#ff9800"
                st.markdown(f"""
                <div style="background: {priority_color}20; padding: 0.5rem; border-radius: 5px; margin: 0.2rem 0; border-left: 3px solid {priority_color};">
                    <strong>{task['plant']}</strong>: {task['task']} (Overdue by {task['overdue_days']} days)
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No plants in your collection yet. Add your first plant above!")

def care_dashboard_tab():
    """Tab for weather and seasonal care dashboard"""
    st.markdown("### 🌤️ Plant Care Dashboard")
    
    # Weather recommendations section
    st.markdown("#### Today's Care Recommendations")
    weather_data, recommendations = get_weather_recommendations()
    
    # Display current conditions
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Temperature", f"{weather_data['temperature']}°C")
    with col2:
        st.metric("Humidity", f"{weather_data['humidity']}%")
    with col3:
        st.metric("Rainfall", f"{weather_data['rainfall']}mm")
    with col4:
        st.metric("UV Index", weather_data['uv_index'])
    
    # Display recommendations
    for rec in recommendations:
        if rec["type"] == "warning":
            st.warning(f"{rec['icon']} **{rec['title']}**: {rec['message']}")
        else:
            st.info(f"{rec['icon']} **{rec['title']}**: {rec['message']}")
    
    # Seasonal tips
    st.markdown("#### Seasonal Care Tips")
    seasonal_data = get_seasonal_tips()
    st.markdown(f"### {seasonal_data['title']}")
    
    for tip in seasonal_data['tips']:
        st.write(f"• {tip}")
    
    # Plant health overview
    if st.session_state.plants:
        st.markdown("#### Plant Health Overview")
        
        health_counts = {}
        for plant in st.session_state.plants:
            status = plant['health_status']
            health_counts[status] = health_counts.get(status, 0) + 1
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Healthy", health_counts.get("Healthy", 0), delta="Good")
        with col2:
            st.metric("Need Attention", health_counts.get("Needs Attention", 0))
        with col3:
            st.metric("Sick", health_counts.get("Sick", 0), delta="Alert" if health_counts.get("Sick", 0) > 0 else None)
        with col4:
            st.metric("Recovering", health_counts.get("Recovering", 0))
    
    # Quick actions
    st.markdown("#### Quick Actions")
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("🔔 Check All Plants", use_container_width=True):
            st.info("Reminder: Check all your plants for signs of stress, pests, or disease")
    
    with action_col2:
        if st.button("💧 Watering Reminder", use_container_width=True):
            st.info("Check soil moisture levels and water plants as needed")
    
    with action_col3:
        if st.button("🧪 Fertilizer Check", use_container_width=True):
            st.info("Review fertilizing schedule - most plants need feeding every 2-4 weeks during growing season")

if __name__ == "__main__":
    display_sidebar()
    main()
