import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

st.title('Hello Pyvis')
# make Network show itself with repr_html

countrycode = 'MX'
institutioncode = 'K'
countryname = 'Mexico'
institutionname = 'Royal Botanic Gardens Kew'
taxon = 'Datura arborea'
namelist = ['Michael Owen','Dillon D. Dillon','Abundio Sagástegui Alva']

# Sample DataFrame
data = {
    'Name': ['John', 'Jane', 'Doe'],
    'Age': [28, 34, 29],
    'Occupation': ['Engineer', 'Doctor', 'Artist']
}

# Display the DataFrame in Streamlit
st.title("Simple DataFrame Display")
st.write("Below is a sample DataFrame displayed using Streamlit:")

# Streamlit method to display dataframe
st.dataframe(data)

# Create the network
g = Network(height='400px', width='80%', heading='')

# Add nodes with different colors
g.add_node(0, label='current specimen', color='#f7b5ca')
g.add_node(1, label=countryname, color='#f5c669')
g.add_node(2, label=institutionname, color='#82b6fa')
g.add_node(3, label=taxon, color='#befa82')

# Add edges
g.add_edge(0, 1, color='black')
g.add_edge(0, 2, color='black')
g.add_edge(0, 3, color='black')

# dashes represent suggestions
num_name = 4
for name in namelist:
    g.add_node(num_name, label=name, color='#fad5c0')
    g.add_edge(0, num_name, color='black', dashes=True)
    num_name = num_name+1

# Generate and show the network
html_file = 'example.html'
g.save_graph(html_file)

HtmlFile = open("example.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
components.html(source_code, height = 900,width=900)
