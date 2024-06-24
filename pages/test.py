import streamlit as st
#import openai
from openai import OpenAI
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
    #openai.api_key = openai_api_key

    # Function to query Neptune
    def query_neptune(query):
        g = client.Client(
            neptune_url, 'g',
            username="", password="",
            message_serializer=serializer.GraphSONSerializersV3d0()
        )
        callback = g.submitAsync(query)
        if callback.result():
            return callback.result().all().result()
        else:
            return "No results found"

    # Function to get OpenAI response
    def get_openai_response(prompt):
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use the appropriate model
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message["content"].strip()

    def get_openai_response_new(prompt):
        client = OpenAI(api_key=openai_api_key)
        response = client.completions.create(
            model="gpt-4",  # Use the appropriate model
            #messages=[{"role": "user", "content": prompt}],
            prompt=f"convert to OpenCypher query in Neptune: {prompt}",
            max_tokens=150
        )
        return response.choices[0].text.strip() #response.choices[0].message["content"].strip()

    # Process user's prompt
    openai_response = get_openai_response_new(prompt)
    st.session_state.messages.append({"role": "assistant", "content": openai_response})
    st.chat_message("assistant").write(openai_response)

    # Assuming the response contains a Cypher query, you may need to adjust this based on your use case
    neptune_query = openai_response  # This should be a parsed Cypher query from the response
    neptune_response = query_neptune(neptune_query)
    st.session_state.messages.append({"role": "assistant", "content": str(neptune_response)})
    st.chat_message("assistant").write(str(neptune_response))
