import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import random

# ============================================================================
# ADVANCED PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Convin AI Support Console - Advanced",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# ADVANCED ENTERPRISE DESIGN
# ============================================================================
st.markdown("""
<style>
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
    }

    .main { background: transparent; }

    h1, h2, h3, h4, h5 {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
        letter-spacing: -0.5px;
    }

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

    .status-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }

    .status-active { background: #22c55e; color: white; }
    .status-warning { background: #f59e0b; color: white; }
    .status-critical { background: #ef4444; color: white; }

    .divider {
        border-top: 1px solid rgba(148, 163, 184, 0.2);
        margin: 24px 0;
    }

    /* Advanced widget */
    .floating-widget {
        position: fixed !important;
        bottom: 20px !important;
        right: 20px !important;
        z-index: 99999 !important;
    }

    .widget-menu {
        background: rgba(15, 23, 42, 0.98) !important;
        border: 1px solid rgba(148, 163, 184, 0.3) !important;
        border-radius: 12px !important;
        padding: 16px !important;
        min-width: 220px !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5) !important;
        margin-bottom: 12px !important;
    }

    .widget-badge {
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
        font-size: 12px !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# ADVANCED SESSION STATE
# ============================================================================
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'advanced_dashboard'

if 'widget_open' not in st.session_state:
    st.session_state.widget_open = False

# Advanced KB with AI
if 'advanced_kb' not in st.session_state:
    st.session_state.advanced_kb = [
        {'id': 1, 'title': 'Getting Started', 'category': 'Onboarding', 'content': 'Step-by-step setup guide...', 'version': 3, 'status': 'published', 'views': 1250, 'helpful': 94},
        {'id': 2, 'title': 'API Integration', 'category': 'Developer', 'content': 'REST API documentation...', 'version': 5, 'status': 'published', 'views': 890, 'helpful': 97},
        {'id': 3, 'title': 'Billing FAQ', 'category': 'Billing', 'content': 'Payment & subscription info...', 'version': 2, 'status': 'draft', 'views': 340, 'helpful': 91},
    ]

# ============================================================================
# ADVANCED FLOATING WIDGET
# ============================================================================
def render_advanced_widget():
    if st.session_state.widget_open:
        st.markdown("""
        <div class="floating-widget">
            <div class="widget-menu" style="display: block;">
                <h4 style="margin: 0 0 12px 0; color: #f1f5f9; font-size: 14px; font-weight: 600;">
                    🚀 How can we help?
                </h4>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2, gap="small")
        with col1:
            if st.button("💬 Chat", key="adv_chat", use_container_width=True):
                st.session_state.current_page = 'advanced_chat'
                st.session_state.widget_open = False
                st.rerun()

        with col2:
            if st.button("☎️ Call", key="adv_call", use_container_width=True):
                st.session_state.widget_open = False
                st.rerun()

        st.markdown("""
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Close", key="adv_close", use_container_width=True):
            st.session_state.widget_open = False
            st.rerun()
    else:
        st.markdown("""
        <div class="floating-widget">
            <div style="text-align: center;">
                <div style="position: relative; display: inline-block;">
                    <span class="widget-badge">3</span>
        """, unsafe_allow_html=True)

        if st.button("💬", key="adv_open_widget"):
            st.session_state.widget_open = True
            st.rerun()

        st.markdown("""
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# ADVANCED DASHBOARD
# ============================================================================
def render_advanced_dashboard():
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="font-size: 32px; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🚀 Convin AI Support Console - ADVANCED
        </h1>
        <p style="color: #94a3b8; margin-top: 8px;">Enterprise Intelligence Platform</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Advanced Filters
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        date_range = st.selectbox("📅 Period", ["Today", "7D", "30D", "90D", "Custom"])
    with col2:
        team = st.selectbox("👥 Team", ["All", "Support", "Sales", "Technical"])
    with col3:
        channel = st.selectbox("📱 Channel", ["All", "Chat", "Voice", "Email"])
    with col4:
        sentiment = st.selectbox("😊 Sentiment", ["All", "Positive", "Neutral", "Negative"])
    with col5:
        ai_quality = st.selectbox("🤖 AI Quality", ["All", "Excellent", "Good", "Poor"])

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Advanced KPIs
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    kpis = [
        (col1, "💬", "892", "Total Tickets", "+15%"),
        (col2, "✅", "94.2%", "Resolution", "+3.2%"),
        (col3, "⚡", "1m 45s", "Avg Response", "-22s"),
        (col4, "😊", "4.87/5", "CSAT", "+0.15"),
        (col5, "🤖", "87%", "AI Containment", "+5%"),
        (col6, "☎️", "312", "Voice Calls", "+18%"),
    ]

    for col, icon, value, label, change in kpis:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 18px;">{icon}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-label">{label}</div>
                <div style="color: #22c55e; font-size: 11px; margin-top: 4px;">{change}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Advanced Analytics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 🧠 AI Insights")
        st.markdown("""
        - **Top Intent**: Billing (34%)
        - **Most Escalated**: API Setup (12%)
        - **Hallucination Rate**: 0.3% ✅
        - **Intent Accuracy**: 96.8% ✅
        - **Suggestion Quality**: 94.2% ✅
        """)

    with col2:
        st.markdown("#### 📊 Performance Trends")
        dates = pd.date_range(start=datetime.now() - timedelta(days=7), periods=7, freq='D')
        resolution = [89, 91, 88, 93, 94, 95, 94.2]

        fig = go.Figure(data=go.Scatter(x=dates, y=resolution, fill='tozeroy',
                                        line=dict(color='#22c55e', width=3)))
        fig.update_layout(template='plotly_dark', height=250, margin=dict(l=0, r=0, t=0, b=0),
                         paper_bgcolor='rgba(30,41,59,0.5)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.markdown("#### 🔍 Quality Metrics")
        st.markdown("""
        - **KB Accuracy**: 98.5% 🟢
        - **Response Quality**: 4.9/5 🟢
        - **Customer Effort**: Low 🟢
        - **First Contact Res**: 89% 🟢
        - **Escalation Rate**: 11% 🟡
        """)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Advanced Analytics Grid
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 💬 Chat Intelligence")
        chat_intel = pd.DataFrame({
            'Metric': ['Avg Messages per Chat', 'Chat Duration', 'KB References', 'Escalation Rate', 'Repeat Customers'],
            'Value': ['4.2', '5m 30s', '2.1', '11%', '8%'],
            'Trend': ['↑ +0.3', '↓ -45s', '↑ +0.5', '↓ -2%', '↓ -1.2%']
        })
        st.dataframe(chat_intel, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("#### ☎️ Voice Intelligence")
        voice_intel = pd.DataFrame({
            'Metric': ['Total Calls', 'Connected Rate', 'Avg Duration', 'Escalation %', 'Repeat Rate'],
            'Value': ['312', '94.2%', '8m 45s', '16%', '12%'],
            'Trend': ['↑ +18%', '↑ +1.8%', '↑ +2m 15s', '↓ -3%', '↓ -2%']
        })
        st.dataframe(voice_intel, use_container_width=True, hide_index=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Real-time Monitoring
    st.markdown("#### 📡 Real-Time Monitoring")

    col1, col2, col3 = st.columns(3)

    monitoring = [
        (col1, "🟢 Chat Bot", "12 Active", "Healthy", "12 agents responding"),
        (col2, "🟢 Voice Bot", "8 Active Calls", "Optimal", "94.2% success rate"),
        (col3, "🟢 AI Agent", "87% Contained", "Excellent", "0.3% hallucination"),
    ]

    for col, title, status, health, detail in monitoring:
        with col:
            st.markdown(f"""
            <div class="enterprise-card">
                <h4 style="margin: 0;">{title}</h4>
                <p style="color: #22c55e; margin: 8px 0; font-weight: 600;">{status}</p>
                <p style="color: #94a3b8; font-size: 12px; margin: 0;">{health}</p>
                <p style="color: #64748b; font-size: 11px; margin-top: 8px;">{detail}</p>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# ADVANCED CHAT
# ============================================================================
def render_advanced_chat():
    st.markdown("### 💬 AI Chat with Advanced Features")

    # AI Features
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Intent Confidence", "96.8%", "+1.2%")
    with col2:
        st.metric("KB Match Score", "94.2%", "+2.5%")
    with col3:
        st.metric("Response Quality", "4.9/5", "+0.2")
    with col4:
        st.metric("Escalation Risk", "Low", "↓ 3%")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Chat with AI features
    st.markdown("**🤖 AI Agent with Semantic Understanding**")

    chat_data = [
        {"role": "customer", "message": "How do I integrate your API?", "confidence": "98%", "intent": "API Integration"},
        {"role": "agent", "message": "Great question! Found 3 KB articles with 97% relevance. Here's the quickstart...", "kb_ref": "API-101, API-102", "escalation": "None"},
    ]

    for msg in chat_data:
        if msg['role'] == 'customer':
            st.markdown(f"""
            **You:** {msg['message']}
            - Intent: {msg['intent']} | Confidence: {msg['confidence']}
            """)
        else:
            st.markdown(f"""
            **🤖 AI Agent:** {msg['message']}
            - KB References: {msg['kb_ref']}
            - Escalation Risk: {msg['escalation']}
            """)

    # Input
    user_msg = st.text_input("Your message...", placeholder="Ask anything with AI understanding")
    if st.button("Send with AI"):
        st.success("✅ Processed with semantic understanding, KB matching, and intent detection")

# ============================================================================
# ADVANCED KB
# ============================================================================
def render_advanced_kb():
    st.markdown("### 📚 Advanced Knowledge Base")

    tab1, tab2, tab3, tab4 = st.tabs(["Articles", "Versioning", "Analytics", "AI Training"])

    with tab1:
        st.markdown("#### Article Management with Versions & Approval")
        for article in st.session_state.advanced_kb:
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col1:
                st.markdown(f"**{article['title']}** (v{article['version']})")
                st.caption(f"{article['category']}")
            with col2:
                status_class = "status-active" if article['status'] == 'published' else "status-warning"
                st.markdown(f"<span class='{status_class}'>{article['status'].upper()}</span>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"👁️ {article['views']}")
            with col4:
                st.markdown(f"👍 {article['helpful']}%")
            st.divider()

    with tab2:
        st.markdown("#### Version Control & Rollback")
        st.markdown("""
        - **v5**: Current (published) - 97% helpful
        - **v4**: Previous - 94% helpful
        - **v3**: Archive - 91% helpful
        - **Rollback available** to any version
        """)

    with tab3:
        st.markdown("#### KB Performance Analytics")
        kb_perf = pd.DataFrame({
            'Article': ['Getting Started', 'API Integration', 'Billing FAQ'],
            'Views': [1250, 890, 340],
            'Helpful': ['94%', '97%', '91%'],
            'Impact': ['High', 'High', 'Medium'],
        })
        st.dataframe(kb_perf, use_container_width=True, hide_index=True)

    with tab4:
        st.markdown("#### AI Training Data")
        st.markdown("""
        - **Articles used**: 156
        - **Training accuracy**: 96.8%
        - **Model version**: v2.5
        - **Last trained**: Today 2:30 PM
        - **Next update**: Scheduled
        """)

# ============================================================================
# ADVANCED ANALYTICS
# ============================================================================
def render_advanced_analytics():
    st.markdown("### 📊 Advanced Analytics & Reporting")

    tab1, tab2, tab3 = st.tabs(["Predictive", "Sentiment", "Business Impact"])

    with tab1:
        st.markdown("#### Predictive Analytics")
        st.markdown("""
        - **Churn Risk**: 12% of customers (↓ 3%)
        - **Escalation Likelihood**: 14% (↓ 2%)
        - **High-intent Queries**: 34% (↑ 5%)
        - **Peak Hour**: 2-4 PM (↑ 8%)
        - **Recommended Action**: Add 2 agents at 2 PM
        """)

    with tab2:
        st.markdown("#### Sentiment Analysis")
        sentiment_data = pd.DataFrame({
            'Sentiment': ['Positive', 'Neutral', 'Negative'],
            'Count': [780, 89, 23],
            'Trend': ['↑ 12%', '↓ 8%', '↓ 4%']
        })
        st.dataframe(sentiment_data, use_container_width=True, hide_index=True)

    with tab3:
        st.markdown("#### Business Impact")
        st.markdown("""
        - **Cost per ticket**: $2.45 (↓ 18%)
        - **Revenue protected**: $12,450 (escalation prevented)
        - **NPS improvement**: +8 points
        - **Support satisfaction**: 94.2%
        - **ROI**: 3.2x (Year-over-year)
        """)

# ============================================================================
# ADVANCED SETTINGS
# ============================================================================
def render_advanced_settings():
    st.markdown("### ⚙️ Advanced Configuration")

    tab1, tab2, tab3, tab4 = st.tabs(["AI Models", "Escalation Logic", "Webhooks", "SLA Rules"])

    with tab1:
        st.markdown("#### AI Model Management")
        st.markdown("""
        - **Chat Model**: Claude Opus (Advanced)
        - **Embedding Model**: Multi-lingual v2.5
        - **Intent Classifier**: Custom trained
        - **Sentiment Model**: Latest
        - **Temperature**: 0.7 (Balanced)
        """)

    with tab2:
        st.markdown("#### Intelligent Escalation")
        st.markdown("""
        - **Low Confidence** (<85%) → Escalate
        - **Sentiment Negative** → Escalate
        - **Repeat Issue** (3+x) → Escalate
        - **KB Match** (<70%) → Escalate
        - **Skill-based routing** → Enabled
        """)

    with tab3:
        st.markdown("#### Webhook Configuration")
        webhooks = pd.DataFrame({
            'Event': ['Chat Started', 'Escalation', 'Call Initiated', 'KB Updated'],
            'URL': ['api.example.com/chat', 'api.example.com/escalate', 'api.example.com/call', 'api.example.com/kb'],
            'Status': ['✅ Active', '✅ Active', '✅ Active', '⚠️ Pending']
        })
        st.dataframe(webhooks, use_container_width=True, hide_index=True)

    with tab4:
        st.markdown("#### SLA Rules")
        st.markdown("""
        - **Priority 1**: Response <5min, Resolution <1hr
        - **Priority 2**: Response <15min, Resolution <4hr
        - **Priority 3**: Response <1hr, Resolution <24hr
        - **Current SLA Met**: 96.2% ✅
        """)

# ============================================================================
# NAVIGATION
# ============================================================================
render_advanced_widget()

st.markdown("""
<div style="text-align: center; padding: 20px 0;">
    <h1 style="font-size: 32px; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        🚀 Convin AI Support Console - ADVANCED
    </h1>
    <p style="color: #94a3b8; margin-top: 8px;">Enterprise Intelligence Platform with AI, Analytics & Insights</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Navigation buttons
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns(5)

with nav_col1:
    if st.button("📊 Dashboard", use_container_width=True):
        st.session_state.current_page = 'advanced_dashboard'
        st.rerun()

with nav_col2:
    if st.button("💬 Chat", use_container_width=True):
        st.session_state.current_page = 'advanced_chat'
        st.rerun()

with nav_col3:
    if st.button("📚 KB", use_container_width=True):
        st.session_state.current_page = 'advanced_kb'
        st.rerun()

with nav_col4:
    if st.button("📈 Analytics", use_container_width=True):
        st.session_state.current_page = 'advanced_analytics'
        st.rerun()

with nav_col5:
    if st.button("⚙️ Settings", use_container_width=True):
        st.session_state.current_page = 'advanced_settings'
        st.rerun()

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============================================================================
# RENDER PAGES
# ============================================================================
if st.session_state.current_page == 'advanced_dashboard':
    render_advanced_dashboard()
elif st.session_state.current_page == 'advanced_chat':
    render_advanced_chat()
elif st.session_state.current_page == 'advanced_kb':
    render_advanced_kb()
elif st.session_state.current_page == 'advanced_analytics':
    render_advanced_analytics()
elif st.session_state.current_page == 'advanced_settings':
    render_advanced_settings()

# Footer
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 12px; padding: 20px 0;">
    <p>🚀 Convin AI Support Console - ADVANCED v2.0 | Enterprise Intelligence Platform</p>
</div>
""", unsafe_allow_html=True)
