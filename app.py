import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os

st.set_page_config(
    page_title="Anamika - Support Widget",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# KB STORAGE
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
        files.append({"name": name, "size": size, "type": file_type, "date": datetime.now().strftime("%Y-%m-%d"), "status": status, "id": len(files) + 1})
        save_kb_files(files)
        return True
    return False

def delete_kb_file(file_name):
    files = load_kb_files()
    files = [f for f in files if f["name"] != file_name]
    save_kb_files(files)

def get_kb_files():
    return load_kb_files()

# ============================================================================
# KNOWLEDGE BASE
# ============================================================================
KB_CONTENT = {
    "Password Reset Guide.pdf": {
        "title": "Password Reset Guide",
        "keywords": ["password", "reset", "forgot", "login", "account", "access"],
        "content": "To reset your password:\n1. Click 'Forgot Password' on login\n2. Enter your email\n3. Check email for reset link (2 min)\n4. Click link and create new password\n5. Login with new password"
    },
    "Billing FAQ.docx": {
        "title": "Billing FAQ",
        "keywords": ["billing", "payment", "invoice", "subscription", "charge", "plan", "pricing"],
        "content": "Payment Methods: Visa, Mastercard, AmEx, PayPal, Bank Transfer\nBilling: Same date each month\nChange Plan: Anytime, takes effect next cycle\nRefund: 30-day money-back on annual plans, 7-day on monthly"
    },
    "API Documentation.pdf": {
        "title": "API Documentation",
        "keywords": ["api", "developer", "integration", "endpoint", "code", "programming"],
        "content": "Base URL: https://api.anamika.ai/v1\nAuthentication: Bearer token in Authorization header\nEndpoints: POST /chat, GET /conversations, POST /escalate\nRate Limits: 100 req/min (standard), 1000 req/min (enterprise)"
    },
    "Troubleshooting Guide.txt": {
        "title": "Troubleshooting Guide",
        "keywords": ["troubleshoot", "error", "problem", "issue", "bug", "not working", "fix"],
        "content": "Widget Not Loading: Clear cache, enable JavaScript\nChat Not Responding: Check internet, refresh page\nAPI Errors: Verify token, check rate limits\nPerformance: Use modern browser, check resources"
    }
}

def search_kb(query):
    try:
        query_lower = query.lower().strip()
        results = []
        for doc_name, doc_data in KB_CONTENT.items():
            score = 0
            for keyword in doc_data.get("keywords", []):
                if keyword in query_lower:
                    score += 3
            if doc_data.get("title", "").lower() in query_lower:
                score += 4
            for word in query_lower.split():
                if len(word) > 2 and word in doc_data.get("content", "").lower():
                    score += 1
            if score > 0:
                results.append({"title": doc_data.get("title", "Unknown"), "content": doc_data.get("content", ""), "score": score})
        results.sort(key=lambda x: x.get("score", 0), reverse=True)
        return results
    except:
        return []

def get_response(msg):
    try:
        kb_results = search_kb(msg)
        if kb_results and kb_results[0].get("score", 0) > 0:
            return kb_results[0]["content"], kb_results[0]["title"]
        msg_lower = msg.lower().strip()
        if any(w in msg_lower for w in ["hello", "hi", "hey"]):
            return "👋 Hi! I'm Anamika. I can help with password reset, billing, API, or troubleshooting. What do you need?", "Welcome"
        elif any(w in msg_lower for w in ["help", "support"]):
            return "I'm here to help! Ask about: password reset, billing, API docs, or troubleshooting.", "Help"
        elif any(w in msg_lower for w in ["agent", "human"]):
            return "👤 Let me connect you with a human agent. They'll be available shortly.", "Agent"
        else:
            return "I can help with password reset, billing, API, or troubleshooting. Be more specific and I'll find the answer!", "Support"
    except:
        return "Error processing request. Let me connect you with an agent.", "Error"

# ============================================================================
# STYLES
# ============================================================================
st.markdown("""
<style>
    :root {
        --primary: #3b82f6;
        --secondary: #8b5cf6;
        --bg: #0f172a;
        --text: #f1f5f9;
    }
    * { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; }
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%); color: var(--text); }
    h1 { font-size: 48px !important; font-weight: 800 !important; background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
    h2, h3 { color: var(--text) !important; }
    .premium-card { background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 16px; padding: 20px; }
    .stButton > button { background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important; color: white !important; }
</style>

<style>
/* DRAGGABLE WIDGET */
#widget-container {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 9999;
    touch-action: none;
    cursor: move;
}
.widget-button {
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
.widget-button:hover {
    transform: scale(1.15);
    box-shadow: 0 18px 48px rgba(59, 130, 246, 0.45);
}
.widget-badge {
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
    box-shadow: 0 3px 12px rgba(239, 68, 68, 0.6);
    border: 2px solid rgba(15, 23, 42, 0.8);
}
.widget-chat {
    position: fixed;
    bottom: 100px;
    right: 20px;
    width: 380px;
    max-height: 500px;
    background: rgba(15, 23, 42, 0.98);
    border: 1px solid rgba(59, 130, 246, 0.3);
    border-radius: 16px;
    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(30px);
    z-index: 9998;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}
.widget-header {
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
    padding: 16px;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.widget-messages {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.msg-bot {
    background: rgba(59, 130, 246, 0.2);
    padding: 10px 12px;
    border-radius: 10px;
    border-left: 3px solid #3b82f6;
    max-width: 85%;
    font-size: 13px;
    color: var(--text);
    align-self: flex-start;
}
.msg-user {
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
    padding: 10px 12px;
    border-radius: 10px;
    max-width: 85%;
    font-size: 13px;
    color: white;
    align-self: flex-end;
}
.widget-input {
    padding: 12px;
    border-top: 1px solid rgba(59, 130, 246, 0.2);
    display: flex;
    gap: 8px;
}
.widget-input input {
    flex: 1;
    padding: 10px;
    background: rgba(30, 41, 59, 0.8);
    border: 1px solid rgba(59, 130, 246, 0.3);
    border-radius: 8px;
    color: var(--text);
    font-size: 13px;
}
.widget-input button {
    padding: 10px 14px;
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
    border: none;
    border-radius: 8px;
    color: white;
    cursor: pointer;
    font-weight: 600;
}
</style>

<div id="widget-container">
    <button class="widget-button" id="widget-btn" onclick="document.getElementById('widget-toggle').click()">
        🎯
        <span class="widget-badge">3</span>
    </button>
</div>

<script>
let container = document.getElementById('widget-container');
let isDragging = false;
let startX = 0;
let startY = 0;

container.addEventListener('mousedown', (e) => {
    isDragging = true;
    startX = e.clientX - container.offsetLeft;
    startY = e.clientY - container.offsetTop;
});

document.addEventListener('mousemove', (e) => {
    if (isDragging) {
        container.style.left = (e.clientX - startX) + 'px';
        container.style.bottom = 'auto';
        container.style.right = 'auto';
        container.style.top = (e.clientY - startY) + 'px';
    }
});

document.addEventListener('mouseup', () => {
    isDragging = false;
});
</script>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = [{"role": "bot", "text": "👋 Hi! How can I help?", "source": "Welcome"}]
if 'widget_open' not in st.session_state:
    st.session_state.widget_open = False
if 'kb_files' not in st.session_state:
    st.session_state.kb_files = get_kb_files()
    if len(st.session_state.kb_files) == 0:
        add_kb_file("Password Reset Guide.pdf", "2.3 MB", "PDF", "Active")
        add_kb_file("Billing FAQ.docx", "1.8 MB", "DOCX", "Active")
        st.session_state.kb_files = get_kb_files()

# ============================================================================
# WIDGET
# ============================================================================
st.markdown("""<script>
document.getElementById('widget-toggle').style.display = 'none';
</script>""", unsafe_allow_html=True)

# Widget toggle button (hidden)
col1, col2 = st.columns([20, 1])
with col2:
    if st.button("⚙️", key="widget_toggle"):
        st.session_state.widget_open = not st.session_state.widget_open
        st.rerun()

# Widget chat display
if st.session_state.widget_open:
    widget_html = """<div class="widget-chat" style="display: flex;">
        <div class="widget-header">
            <div><h3 style="margin:0; color:white; font-size:16px;">🎯 Anamika</h3>
            <p style="margin:4px 0 0 0; color:rgba(255,255,255,0.8); font-size:12px;">AI Support</p></div>
            <button onclick="document.getElementById('widget-toggle').click()" style="background:rgba(255,255,255,0.2); border:none; color:white; width:32px; height:32px; border-radius:50%; cursor:pointer; font-size:18px;">✕</button>
        </div>
        <div class="widget-messages" id="widget-msgs"></div>
        <div class="widget-input">
            <input type="text" id="widget-input" placeholder="Ask me..."/>
            <button onclick="sendWidget()">📤</button>
        </div>
    </div>"""

    st.markdown(widget_html, unsafe_allow_html=True)

    # Messages HTML
    msgs_html = ""
    for msg in st.session_state.chat_messages:
        if msg["role"] == "bot":
            msgs_html += f'<div class="msg-bot"><strong>🤖</strong><br>{msg["text"]}<br><span style="font-size:10px; color:#94a3b8;">📚 {msg.get("source", "Support")}</span></div>'
        else:
            msgs_html += f'<div class="msg-user">{msg["text"]}</div>'

    st.markdown(f"""<script>
    document.getElementById('widget-msgs').innerHTML = `{msgs_html}`;
    document.getElementById('widget-msgs').scrollTop = document.getElementById('widget-msgs').scrollHeight;

    function sendWidget() {{
        let inp = document.getElementById('widget-input');
        if (inp.value.trim()) {{
            document.getElementById('send-widget').click();
        }}
    }}

    document.getElementById('widget-input').addEventListener('keypress', (e) => {{
        if (e.key === 'Enter') sendWidget();
    }});
    </script>""", unsafe_allow_html=True)

# Hidden send button
if st.button("Send", key="send-widget"):
    # Get message from session
    pass

# Chat input area
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input("Your message", key="user_msg", label_visibility="collapsed", placeholder="Ask me something...")
with col2:
    if st.button("Send", key="send_btn"):
        if user_input and user_input.strip():
            st.session_state.chat_messages.append({"role": "user", "text": user_input})
            response, source = get_response(user_input)
            st.session_state.chat_messages.append({"role": "bot", "text": response, "source": source})
            st.rerun()

# ============================================================================
# MAIN PAGES
# ============================================================================
if st.session_state.page == 'home':
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px;">
        <h1>🎯 Anamika</h1>
        <p style="color: #94a3b8; margin-top: 12px;">Enterprise Support Widget</p>
        <p style="color: #22c55e; margin-top: 16px; font-weight: 700;">👉 Use the 🎯 button or type below to chat!</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("💬 Chat", use_container_width=True):
            st.session_state.page = 'chat'
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

elif st.session_state.page == 'chat':
    st.markdown("### 💬 Chat Support")
    for msg in st.session_state.chat_messages:
        if msg["role"] == "bot":
            st.markdown(f'**🤖 Anamika:** {msg["text"]}\n\n📚 Source: {msg.get("source", "Support")}')
        else:
            st.markdown(f'**👤 You:** {msg["text"]}')
    if st.button("Home"):
        st.session_state.page = 'home'
        st.rerun()

elif st.session_state.page == 'analytics':
    st.markdown("### 📊 Analytics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Conversations", "3,847", "+15%")
    with col2:
        st.metric("Avg Time", "12m 30s", "-2m")
    with col3:
        st.metric("Escalation", "13%", "-2%")
    if st.button("Home"):
        st.session_state.page = 'home'
        st.rerun()

elif st.session_state.page == 'admin':
    st.markdown("### ⚙️ Admin Panel")
    tab1, tab2 = st.tabs(["📚 Knowledge Base", "🎤 Voice"])
    with tab1:
        st.markdown("#### Knowledge Base")
        uploaded = st.file_uploader("Upload files", type=['pdf', 'doc', 'docx', 'txt', 'csv', 'xls', 'xlsx'], accept_multiple_files=True)
        if uploaded:
            for f in uploaded:
                st.write(f"📄 {f.name} ({f.size/1024/1024:.1f} MB)")
        st.metric("Files", len(st.session_state.kb_files), "/ 5")
    with tab2:
        st.markdown("#### Voice Config")
        st.text_input("Workspace ID", placeholder="workspace_xyz")
        st.text_input("API Key", type="password", placeholder="sk-...")
        if st.button("💾 Save", use_container_width=True):
            st.success("✅ Saved!")
    if st.button("Home"):
        st.session_state.page = 'home'
        st.rerun()

st.markdown("""<div style="text-align: center; padding: 40px 20px; margin-top: 60px; border-top: 1px solid rgba(59, 130, 246, 0.1);">
    <p style="color: #94a3b8; font-size: 12px;">🎯 Anamika | v6.0 - Draggable Widget</p>
</div>""", unsafe_allow_html=True)
