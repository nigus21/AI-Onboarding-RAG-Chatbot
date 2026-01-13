# app.py

import streamlit as st
from assistant.user_data import get_user_data
from assistant.assistant import assistant_chain, load_vectorstore
from langchain_core.runnables import RunnableMap

# ------------------------------
# Page configuration
# ------------------------------
st.set_page_config(page_title="AI Onboarding Assistant", page_icon="🤖")

# ------------------------------
# Load user data & vector store
# ------------------------------
user_data = get_user_data()
vectorstore = load_vectorstore()

# ------------------------------
# Sidebar
# ------------------------------
with st.sidebar:
    st.image("logo.png", width=150)
    st.header("Employee Profile")
    st.json(user_data)

# ------------------------------
# Session state for chat
# ------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 AI Onboarding Chatbot")

# ------------------------------
# User input
# ------------------------------
query = st.text_input("Ask me anything about company policies:")

if query:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # --------------------------
    # Run the assistant chain
    # --------------------------
    # Streaming response for better UX
    with st.chat_message("assistant"):
        response_text = ""
        for chunk in assistant_chain.stream({
            "question": query,
            "chat_history": st.session_state.messages,
            "user": user_data,
            "context": vectorstore.as_retriever(search_kwargs={"k":4})
        }):
            response_text += chunk
            st.write(response_text, end="")  # Stream text incrementally

        st.session_state.messages.append({"role": "assistant", "content": response_text})

# ------------------------------
# Display chat history (for refresh)
# ------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
