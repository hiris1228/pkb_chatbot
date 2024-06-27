import streamlit as st
from neo4j import GraphDatabase
from pyvis.network import Network
import streamlit.components.v1 as components
import os

# Function to create a Neo4j driver instance
def create_driver(uri, user, password):
    # Ensure the URI starts with 'bolt://'
    if not uri.startswith("bolt://"):
        uri = "bolt://" + uri
    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver

# Function to run a query and fetch results as a graph
def run_query_as_graph(driver, query):
    with driver.session() as session:
        result = session.run(query)
        graph = result.graph()
        return graph

# Function to visualize the graph using pyvis
def visualize_graph(graph):
    net = Network(height='750px', width='100%', directed=True)

    # Add nodes and relationships to the network
    for node in graph.nodes:
        net.add_node(node.id, label=node.get('name', node.id))

    for relationship in graph.relationships:
        net.add_edge(relationship.start_node.id, relationship.end_node.id, label=relationship.type)

    net.set_options("""
    var options = {
      "nodes": {
        "font": {
          "size": 20
        }
      },
      "edges": {
        "font": {
          "size": 15,
          "align": "middle"
        },
        "color": {
          "color": "#848484",
          "highlight": "#848484",
          "hover": "#848484",
          "inherit": false
        },
        "smooth": false
      }
    }
    """)
    
    net.save_graph('graph.html')
    return net

# Streamlit app layout
st.title("Neo4j Streamlit Integration")

# Inputs for Neo4j connection
uri = st.text_input("Ngrok URI", os.getenv("NGROK_URI", "0.tcp.ngrok.io:15025"))
username = st.text_input("Username", os.getenv("NEO4J_USERNAME", "neo4j"))
password = st.text_input("Password", type="password", value=os.getenv("NEO4J_PASSWORD"))

# Use Streamlit session state to manage the driver instance
if 'driver' not in st.session_state:
    st.session_state.driver = None

# Connect to Neo4j
if st.button("Connect"):
    try:
        st.session_state.driver = create_driver(uri, username, password)
        st.success("Connected to Neo4j!")
    except Exception as e:
        st.error(f"Failed to connect to Neo4j: {e}")

# Query input
query = st.text_area("Cypher Query", "MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 25")

# Run the query and visualize the graph
if st.button("Run Query"):
    if st.session_state.driver:
        try:
            graph = run_query_as_graph(st.session_state.driver, query)
            net = visualize_graph(graph)
            HtmlFile = open("graph.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read()
            components.html(source_code, height=750, width="100%")
        except Exception as e:
            st.error(f"Error running query: {e}")
    else:
        st.error("Please connect to the database first.")
