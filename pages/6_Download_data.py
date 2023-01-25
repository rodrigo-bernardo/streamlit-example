from sqlalchemy import create_engine, text
import pymysql
import streamlit as st
import pandas as pd
import plotly.express as px
import time
import datetime

st.title("Download Data")
st.markdown("Select the time interval of the data to download as a CSV file.")

select_test = ""
if ('selected_test' in st.session_state):
    select_test = st.session_state['selected_test']
if select_test == "":
    st.markdown("No selected data. Please, select data on main page.")

if select_test != "":
    d1 = st.date_input(
        "Select the start date / time:",
        datetime.date.today())

    t1 = st.time_input("t1", datetime.datetime.now(),label_visibility="collapsed")

    d2 = st.date_input(
        "Select the final date / time:",
        datetime.date.today())

    t2 = st.time_input("t2", datetime.datetime.now(),label_visibility="collapsed")

    c1 = datetime.datetime.combine(d1,t1)
    c2 = datetime.datetime.combine(d2,t2)

    ts1 = datetime.datetime.timestamp(c1)
    ts2 = datetime.datetime.timestamp(c2)

    str1 = datetime.datetime.fromtimestamp(ts1).strftime("%Y/%m/%d %H:%M:%S")
    str2 = datetime.datetime.fromtimestamp(ts2).strftime("%Y/%m/%d %H:%M:%S")

    if ts2 <= ts1:
        st.write("The selected interval is not possible.")
    else:
        st.write("The selected interval is from ",d1,t1,"to ",d2,t2)
        conn = create_engine("mysql+pymysql://root:.,Descobre123@127.0.0.1/ddsua2023?charset=utf8mb4")
        string_query = "SELECT * FROM "+select_test+" WHERE datahora BETWEEN '" + str1 +"' AND '" + str2 +"'"
        string_query = string_query.replace("/","-")
        print(string_query)
        SQL_Query = pd.read_sql(string_query, conn)
        df = pd.DataFrame(SQL_Query)#, columns=['DATAHORA','T1','T2'])
        df = df.set_index('id')
        csv = df.to_csv().encode('utf-8')

        st.markdown("Data header preview:")
        st.write(df.head())

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='data.csv',
            mime='text/csv',
        )
    