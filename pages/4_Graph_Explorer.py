import streamlit as st
import json
import os
from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from pyvis.network import Network

# Verify aiohttp installation
try:
    import aiohttp
    st.write(f"aiohttp version: {aiohttp.__version__}")
except ImportError:
    st.error("aiohttp is not installed. Please install it by running `pip install aiohttp`.")

# Verify gremlin_python installation
try:
    import gremlin_python
    # st.write(f"gremlin_python version: {gremlin_python.__version__}")
except ImportError:
    st.error("gremlin_python is not installed. Please install it by running `pip install gremlinpython`.")

# Load configuration
config_path = 'config.json'

def load_config(path):
    if not os.path.exists(path):
        st.error(f"Configuration file not found at {path}")
        return None
    try:
        with open(path) as config_file:
            return json.load(config_file)
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON configuration: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

# Hardcoded configuration
config = {
    "neptune": {
        "host": "",
        "port": 8182,
        "use-iam-auth": True  # Set to True if using IAM authentication
    }
}

if config:
    st.success("Configuration loaded successfully")

    # Neptune connection details
    neptune_host = config['neptune']['host']
    neptune_port = config['neptune']['port']
    use_iam_auth = config['neptune']['use-iam-auth']

    # Streamlit app
    st.title("AWS Neptune Graph Explorer")

    # Establish a connection to Neptune
    def create_graph_connection():
        connection_string = f'wss://{neptune_host}:{neptune_port}/gremlin'
        # connection_string = f'https://{neptune_host}:{neptune_port}/gremlin'
        return DriverRemoteConnection(connection_string, 'g')

    # Fetch nodes and edges
    def fetch_graph():
        try:
            g = Graph().traversal().withRemote(create_graph_connection())
            nodes = g.V().limit(100).toList()
            edges = g.E().limit(100).toList()
            return nodes, edges
        except Exception as e:
            st.error(f"An error occurred while fetching the graph: {e}")
            return [], []

    # Visualize graph
    def visualize_graph(nodes, edges):
        net = Network(height="750px", width="100%", notebook=True)
        for node in nodes:
            net.add_node(node.id, label=node.label, title=str(node.valueMap()))
        for edge in edges:
            net.add_edge(edge.outV.id, edge.inV.id, title=edge.label)
        return net

    # Streamlit sidebar
    with st.sidebar:
        st.header("Actions")
        if st.button("Fetch and Visualise Graph"):
            nodes, edges = fetch_graph()
            if nodes and edges:
                net = visualize_graph(nodes, edges)
                net.show("graph.html")

    # Display graph
    st.header("Graph Visualisation")
    st.markdown("Click the button in the sidebar to fetch and visualise the graph.")
