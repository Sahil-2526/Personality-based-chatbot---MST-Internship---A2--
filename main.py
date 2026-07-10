import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.title("🤖 PERSONALITY BASED CHATBOT")

# Personality
personality = st.selectbox(
    "Select the personality",
    [
        "Pro CSE student",
        "Therapist",
        "Angry man who doesn't care about your feelings and says harsh truth in your face"
    ]
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# chat history
show_history = st.sidebar.checkbox("📜 Show Previous Chats")

if show_history:
    st.sidebar.subheader("Previous Chats")

    if not st.session_state.messages:
        st.sidebar.write("No chats yet.")
    else:
        for msg in st.session_state.messages:
            role = "🧑 You" if msg["role"] == "user" else "🤖 Bot"
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

    # convo history
    conversation = ""
    for msg in st.session_state.messages:
        personality_used = msg.get("personality", "Unknown")
        conversation += (
            f"[{personality_used}] "
            f"{msg['role']}: {msg['content']}\n"
        )

    # prompt
    ai_instructions = f"""
    You are acting as {personality}.
    Stay completely in character throughout the conversation.
    Previous conversation:
    {conversation}
    Reply to the latest user message.
    """

    with st.spinner("Connecting to the multiverse..."):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=ai_instructions
        )

    reply = response.text

    # store response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "personality": personality,
            "content": reply
        }
    )

    with st.chat_message("user"):
        st.write(user_msg)

    with st.chat_message("assistant"):
        st.write(reply)