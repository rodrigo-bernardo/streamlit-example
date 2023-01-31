import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy import MetaData
import pandas as pd

st.set_page_config(
    page_title="Mould Management",
    layout="wide")

st.title("Mould Management")


def btn_edit():
    if 'btn_edit' not in st.session_state:
        st.session_state.btn_edit = False
    val = st.session_state.btn_edit
    if val == True:
        st.session_state.btn_edit = False
    if val == False:
        st.session_state.btn_edit = True



with st.expander("Click to see witch moulds and settings are present."):
    conn = create_engine("mysql+pymysql://root:.,Descobre123@127.0.0.1/ddsua2023?charset=utf8mb4")
    SQL_Query = pd.read_sql('SELECT * FROM moldes;', conn)
    df = pd.DataFrame(SQL_Query, columns=['id','name','A','B','C'])
    st.dataframe(df)
    st.button("Edit", key = 0, on_click=btn_edit)
    if st.session_state.btn_edit:
        l1 = []
        idx = -1
        col1, in1, in2, in3 = st.columns([3,1,1,1])
        with col1:
            selected_mould = st.selectbox("Select wich mould settings to edit:", options=df["name"])
            idx = df["name"].to_list().index(selected_mould)
        with in1:
            valA = st.number_input("A value:" , value = df['A'][idx])
            l1.append(valA)
        with in2:
            valB = st.number_input("B value:" , value = df['B'][idx])
            l1.append(valB)
        with in3:
            valC = st.number_input("C value:" , value = df['C'][idx])
            l1.append(valC)

        l2 = df.iloc[idx].to_list()[2:]
        if l2 != l1:
            st.button("Save")
            # acrescentar codigo SQL que dá update da linha na BD
