import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.title("PERSONALITY BASED CHATBOT")

st.sidebar.title("App Settings")

# Personality
personality = st.sidebar.selectbox(
    "Select the personality",
    [
        "Pro CSE student",
        "Therapist",
        "Angry man who doesn't care about your feelings and says harsh truth in your face",
        "A student who has exam in 1 hour and he hasn't studied anything",
        "A man who is sick of his life and want to die",
        "A fitness freak who does exercise the whole day"
    ]
)

if personality == "Pro CSE student":
    bot_avatar = "😎"
elif personality == "Therapist":
    bot_avatar = "🤔"
elif personality == "Angry man who doesn't care about your feelings and says harsh truth in your face":
    bot_avatar = "😡"
elif personality == "A student who has exam in 1 hour and he hasn't studied anything":
    bot_avatar = "😱"
elif personality == "A man who is sick of his life and want to die":
    bot_avatar = "😭"
elif personality == "A fitness freak who does exercise the whole day":
    bot_avatar = "💪"
else:
    bot_avatar = "🤖"

# Intensity
intensity = st.sidebar.slider(
    "Intensity Level",
    min_value=1,
    max_value=10,
    value=5
)

# Response Length
response_length = st.sidebar.selectbox(
    "Response Length",
    ["Short", "Medium", "Detailed"]
)

response_value = {
    "Short": "Maximum 2-3 sentences",
    "Medium": "7-10 sentences",
    "Detailed": "30+ sentences"
}

# Input chat
user_msg = st.text_input("What do you want to say . . .")

if st.button("Send") and user_msg:
    # Prompt
    ai_instructions = f"""
        You are acting as {personality}.
        Intensity Level: {intensity}/10.
        Response Length: {response_value[response_length]}
        Respond naturally to the latest user message: {user_msg}
    """

    # Response
    with st.spinner("Connecting to the multiverse..."):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=ai_instructions
        )

    reply = response.text


    with st.chat_message("user"):
        st.write(user_msg)

    with st.chat_message("assistant", avatar=bot_avatar):
        st.write(reply)