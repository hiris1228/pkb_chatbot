import streamlit as st
from langchain.llms import OpenAI
from langchain.chains import NeptuneOpenCypherQAChain
from langchain_openai import ChatOpenAI

st.title("🦜🔗 Chat with the Planatery Knowledge Base")
"""
Please give us a while, we will get our Neptune connection back!
"""
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    # Define Neptune connection details
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

if prompt := st.chat_input(placeholder="How many nodes in the PKB?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    if not neptune_host:
        st.info("Please add your Neptune Host key to continue.")
        st.stop()

    llm = ChatOpenAI(temperature=0, model="gpt-4", openai_api_key=openai_api_key, streaming=True)
    chain = NeptuneOpenCypherQAChain.from_llm(llm=llm, graph=graph)
    
    with st.chat_message("assistant"):
        response = chain.invoke(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
