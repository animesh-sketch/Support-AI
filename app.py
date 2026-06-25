import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(
    page_title="Anamika - Support Widget",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# ANAMIKA DESIGN SYSTEM - FLOATING CHAT WIDGET
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --primary: #3b82f6;
        --secondary: #8b5cf6;
        --success: #22c55e;
        --bg: #0f172a;
        --bg-secondary: #1e293b;
        --text: #f1f5f9;
        --text-muted: #94a3b8;
    }

    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }

    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        color: var(--text);
    }

    .main { background: transparent; }

    h1 {
        font-size: 48px !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    h2, h3, h4, h5 { color: var(--text) !important; font-weight: 700 !important; }

    .premium-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(20px);
        transition: all 0.3s cubic-bezier(0.23, 1, 0.320, 1);
    }

    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 28px !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.320, 1) !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 30px rgba(59, 130, 246, 0.6) !important;
    }

    /* ============================================================================
    FLOATING CHAT WIDGET
    ============================================================================ */

    .anamika-widget-floating {
        position: fixed !important;
        top: 30px !important;
        right: 30px !important;
        z-index: 999999 !important;
        font-family: 'Inter', sans-serif !important;
    }

    .anamika-button-main {
        width: 70px !important;
        height: 70px !important;
        border-radius: 50% !important;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        font-size: 32px !important;
        cursor: pointer !important;
        box-shadow: 0 12px 32px rgba(59, 130, 246, 0.35) !important;
        transition: all 0.35s cubic-bezier(0.23, 1, 0.320, 1) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        position: relative !important;
    }

    .anamika-button-main:hover {
        transform: scale(1.18) !important;
        box-shadow: 0 18px 48px rgba(59, 130, 246, 0.45) !important;
    }

    .anamika-badge {
        position: absolute !important;
        top: -6px !important;
        right: -6px !important;
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
        color: white !important;
        min-width: 28px !important;
        height: 28px !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 11px !important;
        font-weight: 800 !important;
        box-shadow: 0 3px 12px rgba(239, 68, 68, 0.6) !important;
        border: 2px solid rgba(15, 23, 42, 0.8) !important;
    }

    .anamika-chatbox {
        position: fixed !important;
        top: 110px !important;
        right: 20px !important;
        width: 380px !important;
        height: 600px !important;
        background: rgba(15, 23, 42, 0.98) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 20px !important;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6) !important;
        backdrop-filter: blur(30px) !important;
        display: flex !important;
        flex-direction: column !important;
        z-index: 999998 !important;
        opacity: 0 !important;
        transform: translateY(-20px) scale(0.95) !important;
        transition: all 0.35s cubic-bezier(0.23, 1, 0.320, 1) !important;
        pointer-events: none !important;
    }

    .anamika-chatbox.open {
        opacity: 1 !important;
        transform: translateY(0) scale(1) !important;
        pointer-events: auto !important;
    }

    .anamika-header {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
        padding: 20px !important;
        border-radius: 20px 20px 0 0 !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
    }

    .anamika-header h3 {
        margin: 0 !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: 700 !important;
    }

    .anamika-header p {
        color: rgba(255, 255, 255, 0.8) !important;
        font-size: 12px !important;
        margin: 4px 0 0 0 !important;
    }

    .anamika-close {
        background: rgba(255, 255, 255, 0.2) !important;
        border: none !important;
        color: white !important;
        width: 32px !important;
        height: 32px !important;
        border-radius: 50% !important;
        cursor: pointer !important;
        font-size: 18px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s ease !important;
    }

    .anamika-close:hover {
        background: rgba(255, 255, 255, 0.3) !important;
        transform: scale(1.1) !important;
    }

    .anamika-messages {
        flex: 1 !important;
        overflow-y: auto !important;
        padding: 20px !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 12px !important;
    }

    .message-bot {
        background: rgba(59, 130, 246, 0.2) !important;
        padding: 12px 14px !important;
        border-radius: 12px !important;
        border-left: 3px solid #3b82f6 !important;
        max-width: 85% !important;
        align-self: flex-start !important;
        font-size: 13px !important;
        color: var(--text) !important;
    }

    .message-user {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
        padding: 12px 14px !important;
        border-radius: 12px !important;
        max-width: 85% !important;
        align-self: flex-end !important;
        font-size: 13px !important;
        color: white !important;
    }

    .anamika-input-area {
        padding: 16px !important;
        border-top: 1px solid rgba(59, 130, 246, 0.2) !important;
        display: flex !important;
        gap: 10px !important;
        flex-wrap: wrap !important;
    }

    .anamika-input {
        flex: 1 !important;
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 10px !important;
        padding: 10px 12px !important;
        color: var(--text) !important;
        font-size: 13px !important;
        font-family: 'Inter', sans-serif !important;
        min-height: 0 !important;
    }

    .anamika-input:focus {
        border-color: #3b82f6 !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
    }

    .anamika-button-send {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
        border: none !important;
        color: white !important;
        width: 40px !important;
        height: 40px !important;
        border-radius: 10px !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
    }

    .anamika-button-send:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4) !important;
    }

    .anamika-actions {
        display: flex !important;
        gap: 10px !important;
        width: 100% !important;
    }

    .anamika-action-btn {
        flex: 1 !important;
        background: rgba(59, 130, 246, 0.15) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        color: #3b82f6 !important;
        padding: 8px 12px !important;
        border-radius: 8px !important;
        cursor: pointer !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif !important;
    }

    .anamika-action-btn:hover {
        background: rgba(59, 130, 246, 0.25) !important;
        border-color: rgba(59, 130, 246, 0.5) !important;
    }

    ::-webkit-scrollbar {
        width: 6px !important;
    }

    ::-webkit-scrollbar-track {
        background: transparent !important;
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(59, 130, 246, 0.3) !important;
        border-radius: 3px !important;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: rgba(59, 130, 246, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
if 'widget_open' not in st.session_state:
    st.session_state.widget_open = False
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "content": "Hi! 👋 I'm Anamika. How can I help you today?"}
    ]
if 'admin_password' not in st.session_state:
    st.session_state.admin_password = False

# ============================================================================
# FLOATING WIDGET - RENDERED IN MAIN LAYOUT
# ============================================================================
def render_floating_widget():
    """Render the floating chat widget"""

    # Determine if widget is open
    widget_open = st.session_state.widget_open

    # HTML for floating button and chat
    widget_html = f"""
    <div class="anamika-widget-floating">
        <button class="anamika-button-main" id="anamika-open-btn" onclick="document.getElementById('anamika-widget-toggle').click()">
            🎯
            <div class="anamika-badge">3</div>
        </button>

        <div class="anamika-chatbox {'open' if widget_open else ''}">
            <div class="anamika-header">
                <div>
                    <h3>🎯 Anamika</h3>
                    <p>Always here to help</p>
                </div>
                <button class="anamika-close" onclick="document.getElementById('anamika-close-btn').click()">✕</button>
            </div>

            <div class="anamika-messages" id="anamika-messages">
                <!-- Messages will be rendered here -->
            </div>

            <div class="anamika-input-area">
                <div style="width: 100%;">
                    <div style="display: flex; gap: 10px; margin-bottom: 10px;">
                        <button class="anamika-action-btn" onclick="document.getElementById('call-btn').click()">☎️ Call</button>
                        <button class="anamika-action-btn" onclick="alert('Chat with agent')">👤 Agent</button>
                    </div>
                    <div style="display: flex; gap: 10px;">
                        <input type="text" class="anamika-input" id="anamika-input" placeholder="Type a message..." />
                        <button class="anamika-button-send" onclick="document.getElementById('send-btn').click()">📤</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """

    st.markdown(widget_html, unsafe_allow_html=True)

# ============================================================================
# DASHBOARD PAGE
# ============================================================================
def dashboard():
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px; background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
                 border-radius: 24px; margin-bottom: 40px;">
        <h1>🎯 Anamika</h1>
        <p style="color: var(--text-muted); font-size: 16px; margin-top: 12px;">
            Enterprise Floating Chat Widget
        </p>
        <p style="color: #22c55e; font-size: 13px; margin-top: 16px; font-weight: 700;">
            👉 Click the 🎯 button in TOP RIGHT to start chatting!
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4, gap="small")
    with col1:
        if st.button("💬 Chat", use_container_width=True):
            st.session_state.page = 'chat'
            st.rerun()
    with col2:
        if st.button("☎️ Voice", use_container_width=True):
            st.session_state.page = 'voice'
            st.rerun()
    with col3:
        if st.button("📊 Analytics", use_container_width=True):
            st.session_state.page = 'analytics'
            st.rerun()
    with col4:
        if st.button("🔐 Admin", use_container_width=True):
            st.session_state.page = 'admin_login'
            st.rerun()

    st.markdown("---")

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    metrics = [
        (col1, "💬", "1,245", "Chats", "+12%"),
        (col2, "☎️", "312", "Calls", "+18%"),
        (col3, "✅", "94.2%", "Resolved", "+3.2%"),
        (col4, "😊", "4.87/5", "CSAT", "+0.15"),
        (col5, "🤖", "87%", "AI OK", "+5%"),
        (col6, "⚡", "45s", "Response", "-15s"),
    ]

    for col, icon, value, label, trend in metrics:
        with col:
            st.metric(label, value, trend)

    st.markdown("---")
    st.markdown("""
    <div class="premium-card">
        <h4>✨ Widget Features</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 16px;">
            <div><p><strong>💬 Smart Chat</strong><br><span style="color: var(--text-muted); font-size: 13px;">Ask questions, get instant AI responses</span></p></div>
            <div><p><strong>☎️ Call Support</strong><br><span style="color: var(--text-muted); font-size: 13px;">Schedule or start voice calls</span></p></div>
            <div><p><strong>📚 Knowledge Base</strong><br><span style="color: var(--text-muted); font-size: 13px;">Smart answers from our KB</span></p></div>
            <div><p><strong>👤 Talk to Agent</strong><br><span style="color: var(--text-muted); font-size: 13px;">Get human support anytime</span></p></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# CHAT PAGE
# ============================================================================
def chat():
    st.markdown("### 💬 Chat with Anamika")

    st.markdown("""
    <div class="premium-card">
        <p style="color: var(--text-muted);">🤖 AI-powered • <strong>45s</strong> response time • <strong>96.8%</strong> accuracy</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Display chat messages
    for msg in st.session_state.messages:
        if msg["role"] == "bot":
            st.markdown(f"**Anamika:** {msg['content']}")
        else:
            st.markdown(f"**You:** {msg['content']}")

    # Input area
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("Your message...", placeholder="Ask anything", label_visibility="collapsed")
    with col2:
        send = st.button("Send", use_container_width=True)

    if send and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "bot", "content": "Thanks for your message! How else can I help?"})
        st.rerun()

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("☎️ Talk to Agent", use_container_width=True):
            st.info("📞 Connecting to next available agent...")
    with col2:
        if st.button("📊 Analytics", use_container_width=True):
            st.session_state.page = 'analytics'
            st.rerun()
    with col3:
        if st.button("Home", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()

# ============================================================================
# VOICE PAGE
# ============================================================================
def voice():
    st.markdown("### ☎️ Voice Call")

    st.markdown("""
    <div class="premium-card">
        <p style="color: var(--text-muted);">🎧 Crystal-clear voice • Convin Sense powered</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.text_input("Your Name", placeholder="John Doe", label_visibility="collapsed")
        st.text_input("Email", placeholder="john@example.com", label_visibility="collapsed")
    with col2:
        st.text_input("Phone", placeholder="+1-555-123-4567", label_visibility="collapsed")
        st.selectbox("Best Time", ["9 AM - 12 PM", "12 PM - 3 PM", "3 PM - 6 PM", "6 PM - 9 PM"], label_visibility="collapsed")

    if st.button("📞 Schedule Voice Call", use_container_width=True):
        st.success("✅ Call scheduled! We'll call you within 2 minutes.")
        st.balloons()

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💬 Chat Instead", use_container_width=True):
            st.session_state.page = 'chat'
            st.rerun()
    with col2:
        if st.button("📊 Analytics", use_container_width=True):
            st.session_state.page = 'analytics'
            st.rerun()
    with col3:
        if st.button("Home", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()

# ============================================================================
# ANALYTICS PAGE
# ============================================================================
def analytics():
    st.markdown("### 📊 Analytics")

    tab1, tab2 = st.tabs(["Overview", "Performance"])

    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Conversations", "3,847", "+15%")
        with col2:
            st.metric("Avg Resolution", "12m 30s", "-2m 15s")
        with col3:
            st.metric("Escalation Rate", "13%", "-2%")

    with tab2:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("AI Accuracy", "96.8%", "+1.2%")
        with col2:
            st.metric("CSAT", "4.87/5", "+0.15")
        with col3:
            st.metric("Response Time", "45s", "-15s")

    st.markdown("---")
    if st.button("Back to Home", use_container_width=True):
        st.session_state.page = 'dashboard'
        st.rerun()

# ============================================================================
# ADMIN LOGIN
# ============================================================================
def admin_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="premium-card" style="text-align: center;">
            <h3>🔐 Anamika Admin</h3>
            <p style="color: var(--text-muted); font-size: 13px;">Secure access required</p>
        </div>
        """, unsafe_allow_html=True)

        password = st.text_input("Password", type="password", placeholder="Enter admin password", label_visibility="collapsed")

        if st.button("Login", use_container_width=True):
            if password == "admin@anamika":
                st.session_state.admin_password = True
                st.session_state.page = 'admin_panel'
                st.rerun()
            else:
                st.error("❌ Invalid password")

        if st.button("Back to Home", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()

# ============================================================================
# ADMIN PANEL
# ============================================================================
def admin_panel():
    st.markdown("### ⚙️ Admin Panel")

    if not st.session_state.admin_password:
        st.warning("⚠️ Unauthorized")
        if st.button("Go Home"):
            st.session_state.page = 'dashboard'
            st.rerun()
        return

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📚 KB", "🎤 Voice", "☎️ Agents", "📏 Escalation", "⏰ Hours", "🤖 Bot"])

    with tab1:
        st.markdown("#### Knowledge Base")
        uploaded_file = st.file_uploader("Upload document", type=['pdf', 'doc', 'docx', 'txt'])
        if uploaded_file:
            st.success(f"✅ {uploaded_file.name} uploaded!")

    with tab2:
        st.markdown("#### Voice Configuration")
        st.text_input("Workspace ID", placeholder="workspace_xyz")
        st.text_input("API Key", placeholder="sk-sense-...", type="password")

    with tab3:
        st.markdown("#### Agent Management")
        st.text_input("Agent Name", placeholder="John Doe")
        st.selectbox("Status", ["Available", "Busy", "Break", "Offline"])

    with tab4:
        st.markdown("#### Escalation Rules")
        st.selectbox("Trigger", ["Max attempts", "Low confidence", "Customer request"])

    with tab5:
        st.markdown("#### Business Hours")
        st.time_input("Start Time", value=None)
        st.time_input("End Time", value=None)

    with tab6:
        st.markdown("#### Bot Settings")
        st.toggle("Use Knowledge Base", value=True)
        st.slider("Confidence Threshold", 0, 100, 75)

    st.markdown("---")
    if st.button("Logout", use_container_width=True):
        st.session_state.admin_password = False
        st.session_state.page = 'dashboard'
        st.rerun()

# ============================================================================
# MAIN APP LOGIC
# ============================================================================

# Hidden buttons to control widget state
col1, col2, col3, col4 = st.columns([1, 1, 1, 10])

with col1:
    if st.button("🎯"):
        st.session_state.widget_open = not st.session_state.widget_open
        st.rerun()
    st.markdown('<div id="anamika-widget-toggle" style="display: none;"></div>', unsafe_allow_html=True)

with col2:
    if st.button("✕"):
        st.session_state.widget_open = False
        st.rerun()
    st.markdown('<div id="anamika-close-btn" style="display: none;"></div>', unsafe_allow_html=True)

with col3:
    if st.button("📤"):
        if st.session_state.messages[-1]["role"] != "user":
            user_msg = "User message"
            st.session_state.messages.append({"role": "user", "content": user_msg})
            st.session_state.messages.append({"role": "bot", "content": "Thanks! How else can I help?"})
        st.rerun()
    st.markdown('<div id="send-btn" style="display: none;"></div>', unsafe_allow_html=True)

with col4:
    if st.button("📞 Call"):
        st.session_state.page = 'voice'
        st.rerun()
    st.markdown('<div id="call-btn" style="display: none;"></div>', unsafe_allow_html=True)

# Hide the control buttons
st.markdown("""
<style>
    [data-testid="stHorizontalBlock"] > :nth-child(1) { display: none !important; }
</style>
""", unsafe_allow_html=True)

# Render floating widget
render_floating_widget()

# Render chat messages inside widget
if st.session_state.widget_open:
    messages_html = ""
    for msg in st.session_state.messages:
        if msg["role"] == "bot":
            messages_html += f'<div class="message-bot">{msg["content"]}</div>'
        else:
            messages_html += f'<div class="message-user">{msg["content"]}</div>'

    st.markdown(f"""
    <script>
        const messagesDiv = document.getElementById('anamika-messages');
        if (messagesDiv) {{
            messagesDiv.innerHTML = `{messages_html}`;
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }}
    </script>
    """, unsafe_allow_html=True)

# Main content based on current page
if st.session_state.page == 'dashboard':
    dashboard()
elif st.session_state.page == 'chat':
    chat()
elif st.session_state.page == 'voice':
    voice()
elif st.session_state.page == 'analytics':
    analytics()
elif st.session_state.page == 'admin_login':
    admin_login()
elif st.session_state.page == 'admin_panel':
    admin_panel()

# Footer
st.markdown("""
<div style="text-align: center; padding: 40px 20px; margin-top: 60px; border-top: 1px solid rgba(59, 130, 246, 0.1);">
    <p style="color: var(--text-muted); font-size: 12px; margin: 0;">
        🎯 Anamika Enterprise Widget | Powered by Convin AI | v4.0 Interactive Chat
    </p>
</div>
""", unsafe_allow_html=True)
