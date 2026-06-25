import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# ============================================================================
# PREMIUM PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Convin AI Support Console",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# ULTRA-PREMIUM DESIGN SYSTEM
# ============================================================================
st.markdown("""
<style>
    /* Root colors */
    :root {
        --primary: #3b82f6;
        --primary-dark: #1e40af;
        --secondary: #8b5cf6;
        --success: #22c55e;
        --warning: #f59e0b;
        --danger: #ef4444;
        --bg: #0f172a;
        --bg-secondary: #1e293b;
        --text: #f1f5f9;
        --text-muted: #94a3b8;
    }

    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        color: var(--text);
    }

    /* Main container */
    .main {
        background: transparent;
        padding: 0;
    }

    /* Typography */
    h1 {
        font-size: 48px !important;
        font-weight: 800 !important;
        letter-spacing: -1px !important;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    h2, h3, h4, h5 {
        color: var(--text) !important;
        font-weight: 700 !important;
    }

    /* Premium cards */
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

    /* Premium buttons */
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

    .stButton > button:active {
        transform: translateY(-1px) !important;
    }

    /* Premium metrics */
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

    .metric-value {
        color: #3b82f6;
        font-size: 36px;
        font-weight: 900;
        margin: 12px 0;
        line-height: 1;
    }

    .metric-label {
        color: var(--text-muted);
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .metric-change {
        color: #22c55e;
        font-size: 12px;
        font-weight: 700;
        margin-top: 8px;
    }

    /* Premium divider */
    .premium-divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, rgba(59, 130, 246, 0.3) 50%, transparent 100%);
        margin: 32px 0;
    }

    /* Premium tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: transparent;
        border-bottom: 2px solid rgba(59, 130, 246, 0.1);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 10px;
        padding: 12px 24px;
        color: var(--text-muted);
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
    }

    /* Floating widget */
    .floating-widget {
        position: fixed !important;
        bottom: 20px !important;
        right: 20px !important;
        z-index: 99999 !important;
    }

    .widget-button {
        width: 70px !important;
        height: 70px !important;
        border-radius: 50% !important;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
        border: none !important;
        color: white !important;
        font-size: 32px !important;
        cursor: pointer !important;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4) !important;
        transition: all 0.3s ease !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    .widget-button:hover {
        transform: scale(1.12) !important;
        box-shadow: 0 12px 35px rgba(59, 130, 246, 0.6) !important;
    }

    .widget-menu {
        background: rgba(15, 23, 42, 0.98) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 14px !important;
        padding: 20px !important;
        min-width: 240px !important;
        backdrop-filter: blur(25px) !important;
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.6) !important;
        margin-bottom: 12px !important;
    }

    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .badge-green { background: rgba(34, 197, 94, 0.2); color: #22c55e; }
    .badge-amber { background: rgba(245, 158, 11, 0.2); color: #f59e0b; }
    .badge-red { background: rgba(239, 68, 68, 0.2); color: #ef4444; }

    /* Input styling */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        background: rgba(30, 41, 59, 0.8) !important;
        color: var(--text) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
    }

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'widget_open' not in st.session_state:
    st.session_state.widget_open = False

# ============================================================================
# FLOATING WIDGET
# ============================================================================
def render_widget():
    if st.session_state.widget_open:
        st.markdown("""
        <div class="floating-widget">
            <div class="widget-menu">
                <h4 style="margin: 0 0 16px 0; color: var(--text); font-size: 16px; font-weight: 700;">
                    🚀 How can we help?
                </h4>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2, gap="small")
        with col1:
            if st.button("💬 Chat", key="w_chat", use_container_width=True):
                st.session_state.page = 'chat'
                st.rerun()
        with col2:
            if st.button("☎️ Call", key="w_call", use_container_width=True):
                st.session_state.page = 'call'
                st.rerun()

        st.markdown("</div></div>", unsafe_allow_html=True)

        if st.button("✕ Close", key="w_close", use_container_width=True):
            st.session_state.widget_open = False
            st.rerun()
    else:
        st.markdown("""
        <div class="floating-widget">
            <div style="position: relative; display: inline-block; width: 70px;">
                <div style="position: absolute; top: -8px; right: -8px; background: #ef4444; color: white;
                            width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center;
                            justify-content: center; font-size: 12px; font-weight: 700;
                            box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4); z-index: 10;">3</div>
        """, unsafe_allow_html=True)

        if st.button("💬", key="w_open", help="Open Support Widget"):
            st.session_state.widget_open = True
            st.rerun()

        st.markdown("</div></div>", unsafe_allow_html=True)

# ============================================================================
# HOME PAGE
# ============================================================================
def home():
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px; background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
                 border-radius: 20px; margin-bottom: 40px;">
        <h1>Convin AI Support Console</h1>
        <p style="color: var(--text-muted); font-size: 18px; margin-top: 12px;">
            Enterprise-Grade Support Platform with AI Intelligence
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    # Main action cards
    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown("""
        <div class="premium-card" style="text-align: center;">
            <div style="font-size: 48px; margin-bottom: 16px;">💬</div>
            <h3 style="margin: 0 0 8px 0;">Chat Support</h3>
            <p style="color: var(--text-muted); margin: 0;">AI-powered instant answers</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Chat", key="home_chat", use_container_width=True):
            st.session_state.page = 'chat'
            st.rerun()

    with col2:
        st.markdown("""
        <div class="premium-card" style="text-align: center;">
            <div style="font-size: 48px; margin-bottom: 16px;">☎️</div>
            <h3 style="margin: 0 0 8px 0;">Voice Call</h3>
            <p style="color: var(--text-muted); margin: 0;">Direct support calls</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Schedule Call", key="home_call", use_container_width=True):
            st.session_state.page = 'call'
            st.rerun()

    with col3:
        st.markdown("""
        <div class="premium-card" style="text-align: center;">
            <div style="font-size: 48px; margin-bottom: 16px;">📊</div>
            <h3 style="margin: 0 0 8px 0;">Analytics</h3>
            <p style="color: var(--text-muted); margin: 0;">Real-time insights</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Dashboard", key="home_dash", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    # Stats
    col1, col2, col3, col4 = st.columns(4, gap="medium")

    stats = [
        ("💬", "892", "Total Tickets", "+15%"),
        ("✅", "94.2%", "Resolution Rate", "+3.2%"),
        ("⚡", "1m 45s", "Avg Response", "-22s"),
        ("😊", "4.87/5", "CSAT Score", "+0.15"),
    ]

    for col, icon, value, label, trend in zip([col1, col2, col3, col4], stats):
        with col:
            st.markdown(f"""
            <div class="premium-metric">
                <div style="font-size: 24px;">{icon}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-label">{label}</div>
                <div class="metric-change">{trend}</div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# CHAT PAGE
# ============================================================================
def chat():
    st.markdown("### 💬 AI Chat Support")
    st.markdown("""
    <div class="premium-card">
        <p style="color: var(--text-muted);">🤖 <strong>AI Agent</strong> • Response Time: <strong>1m 45s</strong> • Confidence: <strong>96.8%</strong></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    # Chat messages
    st.markdown("""
    <div class="premium-card" style="height: 400px; overflow-y: auto;">
        <div style="padding: 16px 0;">
            <div style="background: rgba(59, 130, 246, 0.2); padding: 12px 16px; border-radius: 10px; border-left: 3px solid #3b82f6; margin: 8px 0;">
                <p style="margin: 0;"><strong>You:</strong> What are your pricing plans?</p>
            </div>
            <div style="background: rgba(34, 197, 94, 0.2); padding: 12px 16px; border-radius: 10px; border-left: 3px solid #22c55e; margin: 8px 0;">
                <p style="margin: 0;"><strong>AI Agent:</strong> We offer Starter ($99), Pro ($299), and Enterprise (custom) plans.</p>
            </div>
            <div style="background: rgba(59, 130, 246, 0.2); padding: 12px 16px; border-radius: 10px; border-left: 3px solid #3b82f6; margin: 8px 0;">
                <p style="margin: 0;"><strong>You:</strong> Which is best for 20 people?</p>
            </div>
            <div style="background: rgba(34, 197, 94, 0.2); padding: 12px 16px; border-radius: 10px; border-left: 3px solid #22c55e; margin: 8px 0;">
                <p style="margin: 0;"><strong>AI Agent:</strong> Pro plan is ideal for your team size at $299/month.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

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
        if st.button("📞 Request Callback", use_container_width=True):
            st.success("✅ Callback scheduled")
    with col3:
        if st.button("Home", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()

# ============================================================================
# DASHBOARD PAGE
# ============================================================================
def dashboard():
    st.markdown("### 📊 Analytics Dashboard")

    # Filters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.selectbox("Period", ["Today", "7D", "30D", "90D"], label_visibility="collapsed")
    with col2:
        st.selectbox("Team", ["All", "Support", "Sales", "Technical"], label_visibility="collapsed")
    with col3:
        st.selectbox("Channel", ["All", "Chat", "Voice", "Email"], label_visibility="collapsed")
    with col4:
        st.selectbox("Status", ["All", "Resolved", "Pending", "Escalated"], label_visibility="collapsed")

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    # KPIs
    col1, col2, col3, col4, col5, col6 = st.columns(6, gap="small")

    kpis = [
        (col1, "💬", "892", "Tickets", "+15%"),
        (col2, "✅", "94.2%", "Resolved", "+3.2%"),
        (col3, "⚡", "1m 45s", "Response", "-22s"),
        (col4, "😊", "4.87/5", "CSAT", "+0.15"),
        (col5, "🤖", "87%", "AI Contained", "+5%"),
        (col6, "☎️", "312", "Calls", "+18%"),
    ]

    for col, icon, value, label, trend in kpis:
        with col:
            st.markdown(f"""
            <div class="premium-metric">
                <div style="font-size: 20px;">{icon}</div>
                <div class="metric-value" style="font-size: 24px;">{value}</div>
                <div class="metric-label">{label}</div>
                <div class="metric-change">{trend}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📈 Chat Volume Trend")
        dates = pd.date_range(start=datetime.now() - timedelta(days=7), periods=7, freq='D')
        chats = [12, 15, 18, 22, 19, 25, 28]

        fig = go.Figure(data=go.Scatter(x=dates, y=chats, fill='tozeroy',
                                        line=dict(color='#3b82f6', width=3),
                                        marker=dict(size=8)))
        fig.update_layout(template='plotly_dark', height=300, margin=dict(l=0, r=0, t=0, b=0),
                         paper_bgcolor='rgba(30,41,59,0.5)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(148,163,184,0.1)'))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 📊 Channel Distribution")
        channels = ['Chat', 'Voice', 'Email']
        counts = [156, 48, 32]

        fig = go.Figure(data=go.Pie(labels=channels, values=counts,
                                     marker=dict(colors=['#3b82f6', '#8b5cf6', '#06b6d4'])))
        fig.update_layout(template='plotly_dark', height=300, margin=dict(l=0, r=0, t=0, b=0),
                         paper_bgcolor='rgba(30,41,59,0.5)')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    if st.button("Home", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()

# ============================================================================
# CALL PAGE
# ============================================================================
def call():
    st.markdown("### ☎️ Schedule a Call")

    st.markdown("""
    <div class="premium-card">
        <p style="color: var(--text-muted);">Connect with our support team for dedicated assistance</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.text_input("Your Name", placeholder="John Doe")
        st.text_input("Email", placeholder="john@example.com")

    with col2:
        st.text_input("Phone Number", placeholder="+1-555-123-4567")
        st.selectbox("Best Time", ["9 AM - 12 PM", "12 PM - 3 PM", "3 PM - 6 PM", "6 PM - 9 PM"])

    if st.button("📞 Schedule Call Now", use_container_width=True):
        st.success("✅ Call scheduled! We'll call you soon.")
        st.balloons()

    st.markdown('<div class="premium-divider"></div>', unsafe_enable_html=True)

    if st.button("Home", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()

# ============================================================================
# MAIN APP
# ============================================================================
render_widget()

# Navigation
if st.session_state.page == 'home':
    home()
elif st.session_state.page == 'chat':
    chat()
elif st.session_state.page == 'dashboard':
    dashboard()
elif st.session_state.page == 'call':
    call()

# Footer
st.markdown("""
<div style="text-align: center; padding: 40px 20px; margin-top: 60px; border-top: 1px solid rgba(59, 130, 246, 0.1);">
    <p style="color: var(--text-muted); font-size: 12px; margin: 0;">
        🚀 Convin AI Support Console | Enterprise Intelligence Platform
    </p>
</div>
""", unsafe_allow_html=True)
