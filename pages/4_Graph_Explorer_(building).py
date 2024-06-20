import streamlit as st
import json
import os
from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from pyvis.network import Network
import aiohttp

# Load configuration
config_path = 'config.json'

if not os.path.exists(config_path):
    st.error(f"Configuration file not found at {config_path}")
else:
    try:
        with open(config_path) as config_file:
            config = json.load(config_file)
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON configuration: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
    else:
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
            return DriverRemoteConnection(connection_string, 'g')

        # Fetch nodes and edges
        def fetch_graph():
            g = Graph().traversal().withRemote(create_graph_connection())
            nodes = g.V().limit(100).toList()
            edges = g.E().limit(100).toList()
            return nodes, edges

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
            if st.button("Fetch and Visualize Graph"):
                nodes, edges = fetch_graph()
                net = visualize_graph(nodes, edges)
                net.show("graph.html")

        # Display graph
        st.header("Graph Visualization")
        st.markdown("Click the button in the sidebar to fetch and visualize the graph.")
