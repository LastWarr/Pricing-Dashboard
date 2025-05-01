import streamlit as st
import bcrypt
import yaml
from pathlib import Path
from yaml.loader import SafeLoader

USER_FILE = Path("users.yaml")

def load_users():
    if USER_FILE.exists():
        with open(USER_FILE, "r") as f:
            return yaml.load(f, Loader=SafeLoader)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        yaml.dump(users, f)

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def login_form():
    users = load_users()
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = users.get(username)
        if user and check_password(password, user["password"]):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["role"] = user.get("role", "viewer")
            st.success(f"Welcome, {user['name']}!")
        else:
            st.error("Invalid credentials.")

def signup_form():
    users = load_users()
    st.subheader("Sign Up")
    name = st.text_input("Full Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")
    role = st.selectbox("Role", ["viewer", "editor", "admin"])

    if st.button("Create Account"):
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
            st.success("Account created! Please login.")
