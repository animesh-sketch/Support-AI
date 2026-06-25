import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
import base64

st.set_page_config(
    page_title="Anamika - Support Widget",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# ANAMIKA DESIGN SYSTEM - ENTERPRISE PREMIUM
# ============================================================================
st.markdown("""
<style>
    :root {
        --primary: #3b82f6;
        --secondary: #8b5cf6;
        --success: #22c55e;
        --warning: #f59e0b;
        --danger: #ef4444;
        --bg: #0f172a;
        --bg-secondary: #1e293b;
        --text: #f1f5f9;
        --text-muted: #94a3b8;
    }

    * { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; }

    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        color: var(--text);
    }

    .main { background: transparent; padding: 0; }

    h1 {
        font-size: 48px !important;
        font-weight: 800 !important;
        letter-spacing: -1px !important;
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
        transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    .premium-card:hover {
        border-color: rgba(59, 130, 246, 0.5);
        background: rgba(30, 41, 59, 0.9);
        box-shadow: 0 20px 50px rgba(59, 130, 246, 0.2);
        transform: translateY(-4px);
    }

    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 28px !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4) !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 30px rgba(59, 130, 246, 0.6) !important;
    }

    .premium-metric {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }

    .premium-metric:hover {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
        border-color: rgba(59, 130, 246, 0.5);
        transform: scale(1.05);
    }

    .metric-value { color: #3b82f6; font-size: 36px; font-weight: 900; margin: 12px 0; line-height: 1; }
    .metric-label { color: var(--text-muted); font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-change { color: #22c55e; font-size: 12px; font-weight: 700; margin-top: 8px; }

    .premium-divider { border: none; height: 1px; background: linear-gradient(90deg, transparent 0%, rgba(59, 130, 246, 0.3) 50%, transparent 100%); margin: 32px 0; }

    /* ANAMIKA WIDGET - TRULY FLOATING */
    .anamika-widget {
        position: fixed !important;
        bottom: 20px !important;
        right: 20px !important;
        z-index: 999999 !important;
        width: auto !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .anamika-button {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 70px !important;
        height: 70px !important;
        border-radius: 50% !important;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
        border: none !important;
        color: white !important;
        font-size: 32px !important;
        cursor: pointer !important;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.5) !important;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.320, 1) !important;
        position: relative !important;
    }

    .anamika-button:hover {
        transform: scale(1.15) !important;
        box-shadow: 0 12px 40px rgba(59, 130, 246, 0.7) !important;
    }

    .anamika-badge {
        position: absolute !important;
        top: -8px !important;
        right: -8px !important;
        background: #ef4444 !important;
        color: white !important;
        width: 28px !important;
        height: 28px !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 11px !important;
        font-weight: 900 !important;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.5) !important;
        z-index: 1000000 !important;
    }

    .anamika-menu {
        position: fixed !important;
        bottom: 100px !important;
        right: 20px !important;
        background: rgba(15, 23, 42, 0.98) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        min-width: 280px !important;
        backdrop-filter: blur(25px) !important;
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.8) !important;
        z-index: 999998 !important;
    }

    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        background: rgba(30, 41, 59, 0.8) !important;
        color: var(--text) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: transparent;
        border-bottom: 2px solid rgba(59, 130, 246, 0.1);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
    }
</style>

<!-- ANAMIKA FLOATING WIDGET HTML -->
<div id="anamika-widget-container" class="anamika-widget">
    <div id="anamika-button" class="anamika-button" style="cursor: pointer;">
        🎯
        <div class="anamika-badge" id="anamika-badge">3</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
if 'anamika_open' not in st.session_state:
    st.session_state.anamika_open = False
if 'admin_password' not in st.session_state:
    st.session_state.admin_password = False

# ============================================================================
# SAMPLE DATA
# ============================================================================
def generate_sample_data():
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=30, freq='D')
    return {
        'dates': dates,
        'conversations': np.random.randint(50, 150, 30),
        'chat_volume': np.random.randint(30, 100, 30),
        'calls': np.random.randint(10, 40, 30),
        'resolution_rate': np.random.randint(80, 98, 30),
        'csat': np.random.uniform(4.2, 4.9, 30),
    }

# ============================================================================
# DASHBOARD PAGE
# ============================================================================
def dashboard():
    st.markdown("""
    <div style="text-align: center; padding: 40px 20px; background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
                 border-radius: 20px; margin-bottom: 40px;">
        <h1>Anamika - Enterprise Support Widget</h1>
        <p style="color: var(--text-muted); font-size: 16px; margin-top: 12px;">
            🎯 Floating widget with Chat, Voice, KB & Admin Panel
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("💬 Chat", use_container_width=True):
            st.session_state.page = 'chat'
            st.rerun()
    with col2:
        if st.button("☎️ Voice Call", use_container_width=True):
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

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    # KPIs
    st.markdown("#### 📊 Real-time Metrics")
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    metrics = [
        (col1, "💬", "1,245", "Chats Today", "+12%"),
        (col2, "☎️", "312", "Calls Today", "+18%"),
        (col3, "✅", "94.2%", "Resolution", "+3.2%"),
        (col4, "😊", "4.87/5", "CSAT", "+0.15"),
        (col5, "🤖", "87%", "AI Contained", "+5%"),
        (col6, "⚡", "45s", "Avg Response", "-15s"),
    ]

    for col, icon, value, label, trend in metrics:
        with col:
            st.markdown(f"""
            <div class="premium-metric">
                <div style="font-size: 20px;">{icon}</div>
                <div class="metric-value" style="font-size: 28px;">{value}</div>
                <div class="metric-label">{label}</div>
                <div class="metric-change">{trend}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    # Charts
    st.markdown("#### 📈 Engagement Trends")
    col1, col2 = st.columns(2)

    data = generate_sample_data()

    with col1:
        st.markdown("**Total Conversations (30 days)**")
        fig = go.Figure(data=go.Scatter(x=data['dates'], y=data['conversations'], fill='tozeroy',
                                        line=dict(color='#3b82f6', width=3),
                                        marker=dict(size=8)))
        fig.update_layout(template='plotly_dark', height=300, margin=dict(l=0, r=0, t=0, b=0),
                         paper_bgcolor='rgba(30,41,59,0.5)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(148,163,184,0.1)'),
                         showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Chat vs Voice Split**")
        channels = ['Chat', 'Voice', 'Email']
        counts = [520, 240, 132]
        fig = go.Figure(data=go.Pie(labels=channels, values=counts,
                                     marker=dict(colors=['#3b82f6', '#8b5cf6', '#06b6d4']),
                                     textposition='inside', textinfo='label+percent'))
        fig.update_layout(template='plotly_dark', height=300, margin=dict(l=0, r=0, t=0, b=0),
                         paper_bgcolor='rgba(30,41,59,0.5)')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class="premium-card">
        <h4>🎯 Widget Status</h4>
        <p><strong>Name:</strong> Anamika - Enterprise Support Widget</p>
        <p><strong>Status:</strong> <span style="color: #22c55e;">✓ ACTIVE</span></p>
        <p><strong>Features:</strong> Chat • Voice • KB • Admin • Analytics</p>
        <p><strong>Location:</strong> Bottom-right corner (FLOATING)</p>
        <p style="color: var(--text-muted); font-size: 12px; margin-top: 16px;">👉 The floating widget is in the bottom-right corner. Click the 🎯 button to explore!</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# CHAT PAGE
# ============================================================================
def chat():
    st.markdown("### 💬 Chat with Anamika")
    st.markdown("""
    <div class="premium-card">
        <p style="color: var(--text-muted);">🤖 AI Agent powered by Claude • Response Time: <strong>45s</strong> • Accuracy: <strong>96.8%</strong></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="premium-card" style="height: 400px; overflow-y: auto; margin-bottom: 20px;">
        <div style="padding: 16px 0;">
            <div style="background: rgba(59, 130, 246, 0.2); padding: 12px 16px; border-radius: 10px; border-left: 3px solid #3b82f6; margin: 8px 0;">
                <p style="margin: 0;"><strong>You:</strong> How can I reset my password?</p>
            </div>
            <div style="background: rgba(34, 197, 94, 0.2); padding: 12px 16px; border-radius: 10px; border-left: 3px solid #22c55e; margin: 8px 0;">
                <p style="margin: 0;"><strong>Anamika:</strong> You can reset your password by clicking "Forgot Password" on the login page. We'll send a reset link to your email.</p>
            </div>
            <div style="background: rgba(59, 130, 246, 0.2); padding: 12px 16px; border-radius: 10px; border-left: 3px solid #3b82f6; margin: 8px 0;">
                <p style="margin: 0;"><strong>You:</strong> How long does it take?</p>
            </div>
            <div style="background: rgba(34, 197, 94, 0.2); padding: 12px 16px; border-radius: 10px; border-left: 3px solid #22c55e; margin: 8px 0;">
                <p style="margin: 0;"><strong>Anamika:</strong> You should receive the email within 2 minutes. If you don't see it, check your spam folder.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1])
    with col1:
        msg = st.text_input("Your message...", placeholder="Ask anything...", label_visibility="collapsed")
    with col2:
        if st.button("Send", use_container_width=True):
            if msg:
                st.success("✅ Message sent!")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("☎️ Talk to Agent", use_container_width=True):
            st.info("📞 Transferring to human agent...")
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
    st.markdown("### ☎️ Voice Call with Anamika")

    st.markdown("""
    <div class="premium-card">
        <p style="color: var(--text-muted);">🎧 Voice integration with Convin Sense • Crystal clear audio • Expert support</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.text_input("Your Name", placeholder="John Doe", label_visibility="collapsed")
        st.text_input("Email", placeholder="john@example.com", label_visibility="collapsed")

    with col2:
        st.text_input("Phone Number", placeholder="+1-555-123-4567", label_visibility="collapsed")
        st.selectbox("Best Time to Call", ["9 AM - 12 PM", "12 PM - 3 PM", "3 PM - 6 PM", "6 PM - 9 PM"], label_visibility="collapsed")

    if st.button("📞 Schedule Voice Call", use_container_width=True, key="schedule_call"):
        st.success("✅ Call scheduled! We'll call you within 2 minutes.")
        st.balloons()

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

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
    st.markdown("### 📊 Anamika Analytics Dashboard")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Overview", "💬 Chat Intelligence", "☎️ Voice Intelligence", "📚 KB Usage", "🎯 Agent Performance"])

    data = generate_sample_data()

    with tab1:
        st.markdown("#### Key Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Conversations", "3,847", "+15%")
        with col2:
            st.metric("Avg Resolution Time", "12m 30s", "-2m 15s")
        with col3:
            st.metric("Escalation Rate", "13%", "-2%")

        st.markdown("**Conversation Volume Trend**")
        fig = go.Figure(data=go.Bar(x=data['dates'], y=data['conversations'],
                                    marker=dict(color='#3b82f6')))
        fig.update_layout(template='plotly_dark', height=400, margin=dict(l=0, r=0, t=0, b=0),
                         paper_bgcolor='rgba(30,41,59,0.5)', plot_bgcolor='rgba(0,0,0,0)',
                         showlegend=False, xaxis=dict(showgrid=False))
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("#### Chat Performance")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Chat Messages", "1,245", "+12%")
        with col2:
            st.metric("First Response Time", "1m 45s", "-22s")
        with col3:
            st.metric("Chat CSAT", "4.87/5", "+0.15")

        st.markdown("**Chat Volume Trend**")
        fig = go.Figure(data=go.Scatter(x=data['dates'], y=data['chat_volume'], fill='tozeroy',
                                        line=dict(color='#3b82f6', width=3)))
        fig.update_layout(template='plotly_dark', height=300, margin=dict(l=0, r=0, t=0, b=0),
                         paper_bgcolor='rgba(30,41,59,0.5)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis=dict(showgrid=False), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.markdown("#### Voice Call Performance")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Calls", "312", "+18%")
        with col2:
            st.metric("Call Success Rate", "94.2%", "+3.2%")
        with col3:
            st.metric("Avg Call Duration", "8m 30s", "-20s")

        st.markdown("**Call Volume Trend**")
        fig = go.Figure(data=go.Scatter(x=data['dates'], y=data['calls'], mode='lines+markers',
                                        line=dict(color='#8b5cf6', width=3)))
        fig.update_layout(template='plotly_dark', height=300, margin=dict(l=0, r=0, t=0, b=0),
                         paper_bgcolor='rgba(30,41,59,0.5)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis=dict(showgrid=False), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.markdown("#### Knowledge Base Usage")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("KB Articles Used", "847", "+25%")
        with col2:
            st.metric("Deflection Rate", "62%", "+8%")
        with col3:
            st.metric("KB Hit Rate", "78%", "+12%")

        st.markdown("**Top Articles**")
        kb_data = pd.DataFrame({
            'Article': ['How to Reset Password', 'Billing & Subscriptions', 'Account Recovery', 'API Documentation', 'Troubleshooting'],
            'Views': [342, 298, 267, 198, 156]
        })
        fig = go.Figure(data=go.Barh(y=kb_data['Article'], x=kb_data['Views'],
                                     marker=dict(color='#22c55e')))
        fig.update_layout(template='plotly_dark', height=300, margin=dict(l=0, r=0, t=0, b=0),
                         paper_bgcolor='rgba(30,41,59,0.5)', plot_bgcolor='rgba(0,0,0,0)',
                         showlegend=False, xaxis=dict(showgrid=False))
        st.plotly_chart(fig, use_container_width=True)

    with tab5:
        st.markdown("#### Agent Performance")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avg Handling Time", "6m 45s", "-1m 15s")
        with col2:
            st.metric("Customer Satisfaction", "4.82/5", "+0.12")
        with col3:
            st.metric("First Contact Resolution", "87%", "+5%")

        agent_data = pd.DataFrame({
            'Agent': ['AI Bot', 'Agent Sarah', 'Agent Mike', 'Agent Lisa', 'Agent John'],
            'Resolved': [312, 125, 98, 87, 76],
            'CSAT': [4.8, 4.9, 4.7, 4.85, 4.75]
        })
        fig = go.Figure(data=go.Bar(x=agent_data['Agent'], y=agent_data['Resolved'],
                                    marker=dict(color='#3b82f6')))
        fig.update_layout(template='plotly_dark', height=300, margin=dict(l=0, r=0, t=0, b=0),
                         paper_bgcolor='rgba(30,41,59,0.5)', plot_bgcolor='rgba(0,0,0,0)',
                         showlegend=False, xaxis=dict(showgrid=False))
        st.plotly_chart(fig, use_container_width=True)

    if st.button("Back to Home", use_container_width=True):
        st.session_state.page = 'dashboard'
        st.rerun()

# ============================================================================
# ADMIN LOGIN
# ============================================================================
def admin_login():
    st.markdown("### 🔐 Admin Panel Login")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="premium-card" style="text-align: center;">
            <h3>🔐 Anamika Admin</h3>
            <p style="color: var(--text-muted);">Secure Access Required</p>
        </div>
        """, unsafe_allow_html=True)

        password = st.text_input("Admin Password", type="password", placeholder="Enter password")

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
    st.markdown("### ⚙️ Anamika Admin Panel")

    if not st.session_state.admin_password:
        st.warning("⚠️ Unauthorized access")
        if st.button("Go to Home"):
            st.session_state.page = 'dashboard'
            st.rerun()
        return

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📚 Knowledge Base", "🎤 Voice Config", "☎️ Agent Routing", "📏 Escalation Rules", "⏰ Business Hours", "🤖 Bot Controls"])

    with tab1:
        st.markdown("#### Knowledge Base Management")
        st.markdown("""
        <div class="premium-card">
            <p><strong>Upload Document</strong></p>
            <p style="color: var(--text-muted); font-size: 12px;">Supported: PDF, DOC, DOCX, TXT, CSV, XLS, XLSX, PPT, PPTX, URL</p>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'doc', 'docx', 'txt', 'csv', 'xls', 'xlsx', 'ppt', 'pptx'])
        if uploaded_file:
            st.success(f"✅ {uploaded_file.name} uploaded successfully!")

        url = st.text_input("Or paste a URL", placeholder="https://...")
        if st.button("Import from URL"):
            if url:
                st.success(f"✅ Content from {url} imported!")

        st.markdown("#### Existing KB Documents")
        kb_docs = pd.DataFrame({
            'Document': ['Password Reset Guide', 'Billing FAQ', 'API Docs', 'Troubleshooting'],
            'Type': ['PDF', 'DOCX', 'TXT', 'PDF'],
            'Size': ['2.3 MB', '1.8 MB', '456 KB', '3.2 MB'],
            'Status': ['Active', 'Active', 'Active', 'Active']
        })
        st.dataframe(kb_docs, use_container_width=True)

    with tab2:
        st.markdown("#### Voice Configuration (Convin Sense)")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Convin Workspace ID", placeholder="workspace_xyz")
            st.text_input("API Key", placeholder="sk-sense-...", type="password")
        with col2:
            st.toggle("Enable Inbound Calls", value=True)
            st.toggle("Enable Outbound Calls", value=True)

        st.markdown("**Voice Settings**")
        st.selectbox("Default Voice", ["Male (Professional)", "Female (Friendly)", "AI (Natural)"])
        st.slider("Speech Rate", 0.5, 2.0, 1.0)
        st.slider("Voice Confidence Threshold", 0, 100, 75)

        if st.button("Save Voice Configuration", use_container_width=True):
            st.success("✅ Voice configuration saved!")

    with tab3:
        st.markdown("#### Human Agent Routing")
        st.markdown("""
        <div class="premium-card">
            <p><strong>Configure escalation rules and agent assignment</strong></p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            agent_name = st.text_input("Agent Name", placeholder="John Doe")
            agent_email = st.text_input("Email", placeholder="john@company.com")
            agent_skills = st.multiselect("Skills", ["Billing", "Technical", "General", "Premium Support"])
        with col2:
            agent_phone = st.text_input("Phone", placeholder="+1-555-123-4567")
            agent_status = st.selectbox("Status", ["Available", "Busy", "Break", "Offline"])
            max_conversations = st.number_input("Max Concurrent Conversations", 1, 20, 5)

        if st.button("Add Agent", use_container_width=True):
            st.success(f"✅ Agent {agent_name} added!")

        st.markdown("**Existing Agents**")
        agents = pd.DataFrame({
            'Agent': ['Sarah Johnson', 'Mike Chen', 'Lisa Anderson', 'John Smith'],
            'Status': ['Available', 'Available', 'Break', 'Offline'],
            'Conversations': [3, 5, 0, 0],
            'Skills': ['Billing, General', 'Technical, Premium', 'General', 'All']
        })
        st.dataframe(agents, use_container_width=True)

    with tab4:
        st.markdown("#### Escalation Rules")
        col1, col2 = st.columns(2)
        with col1:
            trigger = st.selectbox("Trigger", ["Max attempts exceeded", "Low confidence", "Customer request", "Category match"])
            action = st.selectbox("Action", ["Escalate to agent", "Transfer to manager", "Send email", "Create ticket"])
        with col2:
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
            notify = st.multiselect("Notify", ["Email", "SMS", "In-app", "Slack"])

        if st.button("Create Escalation Rule", use_container_width=True):
            st.success("✅ Escalation rule created!")

    with tab5:
        st.markdown("#### Business Hours Configuration")
        col1, col2 = st.columns(2)
        with col1:
            st.time_input("Monday Start", value=None)
            st.time_input("Tuesday Start", value=None)
            st.time_input("Wednesday Start", value=None)
        with col2:
            st.time_input("Monday End", value=None)
            st.time_input("Tuesday End", value=None)
            st.time_input("Wednesday End", value=None)

        st.toggle("Enable 24/7 Support", value=False)
        st.text_area("After-hours Message", placeholder="We're currently offline. Please try again during business hours.")

        if st.button("Save Business Hours", use_container_width=True):
            st.success("✅ Business hours saved!")

    with tab6:
        st.markdown("#### Bot Behavior Controls")
        col1, col2 = st.columns(2)
        with col1:
            st.toggle("Use Knowledge Base", value=True)
            st.toggle("Enable Auto-escalation", value=True)
            st.toggle("Log Conversations", value=True)
            st.toggle("Enable Feedback", value=True)
        with col2:
            st.slider("Response Confidence Threshold (%)", 0, 100, 75)
            st.slider("Max Conversation Turns", 1, 50, 20)
            st.slider("Escalation Threshold (%)", 0, 100, 20)
            st.slider("Response Timeout (seconds)", 5, 120, 45)

        if st.button("Save Bot Settings", use_container_width=True):
            st.success("✅ Bot settings saved!")

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    if st.button("Logout", use_container_width=True):
        st.session_state.admin_password = False
        st.session_state.page = 'dashboard'
        st.rerun()

# ============================================================================
# MAIN APP
# ============================================================================
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
        🎯 Anamika Enterprise Support Widget | Powered by Convin AI | v2.0
    </p>
</div>
""", unsafe_allow_html=True)
