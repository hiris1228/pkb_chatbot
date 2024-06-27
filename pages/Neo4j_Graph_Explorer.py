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

# Function to run a query and fetch results
def run_query(driver, query):
    with driver.session() as session:
        result = session.run(query)
        records = result.data()  # Fetch all records at once
        return records

# Function to visualize the graph using pyvis
def visualize_graph(records):
    net = Network(height='750px', width='100%', directed=True)
    
    for record in records:
        for key, value in record.items():
            if isinstance(value, dict) and 'id' in value:
                net.add_node(value['id'], label=value['id'])
            elif isinstance(value, list):
                for item in value:
                    if 'start' in item and 'end' in item and 'type' in item:
                        net.add_node(item['start'], label=item['start'])
                        net.add_node(item['end'], label=item['end'])
                        net.add_edge(item['start'], item['end'], label=item['type'])

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
uri = st.text_input("Ngrok URI", os.getenv("NGROK_URI", "0.tcp.ngrok.io:19764"))
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
query = st.text_area("Cypher Query", "MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 30")

# Run the query and visualize the graph
if st.button("Run Query"):
    if st.session_state.driver:
        try:
            records = run_query(st.session_state.driver, query)
            net = visualize_graph(records)
            HtmlFile = open("graph.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read()
            components.html(source_code, height=750, width="100%")
        except Exception as e:
            st.error(f"Error running query: {e}")
    else:
        st.error("Please connect to the database first.")
