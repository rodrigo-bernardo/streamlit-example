from sqlalchemy import create_engine, text
import pymysql
import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(
    page_title="Homepage",
    page_icon="",
    layout="wide"
)

st.title("Homepage")

st.write('Projeto "DDS"')

# database connection information
host = "127.0.0.1"
user = "root"
password = ".,Descobre123"
database = "ddsua2023"


conn = create_engine("mysql+pymysql://root:.,Descobre123@127.0.0.1/ddsua2023?charset=utf8mb4")
c = conn.connect()

st.markdown("""
    <style>
    div[data-testid="stMetricValue"] {
        font-size: 5rem;
    }
    </style>
    """
, unsafe_allow_html=True)

grafico1Todo = st.empty()

if st.button("RESET"):
    sql = text('DELETE FROM molde1;')
    result = conn.execute(sql)
    sql = text('ALTER TABLE molde1 AUTO_INCREMENT = 1;')
    result = conn.execute(sql)
    

while True:
    SQL_Query = pd.read_sql('SELECT DATAHORA,T1,T2,P1,P2,D1,D2,D3,ACCX,ACCY,ACCZ,DEF FROM molde1', conn)
    df = pd.DataFrame(SQL_Query, columns=['DATAHORA','T1','T2','P1','P2','D1','D2','D3','ACCX','ACCY','ACCZ','DEF'])
    data = df[['T1','T2','P1','P2','D1','D2','D3','ACCX','ACCY','ACCZ','DEF']]
    last_row = data.tail(1)

    fig1 = px.line(df, x="DATAHORA", y=data.columns,
        labels={
            "DATAHORA": "Data e Hora",
            "value" : "Valor",
            "variable" : "Legenda"
        },
        title='Sensor values')

    fig1.update_xaxes(showgrid=True, ticks="inside")
    fig1.update_layout({"uirevision": "foo"}, overwrite=True)

    #with label_temperature.container():
    #    t1 = last_row["T1"]
    #    t2 = last_row["T2"]
    #    st.metric(label="Temperature Sensor 1#", value=t1)
    #    st.metric(label="Temperature Sensor 2#", value=t2)

    with grafico1Todo.container():
        st.plotly_chart(fig1, use_container_width=True)


    time.sleep(1)