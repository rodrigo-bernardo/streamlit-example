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

# Print the table names
for table in metadata.tables:
    st.write(table)