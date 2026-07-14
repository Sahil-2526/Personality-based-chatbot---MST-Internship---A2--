import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.title("PERSONALITY BASED CHATBOT")

# Sidebar
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
intensity = st.sidebar.slider("Intensity Level", min_value=1, max_value=10, value=5 )
if intensity <= 3:
    behaviour = "Act subtly. Show only slight hints of the selected personality."
elif intensity <= 7:
    behaviour = "Clearly act as the selected personality while keeping the conversation natural."
else:
    behaviour = "Fully embrace the selected personality and never break character."

# Response length
response_length = st.selectbox(
    "Response Length",
    ["Short", "Medium", "Detailed"]
)

response_value = {
    "Short": "Maximum 2-3 sentences",
    "Medium": "",
    "Detailed": "",
}

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

# Chat history
show_history = st.sidebar.checkbox("Show Previous Chats")

if show_history:
    st.sidebar.subheader("Previous Chats")

    if not st.session_state.messages:
        st.sidebar.write("No chats yet.")
    else:
        for msg in st.session_state.messages:
            role = "You" if msg["role"] == "user" else "ChatBot"
            personality_used = msg.get("personality", "Unknown")
            st.sidebar.markdown(
                f"""
                **{role}**  
                **Personality:** {personality_used}  
                **Message:** {msg['content']}---
                """
            )

user_msg = st.chat_input("What do you want to say...")

if user_msg:
    # Store msg
    st.session_state.messages.append(
        {
            "role": "user",
            "personality": personality,
            "content": user_msg
        }
    )

    # Convo history
    conversation = ""
    for msg in st.session_state.messages:
        personality_used = msg.get("personality", "Unknown")
        conversation += (
            f"[{personality_used}] "
            f"{msg['role']}: {msg['content']}\n"
        )

    # Prompt
    ai_instructions = f"""
        You are acting as {personality}.
        Stay completely in character throughout the conversation.
        Behaviour : {behaviour}.
        Response length: {response_value.get(response_length)}
        Reply to the user's message:
        {user_msg}
    """

    with st.spinner("Connecting to the multiverse..."):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=ai_instructions
        )

    reply = response.text

    # Store response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "personality": personality,
            "content": reply
        }
    )

    with st.chat_message("user"):
        st.write(user_msg)

    with st.chat_message("assistant", avatar = bot_avatar):
        st.write(reply)