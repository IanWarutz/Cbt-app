import streamlit as st
import os
import json
import datetime
import random

# ========== Data Storage ==========
USER_DATA_FILE = "cbt_user_data.json"

def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "streak": 0,
            "last_entry": "",
            "gratitude_list": []
        }

def save_user_data(data):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f)

# ========== Encouragement & Prompts ==========
ENCOURAGEMENTS = [
    "You’re investing in yourself! Proud of you.",
    "Every reflection helps you grow.",
    "Remember, you’re not alone on this journey.",
    "Small steps create big changes.",
    "Consistency is more important than perfection.",
    "You have the power to reframe your thoughts."
]

GRATITUDE_PROMPTS = [
    "What's one thing you're grateful for today?",
    "Name something small that brought you joy recently.",
    "Who is someone you appreciate, and why?",
    "Recall a recent accomplishment, no matter how small."
]

# ========== Cognitive Distortion Dictionary ==========
distortions = {
    "always": "Overgeneralization: Can you think of times this wasn't true?",
    "never": "Overgeneralization: Are there exceptions to this?",
    "should": "‘Should’ Statements: What rule are you holding yourself to?",
    "must": "‘Must’ Thinking: Is this a flexible or rigid belief?",
    "can't": "Helplessness: What might you be able to do instead?",
    "worthless": "Self-labeling: What strengths contradict this belief?",
    "failure": "Catastrophizing: Is this really the end or just a step?",
    "loser": "Labeling: Are you defining your whole self by one experience?",
    "bad": "Negative Filtering: Are you ignoring the positives?",
    "perfect": "All-or-Nothing: Is there room for middle ground?",
    "ruined": "Catastrophizing: What can still be done about this?",
    "stupid": "Labeling: What evidence shows you're learning?",
    "unloveable": "Emotional Reasoning: Feelings aren’t facts. Who does care for you?",
    "hopeless": "Fortune-telling: Can you really know the future?",
    "no one": "Mental Filtering: Who actually supports or appreciates you?",
    "everyone": "Overgeneralization: Really everyone? Who doesn't fit that?",
    "only me": "Personalization: Could there be other reasons for this?",
}

# --- Data Privacy Notice and Consent ---
st.title("CBT Reflective App")

st.info(
    "🔒 **Data Collection & Privacy Notice**\n\n"
    "To improve wellbeing insights, we collect basic demographic information (age, gender, profession) along with your reflections. "
    "Your data will be kept confidential and securely stored. By continuing, you consent to this data collection. "
    "If you do not consent, you will not be able to use the app."
)

# --- Consent Section (MUST be first) ---
if "consent_given" not in st.session_state:
    consent = st.radio(
        "Do you consent to the collection and safe storage of your demographic and reflection data?",
        ["Yes, I consent", "No, I do not consent"],
        index=None
    )
    if consent == "Yes, I consent":
        st.session_state.consent_given = True
        st.rerun()
    elif consent == "No, I do not consent":
        st.session_state.consent_given = False
        st.warning("You must provide consent to use this app. Thank you for considering.")
        st.stop()
else:
    if not st.session_state.consent_given:
        st.warning("You must provide consent to use this app. Thank you for considering.")
        st.stop()

# --- Demographics Section (MUST come before other prompts) ---
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
            st.rerun()
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
                st.rerun()
            else:
                st.error("Access denied: Incorrect password.")
        else:
            st.error("Password file not found. Contact app owner.")
    else:
        st.info("Enter password to access owner tools.")

# Only show owner section if a query param ?owner=1 is present for stealth.
if st.query_params.get("owner") == ["1"]:
    owner_access()

# --- Streamlit Interactions and Data Storage ---
st.header("CBT Reflection Journal")
st.write(
    f"Welcome, {st.session_state.demographics['profession']}! "
    "Interact with the public CBT features below:"
)

# --- Load user data for streaks and gratitude ---
user_data = load_user_data()

# --- Streak and Motivation ---
today = datetime.date.today().isoformat()
if user_data["last_entry"] != today:
    # Check if yesterday was the last entry for streak
    last_date = (
        datetime.datetime.strptime(user_data["last_entry"], "%Y-%m-%d").date()
        if user_data["last_entry"] else None
    )
    if last_date and (datetime.date.today() - last_date).days == 1:
        user_data["streak"] += 1
    else:
        user_data["streak"] = 1
    user_data["last_entry"] = today
    save_user_data(user_data)

st.info(f"🔥 Daily Streak: {user_data['streak']} day(s) in a row! Keep it going! {random.choice(ENCOURAGEMENTS)}")

# --- Thought Analysis Section ---
st.subheader("CBT Thought Analyzer")
thought = st.text_area("Enter a negative or distressing thought you're experiencing:")

# >>>>>>>> NEW PROMPTS ADDED HERE <<<<<<<<
if thought.strip():
    st.text_area("Why are you experiencing those thoughts?", key="why_experiencing")
    stressors = st.multiselect(
        "Are there any social stressors contributing to these thoughts?",
        ["School", "Family", "Work", "Relationships", "Finances", "Health", "Other"]
    )
    sought_help = st.radio("Have you sought personal help before?", ["Yes", "No"], index=None)

def streamlit_analyze_thought(thought):
    detected = []
    for key in distortions:
        if key in thought.lower():
            st.write(f"🔹 **Distortion Detected:** *{key}*")
            st.write(f"   💬 **Reframe Prompt:** {distortions[key]}")
            detected.append(key)

    # Final Action Based on Count
    if len(detected) == 0:
        st.success("✅ No cognitive distortions detected. Keep reflecting and journaling with awareness.")
    elif len(detected) <= 2:
        st.info("🧘 Suggestion: Continue daily journaling and practice positive self-talk. Try rephrasing your thought in a balanced way.")
    else:
        st.warning("⚠️ Multiple distortions detected. Consider guided reflection, talking to a therapist, or reviewing CBT techniques. Today might be a good day to slow down and prioritize self-kindness.")

    # Encourage user to rephrase
    rephrase = st.radio("Would you like to try rewriting your thought in a more balanced, positive way?", ["No", "Yes"])
    if rephrase == "Yes":
        new_thought = st.text_area("Go ahead and rephrase your thought:")
        if new_thought.strip():
            st.success("🌱 Great job reframing! Remember, practice builds resilience.")

if thought.strip():
    streamlit_analyze_thought(thought)

# --- Daily Gratitude Section ---
st.subheader("Gratitude Journal")
if st.button("Prompt me for gratitude!"):
    prompt = random.choice(GRATITUDE_PROMPTS)
    st.session_state["gratitude_prompt"] = prompt

prompt = st.session_state.get("gratitude_prompt", None)
if prompt:
    gratitude = st.text_area(f"{prompt}", key="gratitude_entry")
    if st.button("Save Gratitude Entry"):
        user_data["gratitude_list"].append({
            "date": today,
            "entry": gratitude
        })
        save_user_data(user_data)
        st.success("💖 Wonderful! Gratitude helps rewire the brain for positivity.")
        del st.session_state["gratitude_prompt"]

if user_data["gratitude_list"]:
    st.markdown("#### Your Recent Gratitude Entries")
    for g in user_data["gratitude_list"][-5:][::-1]:
        st.write(f"- *{g['date']}*: {g['entry']}")

st.info("If you need professional help, please seek a qualified therapist or counselor.")
