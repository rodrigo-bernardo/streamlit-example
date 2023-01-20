import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy import MetaData

st.set_page_config(
    page_title="Mould Management",
    layout="wide")


# Connect to the database
conn = create_engine("mysql+pymysql://sql7589569:NTLDAUBVuH@sql7.freesqldatabase.com/sql7589569?charset=utf8mb4")

# Create a metadata object
metadata = MetaData()

# Reflect the tables
metadata.reflect(bind=conn)

options = []
# Print the table names
for table in metadata.tables:
    options.append(table)

options.append("Add a new mould")

selected_option = st.selectbox(label="Select a mould", options=options)

if selected_option == "Add a new mould":
    st.text_input(label="Insert the name for the new mould")
    st.button(label="Done")
