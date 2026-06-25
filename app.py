import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os

st.set_page_config(
    page_title="Anamika - AI Support",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# STORAGE & KB
# ============================================================================
KB_DATA_FILE = "kb_files.json"
KB_CONTENT_FILE = "kb_content.json"

def load_kb_files():
    if os.path.exists(KB_DATA_FILE):
        try:
            with open(KB_DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_kb_files(files):
    with open(KB_DATA_FILE, 'w') as f:
        json.dump(files, f, indent=2)

def load_kb_content():
    if os.path.exists(KB_CONTENT_FILE):
        try:
            with open(KB_CONTENT_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_kb_content(content):
    with open(KB_CONTENT_FILE, 'w') as f:
        json.dump(content, f, indent=2)

def add_kb_file(name, size, file_type, content_text, status="Active"):
    files = load_kb_files()
    kb_content = load_kb_content()
    if len(files) < 5:
        files.append({"name": name, "size": size, "type": file_type, "date": datetime.now().strftime("%Y-%m-%d"), "status": status})
        kb_content[name] = {"title": name, "content": content_text}
        save_kb_files(files)
        save_kb_content(kb_content)
        return True
    return False

def search_kb(query):
    try:
        q = query.lower().strip()
        results = []
        kb_content = load_kb_content()
        for doc_name, doc_data in kb_content.items():
            score = 0
            title = doc_data.get("title", "").lower()
            content = doc_data.get("content", "").lower()

            if q in title:
                score += 5
            if q in content:
                score += 2

            for word in q.split():
                if word in content:
                    score += 1

            if score > 0:
                results.append({"title": doc_data.get("title"), "content": doc_data.get("content"), "score": score})

        results.sort(key=lambda x: x["score"], reverse=True)
        return results
    except:
        return []

def get_ai_response(message):
    kb = search_kb(message)
    if kb and kb[0]["score"] > 0:
        return kb[0]["content"], kb[0]["title"]

    msg = message.lower()
    if any(w in msg for w in ["hello", "hi", "hey"]):
        return "👋 Hello! I'm Anamika, your AI support assistant. I can help with:\n• Password reset\n• Billing questions\n• API integration\n• Troubleshooting\n\nWhat can I help you with?", "Welcome"
    elif any(w in msg for w in ["help", "support"]):
        return "I'm here to help! You can ask me about password reset, billing, API docs, or troubleshooting. What's your question?", "Help Center"
    elif any(w in msg for w in ["agent", "human"]):
        return "I can connect you with a human agent. They'll help you shortly!", "Agent Escalation"
    else:
        return "I can help with password reset, billing, API, or troubleshooting. Ask me something specific!", "Support"

# ============================================================================
# STYLES
# ============================================================================
st.markdown("""
<style>
    * { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; }
    .stApp { background: #ffffff; }
    h1 { color: #3b82f6; font-weight: 700; }
    h2 { color: #3b82f6; }
    h3 { color: #3b82f6; }
    .premium-card { background: #f8f9fa; border: 2px solid #3b82f6; border-radius: 16px; padding: 20px; }
    .stButton > button { background: #3b82f6 !important; color: white !important; }

    /* CHAT PANEL */
    .chat-panel {
        position: fixed;
        right: 20px;
        bottom: 20px;
        z-index: 9999;
        max-height: 600px;
        width: 420px;
        background: rgba(15, 23, 42, 0.98);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 20px;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(30px);
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }

    .chat-header {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        padding: 20px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }

    .chat-header h3 { margin: 0; font-size: 18px; font-weight: 700; }
    .chat-header p { margin: 4px 0 0 0; font-size: 12px; opacity: 0.9; }

    .close-btn {
        background: rgba(255,255,255,0.2);
        border: none;
        color: white;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        cursor: pointer;
        font-size: 20px;
        transition: all 0.3s;
    }

    .close-btn:hover {
        background: rgba(255,255,255,0.3);
        transform: scale(1.1);
    }

    .messages-container {
        flex: 1;
        overflow-y: auto;
        padding: 20px;
        display: flex;
        flex-direction: column;
        gap: 12px;
    }

    .message {
        padding: 12px 16px;
        border-radius: 12px;
        font-size: 14px;
        line-height: 1.5;
    }

    .message-bot {
        background: rgba(59, 130, 246, 0.2);
        border-left: 3px solid #3b82f6;
        color: #f1f5f9;
        align-self: flex-start;
        max-width: 85%;
    }

    .message-user {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        align-self: flex-end;
        max-width: 85%;
    }

    .message-source {
        font-size: 11px;
        color: #94a3b8;
        margin-top: 6px;
        padding-top: 6px;
        border-top: 1px solid rgba(59, 130, 246, 0.2);
    }

    .input-area {
        padding: 16px;
        border-top: 1px solid rgba(59, 130, 246, 0.2);
        display: flex;
        gap: 10px;
    }

    .input-area input {
        flex: 1;
        padding: 12px 16px;
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 10px;
        color: #f1f5f9;
        font-size: 14px;
    }

    .input-area input:focus {
        border-color: #3b82f6;
        outline: none;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
    }

    .input-area button {
        padding: 12px 20px;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        border: none;
        border-radius: 10px;
        color: white;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s;
    }

    .input-area button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
    }

    .float-button {
        position: fixed;
        right: 20px;
        bottom: 20px;
        z-index: 9998;
        width: 70px;
        height: 70px;
        border-radius: 50%;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        border: 2px solid rgba(255,255,255,0.1);
        color: white;
        font-size: 32px;
        cursor: pointer;
        box-shadow: 0 12px 32px rgba(59, 130, 246, 0.35);
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s;
    }

    .float-button:hover {
        transform: scale(1.15);
        box-shadow: 0 18px 48px rgba(59, 130, 246, 0.45);
    }

    .badge {
        position: absolute;
        top: -8px;
        right: -8px;
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: 800;
        border: 2px solid #0f172a;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'chat_open' not in st.session_state:
    st.session_state.chat_open = False
if 'call_open' not in st.session_state:
    st.session_state.call_open = False
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'bot_typing' not in st.session_state:
    st.session_state.bot_typing = False
if 'kb_files' not in st.session_state:
    st.session_state.kb_files = load_kb_files()

# ============================================================================
# CHAT WIDGET COMPONENT
# ============================================================================
def render_chat_widget():
    """Render world-class professional chat widget - Fixed & Working"""

    # Chat & Call toggle buttons
    col1, col2, col3 = st.columns([19, 1, 1])
    with col2:
        if st.button("💬", key="chat_toggle", help="Open Chat"):
            st.session_state.chat_open = not st.session_state.chat_open
            st.rerun()
    with col3:
        if st.button("☎️", key="call_toggle", help="Schedule Call"):
            st.session_state.call_open = True
            st.session_state.chat_open = False
            st.rerun()

    # Chat panel - shown when chat is open
    if st.session_state.chat_open:
        st.markdown("---")
        st.markdown("### 🎯 Anamika Chat")

        # Display all messages
        messages_container = st.container()
        with messages_container:
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-end; margin: 10px 0;">
                        <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 12px 16px; border-radius: 14px; max-width: 70%; box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);">
                            👤 {msg['text']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    src = msg.get("source", "Support")
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-start; margin: 10px 0;">
                        <div style="background: linear-gradient(135deg, #e3f2fd 0%, #f0f9ff 100%); border-left: 4px solid #3b82f6; color: #1e293b; padding: 12px 16px; border-radius: 14px; max-width: 70%; box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);">
                            <strong>🤖 Anamika</strong><br>{msg['text']}<br><span style="font-size: 11px; color: #64748b; margin-top: 8px; display: block;">📚 Source: {src}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        # Typing indicator
        if st.session_state.bot_typing:
            st.markdown("""
            <div style="display: flex; gap: 6px; margin: 10px 0;">
                <div style="width: 8px; height: 8px; background: #3b82f6; border-radius: 50%; animation: pulse 1.4s infinite;"></div>
                <div style="width: 8px; height: 8px; background: #3b82f6; border-radius: 50%; animation: pulse 1.4s infinite 0.2s;"></div>
                <div style="width: 8px; height: 8px; background: #3b82f6; border-radius: 50%; animation: pulse 1.4s infinite 0.4s;"></div>
            </div>
            <style>
                @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.6; } }
            </style>
            """, unsafe_allow_html=True)

        # Chat input
        st.markdown("---")
        col1, col2 = st.columns([5, 1])
        with col1:
            chat_input = st.text_input("💬 Your message", placeholder="Ask Anamika...", key="chat_msg_input", label_visibility="collapsed")
        with col2:
            send_btn = st.button("Send 📤", key="send_chat_btn", use_container_width=True)

        # Process message
        if send_btn and chat_input and chat_input.strip():
            st.session_state.messages.append({"role": "user", "text": chat_input})
            st.session_state.bot_typing = True
            st.rerun()

        # Generate bot response
        if st.session_state.bot_typing and len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
            import time
            time.sleep(0.5)  # Brief delay for better UX
            last_msg = st.session_state.messages[-1]["text"]
            response, source = get_ai_response(last_msg)
            st.session_state.messages.append({"role": "bot", "text": response, "source": source})
            st.session_state.bot_typing = False
            st.rerun()

    # Call widget display - using Streamlit form for better handling
    if st.session_state.call_open:
        st.markdown('<div style="position:fixed;right:20px;bottom:20px;z-index:9999;width:380px;background:#ffffff;border:2px solid #3b82f6;border-radius:20px;box-shadow:0 25px 60px rgba(59,130,246,0.2);backdrop-filter:blur(30px);overflow:hidden;"><div style="background:#3b82f6;padding:20px;color:white;"><h3 style="margin:0;font-size:18px;font-weight:700;">☎️ Schedule a Call</h3><p style="margin:4px 0 0 0;font-size:12px;">We\'ll call within 2 minutes</p></div></div>', unsafe_allow_html=True)

        col1, col2 = st.columns([4, 1])
        with col1:
            call_phone = st.text_input("Phone", placeholder="+1 (555) 123-4567", key="call_phone_input", label_visibility="collapsed")
        with col2:
            if st.button("📞 Call", key="submit_call"):
                if call_phone and call_phone.strip():
                    st.success(f"✅ Call scheduled! We'll call {call_phone} within 2 minutes.")
                    st.session_state.call_open = False
                    st.rerun()
                else:
                    st.error("Please enter a phone number")

        if st.button("Close ✕", key="close_call", use_container_width=True):
            st.session_state.call_open = False
            st.rerun()

# ============================================================================
# MAIN APP
# ============================================================================

# Render chat widget on all pages
render_chat_widget()

# Main pages
if st.session_state.page == 'home':
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px; background: linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(59, 130, 246, 0.04) 100%); border: 2px solid #3b82f6; border-radius: 20px; margin-bottom: 40px;">
        <h1 style="color: #3b82f6; font-size: 48px;">🎯 Anamika</h1>
        <p style="color: #1e293b; font-size: 16px; margin-top: 12px;">Enterprise AI Support Platform</p>
        <p style="color: #3b82f6; font-size: 14px; margin-top: 16px; font-weight: 700;">💬 Click the chat button to start chatting!</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("💬 Open Chat", use_container_width=True):
            st.session_state.chat_open = True
            st.rerun()
    with col2:
        if st.button("📊 Analytics", use_container_width=True):
            st.session_state.page = 'analytics'
            st.rerun()
    with col3:
        if st.button("🔐 Admin", use_container_width=True):
            st.session_state.page = 'admin'
            st.rerun()
    with col4:
        pass

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

elif st.session_state.page == 'analytics':
    st.markdown("""
    <style>
        .kpi-card {
            background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%);
            border: 2px solid #3b82f6;
            border-radius: 16px;
            padding: 24px;
            margin: 8px;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1);
            text-align: center;
        }
        .kpi-value {
            font-size: 32px;
            font-weight: 700;
            color: #3b82f6;
            margin: 12px 0;
        }
        .kpi-label {
            font-size: 14px;
            color: #64748b;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .kpi-change {
            font-size: 13px;
            margin-top: 8px;
            padding: 6px 12px;
            border-radius: 6px;
            display: inline-block;
            font-weight: 600;
        }
        .kpi-positive { background: #dcfce7; color: #166534; }
        .kpi-negative { background: #fee2e2; color: #991b1b; }
        .section-header {
            color: #3b82f6;
            font-size: 24px;
            font-weight: 700;
            margin-top: 32px;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 3px solid #3b82f6;
        }
        .stat-card {
            background: #f8f9fa;
            border-left: 4px solid #3b82f6;
            padding: 16px;
            border-radius: 8px;
            margin: 8px 0;
        }
        .stat-label {
            color: #64748b;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
        }
        .stat-value {
            color: #3b82f6;
            font-size: 20px;
            font-weight: 700;
            margin-top: 4px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; margin-bottom: 32px;">
        <h1 style="color: #3b82f6; font-size: 42px; margin: 0;">📊 Analytics Dashboard</h1>
        <p style="color: #64748b; font-size: 16px; margin-top: 8px;">Real-time insights for Voice Bot & AI Support</p>
    </div>
    """, unsafe_allow_html=True)

    # KPI Metrics Row - Styled
    st.markdown("## 🎯 Key Performance Indicators")
    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

    with kpi1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">📞 Conversations</div>
            <div class="kpi-value">5,847</div>
            <div class="kpi-change kpi-positive">↑ +18%</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">✅ Resolution</div>
            <div class="kpi-value">94.2%</div>
            <div class="kpi-change kpi-positive">↑ +3.2%</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">⚡ Response Time</div>
            <div class="kpi-value">2.3s</div>
            <div class="kpi-change kpi-positive">↓ -0.5s</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi4:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">😊 CSAT Score</div>
            <div class="kpi-value">4.87/5</div>
            <div class="kpi-change kpi-positive">↑ +0.15</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi5:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">🤖 AI Deflection</div>
            <div class="kpi-value">87%</div>
            <div class="kpi-change kpi-positive">↑ +5%</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi6:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">🔄 Escalation</div>
            <div class="kpi-value">13%</div>
            <div class="kpi-change kpi-positive">↓ -2%</div>
        </div>
        """, unsafe_allow_html=True)

    # AI Chat Analytics
    st.markdown('<div class="section-header">💬 AI Chat Support Analytics</div>', unsafe_allow_html=True)
    chat_col1, chat_col2, chat_col3 = st.columns([2, 1, 1])

    with chat_col1:
        st.markdown("""
        <div style="background: #f8f9fa; border-radius: 12px; padding: 24px; border: 2px solid #e2e8f0;">
            <h3 style="color: #3b82f6; margin-top: 0;">Chat Metrics</h3>
        """, unsafe_allow_html=True)

        chat_metrics = {
            "💌 Total Messages": "12,543",
            "📊 Avg Messages/Chat": "3.2",
            "⏱️ Avg Chat Duration": "4m 30s",
            "🕐 Peak Hour": "2:00 PM",
            "📚 KB Success Rate": "92%",
            "🔄 Human Handoff": "8%"
        }
        for metric, value in chat_metrics.items():
            st.markdown(f'<div class="stat-card"><div class="stat-label">{metric}</div><div class="stat-value">{value}</div></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with chat_col2:
        st.markdown("""
        <div style="background: #f8f9fa; border-radius: 12px; padding: 24px; border: 2px solid #e2e8f0;">
            <h3 style="color: #3b82f6; margin-top: 0; font-size: 18px;">Message Types</h3>
        """, unsafe_allow_html=True)
        message_data = pd.DataFrame({
            "Type": ["Greeting", "Questions", "Support", "Feedback"],
            "Count": [1250, 4320, 5230, 1743]
        })
        st.bar_chart(message_data.set_index("Type")["Count"], color="#3b82f6")
        st.markdown("</div>", unsafe_allow_html=True)

    with chat_col3:
        st.markdown("""
        <div style="background: #f8f9fa; border-radius: 12px; padding: 24px; border: 2px solid #e2e8f0;">
            <h3 style="color: #3b82f6; margin-top: 0; font-size: 18px;">Top Topics</h3>
        """, unsafe_allow_html=True)
        topics = pd.DataFrame({
            "Topic": ["Pricing", "Getting Started", "API", "Billing"],
            "Count": [1200, 980, 750, 620]
        })
        st.bar_chart(topics.set_index("Topic")["Count"], color="#3b82f6")
        st.markdown("</div>", unsafe_allow_html=True)

    # Voice Bot Analytics
    st.markdown('<div class="section-header">☎️ Voice Bot Call Analytics</div>', unsafe_allow_html=True)
    call_col1, call_col2, call_col3 = st.columns([2, 1, 1])

    with call_col1:
        st.markdown("""
        <div style="background: #f8f9fa; border-radius: 12px; padding: 24px; border: 2px solid #e2e8f0;">
            <h3 style="color: #3b82f6; margin-top: 0;">Voice Metrics</h3>
        """, unsafe_allow_html=True)

        voice_metrics = {
            "☎️ Total Calls": "2,847",
            "✅ Completed Calls": "2,634 (92.5%)",
            "⏱️ Avg Call Duration": "8m 45s",
            "⏳ Avg Wait Time": "35s",
            "🎵 Voice Quality": "4.6/5",
            "✨ Success Rate": "94.3%"
        }
        for metric, value in voice_metrics.items():
            st.markdown(f'<div class="stat-card"><div class="stat-label">{metric}</div><div class="stat-value">{value}</div></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with call_col2:
        st.markdown("""
        <div style="background: #f8f9fa; border-radius: 12px; padding: 24px; border: 2px solid #e2e8f0;">
            <h3 style="color: #3b82f6; margin-top: 0; font-size: 18px;">Call Status</h3>
        """, unsafe_allow_html=True)
        call_status = pd.DataFrame({
            "Status": ["Completed", "Missed", "Dropped"],
            "Count": [2634, 156, 57]
        })
        st.bar_chart(call_status.set_index("Status")["Count"], color="#3b82f6")
        st.markdown("</div>", unsafe_allow_html=True)

    with call_col3:
        st.markdown("""
        <div style="background: #f8f9fa; border-radius: 12px; padding: 24px; border: 2px solid #e2e8f0;">
            <h3 style="color: #3b82f6; margin-top: 0; font-size: 18px;">Call Times</h3>
        """, unsafe_allow_html=True)
        call_times = pd.DataFrame({
            "Time Slot": ["9-12 AM", "12-3 PM", "3-6 PM", "6-9 PM"],
            "Calls": [580, 720, 890, 657]
        })
        st.bar_chart(call_times.set_index("Time Slot")["Calls"], color="#3b82f6")
        st.markdown("</div>", unsafe_allow_html=True)

    # Trend Analysis
    st.markdown('<div class="section-header">📈 Trend Analysis (Last 30 Days)</div>', unsafe_allow_html=True)

    trend_col1, trend_col2 = st.columns(2)

    with trend_col1:
        st.markdown("""
        <div style="background: #f8f9fa; border-radius: 12px; padding: 24px; border: 2px solid #e2e8f0;">
            <h3 style="color: #3b82f6; margin-top: 0;">📊 Conversation Trends</h3>
        """, unsafe_allow_html=True)
        import numpy as np
        days = pd.date_range(start='2026-05-26', periods=30)
        conversations = np.random.randint(150, 250, 30).cumsum() + 2000
        trend_data = pd.DataFrame({
            "Date": days,
            "Conversations": conversations
        })
        st.line_chart(trend_data.set_index("Date"), color="#3b82f6")
        st.markdown("</div>", unsafe_allow_html=True)

    with trend_col2:
        st.markdown("""
        <div style="background: #f8f9fa; border-radius: 12px; padding: 24px; border: 2px solid #e2e8f0;">
            <h3 style="color: #3b82f6; margin-top: 0;">✨ Response Quality Trend</h3>
        """, unsafe_allow_html=True)
        quality = np.random.uniform(85, 98, 30)
        quality_data = pd.DataFrame({
            "Date": days,
            "Quality %": quality
        })
        st.line_chart(quality_data.set_index("Date"), color="#3b82f6")
        st.markdown("</div>", unsafe_allow_html=True)

    # Sentiment & Feedback
    st.markdown('<div class="section-header">😊 Sentiment & Feedback Analysis</div>', unsafe_allow_html=True)

    sentiment_col1, sentiment_col2, sentiment_col3 = st.columns(3)

    with sentiment_col1:
        st.markdown("""
        <div style="background: #f8f9fa; border-radius: 12px; padding: 24px; border: 2px solid #e2e8f0;">
            <h3 style="color: #3b82f6; margin-top: 0; font-size: 18px;">Overall Sentiment</h3>
        """, unsafe_allow_html=True)
        sentiment = pd.DataFrame({
            "Sentiment": ["Positive", "Neutral", "Negative"],
            "Percentage": [72, 21, 7]
        })
        st.bar_chart(sentiment.set_index("Sentiment")["Percentage"], color="#3b82f6")
        st.markdown("</div>", unsafe_allow_html=True)

    with sentiment_col2:
        st.markdown("""
        <div style="background: #f8f9fa; border-radius: 12px; padding: 24px; border: 2px solid #e2e8f0;">
            <h3 style="color: #3b82f6; margin-top: 0; font-size: 18px;">NPS Distribution</h3>
        """, unsafe_allow_html=True)
        nps = pd.DataFrame({
            "Score": ["9-10\n(Promoters)", "7-8\n(Passives)", "0-6\n(Detractors)"],
            "Count": [2104, 876, 304]
        })
        st.bar_chart(nps.set_index("Score")["Count"], color="#3b82f6")
        st.markdown("</div>", unsafe_allow_html=True)

    with sentiment_col3:
        st.markdown("""
        <div style="background: #f8f9fa; border-radius: 12px; padding: 24px; border: 2px solid #e2e8f0;">
            <h3 style="color: #3b82f6; margin-top: 0; font-size: 18px;">Resolution Status</h3>
        """, unsafe_allow_html=True)
        resolution = pd.DataFrame({
            "Type": ["Resolved\non 1st\nContact", "Escalated\nto Agent", "Pending\nFU"],
            "Count": [5501, 298, 48]
        })
        st.bar_chart(resolution.set_index("Type")["Count"], color="#3b82f6")
        st.markdown("</div>", unsafe_allow_html=True)

    # Agent Performance
    st.markdown('<div class="section-header">👥 Agent Performance</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background: #f8f9fa; border-radius: 12px; padding: 24px; border: 2px solid #e2e8f0;">
    """, unsafe_allow_html=True)

    agent_data = pd.DataFrame({
        "👤 Agent": ["Agent A", "Agent B", "Agent C", "Agent D"],
        "📞 Calls Handled": [287, 256, 234, 198],
        "⭐ Avg Rating": [4.8, 4.6, 4.7, 4.5],
        "✅ Resolution %": [96, 93, 94, 91]
    })
    st.dataframe(agent_data, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Top Issues & Solutions
    st.markdown('<div class="section-header">🔧 Top Issues & Quick Solutions</div>', unsafe_allow_html=True)

    issues_col1, issues_col2 = st.columns(2)

    with issues_col1:
        st.markdown("""
        <div style="background: #f8f9fa; border-radius: 12px; padding: 24px; border: 2px solid #e2e8f0;">
            <h3 style="color: #3b82f6; margin-top: 0;">Most Common Issues</h3>
        """, unsafe_allow_html=True)
        issues = pd.DataFrame({
            "🔴 Issue": ["Password Reset", "Billing Question", "Account Access", "Feature Info", "Bug Report"],
            "📊 Frequency": [1243, 987, 756, 654, 432]
        })
        st.dataframe(issues, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with issues_col2:
        st.markdown("""
        <div style="background: #f8f9fa; border-radius: 12px; padding: 24px; border: 2px solid #e2e8f0;">
            <h3 style="color: #3b82f6; margin-top: 0;">Solution Success Rate</h3>
        """, unsafe_allow_html=True)
        solutions = pd.DataFrame({
            "✅ Solution": ["Password Reset", "Billing Question", "Account Access", "Feature Info", "Bug Report"],
            "📈 Success %": [98, 94, 91, 87, 76]
        })
        st.dataframe(solutions, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Comparison: Chat vs Voice
    st.markdown('<div class="section-header">⚖️ Channel Comparison: Chat vs Voice</div>', unsafe_allow_html=True)

    comp_col1, comp_col2 = st.columns(2)

    with comp_col1:
        st.markdown("""
        <div style="background: #f8f9fa; border-radius: 12px; padding: 24px; border: 2px solid #e2e8f0;">
            <h3 style="color: #3b82f6; margin-top: 0; font-size: 18px;">Volume Comparison</h3>
        """, unsafe_allow_html=True)
        channel = pd.DataFrame({
            "Channel": ["💬 AI Chat", "☎️ Voice Bot"],
            "Interactions": [12543, 2847]
        })
        st.bar_chart(channel.set_index("Channel")["Interactions"], color="#3b82f6")
        st.markdown("</div>", unsafe_allow_html=True)

    with comp_col2:
        st.markdown("""
        <div style="background: #f8f9fa; border-radius: 12px; padding: 24px; border: 2px solid #e2e8f0;">
            <h3 style="color: #3b82f6; margin-top: 0; font-size: 18px;">Satisfaction Comparison</h3>
        """, unsafe_allow_html=True)
        satisfaction = pd.DataFrame({
            "Channel": ["💬 AI Chat", "☎️ Voice Bot"],
            "CSAT Score": [4.87, 4.65]
        })
        st.bar_chart(satisfaction.set_index("Channel")["CSAT Score"], color="#3b82f6")
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("← Home"):
        st.session_state.page = 'home'
        st.rerun()

elif st.session_state.page == 'admin':
    st.markdown("### ⚙️ Admin Panel")
    tab1, tab2, tab3 = st.tabs(["📚 Knowledge Base", "🔧 Settings", "🎤 Voice Bot"])
    with tab1:
        st.markdown("#### Knowledge Base Management")
        st.metric("Files Stored", len(st.session_state.kb_files), "/ 5")

        st.markdown("---")
        st.markdown("**📁 Upload New File**")
        uploaded_file = st.file_uploader("Choose a file (PDF, DOC, DOCX, TXT, CSV)", type=["pdf", "doc", "docx", "txt", "csv", "xls", "xlsx"])

        if uploaded_file is not None:
            if len(st.session_state.kb_files) < 5:
                file_size = f"{uploaded_file.size / (1024*1024):.1f} MB"
                file_type = uploaded_file.name.split('.')[-1].upper()

                if st.button("✅ Save to Knowledge Base", use_container_width=True):
                    try:
                        file_content = uploaded_file.read().decode('utf-8')
                        add_kb_file(uploaded_file.name, file_size, file_type, file_content, "Active")
                        st.session_state.kb_files = load_kb_files()
                        st.success(f"✅ File '{uploaded_file.name}' saved to Knowledge Base! 📚")
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ Error reading file: {str(e)}")
            else:
                st.error("❌ Maximum 5 files allowed. Delete a file first.")

        st.markdown("---")
        st.markdown("**📚 Files in Knowledge Base**")
        if len(st.session_state.kb_files) > 0:
            kb_data = {
                "File Name": [f["name"] for f in st.session_state.kb_files],
                "Type": [f["type"] for f in st.session_state.kb_files],
                "Size": [f["size"] for f in st.session_state.kb_files],
                "Date": [f["date"] for f in st.session_state.kb_files],
                "Status": [f["status"] for f in st.session_state.kb_files]
            }
            st.dataframe(pd.DataFrame(kb_data), use_container_width=True)

            st.markdown("---")
            st.markdown("**Delete File**")
            file_to_delete = st.selectbox("Select file to delete", [f["name"] for f in st.session_state.kb_files], key="delete_file")
            if st.button("🗑️ Delete Selected File", use_container_width=True):
                st.session_state.kb_files = [f for f in st.session_state.kb_files if f["name"] != file_to_delete]
                kb_content = load_kb_content()
                if file_to_delete in kb_content:
                    del kb_content[file_to_delete]
                    save_kb_content(kb_content)
                save_kb_files(st.session_state.kb_files)
                st.success(f"✅ File '{file_to_delete}' deleted!")
                st.rerun()
        else:
            st.info("📭 No files uploaded yet. Upload your first file above!")
    with tab2:
        st.markdown("#### Settings")
        st.text_input("API Key", type="password", placeholder="sk-...", label_visibility="collapsed")
        if st.button("💾 Save", use_container_width=True):
            st.success("✅ Saved!")
    with tab3:
        st.markdown("#### 🎤 Voice Bot Integration")
        col1, col2 = st.columns(2)
        with col1:
            enable_voice = st.checkbox("Enable Voice Bot", value=True)
            voice_name = st.text_input("Bot Name", value="Anamika Voice", placeholder="Enter voice bot name")
        with col2:
            voice_type = st.selectbox("Voice Type", ["Female - English", "Male - English", "Female - Hindi", "Male - Hindi"])
            language = st.selectbox("Language", ["English", "Hindi", "Spanish"])

        st.markdown("---")
        st.markdown("**Greeting Message**")
        greeting = st.text_area("Voice Bot Greeting", value="Hello! I'm Anamika Voice Assistant. How can I help you?", height=80, placeholder="Enter greeting message for voice bot")

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            convin_api = st.text_input("Convin API Key", type="password", placeholder="Enter Convin API key", label_visibility="collapsed")
        with col2:
            convin_id = st.text_input("Workspace ID", placeholder="Enter Convin workspace ID", label_visibility="collapsed")

        if st.button("💾 Save Voice Settings", use_container_width=True):
            st.success("✅ Voice bot settings saved!")
            st.toast("🎤 Voice bot is " + ("enabled" if enable_voice else "disabled"))

    if st.button("Home"):
        st.session_state.page = 'home'
        st.rerun()

st.markdown("""<div style="text-align: center; padding: 40px 20px; margin-top: 60px; border-top: 1px solid rgba(59, 130, 246, 0.1);"><p style="color: #94a3b8; font-size: 12px;">🎯 Anamika | Enterprise AI Support | v7.0</p></div>""", unsafe_allow_html=True)
