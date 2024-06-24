import streamlit as st
import openai
from gremlin_python.driver import client, serializer

st.title("🦜🔗 Chat with the Planetary Knowledge Base")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    neptune_host = st.text_input("Neptune Host Key", type="password")
    neptune_port = 8182  # Typically 8182
    neptune_url = f'wss://{neptune_host}:{neptune_port}/gremlin'
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can interact with the PKB. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Ask something about the PKB"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    if not neptune_host:
        st.info("Please add your Neptune Host key to continue.")
        st.stop()

    # Setup OpenAI API
    openai.api_key = openai_api_key

    # Function to query
