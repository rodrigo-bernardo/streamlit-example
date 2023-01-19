from sqlalchemy import create_engine, text
import pymysql
import streamlit as st
import pandas as pd
import plotly.express as px
import time
#import mysql.connector

# database connection information
host = "sql7.freesqldatabase.com"
user = "sql7589569"
password = "NTLDAUBVuH"
database = "sql7589569"


conn = create_engine("mysql+pymysql://sql7589569:NTLDAUBVuH@sql7.freesqldatabase.com/sql7589569?charset=utf8mb4")
c = conn.connect()

st.set_page_config(layout="wide")

st.markdown("""
    <style>
    div[data-testid="stMetricValue"] {
        font-size: 5 rem;
    }
    </style>
    """
, unsafe_allow_html=True)

st.write('Projeto "DDS"')

col1, col2 = st.columns(2)

with col1:
    grafico1lastMin = st.empty()
with col2:
    label_temperature = st.empty()



grafico1Todo = st.empty()

if st.button("RESET"):
    sql = text('DELETE FROM molde1;')
    result = conn.execute(sql)
    sql = text('ALTER TABLE molde1 AUTO_INCREMENT = 1;')
    result = conn.execute(sql)
    

while True:
    SQL_Query = pd.read_sql('SELECT DATAHORA,T1,P1 FROM molde1', conn)
    df = pd.DataFrame(SQL_Query, columns=['DATAHORA','T1','P1'])
    data = df[["T1", "P1"]]
    last_row = data.tail(1)
    fig = px.line(df, x="DATAHORA", y=data.columns,
        labels={
            "DATAHORA": "Data e Hora",
            "value" : "Valor",
            "variable" : "Legenda"
        },
        title='P1 and T1 sensor values')

    fig.update_xaxes(showgrid=True, ticks="inside")
    fig.update_layout({"uirevision": "foo"}, overwrite=True)

    with grafico1lastMin.container():
        st.plotly_chart(fig, use_container_width=True)

    with label_temperature.container():
        t1 = last_row["T1"]
        st.metric(label="Temperature Sensor 1#", value=t1)
        st.metric(label="Temperature Sensor 2#", value=t1)

    with grafico1Todo.container():
        st.plotly_chart(fig, use_container_width=True)


    time.sleep(1)