import streamlit as st


def initialize_memory():
    """Initialize conversation memory."""
    if "messages" not in st.session_state:
        st.session_state.messages = []


def add_message(role, content):
    """Add a message to memory."""
    st.session_state.messages.append({
        "role": role,
        "content": content
    })


def get_messages():
    """Return conversation history."""
    return st.session_state.messages


def clear_memory():
    """Clear conversation memory."""
    st.session_state.messages = []
