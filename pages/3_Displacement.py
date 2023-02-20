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

conn = create_engine("mysql+pymysql://root:123456789@localhost/ddsua?charset=utf8mb4")
c = conn.connect()

st.set_page_config(
    page_title="Displacement",
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
    label_pressure = st.empty()

grafico1Todo = st.empty()
    
select_test = ""
if ('selected_test' in st.session_state):
    select_test = st.session_state['selected_test']

if select_test != "":
    while True:
        query = 'SELECT DATAHORA,D1,D2,D3 FROM '+select_test+';'
        SQL_Query = pd.read_sql(sql=text(query), con=conn.connect())
        df = pd.DataFrame(SQL_Query, columns=['DATAHORA','D1','D2','D3'])
        data = df[["D1", "D2", "D3"]]
        last_row = data.tail(1)
        last_minute_data = data.tail(60)
        last_minute = df.tail(60)
        fig1 = px.line(df, x="DATAHORA", y=data.columns,
            labels={
                "DATAHORA": "Data e Hora",
                "value" : "Valor",
                "variable" : "Legenda"
            },
            title='D1, D2 and D3 sensor values')

        fig1.update_xaxes(showgrid=True, ticks="inside")
        fig1.update_layout({"uirevision": "foo"}, overwrite=True)

        fig2 = px.line(last_minute, x="DATAHORA", y=last_minute_data.columns,
            labels={
                "DATAHORA": "Data e Hora",
                "value" : "Valor",
                "variable" : "Legenda"
            },
            title='D1, D2 and D3 sensor values (last minute)')

        fig2.update_xaxes(showgrid=True, ticks="inside")
        fig2.update_layout({"uirevision": "foo"}, overwrite=True)

        with grafico1lastMin.container():
            st.plotly_chart(fig2, use_container_width=True)

        with label_pressure.container():
            d1 = last_row["D1"]
            d2 = last_row["D2"]
            d3 = last_row["D3"]
            st.metric(label="Displacement Sensor 1#", value=d1)
            st.metric(label="Displacement Sensor 2#", value=d2)
            st.metric(label="Displacement Sensor 3#", value=d3)

        with grafico1Todo.container():
            st.plotly_chart(fig1, use_container_width=True)


        time.sleep(1)