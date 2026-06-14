import streamlit as st
from gemini_service import get_ai_response
from pdf_export import export_chat_pdf
from database import engine
from models import Base
from chat_history import (
    create_chat,
    get_chats,
    get_messages,
    save_message,
    update_chat_title,
    delete_chat
)

# Create tables
Base.metadata.create_all(bind=engine)

st.title("🤖 Gemini AI Chatbot")
st.caption("Powered by Google Gemini")

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Gemini AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ---------------- Session State ----------------
if "chat_id" not in st.session_state:
    st.session_state.chat_id = create_chat()

# Load current chat messages
previous_messages = get_messages(
    st.session_state.chat_id
)

st.session_state.messages = []

for msg in previous_messages:

    st.session_state.messages.append(
        {
            "role": msg.role,
            "content": msg.content
        }
    )

# ---------------- Sidebar ----------------
with st.sidebar:

    st.title("💬 Chats")

    if st.button("➕ New Chat"):

        st.session_state.chat_id = create_chat()

        st.rerun()

    st.divider()

    chats = get_chats()

    for chat in chats:

        title = chat.title or f"Chat {chat.id}"

        col1, col2 = st.columns([5, 1])

        with col1:

            if st.button(
                title,
                key=f"chat_{chat.id}"
            ):

                st.session_state.chat_id = chat.id

                st.rerun()

        with col2:

            if st.button(
                "🗑",
                key=f"delete_{chat.id}"
            ):

                delete_chat(chat.id)

                if st.session_state.chat_id == chat.id:
                    st.session_state.chat_id = create_chat()

                st.rerun()

    st.divider()

    if st.button("📄 Export PDF"):

        export_chat_pdf(
            st.session_state.messages
        )

        st.success(
            "chat_history.pdf created successfully!"
        )

# ---------------- Display Messages ----------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )

# ---------------- User Input ----------------
prompt = st.chat_input(
    "Ask anything..."
)

if prompt:

    # Display user message
    with st.chat_message("user"):

        st.markdown(prompt)

    save_message(
        st.session_state.chat_id,
        "user",
        prompt
    )

    # First message becomes title
    if len(previous_messages) == 0:

        update_chat_title(
            st.session_state.chat_id,
            prompt[:30]
        )

    # Gemini response
    with st.spinner("Thinking..."):

        response = get_ai_response(prompt)

    # Display AI response
    with st.chat_message("assistant"):

        st.markdown(response)

    save_message(
        st.session_state.chat_id,
        "assistant",
        response
    )

    st.rerun()