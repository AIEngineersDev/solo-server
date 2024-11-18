import streamlit as st


def display_message(message):
    if isinstance(message, dict):
        role = message.get("role")
        content = message.get("content")
    else:
        role = message.role
        content = message.content

    if role in ["system", "assistant", "user"] and content:
        with st.chat_message(role):
            st.markdown(content)
