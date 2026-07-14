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


if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}

if personality not in st.session_state.all_chats:
    st.session_state.all_chats[personality] = []

messages = st.session_state.all_chats[personality]

# Clear Chat
if st.sidebar.button("Clear Chat History"):
    st.session_state.all_chats = {}
    st.rerun()

# Chat History

show_history = st.sidebar.checkbox("Show Previous Chats")

if show_history:
    st.sidebar.subheader("Previous Chats")

    if not any(st.session_state.all_chats.values()):
        st.sidebar.write("No chats yet.")
    else:
        for personality_name, chat in st.session_state.all_chats.items():
            for msg in chat:
                role = "You" if msg["role"] == "user" else "ChatBot"
                st.sidebar.markdown(
                    f"""
                        **{role}**
                        **Personality:** {personality_name}
                        **Message:** {msg['content']}
                        ---
                    """
                )

# Display Chat
for msg in messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    else:
        with st.chat_message(
            "assistant",
            avatar=msg.get("avatar", "🤖")
        ):
            st.write(msg["content"])

# Input chat
user_msg = st.chat_input("What do you want to say?")

if user_msg:

    # Store msg
    messages.append(
        {
            "role": "user",
            "personality": personality,
            "content": user_msg
        }
    )

    # Conco history in one str
    conversation = ""
    for msg in messages:
        conversation += f"{msg['role']}: {msg['content']}\n"

    # Prompt
    ai_instructions = f"""
        You are acting as {personality}.
        Intensity Level: {intensity}/10.
        Response Length: {response_value[response_length]}
        Conversation so far: {conversation}
        Respond naturally to the latest user message: {user_msg}
    """

    # Response
    with st.spinner("Connecting to the multiverse..."):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=ai_instructions
        )

    reply = response.text

    # Store assistant response
    messages.append(
        {
            "role": "assistant",
            "personality": personality,
            "avatar": bot_avatar,
            "content": reply
        }
    )

    # Refresh
    st.rerun()