import streamlit as st
import requests
from pyvis.network import Network

# Load configuration
config = {
    "neptune": {
        "host": "tf-20240207121511848700000014.cluster-ro-c9ezntcdvm4p.eu-west-2.neptune.amazonaws.com",
        "port": 8182,
        "use-iam-auth": True
    }
}

# Neptune connection details
neptune_host = config['neptune']['host']
neptune_port = config['neptune']['port']
use_iam_auth = config['neptune']['use-iam-auth']

# Streamlit app
st.title("AWS Neptune Graph Explorer")

# Function to send Gremlin queries to Neptune using HTTP
def run_gremlin_query(query):
    url = f'https://{neptune_host}:{neptune_port}/gremlin'
    headers = {"Content-Type": "application/json"}
    data = {
        "gremlin": query
    }
    try:
        response = requests.post(url, json=data, headers=headers, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return None

# Fetch nodes and edges
def fetch_graph():
    nodes_query = "g.V().limit(100)"
    edges_query = "g.E().limit(100)"
    
    nodes_response = run_gremlin_query(nodes_query)
    edges_response = run_gremlin_query(edges_query)
    
    nodes = nodes_response.get('result', {}).get('data', []) if nodes_response else []
    edges = edges_response.get('result', {}).get('data', []) if edges_response else []
    
    return nodes, edges

# Visualize graph
def visualize_graph(nodes, edges):
    net = Network(height="750px", width="100%", notebook=True)
    
    for node in nodes:
        node_id = node['id']
        label = node['label']
        properties = node['properties']
        title = f"{label}: {properties}"
        net.add_node(node_id, label=label, title=title)
    
    for edge in edges:
        source = edge['outV']
        target = edge['inV']
        label = edge['label']
        title = f"{label}"
        net.add_edge(source, target, title=title)
    
    return net

# Streamlit sidebar
with st.sidebar:
    st.header("Actions")
    if st.button("Fetch and Visualize Graph"):
        nodes, edges = fetch_graph()
        if nodes and edges:
            net = visualize_graph(nodes, edges)
            net.show("graph.html")

# Display graph
st.header("Graph Visualization")
st.markdown("Click the button in the sidebar to fetch and visualize the graph.")
