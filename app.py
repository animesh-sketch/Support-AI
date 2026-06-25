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

def add_kb_file(name, size, file_type, status="Active"):
    files = load_kb_files()
    if len(files) < 5:
        files.append({"name": name, "size": size, "type": file_type, "date": datetime.now().strftime("%Y-%m-%d"), "status": status})
        save_kb_files(files)
        return True
    return False

KB_CONTENT = {
    "Password Reset Guide.pdf": {"title": "Password Reset Guide", "keywords": ["password", "reset", "forgot", "login"], "content": "To reset your password:\n1. Click 'Forgot Password' on login page\n2. Enter your email address\n3. Check email for reset link (arrives in 2 minutes)\n4. Click the link and create a new password\n5. Use new password to login"},
    "Billing FAQ.docx": {"title": "Billing FAQ", "keywords": ["billing", "payment", "invoice", "subscription", "plan"], "content": "We accept: Credit cards (Visa, Mastercard, AmEx), PayPal, Bank transfers\nBilling occurs on the same date each month\nYou can change plans anytime - changes take effect next billing cycle\nRefund policy: 30 days on annual plans, 7 days on monthly plans"},
    "API Documentation.pdf": {"title": "API Documentation", "keywords": ["api", "developer", "integration", "endpoint"], "content": "Base URL: https://api.anamika.ai/v1\nAuth: Bearer token in Authorization header\nEndpoints:\n- POST /chat - Send message\n- GET /conversations - List conversations\nRate Limits: 100 req/min (standard), 1000 req/min (enterprise)"},
    "Troubleshooting.txt": {"title": "Troubleshooting", "keywords": ["error", "problem", "issue", "not working", "fix"], "content": "Widget not loading? Clear browser cache and enable JavaScript\nChat not responding? Check internet connection, refresh page\nAPI errors? Verify authentication token and check rate limits"}
}

def search_kb(query):
    try:
        q = query.lower().strip()
        results = []
        for doc_name, doc_data in KB_CONTENT.items():
            score = 0
            for kw in doc_data.get("keywords", []):
                if kw in q:
                    score += 3
            if doc_data.get("title", "").lower() in q:
                score += 4
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
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%); }
    h1 { background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .premium-card { background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 16px; padding: 20px; }
    .stButton > button { background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important; }

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
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'kb_files' not in st.session_state:
    st.session_state.kb_files = load_kb_files()
    if len(st.session_state.kb_files) == 0:
        add_kb_file("Password Reset Guide.pdf", "2.3 MB", "PDF", "Active")
        add_kb_file("Billing FAQ.docx", "1.8 MB", "DOCX", "Active")
        st.session_state.kb_files = load_kb_files()

# ============================================================================
# CHAT WIDGET COMPONENT
# ============================================================================
def render_chat_widget():
    """Render the professional chat widget"""

    # Chat toggle button
    col1, col2 = st.columns([20, 1])
    with col2:
        if st.button("💬", key="chat_toggle", help="Toggle Chat"):
            st.session_state.chat_open = not st.session_state.chat_open
            st.rerun()

    # Chat widget display
    if st.session_state.chat_open:
        st.markdown('<div style="position:fixed;right:20px;bottom:20px;z-index:9999;width:420px;max-height:600px;background:rgba(15,23,42,0.98);border:1px solid rgba(59,130,246,0.3);border-radius:20px;box-shadow:0 25px 60px rgba(0,0,0,0.6);backdrop-filter:blur(30px);display:flex;flex-direction:column;overflow:hidden;"><div style="background:linear-gradient(135deg,#3b82f6 0%,#8b5cf6 100%);padding:20px;color:white;"><h3 style="margin:0;font-size:18px;font-weight:700;">🎯 Anamika</h3><p style="margin:4px 0 0 0;font-size:12px;">AI Support</p></div><div id="chat-messages" style="flex:1;overflow-y:auto;padding:20px;display:flex;flex-direction:column;gap:12px;height:350px;"></div><div style="padding:16px;border-top:1px solid rgba(59,130,246,0.2);display:flex;gap:10px;"><input type="text" id="chat-input" placeholder="Ask..." style="flex:1;padding:10px;background:rgba(30,41,59,0.8);border:1px solid rgba(59,130,246,0.3);border-radius:8px;color:#f1f5f9;font-size:13px;"/><button onclick="sendChatMsg()" style="padding:10px 16px;background:linear-gradient(135deg,#3b82f6,#8b5cf6);border:none;border-radius:8px;color:white;cursor:pointer;font-weight:600;">📤</button></div></div>', unsafe_allow_html=True)

        msgs_html = ""
        for msg in st.session_state.messages:
            if msg["role"] == "bot":
                txt = msg["text"].replace('"', '&quot;').replace('\n', '<br>')
                src = msg.get("source", "Support")
                msgs_html += f'<div style="padding:10px;border-radius:10px;background:rgba(59,130,246,0.2);border-left:3px solid #3b82f6;color:#f1f5f9;max-width:85%;"><strong>🤖</strong><br>{txt}<br><span style="font-size:11px;color:#94a3b8;margin-top:4px;">📚 {src}</span></div>'
            else:
                txt = msg["text"].replace('"', '&quot;')
                msgs_html += f'<div style="padding:10px;border-radius:10px;background:linear-gradient(135deg,#3b82f6,#8b5cf6);color:white;max-width:85%;align-self:flex-end;">{txt}</div>'

        st.markdown(f'<script>let m=document.getElementById("chat-messages");m.innerHTML="{msgs_html}";m.scrollTop=m.scrollHeight;function sendChatMsg(){{let i=document.getElementById("chat-input");if(i.value.trim()){{document.getElementById("send-chat").click();i.value=""}}}}; document.getElementById("chat-input").addEventListener("keypress",e=>{{if(e.key==="Enter")sendChatMsg()}});</script>', unsafe_allow_html=True)

        if st.button("Send", key="send-chat"):
            pass

# ============================================================================
# MAIN APP
# ============================================================================

# Render chat widget on all pages
render_chat_widget()

# Hidden input for chat
col1, col2 = st.columns([5, 1])
with col1:
    chat_msg = st.text_input("Message", key="chat_input", label_visibility="collapsed")
with col2:
    if st.button("Send", key="send_main"):
        if chat_msg and chat_msg.strip():
            st.session_state.messages.append({"role": "user", "text": chat_msg})
            response, source = get_ai_response(chat_msg)
            st.session_state.messages.append({"role": "bot", "text": response, "source": source})
            st.rerun()

# Main pages
if st.session_state.page == 'home':
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px; background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%); border-radius: 20px; margin-bottom: 40px;">
        <h1>🎯 Anamika</h1>
        <p style="color: #94a3b8; font-size: 16px; margin-top: 12px;">Enterprise AI Support Platform</p>
        <p style="color: #22c55e; font-size: 14px; margin-top: 16px; font-weight: 700;">💬 Click the chat button to start chatting!</p>
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
    st.markdown("### 📊 Analytics Dashboard")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Conversations", "3,847", "+15%")
    with col2:
        st.metric("Avg Resolution", "12m 30s", "-2m")
    with col3:
        st.metric("Escalation Rate", "13%", "-2%")
    if st.button("Home"):
        st.session_state.page = 'home'
        st.rerun()

elif st.session_state.page == 'admin':
    st.markdown("### ⚙️ Admin Panel")
    tab1, tab2 = st.tabs(["📚 Knowledge Base", "🔧 Settings"])
    with tab1:
        st.markdown("#### Knowledge Base Management")
        st.metric("Files Stored", len(st.session_state.kb_files), "/ 5")
        if len(st.session_state.kb_files) > 0:
            kb_data = {"Name": [f["name"] for f in st.session_state.kb_files], "Type": [f["type"] for f in st.session_state.kb_files], "Size": [f["size"] for f in st.session_state.kb_files]}
            st.dataframe(pd.DataFrame(kb_data), use_container_width=True)
    with tab2:
        st.markdown("#### Settings")
        st.text_input("API Key", type="password", placeholder="sk-...", label_visibility="collapsed")
        if st.button("💾 Save", use_container_width=True):
            st.success("✅ Saved!")
    if st.button("Home"):
        st.session_state.page = 'home'
        st.rerun()

st.markdown("""<div style="text-align: center; padding: 40px 20px; margin-top: 60px; border-top: 1px solid rgba(59, 130, 246, 0.1);"><p style="color: #94a3b8; font-size: 12px;">🎯 Anamika | Enterprise AI Support | v7.0</p></div>""", unsafe_allow_html=True)
