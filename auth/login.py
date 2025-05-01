import streamlit as st
from auth.utils import load_users, check_password

def login_form():
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = load_users()
        user = users.get(username)

        if user and check_password(password, user["password"]):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.name = user["name"]
            st.session_state.role = user.get("role", "viewer")
            st.success("✅ Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials.")
