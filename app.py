# This script requires Streamlit and OpenAI packages.
# Ensure your environment has them installed, or run using Streamlit:
# streamlit run app.py

try:
    import streamlit as st
except ModuleNotFoundError:
    raise ModuleNotFoundError("Streamlit is not installed. Please install it via 'pip install streamlit'")

try:
    import openai
except ModuleNotFoundError:
    raise ModuleNotFoundError("OpenAI package is not installed. Please install it via 'pip install openai'")

# --- CONFIGURATION ---
openai.api_key = st.secrets["OPENAI_API_KEY"]  # Make sure to set this in your .streamlit/secrets.toml

# --- SESSION STATE INIT ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user_data" not in st.session_state:
    st.session_state.user_data = {
        "name": "",
        "email": "",
        "phone": "",
        "experience": "",
        "position": "",
        "location": "",
        "tech_stack": ""
    }

if "stage" not in st.session_state:
    st.session_state.stage = 0

# --- PROMPT HELPERS ---
def generate_tech_questions(tech_stack):
    prompt = f"""
    You are a technical interviewer. The candidate has experience with the following tech stack: {tech_stack}.
    Generate 3-5 concise technical questions to assess their knowledge for each of the technologies mentioned.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# --- MAIN UI ---
st.title("🤖 TalentScout Hiring Assistant")
st.markdown("Hello! I'm here to assist with your job application by collecting key info and asking a few technical questions.")

# --- CHAT STAGES ---
stages = [
    "What is your full name?",
    "Please provide your email address.",
    "Your phone number?",
    "How many years of experience do you have?",
    "What position are you applying for?",
    "Where are you currently located?",
    "List your tech stack (languages, frameworks, tools, databases)."
]

# --- INPUT HANDLER ---
user_input = st.text_input("You:")
if user_input:
    st.session_state.chat_history.append(("You", user_input))

    if user_input.lower() in ["exit", "quit", "bye"]:
        st.session_state.chat_history.append(("Bot", "Thank you for applying! We’ll review your profile and get back to you soon."))
        st.session_state.stage = -1
    elif st.session_state.stage < len(stages):
        keys = list(st.session_state.user_data.keys())
        st.session_state.user_data[keys[st.session_state.stage]] = user_input
        st.session_state.stage += 1

        if st.session_state.stage < len(stages):
            st.session_state.chat_history.append(("Bot", stages[st.session_state.stage]))
        else:
            tech_stack = st.session_state.user_data['tech_stack']
            questions = generate_tech_questions(tech_stack)
            st.session_state.chat_history.append(("Bot", "Thanks! Here are a few questions to test your skills:"))
            st.session_state.chat_history.append(("Bot", questions))
            st.session_state.chat_history.append(("Bot", "That’s all for now. Goodbye and good luck!"))
            st.session_state.stage = -1
    else:
        st.session_state.chat_history.append(("Bot", "The conversation is over. Refresh to restart."))

# --- DISPLAY CHAT ---
for speaker, message in st.session_state.chat_history:
    st.chat_message(speaker).write(message)

# --- END ---

