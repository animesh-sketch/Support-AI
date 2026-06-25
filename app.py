import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Support Platform",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Convin Style
st.markdown("""
<style>
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Remove default sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }

    /* Chat bubbles */
    .chat-message {
        padding: 12px 16px;
        border-radius: 12px;
        margin: 8px 0;
        word-wrap: break-word;
    }

    .chat-user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
        width: fit-content;
        max-width: 70%;
    }

    .chat-bot {
        background: white;
        color: #333;
        border: 1px solid #e0e0e0;
        width: fit-content;
        max-width: 70%;
    }

    /* Cards */
    .card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: none;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 30px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4) !important;
    }

    /* Input fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 8px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 12px !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        background: #f0f0f0;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }

    /* Metrics */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        text-align: center;
    }

    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #667eea;
        margin: 10px 0;
    }

    .metric-label {
        color: #666;
        font-size: 14px;
        font-weight: 500;
    }

    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = [
        {'role': 'user', 'content': 'What is your pricing?', 'time': '2:30 PM'},
        {'role': 'bot', 'content': 'We offer Starter ($99), Pro ($299), and Enterprise (custom) plans.', 'time': '2:31 PM'},
        {'role': 'user', 'content': 'Good for a team of 20?', 'time': '2:32 PM'},
        {'role': 'bot', 'content': 'Yes! Pro plan supports up to 50 users and is perfect for teams of 20.', 'time': '2:32 PM'},
    ]

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# ============================================================================
# HOME PAGE
# ============================================================================
def render_home():
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 40px 0;">
            <h1 style="font-size: 48px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">
                Support Platform
            </h1>
            <p style="color: #666; font-size: 18px; margin-top: 10px;">
                Chat, Voice Calls & Knowledge Base
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Main action cards
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="card" style="text-align: center; border: 2px solid #667eea;">
            <div style="font-size: 48px; margin-bottom: 15px;">💬</div>
            <h2 style="color: #667eea; margin: 0 0 10px 0;">Chat Support</h2>
            <p style="color: #666; margin: 0 0 20px 0;">Get instant answers from our support team</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("💬 Start Chat", use_container_width=True, key="chat_btn"):
            st.session_state.current_page = 'chat'
            st.rerun()

    with col2:
        st.markdown("""
        <div class="card" style="text-align: center; border: 2px solid #764ba2;">
            <div style="font-size: 48px; margin-bottom: 15px;">☎️</div>
            <h2 style="color: #764ba2; margin: 0 0 10px 0;">Voice Call</h2>
            <p style="color: #666; margin: 0 0 20px 0;">Speak directly with our support team</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("☎️ Schedule Call", use_container_width=True, key="call_btn"):
            st.session_state.current_page = 'call'
            st.rerun()

    st.divider()

    # Quick stats
    col1, col2, col3, col4 = st.columns(4)

    stats = [
        ("📊", "Active Chats", "8", "+3"),
        ("☎️", "Calls Today", "48", "+12"),
        ("⏱️", "Avg Response", "2m 30s", "-15s"),
        ("😊", "Satisfaction", "4.8/5", "+0.1")
    ]

    for icon, label, value, change in stats:
        with st.columns(4)[stats.index((icon, label, value, change))]:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 24px;">{icon}</div>
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div style="color: #4caf50; font-size: 12px;">{change}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Other options
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📚 Help Center", use_container_width=True):
            st.session_state.current_page = 'help'
            st.rerun()

    with col2:
        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state.current_page = 'dashboard'
            st.rerun()

    with col3:
        if st.button("⚙️ Settings", use_container_width=True):
            st.session_state.current_page = 'settings'
            st.rerun()

# ============================================================================
# CHAT PAGE
# ============================================================================
def render_chat():
    # Header with back button
    col1, col2 = st.columns([1, 9])
    with col1:
        if st.button("← Back", key="back_chat"):
            st.session_state.current_page = 'home'
            st.rerun()
    with col2:
        st.markdown("### 💬 Chat Support")

    st.divider()

    # Chat messages container
    st.markdown('<div class="card">', unsafe_allow_html=True)

    for msg in st.session_state.chat_messages:
        if msg['role'] == 'user':
            col1, col2 = st.columns([1, 4])
            with col2:
                st.markdown(f"""
                <div class="chat-message chat-user">
                    <strong>{msg['content']}</strong><br>
                    <small>{msg['time']}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                <div class="chat-message chat-bot">
                    {msg['content']}<br>
                    <small>{msg['time']}</small>
                </div>
                """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # Input area
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("Type your message...", placeholder="Ask anything...", label_visibility="collapsed")
    with col2:
        if st.button("Send", use_container_width=True):
            if user_input:
                st.session_state.chat_messages.append({
                    'role': 'user',
                    'content': user_input,
                    'time': datetime.now().strftime("%I:%M %p")
                })
                st.session_state.chat_messages.append({
                    'role': 'bot',
                    'content': 'Thank you! Our team will respond shortly.',
                    'time': datetime.now().strftime("%I:%M %p")
                })
                st.rerun()

    st.caption("✅ Usually responds in 2 minutes")

# ============================================================================
# CALL PAGE
# ============================================================================
def render_call():
    # Header with back button
    col1, col2 = st.columns([1, 9])
    with col1:
        if st.button("← Back", key="back_call"):
            st.session_state.current_page = 'home'
            st.rerun()
    with col2:
        st.markdown("### ☎️ Schedule a Call")

    st.divider()

    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Your Information**")
        name = st.text_input("Full Name", placeholder="John Doe")
        email = st.text_input("Email", placeholder="john@example.com")

    with col2:
        st.markdown("**Contact Details**")
        phone = st.text_input("Phone Number", placeholder="+1-555-123-4567")
        best_time = st.selectbox("Best Time to Call", ["9 AM - 12 PM", "12 PM - 3 PM", "3 PM - 6 PM", "6 PM - 9 PM"])

    st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📞 Schedule Call", use_container_width=True, type="primary"):
            if phone and name:
                st.success(f"✅ Call scheduled! We'll call {phone} at {best_time}")
                st.balloons()
            else:
                st.error("Please fill in Name and Phone Number")

    st.info("💡 Our support team will call you at your scheduled time")

# ============================================================================
# HELP PAGE
# ============================================================================
def render_help():
    # Header with back button
    col1, col2 = st.columns([1, 9])
    with col1:
        if st.button("← Back", key="back_help"):
            st.session_state.current_page = 'home'
            st.rerun()
    with col2:
        st.markdown("### 📚 Help Center")

    st.divider()

    search = st.text_input("🔍 Search articles...", placeholder="Search help topics")

    st.divider()

    articles = [
        ("Getting Started", "Learn how to set up your account and get started", "Getting Started"),
        ("Pricing Plans", "Compare our available pricing tiers", "Billing"),
        ("API Documentation", "Integrate with our REST API", "Developer"),
        ("Account Security", "Secure your account with 2FA", "Security"),
        ("Troubleshooting", "Common issues and solutions", "Support"),
    ]

    for title, desc, category in articles:
        if not search or search.lower() in title.lower() or search.lower() in desc.lower():
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"**{title}**")
                st.caption(desc)
            with col2:
                st.caption(f"📁 {category}")
            with col3:
                st.button("→", key=f"article_{title}")
            st.divider()

# ============================================================================
# DASHBOARD PAGE
# ============================================================================
def render_dashboard():
    # Header with back button
    col1, col2 = st.columns([1, 9])
    with col1:
        if st.button("← Back", key="back_dashboard"):
            st.session_state.current_page = 'home'
            st.rerun()
    with col2:
        st.markdown("### 📊 Admin Dashboard")

    st.divider()

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        (col1, "🟢", "Active Chats", "8", "+3"),
        (col2, "☎️", "Calls Today", "48", "+12"),
        (col3, "⏱️", "Avg Response", "2m 30s", "-15s"),
        (col4, "😊", "Satisfaction", "4.8/5", "+0.1")
    ]

    for col, icon, label, value, change in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 20px;">{icon}</div>
                <div class="metric-label">{label}</div>
                <div class="metric-value" style="font-size: 24px;">{value}</div>
                <div style="color: #4caf50; font-size: 12px;">{change}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Live conversations
    st.markdown("### 💬 Live Conversations")

    conversations = [
        {"name": "Sarah Johnson", "email": "sarah@company.com", "channel": "Chat", "status": "Active", "messages": 8},
        {"name": "Mike Davis", "email": "mike@tech.com", "channel": "Call", "status": "Completed", "messages": 1},
        {"name": "Emma Wilson", "email": "emma@startup.io", "channel": "Chat", "status": "Resolved", "messages": 6},
    ]

    for conv in conversations:
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
        with col1:
            st.markdown(f"**{conv['name']}**")
            st.caption(conv['email'])
        with col2:
            st.markdown(f"{conv['channel']} • {conv['messages']} messages")
        with col3:
            status_icon = "🟢" if conv['status'] == "Active" else "✅"
            st.markdown(f"{status_icon} {conv['status']}")
        with col4:
            st.button("View", key=f"conv_{conv['name']}")

        st.divider()

# ============================================================================
# SETTINGS PAGE
# ============================================================================
def render_settings():
    # Header with back button
    col1, col2 = st.columns([1, 9])
    with col1:
        if st.button("← Back", key="back_settings"):
            st.session_state.current_page = 'home'
            st.rerun()
    with col2:
        st.markdown("### ⚙️ Settings")

    st.divider()

    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**API Configuration**")
        api_url = st.text_input("API URL", value="http://localhost:3000")
        api_key = st.text_input("API Key", type="password", placeholder="Enter your API key")

    with col2:
        st.markdown("**Preferences**")
        notifications = st.checkbox("Enable notifications", value=True)
        theme = st.selectbox("Theme", ["Light", "Dark"])

    st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    if st.button("💾 Save Settings", use_container_width=True, type="primary"):
        st.success("✅ Settings saved!")

# ============================================================================
# MAIN APP
# ============================================================================

if st.session_state.current_page == 'home':
    render_home()
elif st.session_state.current_page == 'chat':
    render_chat()
elif st.session_state.current_page == 'call':
    render_call()
elif st.session_state.current_page == 'help':
    render_help()
elif st.session_state.current_page == 'dashboard':
    render_dashboard()
elif st.session_state.current_page == 'settings':
    render_settings()

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 12px; padding: 20px 0;">
    <p>Support Platform • Built with ❤️ for Convin AI</p>
</div>
""", unsafe_allow_html=True)
