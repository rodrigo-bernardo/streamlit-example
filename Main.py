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
host = "localhost"
user = "root"
password = "123456789"
database = "ddsua"


conn = create_engine("mysql+pymysql://root:123456789@localhost/ddsua?charset=utf8mb4")
c = conn.connect()
select_ensaio = ""
st.markdown("""
    <style>
    div[data-testid="stMetricValue"] {
        font-size: 5rem;
    }
    </style>
    """
, unsafe_allow_html=True)

query = 'SELECT * FROM moldes'
SQL_Query = pd.read_sql_query(sql=text(query), con=conn.connect())
df = pd.DataFrame(SQL_Query, columns=['id','name','A','B','C'])

moldes = df['name'].values.tolist()
moldes.insert(0,"")
idx = 0
if 'selected_mould' in st.session_state:
    idx = moldes.index(st.session_state['selected_mould'])
    
select_mould = st.selectbox("Select the mould:",options=moldes,index=idx)
st.session_state['selected_mould'] = select_mould

idx = 0
if select_mould != "":
    SQL_Query = pd.read_sql("SELECT * FROM ensaios WHERE molde = '" + select_mould+"'", conn)
    df_ensaios = pd.DataFrame(SQL_Query, columns=['id','molde','id_molde','name'])
    ensaios = df_ensaios['name'].values.tolist()
    ensaios.insert(0,"")
    if ('selected_test' in st.session_state) and (st.session_state['selected_test'] in ensaios):
        idx = ensaios.index(st.session_state['selected_test'])
    select_ensaio = st.selectbox("Select the sample:",options=ensaios,index=idx)
    st.session_state['selected_test'] = select_ensaio

grafico1Todo = st.empty()

if select_mould == "":
    st.session_state['selected_test'] = ""
    select_ensaio = ""

if select_ensaio != "":
    if st.button("RESET", key=1):
        sql = text('DELETE FROM '+select_ensaio+';')
        result = conn.execute(sql)
        sql = text('ALTER TABLE '+select_ensaio+' AUTO_INCREMENT = 1;')
        result = conn.execute(sql)

while select_ensaio != "":
    SQL_Query = pd.read_sql("SELECT DATAHORA,T1,T2,P1,P2,D1,D2,D3,ACCX,ACCY,ACCZ,DEF FROM "+select_ensaio+"", conn)
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
    with grafico1Todo.container():
        st.plotly_chart(fig1, use_container_width=True)

    time.sleep(1)