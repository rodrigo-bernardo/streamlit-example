from sqlalchemy import create_engine, text
import pymysql
import streamlit as st
import pandas as pd
import plotly.express as px
import time
#import mysql.connector

# database connection information
host = "127.0.0.1"
user = "root"
password = "123456789"
database = "ddsua"


conn = create_engine("mysql+pymysql://root:.,Descobre123@127.0.0.1/ddsua2023?charset=utf8mb4")
c = conn.connect()

st.set_page_config(
    page_title="Temperature",
    layout="wide")

st.markdown("""
    <style>
    div[data-testid="stMetricValue"] {
        font-size: 5rem;
    }
    </style>
    """
, unsafe_allow_html=True)



col1, col2 = st.columns(2)

with col1:
    grafico1lastMin = st.empty()
with col2:
    label_temperature = st.empty()

grafico1Todo = st.empty()

select_test = ""
if ('selected_test' in st.session_state):
    select_test = st.session_state['selected_test']

if select_test != "":
    while True:
        SQL_Query = pd.read_sql('SELECT DATAHORA,T1,T2 FROM '+select_test+';', conn)
        df = pd.DataFrame(SQL_Query, columns=['DATAHORA','T1','T2'])
        data = df[["T1", "T2"]]
        last_row = data.tail(1)
        last_minute_data = data.tail(60)
        last_minute = df.tail(60)
        fig1 = px.line(df, x="DATAHORA", y=data.columns,
            labels={
                "DATAHORA": "Data e Hora",
                "value" : "Valor",
                "variable" : "Legenda"
            },
            title='T1 and T2 sensor values')

        fig1.update_xaxes(showgrid=True, ticks="inside")
        fig1.update_layout({"uirevision": "foo"}, overwrite=True)
    
        fig2 = px.line(last_minute, x="DATAHORA", y=last_minute_data.columns,
            labels={
                "DATAHORA": "Data e Hora",
                "value" : "Valor",
                "variable" : "Legenda"
            },
            title='T1 and T2 sensor values (last minute)')

        fig2.update_xaxes(showgrid=True, ticks="inside")
        fig2.update_layout({"uirevision": "foo"}, overwrite=True)

        with grafico1lastMin.container():
            st.plotly_chart(fig2, use_container_width=True)

        with label_temperature.container():
            t1 = last_row["T1"]
            t2 = last_row["T2"]
            st.metric(label="Temperature Sensor 1#", value=t1)
            st.metric(label="Temperature Sensor 2#", value=t2)

        with grafico1Todo.container():
            st.plotly_chart(fig1, use_container_width=True)


        time.sleep(1)