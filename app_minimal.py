import streamlit as st

st.set_page_config(page_title="Support Platform", page_icon="💬")

st.markdown("# 🚀 Support Platform")
st.write("✅ App is running!")

password = st.text_input("Password:", type="password")

if st.button("Login"):
    if password == "admin123":
        st.success("✅ Logged in!")
    else:
        st.error("❌ Wrong password")

st.info("Password: admin123")
