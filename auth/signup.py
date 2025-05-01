import streamlit as st
from auth.utils import load_users, save_users, hash_password

def signup_form():
    st.subheader("📝 Sign Up")
    name = st.text_input("Full Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")
    role = st.selectbox("Role", ["viewer", "editor", "admin"])

    if st.button("Create Account"):
        users = load_users()

        if username in users:
            st.error("Username already exists.")
        elif password != confirm:
            st.error("Passwords do not match.")
        else:
            users[username] = {
                "name": name,
                "password": hash_password(password),
                "role": role
            }
            save_users(users)
            st.success("Account created! Please log in.")
