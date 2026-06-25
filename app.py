import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

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

    .premium-divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, rgba(59, 130, 246, 0.3) 50%, transparent 100%);
        margin: 32px 0;
    }

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
    st.session_state.page = 'dashboard'
if 'widget_open' not in st.session_state:
    st.session_state.widget_open = False

# ============================================================================
# SAMPLE DATA GENERATORS
# ============================================================================
def generate_sample_data():
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=30, freq='D')
    return {
        'dates': dates,
        'tickets': np.random.randint(10, 50, 30),
        'chat_volume': np.random.randint(20, 80, 30),
        'calls': np.random.randint(5, 25, 30),
        'sentiment_pos': np.random.randint(70, 95, 30),
        'sentiment_neg': np.random.randint(2, 15, 30),
    }

# ============================================================================
# FLOATING WIDGET
# ============================================================================
def render_widget():
    if st.session_state.widget_open:
        st.markdown("""
        <div class="floating-widget">
            <div class="premium-card" style="min-width: 240px; position: fixed; bottom: 100px; right: 20px; z-index: 99998;">
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
                st.session_state.page = 'voice'
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
# DASHBOARD PAGE (MAIN) - PREMIUM + ADVANCED
# ============================================================================
def dashboard():
    st.markdown("""
    <div style="text-align: center; padding: 40px 20px; background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
                 border-radius: 20px; margin-bottom: 40px;">
        <h1>📊 Support Analytics Dashboard</h1>
        <p style="color: var(--text-muted); font-size: 16px; margin-top: 12px;">
            Real-time insights & AI intelligence
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Advanced Filters
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        period = st.selectbox("📅 Period", ["Today", "7D", "30D", "90D"], label_visibility="collapsed")
    with col2:
        team = st.selectbox("👥 Team", ["All", "Support", "Sales", "Technical"], label_visibility="collapsed")
    with col3:
        channel = st.selectbox("📢 Channel", ["All", "Chat", "Voice", "Email"], label_visibility="collapsed")
    with col4:
        sentiment = st.selectbox("😊 Sentiment", ["All", "Positive", "Neutral", "Negative"], label_visibility="collapsed")
    with col5:
        ai_quality = st.selectbox("🤖 AI Quality", ["All", "High", "Medium", "Low"], label_visibility="collapsed")

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    # KPIs - 6 metrics
    st.markdown("#### 🎯 Key Performance Indicators")
    col1, col2, col3, col4, col5, col6 = st.columns(6, gap="small")

    data = generate_sample_data()

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
                <div class="metric-value" style="font-size: 28px;">{value}</div>
                <div class="metric-label">{label}</div>
                <div class="metric-change">{trend}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    # Advanced Tabs with Charts
    st.markdown("#### 📈 Real-time Analytics")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Trends", "💬 Chat", "☎️ Voice", "😊 Sentiment", "🤖 AI Insights", "📈 Predictive"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Ticket Volume Trend (30 days)**")
            fig = go.Figure(data=go.Scatter(x=data['dates'], y=data['tickets'], fill='tozeroy',
                                            line=dict(color='#3b82f6', width=3),
                                            marker=dict(size=8)))
            fig.update_layout(template='plotly_dark', height=300, margin=dict(l=0, r=0, t=0, b=0),
                             paper_bgcolor='rgba(30,41,59,0.5)', plot_bgcolor='rgba(0,0,0,0)',
                             xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(148,163,184,0.1)'),
                             showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("**Channel Distribution**")
            channels = ['Chat', 'Voice', 'Email']
            counts = [520, 240, 132]
            fig = go.Figure(data=go.Pie(labels=channels, values=counts,
                                         marker=dict(colors=['#3b82f6', '#8b5cf6', '#06b6d4']),
                                         textposition='inside', textinfo='label+percent'))
            fig.update_layout(template='plotly_dark', height=300, margin=dict(l=0, r=0, t=0, b=0),
                             paper_bgcolor='rgba(30,41,59,0.5)')
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Chat Volume (30 days)**")
            fig = go.Figure(data=go.Bar(x=data['dates'], y=data['chat_volume'],
                                        marker=dict(color='#3b82f6')))
            fig.update_layout(template='plotly_dark', height=300, margin=dict(l=0, r=0, t=0, b=0),
                             paper_bgcolor='rgba(30,41,59,0.5)', plot_bgcolor='rgba(0,0,0,0)',
                             showlegend=False, xaxis=dict(showgrid=False))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("""
                <div class="premium-card">
                    <div style="text-align: center;">
                        <div style="font-size: 24px; color: #3b82f6; font-weight: 900;">1,245</div>
                        <div style="color: var(--text-muted); font-size: 12px; margin-top: 8px; text-transform: uppercase;">Chat Messages</div>
                        <div style="color: #22c55e; font-size: 11px; margin-top: 6px;">↑ 12% vs last week</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_b:
                st.markdown("""
                <div class="premium-card">
                    <div style="text-align: center;">
                        <div style="font-size: 24px; color: #8b5cf6; font-weight: 900;">2.1m</div>
                        <div style="color: var(--text-muted); font-size: 12px; margin-top: 8px; text-transform: uppercase;">Avg Response Time</div>
                        <div style="color: #ef4444; font-size: 11px; margin-top: 6px;">↑ 15 sec vs target</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Call Volume & Duration**")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data['dates'], y=data['calls'], mode='lines+markers',
                                     name='Calls', line=dict(color='#8b5cf6', width=3)))
            fig.update_layout(template='plotly_dark', height=300, margin=dict(l=0, r=0, t=0, b=0),
                             paper_bgcolor='rgba(30,41,59,0.5)', plot_bgcolor='rgba(0,0,0,0)',
                             xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(148,163,184,0.1)'))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("""
                <div class="premium-card">
                    <div style="text-align: center;">
                        <div style="font-size: 24px; color: #8b5cf6; font-weight: 900;">312</div>
                        <div style="color: var(--text-muted); font-size: 12px; margin-top: 8px; text-transform: uppercase;">Total Calls</div>
                        <div style="color: #22c55e; font-size: 11px; margin-top: 6px;">✓ 94.2% Connected</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_b:
                st.markdown("""
                <div class="premium-card">
                    <div style="text-align: center;">
                        <div style="font-size: 24px; color: #f59e0b; font-weight: 900;">8.3m</div>
                        <div style="color: var(--text-muted); font-size: 12px; margin-top: 8px; text-transform: uppercase;">Avg Duration</div>
                        <div style="color: #22c55e; font-size: 11px; margin-top: 6px;">↓ 20 sec improvement</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tab4:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Sentiment Distribution**")
            sentiments = ['Positive', 'Neutral', 'Negative']
            counts = [456, 234, 56]
            colors = ['#22c55e', '#94a3b8', '#ef4444']
            fig = go.Figure(data=go.Pie(labels=sentiments, values=counts,
                                         marker=dict(colors=colors),
                                         textposition='inside', textinfo='label+percent'))
            fig.update_layout(template='plotly_dark', height=300, margin=dict(l=0, r=0, t=0, b=0),
                             paper_bgcolor='rgba(30,41,59,0.5)')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("**Sentiment Trend**")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data['dates'], y=data['sentiment_pos'], mode='lines+markers',
                                     name='Positive', line=dict(color='#22c55e', width=3)))
            fig.add_trace(go.Scatter(x=data['dates'], y=data['sentiment_neg'], mode='lines+markers',
                                     name='Negative', line=dict(color='#ef4444', width=3)))
            fig.update_layout(template='plotly_dark', height=300, margin=dict(l=0, r=0, t=0, b=0),
                             paper_bgcolor='rgba(30,41,59,0.5)', plot_bgcolor='rgba(0,0,0,0)',
                             xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(148,163,184,0.1)'))
            st.plotly_chart(fig, use_container_width=True)

    with tab5:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="premium-card">
                <h4 style="margin: 0 0 16px 0;">🤖 AI Performance Metrics</h4>
                <div style="margin: 12px 0;">
                    <div style="display: flex; justify-content: space-between; margin: 8px 0;">
                        <span>Accuracy</span>
                        <strong style="color: #22c55e;">96.8%</strong>
                    </div>
                    <div style="background: rgba(148,163,184,0.2); height: 8px; border-radius: 4px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%); height: 100%; width: 96.8%;"></div>
                    </div>
                </div>
                <div style="margin: 12px 0;">
                    <div style="display: flex; justify-content: space-between; margin: 8px 0;">
                        <span>Resolution Rate</span>
                        <strong style="color: #22c55e;">87%</strong>
                    </div>
                    <div style="background: rgba(148,163,184,0.2); height: 8px; border-radius: 4px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%); height: 100%; width: 87%;"></div>
                    </div>
                </div>
                <div style="margin: 12px 0;">
                    <div style="display: flex; justify-content: space-between; margin: 8px 0;">
                        <span>Containment Rate</span>
                        <strong style="color: #22c55e;">83%</strong>
                    </div>
                    <div style="background: rgba(148,163,184,0.2); height: 8px; border-radius: 4px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%); height: 100%; width: 83%;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="premium-card">
                <h4 style="margin: 0 0 16px 0;">📊 Real-time Bot Status</h4>
                <div style="margin: 16px 0; padding: 12px; background: rgba(34, 197, 94, 0.1); border-radius: 8px; border-left: 3px solid #22c55e;">
                    <div style="font-weight: 700; color: #22c55e;">🤖 Chat Bot</div>
                    <div style="color: var(--text-muted); font-size: 12px; margin-top: 4px;">12 active conversations</div>
                </div>
                <div style="margin: 16px 0; padding: 12px; background: rgba(34, 197, 94, 0.1); border-radius: 8px; border-left: 3px solid #22c55e;">
                    <div style="font-weight: 700; color: #22c55e;">☎️ Voice Bot</div>
                    <div style="color: var(--text-muted); font-size: 12px; margin-top: 4px;">8 active calls at 94.2% success</div>
                </div>
                <div style="margin: 16px 0; padding: 12px; background: rgba(34, 197, 94, 0.1); border-radius: 8px; border-left: 3px solid #22c55e;">
                    <div style="font-weight: 700; color: #22c55e;">🎯 AI Agent</div>
                    <div style="color: var(--text-muted); font-size: 12px; margin-top: 4px;">87% contained, 13% escalated</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab6:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="premium-card">
                <h4 style="margin: 0 0 16px 0;">⚠️ Predictive Insights</h4>
                <div style="margin: 16px 0; padding: 12px; background: rgba(34, 197, 94, 0.1); border-radius: 8px; border-left: 3px solid #22c55e;">
                    <div style="font-weight: 700; color: #22c55e;">✓ Churn Risk</div>
                    <div style="color: var(--text-muted); font-size: 12px; margin-top: 4px;">12 customers identified • Action needed</div>
                </div>
                <div style="margin: 16px 0; padding: 12px; background: rgba(245, 158, 11, 0.1); border-radius: 8px; border-left: 3px solid #f59e0b;">
                    <div style="font-weight: 700; color: #f59e0b;">⚡ Escalation Likelihood</div>
                    <div style="color: var(--text-muted); font-size: 12px; margin-top: 4px;">23% of open tickets may escalate</div>
                </div>
                <div style="margin: 16px 0; padding: 12px; background: rgba(59, 130, 246, 0.1); border-radius: 8px; border-left: 3px solid #3b82f6;">
                    <div style="font-weight: 700; color: #3b82f6;">🕐 Peak Hours</div>
                    <div style="color: var(--text-muted); font-size: 12px; margin-top: 4px;">2-4 PM today (High volume expected)</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="premium-card">
                <h4 style="margin: 0 0 16px 0;">💰 Business Impact</h4>
                <div style="margin: 16px 0; padding: 12px; background: rgba(139, 92, 246, 0.1); border-radius: 8px; border-left: 3px solid #8b5cf6;">
                    <div style="font-weight: 700; color: #8b5cf6;">💵 Cost per Ticket</div>
                    <div style="color: var(--text-muted); font-size: 12px; margin-top: 4px;">$12.50 avg • ↓ 18% vs last month</div>
                </div>
                <div style="margin: 16px 0; padding: 12px; background: rgba(139, 92, 246, 0.1); border-radius: 8px; border-left: 3px solid #8b5cf6;">
                    <div style="font-weight: 700; color: #8b5cf6;">💎 Revenue Protected</div>
                    <div style="color: var(--text-muted); font-size: 12px; margin-top: 4px;">$245K this month via AI automation</div>
                </div>
                <div style="margin: 16px 0; padding: 12px; background: rgba(139, 92, 246, 0.1); border-radius: 8px; border-left: 3px solid #8b5cf6;">
                    <div style="font-weight: 700; color: #8b5cf6;">📈 NPS Improvement</div>
                    <div style="color: var(--text-muted); font-size: 12px; margin-top: 4px;">+8.5 points from AI support</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    # Bottom Navigation
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💬 Start Chat", use_container_width=True):
            st.session_state.page = 'chat'
            st.rerun()
    with col2:
        if st.button("☎️ Schedule Call", use_container_width=True):
            st.session_state.page = 'voice'
            st.rerun()
    with col3:
        if st.button("⚙️ Settings", use_container_width=True):
            st.session_state.page = 'settings'
            st.rerun()

# ============================================================================
# CHAT PAGE
# ============================================================================
def chat():
    st.markdown("### 💬 AI Chat Support")
    st.markdown("""
    <div class="premium-card">
        <p style="color: var(--text-muted);">🤖 <strong>AI Agent</strong> • Response Time: <strong>45s</strong> • Confidence: <strong>96.8%</strong></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="premium-card" style="height: 400px; overflow-y: auto;">
        <div style="padding: 16px 0;">
            <div style="background: rgba(59, 130, 246, 0.2); padding: 12px 16px; border-radius: 10px; border-left: 3px solid #3b82f6; margin: 8px 0;">
                <p style="margin: 0;"><strong>You:</strong> What are your pricing plans?</p>
            </div>
            <div style="background: rgba(34, 197, 94, 0.2); padding: 12px 16px; border-radius: 10px; border-left: 3px solid #22c55e; margin: 8px 0;">
                <p style="margin: 0;"><strong>🤖 AI:</strong> We offer Starter ($99), Pro ($299), and Enterprise (custom) plans with 30-day free trial.</p>
            </div>
            <div style="background: rgba(59, 130, 246, 0.2); padding: 12px 16px; border-radius: 10px; border-left: 3px solid #3b82f6; margin: 8px 0;">
                <p style="margin: 0;"><strong>You:</strong> Which is best for 20 people?</p>
            </div>
            <div style="background: rgba(34, 197, 94, 0.2); padding: 12px 16px; border-radius: 10px; border-left: 3px solid #22c55e; margin: 8px 0;">
                <p style="margin: 0;"><strong>🤖 AI:</strong> Pro plan at $299/month is ideal for your team size. Need more info?</p>
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
        if st.button("Dashboard", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()
    with col3:
        if st.button("Settings", use_container_width=True):
            st.session_state.page = 'settings'
            st.rerun()

# ============================================================================
# VOICE PAGE
# ============================================================================
def voice():
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

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💬 Chat Instead", use_container_width=True):
            st.session_state.page = 'chat'
            st.rerun()
    with col2:
        if st.button("Dashboard", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()
    with col3:
        if st.button("Settings", use_container_width=True):
            st.session_state.page = 'settings'
            st.rerun()

# ============================================================================
# SETTINGS PAGE
# ============================================================================
def settings():
    st.markdown("### ⚙️ Settings")

    tab1, tab2, tab3 = st.tabs(["Profile", "Preferences", "Support"])

    with tab1:
        st.markdown("""
        <div class="premium-card">
            <h4>👤 Profile Information</h4>
        </div>
        """, unsafe_allow_html=True)
        st.text_input("Full Name", value="John Doe")
        st.text_input("Email", value="john@example.com")
        st.text_input("Phone", value="+1-555-123-4567")

    with tab2:
        st.markdown("""
        <div class="premium-card">
            <h4>🎨 Preferences</h4>
        </div>
        """, unsafe_allow_html=True)
        st.toggle("🔔 Email Notifications", value=True)
        st.toggle("📱 SMS Notifications", value=True)
        st.selectbox("📧 Email Frequency", ["Realtime", "Daily Digest", "Weekly"])

    with tab3:
        st.markdown("""
        <div class="premium-card">
            <h4>📞 Support Options</h4>
            <p style="color: var(--text-muted);">Email: support@convin.ai</p>
            <p style="color: var(--text-muted);">Phone: 1-800-CONVIN-AI</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)

    if st.button("Back to Dashboard", use_container_width=True):
        st.session_state.page = 'dashboard'
        st.rerun()

# ============================================================================
# MAIN APP
# ============================================================================
render_widget()

if st.session_state.page == 'dashboard':
    dashboard()
elif st.session_state.page == 'chat':
    chat()
elif st.session_state.page == 'voice':
    voice()
elif st.session_state.page == 'settings':
    settings()

# Footer
st.markdown("""
<div style="text-align: center; padding: 40px 20px; margin-top: 60px; border-top: 1px solid rgba(59, 130, 246, 0.1);">
    <p style="color: var(--text-muted); font-size: 12px; margin: 0;">
        🚀 Convin AI Support Console | Enterprise Intelligence Platform | v2.0
    </p>
</div>
""", unsafe_allow_html=True)
