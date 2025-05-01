import streamlit as st
from auth.login import login_form
from auth.signup import signup_form

st.set_page_config("Login App", layout="wide", )

# Initialize login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Hide pages if not logged in
if not st.session_state.logged_in:
    mode = st.selectbox("Choose Action", ["Login", "Sign Up"])
    if mode == "Login":
        login_form()
    else:
        signup_form()
    st.stop()  # Prevent access to pages
else:
    st.switch_page("pages/1_PricingDashboard.py")  # Redirect logged-in users
