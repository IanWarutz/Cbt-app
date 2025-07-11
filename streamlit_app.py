import streamlit as st
import os

# --- Demographics Section ---
st.title("CBT Reflective App")

with st.form("demographics_form"):
    age = st.number_input("Your Age", min_value=10, max_value=120)
    gender = st.selectbox("Your Gender", ["Male", "Female", "Other", "Prefer not to say"])
    profession = st.text_input("Your Profession")
    submitted = st.form_submit_button("Continue")
    if not submitted:
        st.stop()

st.success("Thank you! You may interact with the app below.")

# --- Owner-only: Secure Code Section ---
def owner_access():
    st.warning("Owner's Secure Access: Enter password to unlock sensitive code/tools.")
    password_input = st.text_input("Password", type="password")
    if password_input:
        if os.path.exists(".owner_password"):
            with open(".owner_password") as f:
                real_pwd = f.read().strip()
            if password_input == real_pwd:
                st.success("Access granted! Owner-only code below:")
                # Import or run your sensitive functions here, e.g.:
                import app_core
                app_core.owner_tools()
            else:
                st.error("Access denied: Incorrect password.")
        else:
            st.error("Password file not found. Contact app owner.")
    else:
        st.info("Enter password to access owner tools.")

# Only show owner section if a query param ?owner=1 is present for stealth.
if st.experimental_get_query_params().get("owner") == ["1"]:
    owner_access()

# --- Public Section: Main App ---
st.header("CBT Reflection Journal")
st.write("Interact with the public CBT features below:")
# Place your regular app functions here, e.g.:
# analyze_thought(), gratitude_journal(), etc.

st.info("If you need professional help, please seek a qualified therapist or counselor.")
