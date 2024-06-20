import asyncio
import streamlit as st
from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
import aiohttp

# Ensure aiohttp is working
st.write(f"aiohttp version: {aiohttp.__version__}")

# Neptune connection details
neptune_host = "your-neptune-endpoint"
neptune_port = 8182

# Establish a connection to Neptune
def create_graph_connection():
    connection_string = f'wss://{neptune_host}:{neptune_port}/gremlin'
    return DriverRemoteConnection(connection_string, 'g')

# Fetch nodes (test function)
async def fetch_nodes():
    try:
        g = Graph().traversal().withRemote(create_graph_connection())
        nodes = await g.V().limit(10).toList()
        st.write("Nodes fetched successfully")
        st.write(nodes)
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Streamlit app
st.title("AWS Neptune Graph Explorer")

if st.button("Test Fetch Nodes"):
    asyncio.run(fetch_nodes())
