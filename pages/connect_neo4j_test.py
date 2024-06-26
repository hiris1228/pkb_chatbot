import streamlit as st
from neo4j import GraphDatabase
import os

# Function to create a Neo4j driver instance
def create_driver(uri, user, password):
    # Ensure the URI starts with 'bolt://'
    if not uri.startswith("bolt://"):
        uri = "bolt://" + uri
    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver

# Streamlit app layout
st.title("Neo4j Streamlit Integration")

# Inputs for Neo4j connection
uri = st.text_input("Ngrok URI", os.getenv("NGROK_URI", "0.tcp.ngrok.io:xxxxx"))
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
query = st.text_area("Cypher Query", "MATCH (n) RETURN n LIMIT 5")

# Run the query
if st.button("Run Query"):
    if st.session_state.driver:
        try:
            result = run_query(st.session_state.driver, query)
            for record in result:
                st.write(record)
        except Exception as e:
            st.error(f"Error running query: {e}")
    else:
        st.error("Please connect to the database first.")

# Function to run a query
def run_query(driver, query):
    with driver.session() as session:
        result = session.run(query)
        return result
