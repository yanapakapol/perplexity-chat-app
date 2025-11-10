import streamlit as st
from perplexity_backend import PerplexityChat

# Page configuration
st.set_page_config(
    page_title="Perplexity AI Chat",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stAlert {
        margin-bottom: 1rem;
    }
    .citation-box {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .process-step {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat' not in st.session_state:
    st.session_state.chat = PerplexityChat()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Main title
st.title("🤖 Perplexity AI Chat Interface")
st.markdown("---")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Model selection
    selected_model = st.selectbox(
        "Select AI Model",
        options=list(st.session_state.chat.available_models.keys()),
        index=3,  # Default to sonar-reasoning-pro
        format_func=lambda x: f"{x}: {st.session_state.chat.available_models[x]}"
    )
    
    st.markdown("---")
    
    # Show AI Process toggle
    show_process = st.checkbox("Show AI Thinking Process", value=True)
    
    st.markdown("---")
    
    # Clear history button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat.clear_history()
        st.session_state.chat_history = []
        st.success("Chat history cleared!")
        st.rerun()

# AI Process Explanation (collapsible)
if show_process:
    with st.expander("🧠 How AI Processes Your Question", expanded=False):
        process = st.session_state.chat.get_ai_process_explanation()
        for step in process["steps"]:
            st.markdown(f"""
            <div class="process-step">
                <h4>{step['icon']} {step['title']}</h4>
                <p>{step['description']}</p>
            </div>
            """, unsafe_allow_html=True)

# Main chat interface
st.header("💬 Chat")

# Display chat history
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat["question"])
    
    with st.chat_message("assistant"):
        st.markdown(chat["answer"])
        
        # Show citations if available
        if chat["citations"]:
            with st.expander(f"📚 {len(chat['citations'])} Sources Consulted"):
                for cite in chat["citations"]:
                    st.markdown(f"""
                    <div class="citation-box">
                        <strong>[{cite['number']}]</strong> ({cite['domain']}, {cite['year']})<br>
                        <small><a href="{cite['url']}" target="_blank">{cite['url']}</a></small>
                    </div>
                    """, unsafe_allow_html=True)

# Input area
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Show user message immediately
    with st.chat_message("user"):
        st.write(user_input)
    
    # Show loading spinner while processing
    with st.chat_message("assistant"):
        with st.spinner(f"🔄 AI is thinking using {selected_model}..."):
            try:
                # Get response from backend
                result = st.session_state.chat.ask(user_input, model=selected_model)
                
                # Display answer
                st.markdown(result["answer"])
                
                # Display citations
                if result["citations"]:
                    with st.expander(f"📚 {len(result['citations'])} Sources Consulted"):
                        for cite in result["citations"]:
                            st.markdown(f"""
                            <div class="citation-box">
                                <strong>[{cite['number']}]</strong> ({cite['domain']}, {cite['year']})<br>
                                <small><a href="{cite['url']}" target="_blank">{cite['url']}</a></small>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Add to chat history
                st.session_state.chat_history.append(result)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.caption(f"Model: {selected_model} | Chat messages: {len(st.session_state.chat_history)}")
