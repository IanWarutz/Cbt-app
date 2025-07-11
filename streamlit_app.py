import streamlit as st
import os

# --- Data Privacy Notice and Consent ---
st.title("CBT Reflective App")

st.info(
    "🔒 **Data Collection & Privacy Notice**\n\n"
    "To improve wellbeing insights, we collect basic demographic information (age, gender, profession) along with your reflections. "
    "Your data will be kept confidential and securely stored. By continuing, you consent to this data collection. "
    "If you do not consent, you will not be able to use the app."
)

if "consent_given" not in st.session_state:
    consent = st.radio(
        "Do you consent to the collection and safe storage of your demographic and reflection data?",
        ["Yes, I consent", "No, I do not consent"],
        index=None
    )
    if consent == "Yes, I consent":
        st.session_state.consent_given = True
        st.experimental_rerun()
    elif consent == "No, I do not consent":
        st.session_state.consent_given = False
        st.warning("You must provide consent to use this app. Thank you for considering.")
        st.stop()
else:
    if not st.session_state.consent_given:
        st.warning("You must provide consent to use this app. Thank you for considering.")
        st.stop()

# --- Demographics Section ---
if "demographics" not in st.session_state:
    with st.form("demographics_form"):
        age = st.number_input("Your Age", min_value=10, max_value=120)
        gender = st.selectbox("Your Gender", ["Male", "Female", "Other", "Prefer not to say"])
        profession = st.text_input("Your Profession")
        submitted = st.form_submit_button("Continue")
        if submitted and profession.strip() != "":
            st.session_state.demographics = {
                "age": int(age),
                "gender": gender,
                "profession": profession.strip()
            }
            st.success("Thank you! You may interact with the app below.")
            st.experimental_rerun()
        elif submitted:
            st.error("Please fill in all fields.")
            st.stop()

if "demographics" not in st.session_state:
    st.stop()

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
st.write(
    f"Welcome, {st.session_state.demographics['profession']}! "
    "Interact with the public CBT features below:"
)
# Place your regular app functions here, e.g.:
# analyze_thought(), gratitude_journal(), etc.

st.info("If you need professional help, please seek a qualified therapist or counselor.")
