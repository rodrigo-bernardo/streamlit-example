import streamlit as st
from sqlalchemy import create_engine, text, MetaData
import pandas as pd

st.set_page_config(
    page_title="Mould Management",
    layout="wide")

st.markdown("""
    <style>
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-k1vhr4.egzxvld5 > div.block-container.css-k1ih3n.egzxvld4 > div:nth-child(1) > div > div.css-1fcdlhc.e1s6o5jp0 > ul > li > div.st-am.st-ce.st-cf.st-cg.st-ch > div > div:nth-child(1) > div > div.css-ocqkz7.e1tzin5v4 > div:nth-child(4) > div:nth-child(1) > div > div:nth-child(2) > div > button{
        float: right;
    }
    </style>
    """
, unsafe_allow_html=True)

st.title("Mould Management")

if not hasattr(st.session_state,'btn_edit'):
    st.session_state.btn_edit = False

def btn_edit():
    val = st.session_state.btn_edit
    if val == True:
        st.session_state.btn_edit = False
    if val == False:
        st.session_state.btn_edit = True

conn = None

with st.expander("Click to see witch moulds and settings are present."):
    conn = create_engine("mysql+pymysql://root:123456789@127.0.0.1/ddsua?charset=utf8mb4")
    query = 'SELECT * FROM moldes;'
    SQL_Query = pd.read_sql(sql=text(query), con=conn.connect())
    df = pd.DataFrame(SQL_Query, columns=['id','name','A','B','C'])
    st.dataframe(df)
    st.button("Edit", key = 0, on_click=btn_edit)
    if st.session_state.btn_edit:
        selected_mould = ""
        l1 = []
        idx = -1
        col1, in1, in2, in3, dell = st.columns([3,1,1,1,1])
        with col1:
            selected_mould = st.selectbox("Select wich mould settings to edit:", options=df["name"])
            idx = df["name"].to_list().index(selected_mould)
            empty1 = st.empty()
        with in1:
            valA = st.number_input("A value:" , value = df['A'][idx])
            l1.append(valA)
        with in2:
            valB = st.number_input("B value:" , value = df['B'][idx])
            l1.append(valB)
        with in3:
            valC = st.number_input("C value:" , value = df['C'][idx])
            l1.append(valC)
        with dell:
            st.header("")
            if st.button("Delete mould", key = "btn_delete"):
                sql = text('DELETE FROM moldes WHERE name="'+selected_mould+'";')
                with conn.connect() as connection:
                    result = connection.execute(sql)
                    connection.commit()
                st.experimental_rerun()

        l2 = df.iloc[idx].to_list()[2:]
        if l2 != l1:
            with empty1:
                if st.button("Save"):
                    sql = text('UPDATE moldes SET A = '+ str(l1[0]) + ', B = ' + str(l1[1]) + ', C = ' + str(l1[2]) + ' WHERE name = "' + selected_mould + '";')
                    with conn.connect() as connection:
                        result = connection.execute(sql)
                        connection.commit()
                    st.experimental_rerun()

with st.expander("Click to add a new mould."):
    conn = create_engine("mysql+pymysql://root:123456789@localhost/ddsua?charset=utf8mb4")
    col1, in1, in2, in3 = st.columns([3,1,1,1])
    l1 = []
    with col1:
        mould_name = st.text_input("Mould name:",value="")
    with in1:
        valA = st.number_input("A value:" , value = 0)
        l1.append(valA)
    with in2:
        valB = st.number_input("B value:" , value = 0)
        l1.append(valB)
    with in3:
        valC = st.number_input("C value:" , value = 0)
        l1.append(valC)

    ena = False
    if mould_name == "":
        ena = True

    if st.button("Add new mould",disabled=ena):
        sql = text('INSERT INTO moldes (name, A, B, C) VALUES ("'+mould_name+'", '+str(l1[0])+', '+str(l1[1])+', '+str(l1[2])+');')
        with conn.connect() as connection:
            result = connection.execute(sql)
            connection.commit()
        st.experimental_rerun()

st.session_state['previus_page'] = "management"