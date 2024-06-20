from openai import OpenAI
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("🌍🤖️💬 PKB Chatbot Demo")
st.caption("🚀 A Very Friendly chatbot powered by OpenAI and AWS")

"""
This is a draft of PKB Chatbot Demo
"""
"""
1⃣️📷Image OCR - where you can upload a label and extract text information.
"""
"""
2⃣️🔍Chat with Search - where you can ask the PKB Chatbot to search more precise botanist content via the World Wide Web (Very difficult to rate its performance😂)
3⃣️🌳Chat with PKB - where you can chat with the PKB Chatbot and allow interaction with our PKB Neptune Could service using Natural Language
(Please remember that the 'Chat with PKB' is not currently fully functioning due to Neptune Engine Issue. I will fix it in a day or two.)
4⃣️🗺️Graph Navigator - coming soon!
"""

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello, I'm the NHM PKB project assistant. How can I help you today?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
