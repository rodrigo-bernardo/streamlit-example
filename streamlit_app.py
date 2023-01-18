#from sqlalchemy import create_engine, text
import streamlit as st
import pandas as pd
import plotly.express as px
import time
import mysql.connector

# database connection information
host = "sql7.freesqldatabase.com"
user = "sql7589569"
password = "NTLDAUBVuH"
database = "sql7589569"

conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
c = conn.cursor()
#conn = create_engine("mysql+pymysql://sql7589569:NTLDAUBVuH@sql7.freesqldatabase.com/sql7589569?charset=utf8mb4")


st.set_page_config(layout="wide")

st.write("My First App")

placeholder = st.empty()

if st.button("RESET"):
    query = 'DELETE FROM molde1;'
    c.execute(query)
    query = 'ALTER TABLE molde1 AUTO_INCREMENT = 1;'
    c.execute(query)
    #sql = text('DELETE FROM molde1;')
    #result = conn.execute(sql)
    #sql = text('ALTER TABLE molde1 AUTO_INCREMENT = 1;')
    #result = conn.execute(sql)
    

while True:
    #SQL_Query = pd.read_sql('SELECT DATAHORA,T1,P1 FROM molde1', conn)
    #df = pd.DataFrame(SQL_Query, columns=['DATAHORA','T1','P1'])
    query = "Select * from molde1;"
    df = pd.read_sql(query,conn)
    data = df[["T1", "P1"]]
    fig = px.line(df, x="DATAHORA", y=data.columns,
        labels={
            "DATAHORA": "Data e Hora",
            "value" : "Valor",
            "variable" : "Legenda"
        },
        title='P1 and T1 sensor values')

    fig.update_xaxes(showgrid=True, ticks="inside")
    fig.update_layout({"uirevision": "foo"}, overwrite=True)

    with placeholder.container():
        st.plotly_chart(fig, use_container_width=True)

    time.sleep(1)