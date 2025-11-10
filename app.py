import streamlit as st
from perplexity_backend import PerplexityChat

# Page configuration
st.set_page_config(
    page_title="Perplexity AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Apple-inspired minimal luxury CSS
st.markdown("""
<style>
    /* Import SF Pro Display font (Apple's font) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
        padding: 0;
    }
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 800px !important;
    }
    
    /* Title styling */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.02em;
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #6B7280;
        font-size: 0.95rem;
        font-weight: 400;
        margin-bottom: 2rem;
        letter-spacing: 0.01em;
    }
    
    /* Chat messages */
    .stChatMessage {
        background: white !important;
        border-radius: 16px !important;
        padding: 1.25rem !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
        border: 1px solid #f0f0f0 !important;
        transition: all 0.3s ease !important;
    }
    
    .stChatMessage:hover {
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08) !important;
        transform: translateY(-2px);
    }
    
    /* User message */
    [data-testid="stChatMessageContent"] {
        font-size: 0.95rem;
        line-height: 1.6;
        color: #1F2937;
    }
    
    /* Input area */
    .stChatInputContainer {
        border-radius: 24px !important;
        background: white !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08) !important;
        border: 1px solid #e5e7eb !important;
        padding: 0.5rem !important;
        margin-top: 1rem !important;
    }
    
    .stChatInput {
        border: none !important;
        background: transparent !important;
    }
    
    textarea {
        border: none !important;
        font-size: 0.95rem !important;
        color: #1F2937 !important;
    }
    
    textarea:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.625rem 1.5rem !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.01em !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Select box */
    .stSelectbox > div > div {
        background: white !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 12px !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: white !important;
        border-radius: 12px !important;
        border: 1px solid #e5e7eb !important;
        font-weight: 500 !important;
        color: #374151 !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: #f9fafb !important;
        border-color: #667eea !important;
    }
    
    .streamlit-expanderContent {
        background: white !important;
        border: 1px solid #e5e7eb !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
        padding: 1rem !important;
    }
    
    /* Citations */
    .citation-card {
        background: #f9fafb;
        border-left: 3px solid #667eea;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        font-size: 0.85rem;
        transition: all 0.3s ease;
    }
    
    .citation-card:hover {
        background: #f3f4f6;
        transform: translateX(4px);
    }
    
    .citation-number {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 6px;
        padding: 0.125rem 0.5rem;
        font-weight: 600;
        font-size: 0.75rem;
        margin-right: 0.5rem;
    }
    
    /* Model badge */
    .model-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
        margin: 0.25rem 0.25rem 0.25rem 0;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
    }
    
    .tier-badge {
        display: inline-block;
        padding: 0.125rem 0.5rem;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }
    
    .tier-free {
        background: #E0F2FE;
        color: #0369A1;
    }
    
    .tier-pro {
        background: #FEF3C7;
        color: #D97706;
    }
    
    .tier-max {
        background: #F3E8FF;
        color: #7C3AED;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0 !important;
        border: none !important;
        height: 1px !important;
        background: linear-gradient(to right, transparent, #e5e7eb, transparent) !important;
    }
    
    /* Loading animation */
    .stSpinner > div {
        border-color: #667eea !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat' not in st.session_state:
    st.session_state.chat = PerplexityChat()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Header
st.markdown("<h1>✨ Perplexity AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Ask anything. Get intelligent answers with sources.</p>", unsafe_allow_html=True)

# Model selector in expander
with st.expander("🎯 Choose Your AI Model", expanded=False):
    st.markdown("### Available Models")
    
    # Filter options
    filter_option = st.radio(
        "Filter by:",
        ["All Models", "Reasoning Models", "By Tier"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    if filter_option == "Reasoning Models":
        available_models = st.session_state.chat.get_reasoning_models()
    elif filter_option == "By Tier":
        tier = st.selectbox("Select Tier", ["Free", "Pro", "Max"])
        available_models = st.session_state.chat.get_models_by_tier(tier)
    else:
        available_models = st.session_state.chat.available_models
    
    # Model selection with enhanced display
    model_options = list(available_models.keys())
    model_labels = [
        f"{v['icon']} {v['name']} · {v['description']}" 
        for v in available_models.values()
    ]
    
    selected_model = st.selectbox(
        "Model",
        options=model_options,
        format_func=lambda x: f"{available_models[x]['icon']} {available_models[x]['name']} · {available_models[x]['description']}",
        index=model_options.index("sonar-reasoning-pro") if "sonar-reasoning-pro" in model_options else 0,
        label_visibility="collapsed"
    )
    
    # Display model details
    model_info = available_models[selected_model]
    tier_class = f"tier-{model_info['tier'].lower()}"
    
    st.markdown(f"""
    <div style="background: white; border-radius: 12px; padding: 1rem; margin-top: 1rem; border: 1px solid #e5e7eb;">
        <span class="model-badge">{model_info['icon']} {model_info['name']}</span>
        <span class="tier-badge {tier_class}">{model_info['tier']}</span>
        <p style="margin-top: 0.75rem; color: #6B7280; font-size: 0.9rem; margin-bottom: 0;">
            {model_info['description']}
            {'<br><strong>💭 Reasoning enabled</strong>' if model_info['reasoning'] else ''}
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Display chat history
for chat in st.session_state.chat_history:
    with st.chat_message("user", avatar="👤"):
        st.write(chat["question"])
    
    with st.chat_message("assistant", avatar="✨"):
        st.write(chat["answer"])
        
        # Display citations
        if chat["citations"]:
            with st.expander(f"📚 Sources ({len(chat['citations'])})"):
                for citation in chat["citations"]:
                    st.markdown(f"""
                    <div class="citation-card">
                        <span class="citation-number">{citation['number']}</span>
                        <strong>{citation['domain']}</strong><br>
                        <a href="{citation['url']}" target="_blank" style="color: #667eea; text-decoration: none; font-size: 0.8rem;">
                            {citation['url'][:60]}...
                        </a>
                    </div>
                    """, unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.write(user_input)
    
    # Get AI response
    with st.chat_message("assistant", avatar="✨"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat.ask(user_input, model=selected_model)
            st.write(response["answer"])
            
            # Display citations
            if response["citations"]:
                with st.expander(f"📚 Sources ({len(response['citations'])})"):
                    for citation in response["citations"]:
                        st.markdown(f"""
                        <div class="citation-card">
                            <span class="citation-number">{citation['number']}</span>
                            <strong>{citation['domain']}</strong><br>
                            <a href="{citation['url']}" target="_blank" style="color: #667eea; text-decoration: none; font-size: 0.8rem;">
                                {citation['url'][:60]}...
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
    
    # Save to history
    st.session_state.chat_history.append(response)

# Footer actions
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.chat.clear_history()
        st.session_state.chat_history = []
        st.rerun()

with col2:
    st.markdown(f"""
    <div style="text-align: right; color: #9CA3AF; font-size: 0.8rem; padding: 0.75rem;">
        💬 {len(st.session_state.chat_history)} messages
    </div>
    """, unsafe_allow_html=True)
