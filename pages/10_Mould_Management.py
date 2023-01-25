import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy import MetaData
import pandas as pd

st.set_page_config(
    page_title="Mould Management",
    layout="wide")

st.title("Mould Management")

with st.expander("Click to see witch moulds and settings are present."):
    conn = create_engine("mysql+pymysql://root:.,Descobre123@127.0.0.1/ddsua2023?charset=utf8mb4")
    SQL_Query = pd.read_sql('SELECT * FROM moldes;', conn)
    df = pd.DataFrame(SQL_Query, columns=['id','name','A','B','C'])
    st.dataframe(df)
