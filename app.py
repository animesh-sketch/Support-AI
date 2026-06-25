import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(
    page_title="Anamika - Support Widget",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# DESIGN SYSTEM
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

    /* WIDGET STYLES */
    .widget-button-float {
        position: fixed !important;
        top: 30px !important;
        right: 30px !important;
        z-index: 999999 !important;
        width: 70px !important;
        height: 70px !important;
        border-radius: 50% !important;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        font-size: 32px !important;
        cursor: pointer !important;
        box-shadow: 0 12px 32px rgba(59, 130, 246, 0.35) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.35s cubic-bezier(0.23, 1, 0.320, 1) !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    .widget-button-float:hover {
        transform: scale(1.18) !important;
        box-shadow: 0 18px 48px rgba(59, 130, 246, 0.45) !important;
    }

    .widget-badge {
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
        animation: badge-pulse 2s ease-in-out infinite !important;
    }

    @keyframes badge-pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.12); }
    }

    .widget-chat {
        position: fixed !important;
        top: 110px !important;
        right: 20px !important;
        width: 380px !important;
        max-height: 550px !important;
        background: rgba(15, 23, 42, 0.98) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 20px !important;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6) !important;
        backdrop-filter: blur(30px) !important;
        z-index: 999998 !important;
        display: flex !important;
        flex-direction: column !important;
        overflow: hidden !important;
    }

    .widget-header {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
        padding: 16px !important;
        border-radius: 20px 20px 0 0 !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
    }

    .widget-header h3 {
        margin: 0 !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: 700 !important;
    }

    .widget-messages {
        flex: 1 !important;
        overflow-y: auto !important;
        padding: 16px !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 10px !important;
    }

    .msg-bot {
        background: rgba(59, 130, 246, 0.2) !important;
        padding: 10px 12px !important;
        border-radius: 12px !important;
        border-left: 3px solid #3b82f6 !important;
        max-width: 85% !important;
        align-self: flex-start !important;
        font-size: 13px !important;
        color: var(--text) !important;
        animation: slideIn 0.3s ease !important;
    }

    .msg-user {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
        padding: 10px 12px !important;
        border-radius: 12px !important;
        max-width: 85% !important;
        align-self: flex-end !important;
        font-size: 13px !important;
        color: white !important;
        animation: slideIn 0.3s ease !important;
    }

    @keyframes slideIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .widget-input-area {
        padding: 12px !important;
        border-top: 1px solid rgba(59, 130, 246, 0.2) !important;
    }

    .widget-input {
        width: 100% !important;
        padding: 10px 12px !important;
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 10px !important;
        color: var(--text) !important;
        font-size: 13px !important;
        font-family: 'Inter', sans-serif !important;
        box-sizing: border-box !important;
        transition: all 0.3s ease !important;
    }

    .widget-input:focus {
        border-color: #3b82f6 !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
    }

    .widget-buttons {
        display: flex !important;
        gap: 8px !important;
        margin-top: 10px !important;
    }

    .widget-btn {
        flex: 1 !important;
        padding: 8px !important;
        background: rgba(59, 130, 246, 0.15) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        color: #3b82f6 !important;
        border-radius: 8px !important;
        cursor: pointer !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif !important;
    }

    .widget-btn:hover {
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
if 'widget_chat' not in st.session_state:
    st.session_state.widget_chat = [
        {"role": "bot", "text": "Hi! 👋 How can I help you today?"}
    ]
if 'widget_input' not in st.session_state:
    st.session_state.widget_input = ""
if 'admin_pass' not in st.session_state:
    st.session_state.admin_pass = False
if 'kb_files' not in st.session_state:
    st.session_state.kb_files = [
        {"name": "Password Reset Guide.pdf", "size": "2.3 MB", "type": "PDF", "date": "2026-06-20", "status": "Active"},
        {"name": "Billing FAQ.docx", "size": "1.8 MB", "type": "DOCX", "date": "2026-06-19", "status": "Active"},
    ]

# ============================================================================
# FLOATING WIDGET COMPONENT
# ============================================================================
def render_widget():
    """Render the floating chat widget"""

    # Widget HTML structure
    widget_html = """
    <div class="widget-button-float" id="widget-btn">
        🎯
        <div class="widget-badge">3</div>
    </div>
    <div class="widget-chat" id="widget-chat" style="display: none;">
        <div class="widget-header">
            <div>
                <h3>🎯 Anamika</h3>
                <p style="margin: 4px 0 0 0; color: rgba(255,255,255,0.8); font-size: 12px;">Always here to help</p>
            </div>
            <button style="background: rgba(255,255,255,0.2); border: none; color: white; width: 32px; height: 32px; border-radius: 50%; cursor: pointer; font-size: 18px;" id="close-btn">✕</button>
        </div>
        <div class="widget-messages" id="messages"></div>
        <div class="widget-input-area">
            <input type="text" class="widget-input" id="msg-input" placeholder="Type message..." />
            <div class="widget-buttons">
                <button class="widget-btn" id="call-btn">☎️ Call</button>
                <button class="widget-btn" id="agent-btn">👤 Agent</button>
            </div>
        </div>
    </div>
    """

    st.markdown(widget_html, unsafe_allow_html=True)

    # JavaScript to handle widget interactions
    st.markdown("""
    <script>
        setTimeout(() => {
            const btn = document.getElementById('widget-btn');
            const chat = document.getElementById('widget-chat');
            const closeBtn = document.getElementById('close-btn');
            const msgInput = document.getElementById('msg-input');
            const callBtn = document.getElementById('call-btn');
            const agentBtn = document.getElementById('agent-btn');

            // Toggle widget
            btn.addEventListener('click', () => {
                chat.style.display = chat.style.display === 'none' ? 'flex' : 'none';
                if (chat.style.display === 'flex') {
                    msgInput.focus();
                }
            });

            // Close widget
            closeBtn.addEventListener('click', () => {
                chat.style.display = 'none';
            });

            // Smooth scroll to bottom
            function scrollToBottom() {
                const messages = document.getElementById('messages');
                messages.scrollTop = messages.scrollHeight;
            }

            setTimeout(scrollToBottom, 100);
        }, 500);
    </script>
    """, unsafe_allow_html=True)

# ============================================================================
# DASHBOARD
# ============================================================================
def dashboard():
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px; background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%); border-radius: 24px; margin-bottom: 40px;">
        <h1>🎯 Anamika</h1>
        <p style="color: var(--text-muted); font-size: 16px; margin-top: 12px;">Enterprise Floating Chat Widget</p>
        <p style="color: #22c55e; font-size: 13px; margin-top: 16px; font-weight: 700;">👉 Click the 🎯 button in TOP RIGHT to chat!</p>
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
            st.session_state.page = 'admin'
            st.rerun()

    st.markdown("---")

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric("Chats", "1,245", "+12%")
    with col2:
        st.metric("Calls", "312", "+18%")
    with col3:
        st.metric("Resolved", "94.2%", "+3.2%")
    with col4:
        st.metric("CSAT", "4.87/5", "+0.15")
    with col5:
        st.metric("AI OK", "87%", "+5%")
    with col6:
        st.metric("Response", "45s", "-15s")

# ============================================================================
# CHAT PAGE
# ============================================================================
def chat_page():
    st.markdown("### 💬 Chat Support")

    # Display chat
    for msg in st.session_state.widget_chat:
        if msg["role"] == "bot":
            st.info(f"🤖 **Anamika:** {msg['text']}")
        else:
            st.success(f"👤 **You:** {msg['text']}")

    # Input
    col1, col2 = st.columns([5, 1])
    with col1:
        user_msg = st.text_input("Message...", label_visibility="collapsed", placeholder="Type your question")
    with col2:
        send = st.button("Send", use_container_width=True)

    if send and user_msg:
        st.session_state.widget_chat.append({"role": "user", "text": user_msg})
        st.session_state.widget_chat.append({"role": "bot", "text": "Thanks! I'm here to help. What else can I do?"})
        st.rerun()

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("☎️ Call Agent", use_container_width=True):
            st.info("📞 Connecting to agent...")
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
def voice_page():
    st.markdown("### ☎️ Schedule Call")

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Your Name", label_visibility="collapsed", placeholder="John Doe")
        st.text_input("Email", label_visibility="collapsed", placeholder="john@example.com")
    with col2:
        st.text_input("Phone", label_visibility="collapsed", placeholder="+1-555-123-4567")
        st.selectbox("Best Time", ["9 AM - 12 PM", "12 PM - 3 PM", "3 PM - 6 PM", "6 PM - 9 PM"], label_visibility="collapsed")

    if st.button("📞 Schedule Call", use_container_width=True):
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
def analytics_page():
    st.markdown("### 📊 Analytics")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Conversations", "3,847", "+15%")
    with col2:
        st.metric("Avg Resolution", "12m 30s", "-2m")
    with col3:
        st.metric("Escalation Rate", "13%", "-2%")

    st.markdown("---")
    if st.button("Back to Home", use_container_width=True):
        st.session_state.page = 'dashboard'
        st.rerun()

# ============================================================================
# ADMIN PAGE
# ============================================================================
def admin_page():
    if not st.session_state.admin_pass:
        st.markdown("### 🔐 Admin Login")
        pwd = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Enter password")
        if st.button("Login", use_container_width=True):
            if pwd == "admin@anamika":
                st.session_state.admin_pass = True
                st.rerun()
            else:
                st.error("❌ Invalid password")
        if st.button("Back", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()
    else:
        st.markdown("### ⚙️ Admin Panel")

        tab1, tab2, tab3, tab4 = st.tabs(["📚 Knowledge Base", "🎤 Voice Config", "🤖 Bot Settings", "⚡ Advanced"])

        with tab1:
            st.markdown("#### 📚 Knowledge Base Management")
            st.markdown("""
            <div class="premium-card">
                <p style="margin: 0; color: var(--text-muted); font-size: 12px;">
                    Supported formats: PDF, DOC, DOCX, TXT, CSV, XLS, XLSX, PPT, PPTX, JSON, XML
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("##### Upload Documents (Up to 5 files)")

            # File uploader for multiple formats
            col1, col2 = st.columns(2)
            with col1:
                uploaded_files = st.file_uploader(
                    "Choose files",
                    type=['pdf', 'doc', 'docx', 'txt', 'csv', 'xls', 'xlsx', 'ppt', 'pptx', 'json', 'xml'],
                    accept_multiple_files=True,
                    label_visibility="collapsed"
                )

                if uploaded_files:
                    st.markdown("**Uploading Files:**")
                    for file in uploaded_files:
                        file_size = f"{file.size / 1024 / 1024:.1f}" if file.size < 10_000_000 else f"{file.size / 1024 / 1024 / 1024:.2f}"
                        file_unit = "MB" if file.size < 10_000_000 else "GB"

                        st.markdown(f"""
                        <div class="premium-card" style="padding: 12px; margin: 8px 0;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <p style="margin: 0; font-weight: 700;">📄 {file.name}</p>
                                    <p style="margin: 4px 0 0 0; color: var(--text-muted); font-size: 12px;">{file_size} {file_unit}</p>
                                </div>
                                <span style="color: #22c55e; font-weight: 700;">✓</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    if st.button("✅ Upload All Files", use_container_width=True, key="upload_kb"):
                        for file in uploaded_files:
                            if len(st.session_state.kb_files) < 5:
                                st.session_state.kb_files.append({
                                    "name": file.name,
                                    "size": f"{file.size / 1024:.1f} KB" if file.size < 1_000_000 else f"{file.size / 1024 / 1024:.1f} MB",
                                    "type": file.name.split('.')[-1].upper(),
                                    "date": datetime.now().strftime("%Y-%m-%d"),
                                    "status": "Active"
                                })
                        st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")
                        st.rerun()

            with col2:
                st.markdown("**Upload Status**")
                st.markdown(f"""
                <div class="premium-card">
                    <div style="text-align: center;">
                        <p style="margin: 0; font-size: 24px; font-weight: 900; color: #3b82f6;">{len(st.session_state.kb_files)}</p>
                        <p style="margin: 6px 0 0 0; color: var(--text-muted); font-size: 12px; text-transform: uppercase;">Files Stored</p>
                    </div>
                    <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(59, 130, 246, 0.2);">
                        <p style="margin: 0; font-size: 12px;"><strong>Max Files:</strong> 5</p>
                        <p style="margin: 6px 0 0 0; font-size: 12px;"><strong>Remaining:</strong> {5 - len(st.session_state.kb_files)} slots</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("##### 📋 Knowledge Base Files")

            if len(st.session_state.kb_files) == 0:
                st.info("📚 No files uploaded yet. Upload files above to get started!")
            else:
                # Display KB files in a table
                kb_data = {
                    "📄 File Name": [f["name"] for f in st.session_state.kb_files],
                    "📊 Type": [f["type"] for f in st.session_state.kb_files],
                    "💾 Size": [f["size"] for f in st.session_state.kb_files],
                    "📅 Date": [f["date"] for f in st.session_state.kb_files],
                    "✓ Status": [f["status"] for f in st.session_state.kb_files],
                }
                df = pd.DataFrame(kb_data)
                st.dataframe(df, use_container_width=True, hide_index=True)

                st.markdown("**File Actions:**")
                col_action1, col_action2, col_action3 = st.columns(3)

                with col_action1:
                    if st.button("🔍 View Files", use_container_width=True):
                        st.info("📂 Viewing all files in Knowledge Base...")

                with col_action2:
                    file_to_delete = st.selectbox(
                        "Delete file",
                        options=[f["name"] for f in st.session_state.kb_files],
                        label_visibility="collapsed"
                    )
                    if st.button("🗑️ Delete Selected", use_container_width=True):
                        st.session_state.kb_files = [f for f in st.session_state.kb_files if f["name"] != file_to_delete]
                        st.success(f"✅ {file_to_delete} deleted!")
                        st.rerun()

                with col_action3:
                    if st.button("📊 Analytics", use_container_width=True):
                        st.info("📈 KB usage analytics coming soon...")

        with tab2:
            st.markdown("#### 🎤 Voice Configuration (Convin Sense)")
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Workspace ID", placeholder="workspace_xyz", label_visibility="collapsed")
                st.text_input("API Key", placeholder="sk-sense-...", type="password", label_visibility="collapsed")
            with col2:
                st.toggle("Enable Inbound Calls", value=True)
                st.toggle("Enable Outbound Calls", value=True)

            st.selectbox("Default Voice", ["Male (Professional)", "Female (Friendly)", "AI (Natural)"], label_visibility="collapsed")
            st.slider("Speech Rate", 0.5, 2.0, 1.0)

            if st.button("💾 Save Voice Config", use_container_width=True):
                st.success("✅ Voice configuration saved!")

        with tab3:
            st.markdown("#### 🤖 Bot Settings")
            col1, col2 = st.columns(2)
            with col1:
                st.toggle("Use Knowledge Base", value=True)
                st.toggle("Auto-escalation", value=True)
            with col2:
                st.toggle("Log Conversations", value=True)
                st.toggle("Enable Feedback", value=True)

            st.slider("Confidence Threshold (%)", 0, 100, 75)
            st.slider("Response Timeout (seconds)", 5, 120, 45)

            if st.button("💾 Save Bot Settings", use_container_width=True):
                st.success("✅ Bot settings saved!")

        with tab4:
            st.markdown("#### ⚡ Advanced Settings")
            st.markdown("""
            <div class="premium-card">
                <p><strong>🔐 Security</strong></p>
                <p style="color: var(--text-muted); font-size: 13px; margin-top: 6px;">Enable two-factor authentication and security logs</p>
            </div>
            """, unsafe_allow_html=True)

            st.toggle("🔐 Enable 2FA", value=False)
            st.toggle("📝 Enable Audit Logs", value=True)
            st.toggle("🔒 Enable IP Whitelist", value=False)

            if st.button("💾 Save Advanced Settings", use_container_width=True):
                st.success("✅ Advanced settings saved!")

        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            st.session_state.admin_pass = False
            st.rerun()

# ============================================================================
# MAIN APP
# ============================================================================

# Render floating widget
render_widget()

# Render content based on page
if st.session_state.page == 'dashboard':
    dashboard()
elif st.session_state.page == 'chat':
    chat_page()
elif st.session_state.page == 'voice':
    voice_page()
elif st.session_state.page == 'analytics':
    analytics_page()
elif st.session_state.page == 'admin':
    admin_page()

# Update widget messages with JavaScript
messages_html = ""
for msg in st.session_state.widget_chat:
    if msg["role"] == "bot":
        messages_html += f'<div class="msg-bot">{msg["text"]}</div>'
    else:
        messages_html += f'<div class="msg-user">{msg["text"]}</div>'

st.markdown(f"""
<script>
    setTimeout(() => {{
        const messagesDiv = document.getElementById('messages');
        if (messagesDiv) {{
            messagesDiv.innerHTML = `{messages_html}`;
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }}

        const input = document.getElementById('msg-input');
        const callBtn = document.getElementById('call-btn');
        const agentBtn = document.getElementById('agent-btn');

        if (input && input.value === '') {{
            input.addEventListener('keypress', (e) => {{
                if (e.key === 'Enter' && input.value.trim()) {{
                    // Send message via Streamlit
                    const event = new Event('change', {{ bubbles: true }});
                    input.dispatchEvent(event);
                }}
            }});
        }}

        if (callBtn) {{
            callBtn.addEventListener('click', () => {{
                alert('📞 Connecting to voice support...');
            }});
        }}

        if (agentBtn) {{
            agentBtn.addEventListener('click', () => {{
                alert('👤 Connecting to agent...');
            }});
        }}
    }}, 300);
</script>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 40px 20px; margin-top: 60px; border-top: 1px solid rgba(59, 130, 246, 0.1);">
    <p style="color: var(--text-muted); font-size: 12px; margin: 0;">
        🎯 Anamika | Enterprise Widget | v4.1 Smooth & Functional
    </p>
</div>
""", unsafe_allow_html=True)
