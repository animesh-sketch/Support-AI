import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json

# ============================================================================
# PAGE CONFIG & THEME
# ============================================================================
st.set_page_config(
    page_title="Convin AI Support Console",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# ENTERPRISE DESIGN SYSTEM
# ============================================================================
st.markdown("""
<style>
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    }

    /* Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
    }

    /* Main content */
    .main {
        background: transparent;
    }

    /* Headers */
    h1, h2, h3, h4, h5 {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
        letter-spacing: -0.5px;
    }

    /* Enterprise card */
    .enterprise-card {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px;
        padding: 24px;
        backdrop-filter: blur(10px);
        margin: 12px 0;
        transition: all 0.3s ease;
    }

    .enterprise-card:hover {
        border-color: rgba(148, 163, 184, 0.4);
        background: rgba(30, 41, 59, 0.95);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        padding: 10px 24px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.5) !important;
    }

    /* Metrics */
    .metric-card {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }

    .metric-value {
        color: #3b82f6;
        font-size: 28px;
        font-weight: 700;
        margin: 8px 0;
    }

    .metric-label {
        color: #94a3b8;
        font-size: 12px;
        font-weight: 500;
    }

    /* Chat */
    .chat-widget {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px;
        padding: 16px;
        height: 500px;
        overflow-y: auto;
    }

    .message {
        padding: 12px 16px;
        border-radius: 8px;
        margin: 8px 0;
        word-wrap: break-word;
    }

    .message-user {
        background: rgba(59, 130, 246, 0.2);
        border-left: 3px solid #3b82f6;
        margin-left: auto;
        max-width: 70%;
        color: #e2e8f0;
    }

    .message-agent {
        background: rgba(34, 197, 94, 0.1);
        border-left: 3px solid #22c55e;
        margin-right: auto;
        max-width: 70%;
        color: #e2e8f0;
    }

    /* Input */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: rgba(30, 41, 59, 0.8) !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 8px;
        padding: 12px 20px;
        border: 1px solid rgba(148, 163, 184, 0.2);
        color: #94a3b8;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
    }

    /* Status badges */
    .status-active {
        display: inline-block;
        width: 8px;
        height: 8px;
        background: #22c55e;
        border-radius: 50%;
        margin-right: 6px;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    /* Divider */
    .divider {
        border-top: 1px solid rgba(148, 163, 184, 0.2);
        margin: 24px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'

if 'kb_articles' not in st.session_state:
    st.session_state.kb_articles = [
        {'id': 1, 'title': 'Getting Started', 'category': 'Onboarding', 'content': 'How to set up your account...', 'version': 1, 'created': '2024-01-01'},
        {'id': 2, 'title': 'Pricing Plans', 'category': 'Billing', 'content': 'We offer Starter, Pro, and Enterprise plans...', 'version': 1, 'created': '2024-01-02'},
        {'id': 3, 'title': 'API Integration', 'category': 'Developer', 'content': 'REST API documentation and examples...', 'version': 2, 'created': '2024-01-03'},
    ]

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {'role': 'customer', 'message': 'What are your pricing plans?', 'time': '10:30 AM'},
        {'role': 'agent', 'message': 'We offer three plans: Starter ($99), Pro ($299), Enterprise (custom). KB-sourced answer.', 'time': '10:31 AM'},
    ]

# ============================================================================
# HEADER
# ============================================================================
def render_header():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="margin: 0; font-size: 32px; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                🚀 Convin AI Support Console
            </h1>
            <p style="margin: 8px 0 0 0; color: #94a3b8; font-size: 13px;">
                Enterprise-Grade Support Platform
            </p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# DASHBOARD PAGE
# ============================================================================
def render_dashboard():
    st.markdown("### 📊 Executive Dashboard")

    # Global filters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        date_range = st.selectbox("📅 Date Range", ["Today", "Last 7 Days", "Last 30 Days", "Custom"])
    with col2:
        team_filter = st.selectbox("👥 Team", ["All Teams", "Support", "Sales", "Technical"])
    with col3:
        channel_filter = st.selectbox("📱 Channel", ["All", "Chat", "Voice", "Email"])
    with col4:
        product_filter = st.selectbox("🏢 Product", ["All Products", "Product A", "Product B"])

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # KPIs
    col1, col2, col3, col4, col5 = st.columns(5)

    kpis = [
        (col1, "💬", "156", "Total Chats", "-2%"),
        (col2, "✅", "89%", "Resolution Rate", "+5%"),
        (col3, "☎️", "48", "Voice Calls", "+12%"),
        (col4, "⏱️", "2m 15s", "Avg Response", "-30s"),
        (col5, "😊", "4.8/5", "CSAT", "+0.2"),
    ]

    for col, icon, value, label, change in kpis:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 20px;">{icon}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-label">{label}</div>
                <div style="color: #22c55e; font-size: 11px; margin-top: 4px;">{change}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📈 Chat Volume (7 Days)")
        dates = pd.date_range(start=datetime.now() - timedelta(days=7), periods=7, freq='D')
        chats = [12, 15, 18, 22, 19, 25, 28]

        fig = go.Figure(data=go.Scatter(x=dates, y=chats, fill='tozeroy', mode='lines+markers',
                                        line=dict(color='#3b82f6', width=3),
                                        marker=dict(size=8, color='#2563eb')))
        fig.update_layout(template='plotly_dark', height=300, margin=dict(l=0, r=0, t=0, b=0),
                         paper_bgcolor='rgba(30,41,59,0.5)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(148,163,184,0.1)'))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 📊 Channel Distribution")
        channels = ['Chat', 'Voice', 'Email']
        counts = [156, 48, 32]

        fig = go.Figure(data=go.Pie(labels=channels, values=counts,
                                     marker=dict(colors=['#3b82f6', '#2563eb', '#1e40af'])))
        fig.update_layout(template='plotly_dark', height=300, margin=dict(l=0, r=0, t=0, b=0),
                         paper_bgcolor='rgba(30,41,59,0.5)', textinfo='label+percent')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Live conversations
    st.markdown("#### 💬 Live Conversations")

    conversations = [
        {"customer": "Sarah Johnson", "channel": "Chat", "status": "Active", "duration": "5 min", "intent": "Pricing"},
        {"customer": "Mike Davis", "channel": "Voice", "status": "In Progress", "duration": "12 min", "intent": "Technical Support"},
        {"customer": "Emma Wilson", "channel": "Chat", "status": "Resolved", "duration": "8 min", "intent": "Account"},
    ]

    for conv in conversations:
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        with col1:
            st.markdown(f"**{conv['customer']}**")
            st.caption(conv['intent'])
        with col2:
            st.markdown(f"{conv['channel']}")
        with col3:
            st.markdown(f"⏱️ {conv['duration']}")
        with col4:
            status_badge = "🟢" if conv['status'] == "Active" else "🟡" if conv['status'] == "In Progress" else "⚪"
            st.markdown(f"{status_badge} {conv['status']}")
        st.divider()

# ============================================================================
# CHAT PAGE
# ============================================================================
def render_chat():
    st.markdown("### 💬 AI Chat Support")

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**Agent Status:** <span class='status-active'></span> Online & Ready", unsafe_allow_html=True)
    with col2:
        if st.button("Request Agent", use_container_width=True):
            st.info("📞 Escalating to human agent...")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Chat widget
    st.markdown('<div class="chat-widget">', unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        if msg['role'] == 'customer':
            st.markdown(f"""
            <div class="message message-user">
                <strong>You:</strong> {msg['message']}<br>
                <small style="opacity: 0.7;">{msg['time']}</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message message-agent">
                <strong>🤖 AI Agent:</strong> {msg['message']}<br>
                <small style="opacity: 0.7;">{msg['time']} • KB-Sourced</small>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Input
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("Type your message...", placeholder="Ask anything about our products", label_visibility="collapsed")
    with col2:
        if st.button("Send", use_container_width=True):
            if user_input:
                st.session_state.chat_history.append({'role': 'customer', 'message': user_input, 'time': datetime.now().strftime("%I:%M %p")})
                st.session_state.chat_history.append({'role': 'agent', 'message': f'✅ Found in KB: {user_input[:30]}...', 'time': datetime.now().strftime("%I:%M %p")})
                st.rerun()

    # Quick actions
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("☎️ Talk to Agent"):
            st.info("📞 Convin Sense: Transferring to agent with full context...")
    with col2:
        if st.button("📞 Request Callback"):
            st.success("✅ Callback scheduled for next available agent")
    with col3:
        if st.button("📚 Browse KB"):
            st.session_state.current_page = 'kb'
            st.rerun()

# ============================================================================
# VOICE ANALYTICS
# ============================================================================
def render_voice_analytics():
    st.markdown("### ☎️ Voice Bot Analytics")

    col1, col2, col3, col4, col5 = st.columns(5)

    voice_metrics = [
        (col1, "☎️", "248", "Total Calls", "-5%"),
        (col2, "✅", "196", "Connected", "+8%"),
        (col3, "❌", "52", "Failed", "-12%"),
        (col4, "86%", "Success Rate", "+3%"),
        (col5, "8m 30s", "Avg Duration", "+45s"),
    ]

    for col, icon, value, label, change in voice_metrics:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 18px;">{icon}</div>
                <div class="metric-value" style="font-size: 20px;">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Intent Distribution")
        intents = ['Billing', 'Technical', 'General', 'Escalation']
        counts = [85, 78, 52, 33]

        fig = go.Figure(data=go.Bar(x=intents, y=counts, marker=dict(color='#3b82f6')))
        fig.update_layout(template='plotly_dark', height=300, margin=dict(l=0, r=0, t=0, b=0),
                         paper_bgcolor='rgba(30,41,59,0.5)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Resolution Metrics")
        metrics = {
            'Bot Containment': '78%',
            'Escalation Rate': '22%',
            'First Call Resolution': '72%',
            'STT Accuracy': '96.2%',
            'TTS Quality': '4.5/5',
            'Response Latency': '1.2s'
        }

        for key, value in metrics.items():
            st.markdown(f"**{key}:** `{value}`")

# ============================================================================
# CHAT ANALYTICS
# ============================================================================
def render_chat_analytics():
    st.markdown("### 💬 Chat Analytics")

    col1, col2, col3, col4, col5 = st.columns(5)

    chat_metrics = [
        (col1, "💬", "156", "Total Chats", "+12%"),
        (col2, "✅", "139", "Resolved", "+15%"),
        (col3, "⏳", "17", "Unresolved", "-8%"),
        (col4, "89%", "Containment", "+5%"),
        (col5, "2m 15s", "Avg Response", "-30s"),
    ]

    for col, icon, value, label, change in chat_metrics:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 18px;">{icon}</div>
                <div class="metric-value" style="font-size: 20px;">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### KB Usage & Topics")
        topics = {
            'Billing': '45 chats',
            'Technical': '38 chats',
            'Account': '32 chats',
            'General': '28 chats',
            'Other': '13 chats',
        }

        for topic, count in topics.items():
            st.markdown(f"📚 **{topic}**: {count}")

    with col2:
        st.markdown("#### Performance Indicators")
        indicators = {
            'First Response Time': '2m 15s ✅',
            'Resolution Time': '8m 45s ✅',
            'SLA Compliance': '96% ✅',
            'Repeat Query Rate': '12% ⚠️',
            'Hallucination Rate': '0.8% ✅',
            'Agent Performance': '4.7/5 ✅',
        }

        for indicator, value in indicators.items():
            st.markdown(f"**{indicator}**: {value}")

# ============================================================================
# KNOWLEDGE BASE (ADMIN)
# ============================================================================
def render_kb():
    st.markdown("### 📚 Knowledge Base Management")

    tab1, tab2, tab3 = st.tabs(["Browse Articles", "Create/Edit", "Analytics"])

    with tab1:
        st.markdown("#### Existing Articles")
        search = st.text_input("🔍 Search KB...", placeholder="Search articles")

        for article in st.session_state.kb_articles:
            if not search or search.lower() in article['title'].lower():
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                with col1:
                    st.markdown(f"**{article['title']}**")
                    st.caption(f"Category: {article['category']}")
                with col2:
                    st.markdown(f"v{article['version']}")
                with col3:
                    st.markdown(f"{article['created']}")
                with col4:
                    if st.button("Edit", key=f"edit_{article['id']}"):
                        st.info(f"Editing: {article['title']}")
                st.divider()

    with tab2:
        st.markdown("#### Create New Article")
        col1, col2 = st.columns(2)

        with col1:
            new_title = st.text_input("Article Title")
            new_category = st.selectbox("Category", ["Onboarding", "Billing", "Developer", "Technical", "Account"])

        with col2:
            new_content = st.text_area("Content", height=150, placeholder="Write your article...")

        if st.button("📤 Create Article", use_container_width=True):
            if new_title and new_content:
                st.success(f"✅ Article '{new_title}' created!")

    with tab3:
        st.markdown("#### KB Analytics")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Most Used Articles:**")
            for i, article in enumerate(st.session_state.kb_articles[:3], 1):
                st.markdown(f"{i}. **{article['title']}** - {50-i*10} references")

        with col2:
            st.markdown("**Knowledge Gaps:**")
            gaps = ["Refund Process (15 queries)", "API Rate Limits (12 queries)", "Integration Guide (8 queries)"]
            for gap in gaps:
                st.markdown(f"⚠️ {gap}")

# ============================================================================
# SETTINGS (ADMIN)
# ============================================================================
def render_settings():
    st.markdown("### ⚙️ Admin Settings")

    tab1, tab2, tab3 = st.tabs(["API Configuration", "Integrations", "Team"])

    with tab1:
        st.markdown("#### Convin Sense Setup")
        col1, col2 = st.columns(2)

        with col1:
            api_key = st.text_input("Convin API Key", type="password", placeholder="Enter API key")
            phone_pool = st.text_input("Phone Pool", value="+1-800-SUPPORT")

        with col2:
            skill_routing = st.checkbox("Enable Skill-Based Routing", value=True)
            priority_routing = st.checkbox("Enable Priority Routing", value=True)
            queue_management = st.checkbox("Enable Queue Management", value=True)

        if st.button("💾 Save Configuration"):
            st.success("✅ Configuration saved!")

    with tab2:
        st.markdown("#### Active Integrations")
        integrations = [
            {"name": "Slack", "status": "Connected", "icon": "✅"},
            {"name": "Salesforce", "status": "Connected", "icon": "✅"},
            {"name": "Zendesk", "status": "Pending", "icon": "⏳"},
            {"name": "Jira", "status": "Not Connected", "icon": "❌"},
        ]

        for integration in integrations:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"**{integration['name']}**")
            with col2:
                st.markdown(integration['status'])
            with col3:
                st.markdown(integration['icon'])

    with tab3:
        st.markdown("#### Team Management")
        team = pd.DataFrame({
            'Name': ['Alice Johnson', 'Bob Smith', 'Carol White'],
            'Role': ['Admin', 'Supervisor', 'Agent'],
            'Status': ['🟢 Online', '🟡 Away', '🟢 Online'],
            'Chats': [0, 5, 12],
        })
        st.dataframe(team, use_container_width=True, hide_index=True)

# ============================================================================
# NAVIGATION
# ============================================================================
render_header()

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Navigation buttons
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_col6 = st.columns(6)

with nav_col1:
    if st.button("📊 Dashboard", use_container_width=True):
        st.session_state.current_page = 'dashboard'
        st.rerun()

with nav_col2:
    if st.button("💬 Chat", use_container_width=True):
        st.session_state.current_page = 'chat'
        st.rerun()

with nav_col3:
    if st.button("☎️ Voice", use_container_width=True):
        st.session_state.current_page = 'voice'
        st.rerun()

with nav_col4:
    if st.button("📈 Chat Analytics", use_container_width=True):
        st.session_state.current_page = 'chat_analytics'
        st.rerun()

with nav_col5:
    if st.button("📚 KB", use_container_width=True):
        st.session_state.current_page = 'kb'
        st.rerun()

with nav_col6:
    if st.button("⚙️ Settings", use_container_width=True):
        st.session_state.current_page = 'settings'
        st.rerun()

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============================================================================
# RENDER PAGES
# ============================================================================
if st.session_state.current_page == 'dashboard':
    render_dashboard()
elif st.session_state.current_page == 'chat':
    render_chat()
elif st.session_state.current_page == 'voice':
    render_voice_analytics()
elif st.session_state.current_page == 'chat_analytics':
    render_chat_analytics()
elif st.session_state.current_page == 'kb':
    render_kb()
elif st.session_state.current_page == 'settings':
    render_settings()

# Footer
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 12px; padding: 20px 0;">
    <p>🚀 Convin AI Support Console v1.0 • Enterprise-Grade Support Platform</p>
</div>
""", unsafe_allow_html=True)
