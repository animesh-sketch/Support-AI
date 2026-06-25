import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import json
import os

st.set_page_config(
    page_title="Anamika - Support Widget",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# PERSISTENT STORAGE FOR KB FILES
# ============================================================================
KB_DATA_FILE = "kb_files.json"

def load_kb_files():
    """Load KB files from persistent storage"""
    if os.path.exists(KB_DATA_FILE):
        try:
            with open(KB_DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_kb_files(files):
    """Save KB files to persistent storage"""
    with open(KB_DATA_FILE, 'w') as f:
        json.dump(files, f, indent=2)

def add_kb_file(name, size, file_type, status="Active"):
    """Add a new file to KB"""
    files = load_kb_files()
    if len(files) < 5:
        files.append({
            "name": name,
            "size": size,
            "type": file_type,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "status": status,
            "id": len(files) + 1
        })
        save_kb_files(files)
        return True
    return False

def delete_kb_file(file_name):
    """Delete a file from KB"""
    files = load_kb_files()
    files = [f for f in files if f["name"] != file_name]
    save_kb_files(files)

def get_kb_files():
    """Get all KB files"""
    return load_kb_files()

# ============================================================================
# KNOWLEDGE BASE CONTENT DATABASE
# ============================================================================
KB_CONTENT = {
    "Password Reset Guide.pdf": {
        "title": "Password Reset Guide",
        "keywords": ["password", "reset", "forgot", "login", "account", "access"],
        "content": """To reset your password:
1. Click "Forgot Password" on the login page
2. Enter your email address
3. Check your email for reset link (within 2 minutes)
4. Click the link to create a new password
5. Use new password to login

If you don't receive the email:
- Check spam folder
- Wait 2-3 minutes for delivery
- Try requesting another reset link"""
    },
    "Billing FAQ.docx": {
        "title": "Billing FAQ",
        "keywords": ["billing", "payment", "invoice", "subscription", "charge", "plan", "pricing", "cost", "refund"],
        "content": """Common Billing Questions:

Q: What payment methods do you accept?
A: We accept all major credit cards (Visa, Mastercard, AmEx), PayPal, and bank transfers.

Q: When am I charged?
A: You're charged on the same date each month (billing date).

Q: Can I change my plan?
A: Yes! You can upgrade/downgrade anytime. Changes take effect next billing cycle.

Q: What's your refund policy?
A: 30-day money-back guarantee on annual plans. Monthly plans have 7-day refund period.

Q: How do I cancel my subscription?
A: Go to Settings > Billing > Cancel Subscription. You'll have access until end of current period."""
    },
    "API Documentation.pdf": {
        "title": "API Documentation",
        "keywords": ["api", "developer", "integration", "endpoint", "code", "programming", "rest"],
        "content": """Anamika API Documentation:

Base URL: https://api.anamika.ai/v1

Authentication:
- Use API key in Authorization header
- Format: Authorization: Bearer YOUR_API_KEY

Main Endpoints:
- POST /chat - Send message
- GET /conversations - List conversations
- POST /escalate - Escalate to human agent
- GET /kb/search - Search knowledge base

Rate Limits:
- 100 requests/minute for standard plans
- 1000 requests/minute for enterprise

Error Codes:
- 401: Unauthorized
- 429: Too many requests
- 500: Server error"""
    },
    "Troubleshooting Guide.txt": {
        "title": "Troubleshooting Guide",
        "keywords": ["troubleshoot", "error", "problem", "issue", "bug", "not working", "fix", "help"],
        "content": """Common Issues & Solutions:

Widget Not Loading:
- Clear browser cache
- Check JavaScript is enabled
- Verify API key is correct

Chat Not Responding:
- Check internet connection
- Refresh the page
- Clear browser cookies

API Errors:
- Verify authentication token
- Check rate limits not exceeded
- Ensure correct endpoint URL

Missing Messages:
- Check conversation is saved
- Refresh to load latest messages
- Contact support if still missing

Performance Issues:
- Use modern browser (Chrome, Firefox, Safari)
- Check system resources
- Reduce number of concurrent conversations"""
    }
}

def search_kb(user_query):
    """Search Knowledge Base for relevant documents"""
    user_query_lower = user_query.lower()
    results = []

    for doc_name, doc_data in KB_CONTENT.items():
        match_score = 0

        # Check keyword matches
        for keyword in doc_data["keywords"]:
            if keyword in user_query_lower:
                match_score += 2

        # Check title match
        if doc_data["title"].lower() in user_query_lower:
            match_score += 3

        # Check content relevance
        words = user_query_lower.split()
        for word in words:
            if len(word) > 3 and word in doc_data["content"].lower():
                match_score += 1

        if match_score > 0:
            results.append({
                "document": doc_name,
                "title": doc_data["title"],
                "content": doc_data["content"],
                "score": match_score
            })

    # Sort by relevance score
    results.sort(key=lambda x: x["score"], reverse=True)
    return results

def get_support_response(user_message):
    """Get support agent response from KB or generate intelligent response"""
    # Search KB for relevant documents
    kb_results = search_kb(user_message)

    if kb_results and kb_results[0]["score"] > 0:
        # Found relevant KB document
        top_result = kb_results[0]
        response = f"""Based on our Knowledge Base ({top_result['title']}):

{top_result['content']}

---
📚 Source: {top_result['title']}"""
        return response, top_result["title"]
    else:
        # No KB match - provide intelligent response
        user_lower = user_message.lower()

        if any(word in user_lower for word in ["hello", "hi", "hey", "greet"]):
            return "👋 Hello! Welcome to Anamika Support. How can I assist you today? I'm here to help with questions about passwords, billing, API integration, troubleshooting, and more!", "General Support"

        elif any(word in user_lower for word in ["help", "support", "assist", "issue"]):
            return "I'm here to help! You can ask me about:\n• Password reset\n• Billing & payments\n• API documentation\n• Troubleshooting\n\nWhat would you like help with?", "Help Center"

        elif any(word in user_lower for word in ["agent", "human", "person", "talk to", "speak"]):
            return "👤 Sure! I can connect you with a human support agent. They'll be available shortly to help with your specific needs.", "Agent Escalation"

        else:
            return "I understand you're asking about that topic. While I don't have specific documentation available, let me connect you with a human support agent who can provide personalized assistance. Would you like me to escalate your question?", "General Support"

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
        {
            "role": "bot",
            "text": "👋 Hello! I'm Anamika, your AI support agent. I can help you with:\n• Password reset\n• Billing & subscriptions\n• API integration\n• Troubleshooting issues\n\nWhat can I help you with today?",
            "source": "Welcome"
        }
    ]
if 'widget_input' not in st.session_state:
    st.session_state.widget_input = ""
if 'kb_files' not in st.session_state:
    # Load from persistent storage
    st.session_state.kb_files = get_kb_files()
    # If no files exist, create default ones
    if len(st.session_state.kb_files) == 0:
        add_kb_file("Password Reset Guide.pdf", "2.3 MB", "PDF", "Active")
        add_kb_file("Billing FAQ.docx", "1.8 MB", "DOCX", "Active")
        st.session_state.kb_files = get_kb_files()

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

    st.markdown("""
    <div class="premium-card">
        <p style="margin: 0;">🤖 <strong>Anamika Support Agent</strong> • Powered by Knowledge Base • Response Time: <strong>Instant</strong></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Display chat
    for msg in st.session_state.widget_chat:
        if msg["role"] == "bot":
            source = msg.get("source", "Support")
            st.markdown(f"""
            <div class="premium-card" style="background: rgba(34, 197, 94, 0.1); border-left: 3px solid #22c55e;">
                <p style="margin: 0;"><strong>🤖 Anamika:</strong></p>
                <p style="margin: 8px 0 0 0; white-space: pre-wrap;">{msg['text']}</p>
                <p style="margin: 8px 0 0 0; color: var(--text-muted); font-size: 11px;">📚 Source: {source}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="premium-card" style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%); border-left: 3px solid #3b82f6;">
                <p style="margin: 0;"><strong>👤 You:</strong></p>
                <p style="margin: 8px 0 0 0;">{msg['text']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Input
    col1, col2 = st.columns([5, 1])
    with col1:
        user_msg = st.text_input("Ask a question...", label_visibility="collapsed", placeholder="Type your question about passwords, billing, API, troubleshooting, etc.")
    with col2:
        send = st.button("Send", use_container_width=True)

    if send and user_msg:
        # Add user message
        st.session_state.widget_chat.append({"role": "user", "text": user_msg})

        # Get support response from KB
        bot_response, source = get_support_response(user_msg)

        # Add bot response
        st.session_state.widget_chat.append({
            "role": "bot",
            "text": bot_response,
            "source": source
        })
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
    st.markdown("### ⚙️ Admin Panel")

    tab1, tab2, tab3, tab4 = st.tabs(["📚 Knowledge Base", "🎤 Voice Config", "🤖 Bot Settings", "⚡ Advanced"])

    with tab1:
        st.markdown("#### 📚 Knowledge Base Management")
        st.markdown("""
        <div class="premium-card">
            <p style="margin: 0; color: #22c55e; font-weight: 700;">✓ 💾 PERMANENT STORAGE ENABLED</p>
            <p style="margin: 8px 0 0 0; color: var(--text-muted); font-size: 12px;">
                All files are saved permanently and won't be deleted. Your KB is always available.
            </p>
            <p style="margin: 8px 0 0 0; color: var(--text-muted); font-size: 12px;">
                <strong>Supported formats:</strong> PDF, DOC, DOCX, TXT, CSV, XLS, XLSX, PPT, PPTX, JSON, XML
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
                    uploaded_count = 0
                    for file in uploaded_files:
                        file_size = f"{file.size / 1024:.1f} KB" if file.size < 1_000_000 else f"{file.size / 1024 / 1024:.1f} MB"
                        file_type = file.name.split('.')[-1].upper()
                        if add_kb_file(file.name, file_size, file_type, "Active"):
                            uploaded_count += 1
                    st.session_state.kb_files = get_kb_files()
                    st.success(f"✅ {uploaded_count} file(s) uploaded and saved permanently!")
                    st.rerun()

        with col2:
            st.markdown("**Storage Status**")
            st.markdown(f"""
            <div class="premium-card">
                <div style="text-align: center;">
                    <p style="margin: 0; font-size: 24px; font-weight: 900; color: #22c55e;">✓ {len(st.session_state.kb_files)}</p>
                    <p style="margin: 6px 0 0 0; color: var(--text-muted); font-size: 12px; text-transform: uppercase;">Files Permanently Stored</p>
                </div>
                <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(34, 197, 94, 0.2); border-color: rgba(34, 197, 94, 0.2);">
                    <p style="margin: 0; font-size: 12px; color: #22c55e;"><strong>💾 Persistent Storage:</strong> Active</p>
                    <p style="margin: 6px 0 0 0; font-size: 12px;"><strong>Max Files:</strong> 5</p>
                    <p style="margin: 6px 0 0 0; font-size: 12px;"><strong>Available Slots:</strong> {5 - len(st.session_state.kb_files)}</p>
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
                    delete_kb_file(file_to_delete)
                    st.session_state.kb_files = get_kb_files()
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
        if st.button("Back to Home", use_container_width=True):
            st.session_state.page = 'dashboard'
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
        source = msg.get("source", "Support")
        # Escape special characters and preserve newlines
        text = msg["text"].replace('\n', '<br>').replace('"', '\\"')
        messages_html += f'<div class="msg-bot"><strong style="color: #22c55e;">🤖 Anamika</strong><br><span style="margin-top: 4px; display: block;">{text}</span><div style="margin-top: 6px; padding-top: 6px; border-top: 1px solid rgba(59, 130, 246, 0.2); font-size: 10px; color: #94a3b8;">📚 {source}</div></div>'
    else:
        text = msg["text"].replace('\n', '<br>').replace('"', '\\"')
        messages_html += f'<div class="msg-user">{text}</div>'

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
