import streamlit as st
from datetime import datetime
import time

# Page config
st.set_page_config(
    page_title="Support Platform",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# FANCY CSS STYLING
# ============================================================================
st.markdown("""
<style>
    * {
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }

    /* Main container */
    .main-container {
        background: white;
        border-radius: 20px;
        padding: 40px;
        margin: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }

    /* Header */
    .fancy-header {
        text-align: center;
        padding: 40px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* Fancy buttons */
    .fancy-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 16px 32px;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        width: 100%;
        margin: 10px 0;
    }

    .fancy-btn:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }

    /* Card styling */
    .fancy-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.8);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        margin: 16px 0;
    }

    .fancy-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.2);
    }

    /* Chat widget */
    .chat-widget {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 20px;
        padding: 24px;
        height: 500px;
        overflow-y: auto;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.05);
    }

    .message {
        padding: 12px 16px;
        border-radius: 12px;
        margin: 10px 0;
        word-wrap: break-word;
        animation: slideIn 0.3s ease-out;
    }

    .message-user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
        width: fit-content;
        max-width: 80%;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }

    .message-bot {
        background: white;
        color: #333;
        margin-right: auto;
        width: fit-content;
        max-width: 80%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Input fields */
    .fancy-input {
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 12px 16px;
        font-size: 14px;
        transition: all 0.3s ease;
        background: white;
    }

    .fancy-input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    /* Status indicators */
    .status-online {
        display: inline-block;
        width: 12px;
        height: 12px;
        background: #4caf50;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }

    /* Action cards */
    .action-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .action-card:hover {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
        border-color: rgba(102, 126, 234, 0.6);
        transform: translateY(-8px);
    }

    .action-icon {
        font-size: 48px;
        margin-bottom: 16px;
    }

    /* Form styling */
    .form-group {
        margin-bottom: 20px;
    }

    .form-label {
        font-weight: 600;
        color: #333;
        margin-bottom: 8px;
        display: block;
    }

    /* Metrics */
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }

    .metric-value {
        font-size: 32px;
        font-weight: 700;
        margin: 10px 0;
    }

    .metric-label {
        font-size: 14px;
        opacity: 0.9;
    }

    /* Divider */
    .fancy-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #667eea 50%, transparent 100%);
        margin: 30px 0;
    }

    /* Badge */
    .badge {
        display: inline-block;
        background: #4caf50;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = [
        {'role': 'user', 'content': 'Hi! What are your pricing plans?', 'time': '2:30 PM'},
        {'role': 'bot', 'content': 'We offer Starter ($99), Pro ($299), and Enterprise (custom) plans. Which interests you?', 'time': '2:31 PM'},
        {'role': 'user', 'content': 'Good for a team of 20 people?', 'time': '2:32 PM'},
        {'role': 'bot', 'content': '✨ Perfect! Our Pro plan supports up to 50 users and is ideal for teams of 20. Includes all core features!', 'time': '2:32 PM'},
    ]

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# ============================================================================
# HOME PAGE
# ============================================================================
def render_home():
    # Fancy Header
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px;">
        <h1 style="font-size: 56px; margin: 0; color: white; text-shadow: 0 4px 20px rgba(0,0,0,0.3);">
            💬 Support Platform
        </h1>
        <p style="color: rgba(255,255,255,0.9); font-size: 18px; margin-top: 12px; text-shadow: 0 2px 10px rgba(0,0,0,0.2);">
            Chat, Voice Calls & Instant Support
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Main action cards
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="action-card">
            <div class="action-icon">💬</div>
            <h2 style="margin: 0 0 10px 0; color: #667eea;">Chat Support</h2>
            <p style="color: #666; margin: 0;">Get instant answers from our support team</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("💬 Start Chat Now", key="chat_btn", use_container_width=True):
            st.session_state.current_page = 'chat'
            st.rerun()

    with col2:
        st.markdown("""
        <div class="action-card">
            <div class="action-icon">☎️</div>
            <h2 style="margin: 0 0 10px 0; color: #764ba2;">Voice Call</h2>
            <p style="color: #666; margin: 0;">Speak directly with our support team</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("☎️ Schedule Call Now", key="call_btn", use_container_width=True):
            st.session_state.current_page = 'call'
            st.rerun()

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # Stats
    col1, col2, col3, col4 = st.columns(4)

    stats = [
        ("📊", "8", "Active Chats"),
        ("☎️", "48", "Calls Today"),
        ("⏱️", "2m 30s", "Avg Response"),
        ("😊", "4.8/5", "Satisfaction"),
    ]

    for col, (icon, value, label) in zip([col1, col2, col3, col4], stats):
        with col:
            st.markdown(f"""
            <div class="metric-box">
                <div style="font-size: 28px;">{icon}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

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
# FANCY CHAT PAGE
# ============================================================================
def render_chat():
    col1, col2 = st.columns([1, 9])
    with col1:
        if st.button("←", key="back_chat"):
            st.session_state.current_page = 'home'
            st.rerun()
    with col2:
        st.markdown("### 💬 Chat Support")

    # Agent info
    st.markdown("""
    <div class="fancy-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <h3 style="margin: 0; color: white;">Support Agent Online</h3>
                <p style="margin: 5px 0 0 0; opacity: 0.9;">Usually responds in 2 minutes</p>
            </div>
            <div style="text-align: right;">
                <div class="status-online"></div>
                <span style="font-weight: 600;">Available</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Chat area
    st.markdown('<div class="chat-widget">', unsafe_allow_html=True)

    for msg in st.session_state.chat_messages:
        if msg['role'] == 'user':
            st.markdown(f"""
            <div style="text-align: right; margin-bottom: 16px;">
                <div class="message message-user">
                    <div>{msg['content']}</div>
                    <div style="font-size: 12px; margin-top: 4px; opacity: 0.8;">{msg['time']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="text-align: left; margin-bottom: 16px;">
                <div class="message message-bot">
                    <div>{msg['content']}</div>
                    <div style="font-size: 12px; margin-top: 4px; color: #999;">{msg['time']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # Input area
    st.markdown('<div class="form-group">', unsafe_allow_html=True)
    col1, col2 = st.columns([5, 1])

    with col1:
        user_input = st.text_input(
            "Message",
            placeholder="💭 Type your message here...",
            label_visibility="collapsed",
            key="chat_input"
        )

    with col2:
        if st.button("📤", use_container_width=True, key="send_btn"):
            if user_input:
                st.session_state.chat_messages.append({
                    'role': 'user',
                    'content': user_input,
                    'time': datetime.now().strftime("%I:%M %p")
                })
                st.session_state.chat_messages.append({
                    'role': 'bot',
                    'content': '✨ Thank you! Our team will respond shortly.',
                    'time': datetime.now().strftime("%I:%M %p")
                })
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# FANCY CALL PAGE
# ============================================================================
def render_call():
    col1, col2 = st.columns([1, 9])
    with col1:
        if st.button("←", key="back_call"):
            st.session_state.current_page = 'home'
            st.rerun()
    with col2:
        st.markdown("### ☎️ Schedule a Call")

    st.markdown("""
    <div class="fancy-card" style="background: linear-gradient(135deg, #764ba2 0%, #f093fb 100%); color: white; text-align: center;">
        <h2 style="margin: 0; color: white;">🎤 Connect with Our Team</h2>
        <p style="margin: 8px 0 0 0; opacity: 0.9;">Schedule a call at your convenience</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # Form
    st.markdown('<div class="fancy-card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="form-group"><label class="form-label">👤 Your Name</label></div>', unsafe_allow_html=True)
        name = st.text_input("Name", placeholder="John Doe", label_visibility="collapsed")

        st.markdown('<div class="form-group"><label class="form-label">📧 Email</label></div>', unsafe_allow_html=True)
        email = st.text_input("Email", placeholder="john@example.com", label_visibility="collapsed")

    with col2:
        st.markdown('<div class="form-group"><label class="form-label">☎️ Phone Number</label></div>', unsafe_allow_html=True)
        phone = st.text_input("Phone", placeholder="+1-555-123-4567", label_visibility="collapsed")

        st.markdown('<div class="form-group"><label class="form-label">⏰ Best Time to Call</label></div>', unsafe_allow_html=True)
        best_time = st.selectbox(
            "Time",
            ["9 AM - 12 PM", "12 PM - 3 PM", "3 PM - 6 PM", "6 PM - 9 PM"],
            label_visibility="collapsed"
        )

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # Benefits
    col1, col2, col3 = st.columns(3)

    benefits = [
        ("⚡", "Quick Response", "Connect in minutes"),
        ("🎯", "Expert Support", "Dedicated team"),
        ("🔒", "Secure", "Your data protected"),
    ]

    for col, (icon, title, desc) in zip([col1, col2, col3], benefits):
        with col:
            st.markdown(f"""
            <div class="fancy-card">
                <div style="font-size: 32px; margin-bottom: 8px;">{icon}</div>
                <h4 style="margin: 0; color: #667eea;">{title}</h4>
                <p style="margin: 4px 0 0 0; color: #666; font-size: 13px;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📞 Schedule Call", use_container_width=True):
            if phone and name:
                st.markdown("""
                <div class="fancy-card" style="background: linear-gradient(135deg, #4caf50 0%, #45a049 100%); color: white; text-align: center;">
                    <div style="font-size: 32px; margin-bottom: 12px;">✅</div>
                    <h3 style="margin: 0; color: white;">Call Scheduled!</h3>
                    <p style="margin: 8px 0 0 0;">We'll call <strong>{phone}</strong> at <strong>{best_time}</strong></p>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(2)
                st.balloons()
            else:
                st.error("❌ Please fill in Name and Phone Number")

# ============================================================================
# HELP PAGE
# ============================================================================
def render_help():
    col1, col2 = st.columns([1, 9])
    with col1:
        if st.button("←", key="back_help"):
            st.session_state.current_page = 'home'
            st.rerun()
    with col2:
        st.markdown("### 📚 Help Center")

    search = st.text_input("🔍 Search articles...", placeholder="Search help topics")
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    articles = [
        ("Getting Started", "Learn how to set up your account and get started", "Getting Started"),
        ("Pricing Plans", "Compare our available pricing tiers", "Billing"),
        ("API Documentation", "Integrate with our REST API", "Developer"),
        ("Account Security", "Secure your account with 2FA", "Security"),
        ("Troubleshooting", "Common issues and solutions", "Support"),
    ]

    for title, desc, category in articles:
        if not search or search.lower() in title.lower():
            st.markdown(f"""
            <div class="fancy-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <h4 style="margin: 0; color: #667eea;">{title}</h4>
                        <p style="margin: 8px 0 0 0; color: #666; font-size: 14px;">{desc}</p>
                    </div>
                    <span class="badge">{category}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# DASHBOARD PAGE
# ============================================================================
def render_dashboard():
    col1, col2 = st.columns([1, 9])
    with col1:
        if st.button("←", key="back_dashboard"):
            st.session_state.current_page = 'home'
            st.rerun()
    with col2:
        st.markdown("### 📊 Admin Dashboard")

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        (col1, "🟢", "8", "Active Chats", "+3"),
        (col2, "☎️", "48", "Calls Today", "+12"),
        (col3, "⏱️", "2m 30s", "Avg Response", "-15s"),
        (col4, "😊", "4.8/5", "Satisfaction", "+0.1")
    ]

    for col, icon, value, label, change in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-box">
                <div style="font-size: 24px; margin-bottom: 8px;">{icon}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-label">{label}</div>
                <div style="font-size: 12px; margin-top: 6px; opacity: 0.8;">{change}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # Conversations
    st.markdown("### 💬 Live Conversations")

    conversations = [
        {"name": "Sarah Johnson", "email": "sarah@company.com", "channel": "Chat", "status": "Active", "messages": 8},
        {"name": "Mike Davis", "email": "mike@tech.com", "channel": "Call", "status": "Completed", "messages": 1},
        {"name": "Emma Wilson", "email": "emma@startup.io", "channel": "Chat", "status": "Resolved", "messages": 6},
    ]

    for conv in conversations:
        st.markdown(f"""
        <div class="fancy-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="flex: 1;">
                    <h4 style="margin: 0; color: #667eea;">{conv['name']}</h4>
                    <p style="margin: 4px 0 0 0; color: #666; font-size: 13px;">{conv['email']}</p>
                </div>
                <div style="text-align: right;">
                    <p style="margin: 0; font-weight: 600;">{conv['channel']} • {conv['messages']} msgs</p>
                    <p style="margin: 4px 0 0 0; color: #4caf50; font-weight: 600;">✓ {conv['status']}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# SETTINGS PAGE
# ============================================================================
def render_settings():
    col1, col2 = st.columns([1, 9])
    with col1:
        if st.button("←", key="back_settings"):
            st.session_state.current_page = 'home'
            st.rerun()
    with col2:
        st.markdown("### ⚙️ Settings")

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="fancy-card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<label class="form-label">🔗 API URL</label>')
        api_url = st.text_input("API URL", value="http://localhost:3000", label_visibility="collapsed")

        st.markdown('<label class="form-label">🔑 API Key</label>')
        api_key = st.text_input("API Key", type="password", placeholder="Enter your API key", label_visibility="collapsed")

    with col2:
        st.markdown('<label class="form-label">🎨 Theme</label>')
        theme = st.selectbox("Theme", ["Light", "Dark", "Auto"], label_visibility="collapsed")

        st.markdown('<label class="form-label">📬 Notifications</label>')
        notifications = st.checkbox("Enable notifications", value=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    if st.button("💾 Save Settings", use_container_width=True):
        st.success("✅ Settings saved successfully!")

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
    <p>Support Platform • Built with ❤️ for Convin AI • Made Beautiful</p>
</div>
""", unsafe_allow_html=True)
