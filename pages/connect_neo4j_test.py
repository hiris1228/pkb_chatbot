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

# Function to run a query
def run_query(driver, query):
    with driver.session() as session:
        result = session.run(query)
        return result

# Streamlit app layout
st.title("Neo4j Streamlit Integration")

# Inputs for Neo4j connection
uri = st.text_input("Ngrok URI", os.getenv("NGROK_URI", "2.tcp.ngrok.io:14746"))
username = st.text_input("Username", os.getenv("NEO4J_USERNAME", "neo4j"))
password = st.text_input("Password", type="password", value=os.getenv("NEO4J_PASSWORD"))

# Connect to Neo4j
if st.button("Connect"):
    driver = create_driver(uri, username, password)
    st.success("Connected to Neo4j!")

# Query input
query = st.text_area("Cypher Query", "MATCH (n) RETURN n LIMIT 5")

# Run the query
if st.button("Run Query"):
    if 'driver' in locals():
        try:
            result = run_query(driver, query)
            for record in result:
                st.write(record)
        except Exception as e:
            st.error(f"Error running query: {e}")
    else:
        st.error("Please connect to the database first.")
