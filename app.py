import streamlit as st
from perplexity_backend import PerplexityChat
import time

# Page configuration with dark theme
st.set_page_config(
    page_title="Perplexity AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# FIXED: Complete dark theme with proper contrast
st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* ===== FORCE DARK THEME ===== */
    .stApp {
        background: linear-gradient(135deg, #0a0118 0%, #1a0b2e 50%, #2d1b3d 100%) !important;
    }
    
    /* Force dark on all Streamlit containers */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0118 0%, #1a0b2e 50%, #2d1b3d 100%) !important;
    }
    
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* ===== GLOBAL STYLES ===== */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        box-sizing: border-box;
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Main container */
    .main {
        background: transparent !important;
    }
    
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 900px !important;
        background: transparent !important;
    }
    
    /* ===== ANIMATED BACKGROUND ELEMENTS ===== */
    .main::before {
        content: '';
        position: fixed;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(
            circle at 50% 50%,
            rgba(168, 85, 247, 0.15) 0%,
            transparent 50%
        );
        animation: pulse 15s ease-in-out infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.3; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(1.1); }
    }
    
    /* ===== HEADER STYLES ===== */
    .header-title {
        font-size: 2.75rem;
        font-weight: 700;
        background: linear-gradient(135deg, #a855f7 0%, #ec4899 50%, #f97316 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.03em;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .header-subtitle {
        text-align: center;
        color: #cbd5e1;
        font-size: 1.05rem;
        font-weight: 400;
        margin-bottom: 2rem;
        animation: fadeInUp 0.8s ease-out 0.2s both;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* ===== CHAT MESSAGES ===== */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.06) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 1.25rem !important;
        padding: 1.5rem !important;
        margin-bottom: 1rem !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        animation: slideIn 0.5s ease-out;
    }
    
    .stChatMessage:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(168, 85, 247, 0.4) !important;
        transform: translateX(4px);
        box-shadow: 0 8px 32px rgba(168, 85, 247, 0.2);
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* HIGH CONTRAST TEXT */
    [data-testid="stChatMessageContent"] {
        font-size: 1rem !important;
        line-height: 1.7 !important;
        color: #f1f5f9 !important;
        font-weight: 400 !important;
    }
    
    [data-testid="stChatMessageContent"] p {
        color: #f1f5f9 !important;
    }
    
    /* User message - blue tint */
    .stChatMessage[data-testid="user-message"] {
        background: rgba(59, 130, 246, 0.08) !important;
        border-color: rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Assistant message - purple tint */
    .stChatMessage[data-testid="assistant-message"] {
        background: rgba(168, 85, 247, 0.08) !important;
        border-color: rgba(168, 85, 247, 0.3) !important;
    }
    
    /* ===== CHAT INPUT ===== */
    .stChatInputContainer {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(30px) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 1.5rem !important;
        padding: 0.75rem !important;
        margin-top: 1.5rem !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stChatInputContainer:focus-within {
        border-color: rgba(168, 85, 247, 0.6) !important;
        box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.2) !important;
        background: rgba(255, 255, 255, 0.1) !important;
    }
    
    textarea {
        color: #f8fafc !important;
        font-size: 1rem !important;
        background: transparent !important;
        border: none !important;
    }
    
    textarea::placeholder {
        color: #94a3b8 !important;
    }
    
    textarea:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 1rem !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.02em !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 20px rgba(168, 85, 247, 0.5) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 6px 30px rgba(168, 85, 247, 0.7) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) scale(0.98) !important;
    }
    
    /* Clear button - Red theme */
    [data-testid="column"]:first-child .stButton > button {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.5) !important;
    }
    
    [data-testid="column"]:first-child .stButton > button:hover {
        box-shadow: 0 6px 30px rgba(239, 68, 68, 0.7) !important;
    }
    
    /* ===== EXPANDER (Model Selector) ===== */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.06) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 1rem !important;
        color: #f1f5f9 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 1rem 1.25rem !important;
        transition: all 0.3s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(168, 85, 247, 0.5) !important;
        box-shadow: 0 4px 20px rgba(168, 85, 247, 0.2);
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.04) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-top: none !important;
        border-radius: 0 0 1rem 1rem !important;
        padding: 1.5rem !important;
    }
    
    /* Expander text */
    .streamlit-expanderContent p,
    .streamlit-expanderContent label,
    .streamlit-expanderContent h3 {
        color: #f1f5f9 !important;
    }
    
    /* ===== SELECT BOX ===== */
    .stSelectbox label {
        color: #f1f5f9 !important;
        font-weight: 500 !important;
    }
    
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.06) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 0.75rem !important;
        color: #f1f5f9 !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: rgba(168, 85, 247, 0.5) !important;
        box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.15) !important;
    }
    
    /* Dropdown options */
    [data-baseweb="popover"] {
        background: #1a0b2e !important;
    }
    
    [role="option"] {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #f1f5f9 !important;
    }
    
    [role="option"]:hover {
        background: rgba(168, 85, 247, 0.2) !important;
    }
    
    /* ===== MODEL CARDS ===== */
    .model-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 1rem;
        padding: 1.25rem;
        margin: 0.75rem 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .model-card:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(168, 85, 247, 0.5);
        transform: translateX(4px);
        box-shadow: 0 8px 30px rgba(168, 85, 247, 0.25);
    }
    
    .model-card.selected {
        background: rgba(168, 85, 247, 0.15);
        border-color: rgba(168, 85, 247, 0.6);
        box-shadow: 0 8px 30px rgba(168, 85, 247, 0.3);
    }
    
    /* ===== TIER BADGES ===== */
    .tier-badge {
        display: inline-block;
        padding: 0.3rem 0.85rem;
        border-radius: 1rem;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    
    .tier-free {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.25), rgba(59, 130, 246, 0.25));
        color: #67e8f9;
        border: 1px solid rgba(6, 182, 212, 0.4);
        box-shadow: 0 2px 10px rgba(6, 182, 212, 0.2);
    }
    
    .tier-pro {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.25), rgba(249, 115, 22, 0.25));
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.4);
        box-shadow: 0 2px 10px rgba(245, 158, 11, 0.2);
    }
    
    .tier-max {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.25), rgba(236, 72, 153, 0.25));
        color: #e879f9;
        border: 1px solid rgba(168, 85, 247, 0.4);
        box-shadow: 0 2px 10px rgba(168, 85, 247, 0.2);
    }
    
    /* ===== CITATION STYLES ===== */
    .citation-container {
        margin-top: 1rem;
        padding: 1rem;
        background: rgba(168, 85, 247, 0.1);
        border-left: 3px solid #a855f7;
        border-radius: 0.75rem;
        animation: fadeIn 0.4s ease-out;
    }
    
    .citation-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 0.75rem;
        padding: 0.85rem 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .citation-card:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(168, 85, 247, 0.4);
        transform: translateX(4px);
    }
    
    .citation-number {
        display: inline-block;
        background: linear-gradient(135deg, #a855f7, #ec4899);
        color: white;
        border-radius: 0.5rem;
        padding: 0.3rem 0.65rem;
        font-weight: 700;
        font-size: 0.75rem;
        margin-right: 0.75rem;
    }
    
    .citation-link {
        color: #c4b5fd;
        text-decoration: none;
        font-size: 0.85rem;
        transition: color 0.2s ease;
    }
    
    .citation-link:hover {
        color: #e9d5ff;
        text-decoration: underline;
    }
    
    /* ===== WELCOME SCREEN ===== */
    .welcome-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .welcome-subtitle {
        color: #cbd5e1;
        text-align: center;
        font-size: 1.15rem;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 1.25rem;
        padding: 1.75rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
    }
    
    .feature-card:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateY(-6px);
        box-shadow: 0 12px 40px rgba(168, 85, 247, 0.25);
        border-color: rgba(168, 85, 247, 0.4);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .suggestion-chip {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 1.5rem;
        padding: 0.75rem 1.25rem;
        color: #e2e8f0;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        cursor: pointer;
        display: inline-block;
        margin: 0.5rem;
    }
    
    .suggestion-chip:hover {
        background: rgba(168, 85, 247, 0.2);
        border-color: rgba(168, 85, 247, 0.5);
        transform: translateY(-2px);
        color: #f1f5f9;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.3);
    }
    
    /* ===== LOADING ANIMATION ===== */
    .loading-container {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 1rem;
    }
    
    .loading-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: linear-gradient(135deg, #a855f7, #ec4899);
        animation: bounce 1.4s infinite ease-in-out;
        box-shadow: 0 2px 8px rgba(168, 85, 247, 0.5);
    }
    
    .loading-dot:nth-child(1) { animation-delay: -0.32s; }
    .loading-dot:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes bounce {
        0%, 80%, 100% { transform: scale(0); opacity: 0.5; }
        40% { transform: scale(1); opacity: 1; }
    }
    
    /* ===== FOOTER ===== */
    .footer-info {
        text-align: center;
        color: #94a3b8;
        font-size: 0.9rem;
        padding: 1.5rem 0 0.5rem 0;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        margin-top: 2rem;
    }
    
    .footer-badge {
        display: inline-block;
        background: rgba(168, 85, 247, 0.15);
        border: 1px solid rgba(168, 85, 247, 0.3);
        border-radius: 1rem;
        padding: 0.4rem 0.85rem;
        margin: 0.25rem;
        color: #e9d5ff;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #a855f7, #ec4899);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #9333ea, #db2777);
    }
    
    /* ===== RADIO BUTTONS ===== */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.04);
        border-radius: 0.75rem;
        padding: 0.5rem;
    }
    
    .stRadio label {
        color: #e2e8f0 !important;
        font-weight: 500 !important;
    }
    
    /* ===== DIVIDER ===== */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(to right, transparent, rgba(255,255,255,0.1), transparent) !important;
        margin: 2rem 0 !important;
    }
    
    /* ===== MARKDOWN TEXT ===== */
    .element-container p {
        color: #f1f5f9 !important;
    }
    
    .element-container h1,
    .element-container h2,
    .element-container h3 {
        color: #f8fafc !important;
    }
    
    /* ===== SPINNER ===== */
    .stSpinner > div {
        border-color: #a855f7 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat' not in st.session_state:
    st.session_state.chat = PerplexityChat()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'model_filter' not in st.session_state:
    st.session_state.model_filter = "all"
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = "sonar-reasoning-pro"

# ===== HEADER =====
st.markdown("<h1 class='header-title'>✨ Perplexity AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='header-subtitle'>Ask anything. Get intelligent answers with sources.</p>", unsafe_allow_html=True)

# ===== MODEL SELECTOR =====
with st.expander("🎯 Choose Your AI Model", expanded=False):
    st.markdown("### Available Models")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("All Models", use_container_width=True):
            st.session_state.model_filter = "all"
    with col2:
        if st.button("Reasoning Only", use_container_width=True):
            st.session_state.model_filter = "reasoning"
    with col3:
        if st.button("By Tier", use_container_width=True):
            st.session_state.model_filter = "tier"
    
    # Apply filter
    if st.session_state.model_filter == "reasoning":
        available_models = st.session_state.chat.get_reasoning_models()
    elif st.session_state.model_filter == "tier":
        tier = st.selectbox("Select Tier", ["Free", "Pro", "Max"])
        available_models = st.session_state.chat.get_models_by_tier(tier)
    else:
        available_models = st.session_state.chat.available_models
    
    # Model selection
    model_options = list(available_models.keys())
    
    selected_model = st.selectbox(
        "Select Model",
        options=model_options,
        format_func=lambda x: f"{available_models[x]['icon']} {available_models[x]['name']} - {available_models[x]['description']}",
        index=model_options.index(st.session_state.selected_model) if st.session_state.selected_model in model_options else 0,
        key="model_selector"
    )
    
    st.session_state.selected_model = selected_model
    
    # Display selected model info
    model_info = available_models[selected_model]
    tier_class = f"tier-{model_info['tier'].lower()}"
    
    st.markdown(f"""
    <div class="model-card selected">
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem;">
            <span style="font-size: 1.75rem;">{model_info['icon']}</span>
            <div>
                <span style="font-size: 1.15rem; font-weight: 600; color: #f8fafc;">{model_info['name']}</span>
                <span class="tier-badge {tier_class}">{model_info['tier']}</span>
            </div>
        </div>
        <p style="color: #cbd5e1; font-size: 0.95rem; margin-bottom: 0.5rem; line-height: 1.5;">
            {model_info['description']}
        </p>
        {'<p style="color: #e9d5ff; font-size: 0.9rem; margin: 0;"><strong>💭 Reasoning Mode:</strong> Step-by-step analysis enabled</p>' if model_info['reasoning'] else ''}
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ===== WELCOME SCREEN =====
if len(st.session_state.chat_history) == 0:
    st.markdown("""
    <div style="animation: fadeIn 1s ease-out;">
        <h2 class="welcome-title">Welcome to the Future of AI</h2>
        <p class="welcome-subtitle">Ask anything and get intelligent, sourced answers powered by cutting-edge AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🧠</span>
            <h3 style="color: #f8fafc; font-size: 1.15rem; margin-bottom: 0.5rem; font-weight: 600;">Advanced Reasoning</h3>
            <p style="color: #cbd5e1; font-size: 0.95rem; margin: 0; line-height: 1.6;">Complex problem-solving with step-by-step analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card" style="margin-top: 1rem;">
            <span class="feature-icon">🛡️</span>
            <h3 style="color: #f8fafc; font-size: 1.15rem; margin-bottom: 0.5rem; font-weight: 600;">Accurate & Reliable</h3>
            <p style="color: #cbd5e1; font-size: 0.95rem; margin: 0; line-height: 1.6;">Backed by verified sources and citations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">⚡</span>
            <h3 style="color: #f8fafc; font-size: 1.15rem; margin-bottom: 0.5rem; font-weight: 600;">Lightning Fast</h3>
            <p style="color: #cbd5e1; font-size: 0.95rem; margin: 0; line-height: 1.6;">Get instant responses with real-time processing</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card" style="margin-top: 1rem;">
            <span class="feature-icon">🌐</span>
            <h3 style="color: #f8fafc; font-size: 1.15rem; margin-bottom: 0.5rem; font-weight: 600;">Web-Connected</h3>
            <p style="color: #cbd5e1; font-size: 0.95rem; margin: 0; line-height: 1.6;">Access to real-time information from the web</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Suggestions
    st.markdown("<p style='color: #cbd5e1; font-size: 1.05rem; margin-top: 2.5rem; margin-bottom: 1rem; font-weight: 500;'>💡 Try asking:</p>", unsafe_allow_html=True)
    suggestions = [
        "Explain quantum computing in simple terms",
        "What are the latest developments in AI?",
        "How does blockchain technology work?",
        "Compare different programming languages"
    ]
    suggestion_html = ""
    for suggestion in suggestions:
        suggestion_html += f"<span class='suggestion-chip'>{suggestion}</span>"
    st.markdown(suggestion_html, unsafe_allow_html=True)

# ===== CHAT HISTORY =====
for i, chat in enumerate(st.session_state.chat_history):
    with st.chat_message("user", avatar="👤"):
        st.markdown(f"<div style='color: #f1f5f9; font-size: 1rem;'>{chat['question']}</div>", unsafe_allow_html=True)
    
    with st.chat_message("assistant", avatar="✨"):
        st.markdown(f"<div style='color: #f1f5f9; font-size: 1rem; line-height: 1.7;'>{chat['answer']}</div>", unsafe_allow_html=True)
        
        # Display citations
        if chat["citations"]:
            with st.expander(f"📚 {len(chat['citations'])} Sources", expanded=False):
                st.markdown("<div class='citation-container'>", unsafe_allow_html=True)
                for citation in chat["citations"]:
                    st.markdown(f"""
                    <div class="citation-card">
                        <span class="citation-number">{citation['number']}</span>
                        <strong style="color: #f1f5f9; font-size: 0.95rem;">{citation['domain']}</strong><br>
                        <a href="{citation['url']}" target="_blank" class="citation-link">
                            {citation['url'][:70]}...
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

# ===== CHAT INPUT =====
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(f"<div style='color: #f1f5f9; font-size: 1rem;'>{user_input}</div>", unsafe_allow_html=True)
    
    # Get AI response
    with st.chat_message("assistant", avatar="✨"):
        with st.spinner(""):
            loading_placeholder = st.empty()
            loading_placeholder.markdown("""
            <div class="loading-container">
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
                <span style="color: #cbd5e1; margin-left: 0.5rem; font-weight: 500;">Thinking...</span>
            </div>
            """, unsafe_allow_html=True)
            
            response = st.session_state.chat.ask(user_input, model=st.session_state.selected_model)
            
            loading_placeholder.empty()
            st.markdown(f"<div style='color: #f1f5f9; font-size: 1rem; line-height: 1.7;'>{response['answer']}</div>", unsafe_allow_html=True)
            
            # Display citations
            if response["citations"]:
                with st.expander(f"📚 {len(response['citations'])} Sources", expanded=False):
                    st.markdown("<div class='citation-container'>", unsafe_allow_html=True)
                    for citation in response["citations"]:
                        st.markdown(f"""
                        <div class="citation-card">
                            <span class="citation-number">{citation['number']}</span>
                            <strong style="color: #f1f5f9; font-size: 0.95rem;">{citation['domain']}</strong><br>
                            <a href="{citation['url']}" target="_blank" class="citation-link">
                                {citation['url'][:70]}...
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
    
    # Save to history
    st.session_state.chat_history.append(response)
    st.rerun()

# ===== FOOTER =====
st.markdown("<hr>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.chat.clear_history()
        st.session_state.chat_history = []
        st.rerun()

with col2:
    st.markdown(f"""
    <div style="text-align: center; padding: 0.75rem;">
        <span class="footer-badge">💬 {len(st.session_state.chat_history)} messages</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    model_info = st.session_state.chat.available_models[st.session_state.selected_model]
    st.markdown(f"""
    <div style="text-align: center; padding: 0.75rem;">
        <span class="footer-badge">{model_info['icon']} {model_info['name']}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="footer-info">
    <p style="margin: 0; font-weight: 500;">Powered by Perplexity API ✨</p>
</div>
""", unsafe_allow_html=True)
