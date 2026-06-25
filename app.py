import streamlit as st

# Page config
st.set_page_config(page_title="Support Platform", page_icon="💬", layout="wide")

# ============================================================================
# MAIN APP
# ============================================================================

# Sidebar navigation
with st.sidebar:
    st.markdown("# 📱 Support Platform")
    mode = st.radio("Select:", ["Widget", "Dashboard", "Settings"])

# ============================================================================
# WIDGET MODE
# ============================================================================
if mode == "Widget":
    st.markdown("# 💬 Support Widget")

    # Initialize chat
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {'role': 'user', 'content': 'What is your pricing?'},
            {'role': 'assistant', 'content': 'We offer Starter ($99), Pro ($299), and Enterprise (custom)'},
        ]

    # Chat interface
    tab1, tab2, tab3 = st.tabs(["💬 Chat", "☎️ Call", "📚 Help"])

    # Chat Tab
    with tab1:
        st.subheader("Chat Support")

        # Display messages
        for msg in st.session_state.messages:
            if msg['role'] == 'user':
                st.write(f"**You:** {msg['content']}")
            else:
                st.write(f"**Support:** {msg['content']}")

        st.divider()

        # Input
        col1, col2 = st.columns([4, 1])
        with col1:
            user_msg = st.text_input("Type message...", placeholder="Ask anything")
        with col2:
            if st.button("Send"):
                if user_msg:
                    st.session_state.messages.append({'role': 'user', 'content': user_msg})
                    st.session_state.messages.append({'role': 'assistant', 'content': 'Thanks! We will respond soon.'})
                    st.rerun()

    # Call Tab
    with tab2:
        st.subheader("Call Support")
        name = st.text_input("Your Name")
        phone = st.text_input("Phone Number")

        if st.button("📞 Call Now", type="primary", use_container_width=True):
            if phone:
                st.success(f"✅ Call initiated to {phone}!")
                st.balloons()
            else:
                st.error("Please enter phone number")

    # Help Tab
    with tab3:
        st.subheader("Help Center")
        search = st.text_input("Search articles...")

        articles = [
            "Getting Started",
            "Pricing Plans",
            "API Documentation",
            "Account Security",
            "Troubleshooting"
        ]

        for article in articles:
            if not search or search.lower() in article.lower():
                st.write(f"📄 {article}")

# ============================================================================
# DASHBOARD MODE
# ============================================================================
elif mode == "Dashboard":
    st.markdown("# 📊 Admin Dashboard")

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Chats", "8", "+3")
    with col2:
        st.metric("Calls Today", "48", "+12")
    with col3:
        st.metric("Avg Response", "2m 30s", "-15s")
    with col4:
        st.metric("Satisfaction", "4.8/5", "+0.1")

    st.divider()

    # Conversations
    st.subheader("Live Conversations")

    conversations = [
        {"name": "Sarah Johnson", "email": "sarah@company.com", "channel": "Chat", "status": "Resolved"},
        {"name": "Mike Davis", "email": "mike@tech.com", "channel": "Call", "status": "Completed"},
        {"name": "Emma Wilson", "email": "emma@startup.io", "channel": "Chat", "status": "Active"},
        {"name": "James Smith", "email": "james@techcorp.net", "channel": "Chat", "status": "Resolved"},
    ]

    for conv in conversations:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**{conv['name']}**")
            st.caption(conv['email'])
        with col2:
            st.write(conv['channel'])
        with col3:
            if conv['status'] == 'Active':
                st.write("🟢 Active")
            else:
                st.write("⚪ " + conv['status'])
        st.divider()

# ============================================================================
# SETTINGS MODE
# ============================================================================
elif mode == "Settings":
    st.markdown("# ⚙️ Settings")

    st.subheader("API Configuration")
    api_url = st.text_input("API URL", value="http://localhost:3000")

    if st.button("💾 Save"):
        st.success("✅ Saved!")

# Footer
st.divider()
st.caption("Support Platform • Streamlit Cloud • Built with ❤️")
