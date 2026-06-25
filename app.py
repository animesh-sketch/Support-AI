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
if 'call_open' not in st.session_state:
    st.session_state.call_open = False
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'kb_files' not in st.session_state:
    st.session_state.kb_files = load_kb_files()

# ============================================================================
# CHAT WIDGET COMPONENT
# ============================================================================
def render_chat_widget():
    """Render the professional chat widget"""

    # Chat & Call toggle buttons
    col1, col2, col3 = st.columns([19, 1, 1])
    with col2:
        if st.button("💬", key="chat_toggle", help="Toggle Chat"):
            st.session_state.chat_open = not st.session_state.chat_open
            st.rerun()
    with col3:
        if st.button("☎️", key="call_toggle", help="Schedule Call"):
            st.session_state.call_open = True
            st.session_state.chat_open = False
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

    # Call widget display
    if st.session_state.call_open:
        st.markdown('<div style="position:fixed;right:20px;bottom:20px;z-index:9999;width:380px;background:rgba(15,23,42,0.98);border:1px solid rgba(34,197,94,0.3);border-radius:20px;box-shadow:0 25px 60px rgba(0,0,0,0.6);backdrop-filter:blur(30px);display:flex;flex-direction:column;overflow:hidden;"><div style="background:linear-gradient(135deg,#22c55e 0%,#16a34a 100%);padding:20px;color:white;"><h3 style="margin:0;font-size:18px;font-weight:700;">☎️ Schedule Call</h3><p style="margin:4px 0 0 0;font-size:12px;">Quick callback</p></div><div style="padding:20px;"><p style="color:#94a3b8;font-size:13px;margin-bottom:12px;">Get a call from our support team</p></div></div>', unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])
        with col1:
            phone = st.text_input("Phone Number", placeholder="+1 (555) 000-0000", label_visibility="collapsed")
        with col2:
            if st.button("📞 Call Me", use_container_width=True):
                if phone and phone.strip():
                    st.success(f"✅ Call scheduled! We'll call {phone} within 2 minutes")
                    st.session_state.call_open = False
                    st.rerun()

        if st.button("Close Call", key="close_call"):
            st.session_state.call_open = False
            st.rerun()

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
