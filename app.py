import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(
    page_title="Anamika - Support Widget",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# ANAMIKA DESIGN SYSTEM - CLASSY & SMOOTH
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

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

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        letter-spacing: -0.3px;
    }

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
        transition: all 0.3s cubic-bezier(0.23, 1, 0.320, 1);
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
        transition: all 0.3s cubic-bezier(0.23, 1, 0.320, 1) !important;
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
        transition: all 0.3s cubic-bezier(0.23, 1, 0.320, 1);
    }

    .premium-metric:hover {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
        border-color: rgba(59, 130, 246, 0.5);
        transform: scale(1.05);
    }

    .metric-value { color: #3b82f6; font-size: 36px; font-weight: 800; margin: 12px 0; line-height: 1; }
    .metric-label { color: var(--text-muted); font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-change { color: #22c55e; font-size: 12px; font-weight: 700; margin-top: 8px; }

    .premium-divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, rgba(59, 130, 246, 0.3) 50%, transparent 100%);
        margin: 32px 0;
    }

    /* ============================================================================
    ANAMIKA WIDGET - CLASSY & SMOOTH - FIXED RIGHT CORNER
    ============================================================================ */

    #anamika-widget-container {
        position: fixed !important;
        top: 30px !important;
        right: 30px !important;
        z-index: 999999 !important;
        font-family: 'Inter', sans-serif !important;
        width: auto !important;
        height: auto !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    #anamika-widget {
        position: relative !important;
        z-index: 999999 !important;
        font-family: 'Inter', sans-serif !important;
    }

    .anamika-main-button {
        width: 70px !important;
        height: 70px !important;
        border-radius: 50% !important;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        font-size: 32px !important;
        cursor: pointer !important;
        box-shadow: 0 12px 32px rgba(59, 130, 246, 0.35),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        transition: all 0.35s cubic-bezier(0.23, 1, 0.320, 1) !important;
        position: relative !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        backdrop-filter: blur(10px) !important;
    }

    .anamika-main-button:hover {
        transform: scale(1.18) translateY(-3px) !important;
        box-shadow: 0 18px 48px rgba(59, 130, 246, 0.45),
                    inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    }

    .anamika-main-button:active {
        transform: scale(1.12) !important;
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
        box-shadow: 0 3px 12px rgba(239, 68, 68, 0.6),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        z-index: 1000000 !important;
        border: 2px solid rgba(15, 23, 42, 0.8) !important;
        animation: badge-pulse 2s ease-in-out infinite !important;
    }

    @keyframes badge-pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.12); }
    }

    /* Menu Container */
    #anamika-menu-container {
        position: fixed !important;
        bottom: 0 !important;
        right: 0 !important;
        left: 0 !important;
        top: 0 !important;
        z-index: 999998 !important;
        pointer-events: none !important;
    }

    .anamika-menu-backdrop {
        position: absolute !important;
        bottom: 0 !important;
        right: 0 !important;
        left: 0 !important;
        top: 0 !important;
        background: rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(4px) !important;
        pointer-events: auto !important;
        opacity: 0 !important;
        transition: opacity 0.35s cubic-bezier(0.23, 1, 0.320, 1) !important;
    }

    .anamika-menu-backdrop.open {
        opacity: 1 !important;
    }

    .anamika-menu {
        position: fixed !important;
        top: 100px !important;
        right: 20px !important;
        background: rgba(15, 23, 42, 0.95) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 20px !important;
        padding: 24px !important;
        min-width: 320px !important;
        backdrop-filter: blur(30px) !important;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.5),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        z-index: 999998 !important;
        pointer-events: auto !important;
        opacity: 0 !important;
        transform: translateY(-20px) scale(0.95) !important;
        transition: all 0.35s cubic-bezier(0.23, 1, 0.320, 1) !important;
    }

    .anamika-menu.open {
        opacity: 1 !important;
        transform: translateY(0) scale(1) !important;
    }

    .anamika-menu-header {
        margin-bottom: 20px !important;
        text-align: center !important;
    }

    .anamika-menu-header h3 {
        color: var(--text) !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        margin: 8px 0 !important;
        letter-spacing: -0.5px !important;
    }

    .anamika-menu-header p {
        color: var(--text-muted) !important;
        font-size: 13px !important;
        margin: 6px 0 0 0 !important;
    }

    .anamika-menu-options {
        display: flex !important;
        flex-direction: column !important;
        gap: 12px !important;
        margin-bottom: 16px !important;
    }

    .anamika-option {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.08) 100%) !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.320, 1) !important;
        color: var(--text) !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
    }

    .anamika-option:hover {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.15) 100%) !important;
        border-color: rgba(59, 130, 246, 0.4) !important;
        transform: translateX(6px) !important;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.15) !important;
    }

    .anamika-option-icon {
        font-size: 18px !important;
        min-width: 24px !important;
    }

    .anamika-option-label {
        flex: 1 !important;
    }

    .anamika-option-desc {
        color: var(--text-muted) !important;
        font-size: 12px !important;
        font-weight: 500 !important;
    }

    .anamika-menu-divider {
        height: 1px !important;
        background: linear-gradient(90deg, transparent 0%, rgba(59, 130, 246, 0.2) 50%, transparent 100%) !important;
        margin: 12px 0 !important;
    }

    .anamika-menu-footer {
        display: flex !important;
        gap: 8px !important;
    }

    .anamika-close-btn {
        flex: 1 !important;
        background: rgba(239, 68, 68, 0.15) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        color: #ef4444 !important;
        padding: 10px 14px !important;
        border-radius: 10px !important;
        cursor: pointer !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.320, 1) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }

    .anamika-close-btn:hover {
        background: rgba(239, 68, 68, 0.25) !important;
        border-color: rgba(239, 68, 68, 0.5) !important;
    }

    /* Smooth transitions */
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

    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        background: rgba(30, 41, 59, 0.8) !important;
        color: var(--text) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
    }
</style>

<!-- ANAMIKA FLOATING WIDGET - CLASSY & SMOOTH -->
<div id="anamika-widget">
    <div class="anamika-main-button" id="anamika-button">
        🎯
        <div class="anamika-badge" id="anamika-badge">3</div>
    </div>
</div>

<script>
    // Smooth widget interactions
    document.addEventListener('DOMContentLoaded', function() {
        const button = document.getElementById('anamika-button');
        const badge = document.getElementById('anamika-badge');

        if (button) {
            button.style.cursor = 'pointer';
            button.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
            });
        }
    });
</script>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
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
    }

# ============================================================================
# CLASSY WIDGET MENU - SIDEBAR STYLE
# ============================================================================
def render_anamika_menu():
    """Render the smooth, classy Anamika menu using columns"""

    # Create a floating menu UI
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.session_state.page != 'dashboard':
                st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

                st.markdown("""
                <div style="text-align: center; padding: 20px 0;">
                    <h3 style="margin: 0; color: #3b82f6;">✨ Anamika Menu</h3>
                    <p style="color: var(--text-muted); font-size: 13px; margin: 8px 0 0 0;">Select an option</p>
                </div>
                """, unsafe_allow_html=True)

                # Menu options with smooth styling
                menu_cols = st.columns(2, gap="small")

                with menu_cols[0]:
                    if st.button("💬 Chat", use_container_width=True, key="menu_chat"):
                        st.session_state.page = 'chat'
                        st.rerun()

                with menu_cols[1]:
                    if st.button("☎️ Voice", use_container_width=True, key="menu_voice"):
                        st.session_state.page = 'voice'
                        st.rerun()

                menu_cols2 = st.columns(2, gap="small")

                with menu_cols2[0]:
                    if st.button("📊 Analytics", use_container_width=True, key="menu_analytics"):
                        st.session_state.page = 'analytics'
                        st.rerun()

                with menu_cols2[1]:
                    if st.button("🔐 Admin", use_container_width=True, key="menu_admin"):
                        st.session_state.page = 'admin_login'
                        st.rerun()

                if st.button("🏠 Home", use_container_width=True, key="menu_home"):
                    st.session_state.page = 'dashboard'
                    st.rerun()

# ============================================================================
# DASHBOARD PAGE
# ============================================================================
def dashboard():
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px; background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
                 border-radius: 24px; margin-bottom: 40px;">
        <h1>🎯 Anamika</h1>
        <p style="color: var(--text-muted); font-size: 16px; margin-top: 12px; letter-spacing: -0.3px;">
            Enterprise Floating Support Widget
        </p>
        <p style="color: var(--text-muted); font-size: 13px; margin-top: 16px;">
            👉 Look for the <strong style="color: #3b82f6;">🎯 button in the bottom-right corner</strong> to get started
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Quick nav
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

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    # KPIs
    st.markdown("#### 📊 Real-time Status")
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
            st.markdown(f"""
            <div class="premium-metric">
                <div style="font-size: 20px;">{icon}</div>
                <div class="metric-value" style="font-size: 26px;">{value}</div>
                <div class="metric-label">{label}</div>
                <div class="metric-change">{trend}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    # Info
    st.markdown("""
    <div class="premium-card">
        <h4>✨ Widget Features</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 16px;">
            <div>
                <p><strong>💬 Smart Chat</strong><br><span style="color: var(--text-muted); font-size: 13px;">AI responses with human escalation</span></p>
            </div>
            <div>
                <p><strong>☎️ Voice Calls</strong><br><span style="color: var(--text-muted); font-size: 13px;">Schedule callbacks with the team</span></p>
            </div>
            <div>
                <p><strong>📚 Knowledge Base</strong><br><span style="color: var(--text-muted); font-size: 13px;">Admin-managed document library</span></p>
            </div>
            <div>
                <p><strong>📊 Analytics</strong><br><span style="color: var(--text-muted); font-size: 13px;">Real-time performance metrics</span></p>
            </div>
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

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    # Chat simulation
    st.markdown("""
    <div class="premium-card" style="height: 350px; overflow-y: auto; margin-bottom: 20px;">
        <div style="padding: 12px 0;">
            <div style="background: rgba(59, 130, 246, 0.2); padding: 12px 14px; border-radius: 10px; border-left: 3px solid #3b82f6; margin: 8px 0;">
                <p style="margin: 0; font-size: 13px;"><strong>You:</strong> How do I reset my password?</p>
            </div>
            <div style="background: rgba(34, 197, 94, 0.2); padding: 12px 14px; border-radius: 10px; border-left: 3px solid #22c55e; margin: 8px 0;">
                <p style="margin: 0; font-size: 13px;"><strong>Anamika:</strong> Click "Forgot Password" on login. We'll email you a reset link within 2 minutes.</p>
            </div>
            <div style="background: rgba(59, 130, 246, 0.2); padding: 12px 14px; border-radius: 10px; border-left: 3px solid #3b82f6; margin: 8px 0;">
                <p style="margin: 0; font-size: 13px;"><strong>You:</strong> What if I don't receive it?</p>
            </div>
            <div style="background: rgba(34, 197, 94, 0.2); padding: 12px 14px; border-radius: 10px; border-left: 3px solid #22c55e; margin: 8px 0;">
                <p style="margin: 0; font-size: 13px;"><strong>Anamika:</strong> Check your spam folder. If still missing, talk to an agent below. ↓</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([5, 1])
    with col1:
        st.text_input("Message...", placeholder="Type your question", label_visibility="collapsed")
    with col2:
        st.button("Send", use_container_width=True)

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
    st.markdown("### ☎️ Voice Call with Anamika")

    st.markdown("""
    <div class="premium-card">
        <p style="color: var(--text-muted);">🎧 Crystal-clear voice • Convin Sense powered • Expert support</p>
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
    st.markdown("### 📊 Anamika Analytics")

    tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "💬 Chat", "☎️ Voice", "🎯 Performance"])

    data = generate_sample_data()

    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Conversations", "3,847", "+15%")
        with col2:
            st.metric("Avg Resolution Time", "12m 30s", "-2m 15s")
        with col3:
            st.metric("Escalation Rate", "13%", "-2%")

        fig = go.Figure(data=go.Bar(x=data['dates'], y=data['conversations'],
                                    marker=dict(color='#3b82f6')))
        fig.update_layout(template='plotly_dark', height=350, margin=dict(l=0, r=0, t=0, b=0),
                         paper_bgcolor='rgba(30,41,59,0.5)', plot_bgcolor='rgba(0,0,0,0)',
                         showlegend=False, xaxis=dict(showgrid=False))
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Chat Messages", "1,245", "+12%")
        with col2:
            st.metric("Response Time", "1m 45s", "-22s")
        with col3:
            st.metric("Chat CSAT", "4.87/5", "+0.15")

        fig = go.Figure(data=go.Scatter(x=data['dates'], y=data['chat_volume'], fill='tozeroy',
                                        line=dict(color='#3b82f6', width=3)))
        fig.update_layout(template='plotly_dark', height=350, margin=dict(l=0, r=0, t=0, b=0),
                         paper_bgcolor='rgba(30,41,59,0.5)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis=dict(showgrid=False), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Calls", "312", "+18%")
        with col2:
            st.metric("Success Rate", "94.2%", "+3.2%")
        with col3:
            st.metric("Avg Duration", "8m 30s", "-20s")

        fig = go.Figure(data=go.Scatter(x=data['dates'], y=data['calls'], mode='lines+markers',
                                        line=dict(color='#8b5cf6', width=3)))
        fig.update_layout(template='plotly_dark', height=350, margin=dict(l=0, r=0, t=0, b=0),
                         paper_bgcolor='rgba(30,41,59,0.5)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis=dict(showgrid=False), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("AI Accuracy", "96.8%", "+1.2%")
        with col2:
            st.metric("Containment", "87%", "+5%")
        with col3:
            st.metric("First Contact", "78%", "+8%")
        with col4:
            st.metric("NPS Score", "72", "+6")

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

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
            <p style="color: var(--text-muted); font-size: 13px; margin: 8px 0 0 0;">Secure access required</p>
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
        st.toggle("Enable Inbound Calls", value=True)
        st.toggle("Enable Outbound Calls", value=True)
        if st.button("Save Voice Config", use_container_width=True):
            st.success("✅ Saved!")

    with tab3:
        st.markdown("#### Agent Management")
        st.text_input("Agent Name", placeholder="John Doe")
        st.text_input("Email", placeholder="john@company.com")
        st.selectbox("Status", ["Available", "Busy", "Break", "Offline"])
        if st.button("Add Agent", use_container_width=True):
            st.success("✅ Agent added!")

    with tab4:
        st.markdown("#### Escalation Rules")
        st.selectbox("Trigger", ["Max attempts", "Low confidence", "Customer request"])
        st.selectbox("Action", ["Escalate to agent", "Transfer to manager", "Create ticket"])
        if st.button("Create Rule", use_container_width=True):
            st.success("✅ Rule created!")

    with tab5:
        st.markdown("#### Business Hours")
        st.time_input("Start Time", value=None)
        st.time_input("End Time", value=None)
        st.toggle("24/7 Support", value=False)
        if st.button("Save Hours", use_container_width=True):
            st.success("✅ Saved!")

    with tab6:
        st.markdown("#### Bot Settings")
        st.toggle("Use Knowledge Base", value=True)
        st.toggle("Auto-escalation", value=True)
        st.slider("Confidence Threshold", 0, 100, 75)
        st.slider("Response Timeout (s)", 5, 120, 45)
        if st.button("Save Bot Settings", use_container_width=True):
            st.success("✅ Saved!")

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

# Sidebar menu
render_anamika_menu()

# Footer
st.markdown("""
<div style="text-align: center; padding: 40px 20px; margin-top: 60px; border-top: 1px solid rgba(59, 130, 246, 0.1);">
    <p style="color: var(--text-muted); font-size: 12px; margin: 0; letter-spacing: -0.3px;">
        🎯 Anamika Enterprise Widget | Powered by Convin AI | v3.0 Ultra Premium
    </p>
</div>
""", unsafe_allow_html=True)
