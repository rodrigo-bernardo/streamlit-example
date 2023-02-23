from sqlalchemy import create_engine, text
import pymysql
import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(
    page_title="Dashboard",
    page_icon="",
    layout="wide"
)

if 'selected_mould' not in st.session_state:
    st.session_state['selected_mould'] = ""

if 'selected_test' not in st.session_state:
    st.session_state['selected_test'] = ""

if 'select_disable' not in st.session_state:
    st.session_state['select_disable'] = False

if 'btn_start_stream' not in st.session_state:
    st.session_state['btn_start_stream'] = "Start data stream"

st.title("Dashboard")

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
 

def _set_slc_mould():
    st.session_state['selected_mould'] = st.session_state.select_mould



idx=moldes.index(st.session_state['selected_mould'])
st.session_state['selected_mould'] = st.selectbox("Select the mould:",options=moldes,
                                                  key="select_mould",
                                                  index = idx, 
                                                  on_change=_set_slc_mould,
                                                  disabled=st.session_state['select_disable'])

select_mould = st.session_state['selected_mould']

if select_mould != "":
    query = "SELECT * FROM ensaios WHERE molde = '" + select_mould+"'"
    SQL_Query = pd.read_sql_query(sql=text(query), con=conn.connect())
    df_ensaios = pd.DataFrame(SQL_Query, columns=['id','molde','id_molde','name'])
    ensaios = df_ensaios['name'].values.tolist()
    ensaios.insert(0,"")

    def _set_slc_test():
        st.session_state['selected_test'] = st.session_state.AAA

    idx = ensaios.index(st.session_state['selected_test'])
    st.selectbox("Select the sample:",options=ensaios,key="AAA",index=idx, on_change=_set_slc_test, disabled=st.session_state['select_disable'])
    select_ensaio = st.session_state['selected_test']


if select_mould == "":
    st.session_state['selected_test'] = ""
    select_ensaio = ""

def _on_start_stream():
    if not st.session_state['select_disable']:
        st.session_state['select_disable'] = True
        st.session_state['btn_start_stream'] = "Stop data stream"
        
    if st.session_state['select_disable']:
        st.session_state['select_disable'] = False
        st.session_state['btn_start_stream'] = "Start data stream"
        

if select_ensaio != "":
    st.button(st.session_state['btn_start_stream'],key="start_stream", on_click=_on_start_stream)


if select_ensaio != "":
    page = st.selectbox("Select variables:",["All","Temperature","Pressure","Displacement","Accelerometer","Strain"],index=0,key="page")
    if page == "All":
        grafico = st.empty()
        if st.button("RESET", key=1):
            with conn.connect() as connection:
                sql = text('DELETE FROM '+select_ensaio+';')
                result = connection.execute(sql)
                sql = text('ALTER TABLE '+select_ensaio+' AUTO_INCREMENT = 1;')
                result = connection.execute(sql)
                connection.commit()
ts = 2

if select_ensaio != "":    
    while page == "All":
        query = "SELECT DATAHORA,T1,T2,P1,P2,D1,D2,D3,ACCX,ACCY,ACCZ,DEF FROM "+select_ensaio+""
        SQL_Query = pd.read_sql(sql=text(query), con=conn.connect())
        df = pd.DataFrame(SQL_Query, columns=['DATAHORA','T1','T2','P1','P2','D1','D2','D3','ACCX','ACCY','ACCZ','DEF'])
        data = df[['T1','T2','P1','P2','D1','D2','D3','ACCX','ACCY','ACCZ','DEF']]
        fig1 = px.line(df, x="DATAHORA", y=data.columns,
            labels={
                "DATAHORA": "Data e Hora",
                "value" : "Valor",
                "variable" : "Legenda"
            },
            title='Sensor values')
        fig1.update_xaxes(showgrid=True, ticks="inside")
        fig1.update_layout({"uirevision": "foo"}, overwrite=True)
        with grafico.container():
            st.plotly_chart(fig1, use_container_width=True)

        time.sleep(ts)

    while page == "Temperature":
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
                query = 'SELECT DATAHORA,T1,T2 FROM '+select_test+';'
                SQL_Query = pd.read_sql(sql=text(query), con=conn.connect())
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

                time.sleep(ts)

    while page == "Pressure":
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
                query = 'SELECT DATAHORA,P1,P2 FROM '+select_test+';'
                SQL_Query = pd.read_sql_query(sql=text(query), con=conn.connect())
                df = pd.DataFrame(SQL_Query, columns=['DATAHORA','P1','P2'])
                data = df[["P1", "P2"]]
                last_row = data.tail(1)
                last_minute_data = data.tail(60)
                last_minute = df.tail(60)
                fig1 = px.line(df, x="DATAHORA", y=data.columns,
                    labels={
                        "DATAHORA": "Data e Hora",
                        "value" : "Valor",
                        "variable" : "Legenda"
                    },
                    title='P1 and P2 sensor values')

                fig1.update_xaxes(showgrid=True, ticks="inside")
                fig1.update_layout({"uirevision": "foo"}, overwrite=True)

                fig2 = px.line(last_minute, x="DATAHORA", y=last_minute_data.columns,
                    labels={
                        "DATAHORA": "Data e Hora",
                        "value" : "Valor",
                        "variable" : "Legenda"
                    },
                    title='P1 and P2 sensor values (last minute)')

                fig2.update_xaxes(showgrid=True, ticks="inside")
                fig2.update_layout({"uirevision": "foo"}, overwrite=True)

                with grafico1lastMin.container():
                    st.plotly_chart(fig2, use_container_width=True)

                with label_pressure.container():
                    p1 = last_row["P1"]
                    p2 = last_row["P2"]
                    st.metric(label="Pressure Sensor 1#", value=p1)
                    st.metric(label="Pressure Sensor 2#", value=p2)

                with grafico1Todo.container():
                    st.plotly_chart(fig1, use_container_width=True)

        time.sleep(ts)

    while page == "Displacement":
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
                SQL_Query = pd.read_sql_query(sql=text(query), con=conn.connect())
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

        time.sleep(ts)

    while page == "Accelerometer":
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
                query = 'SELECT DATAHORA,ACCX,ACCY,ACCZ FROM '+select_test+';'
                SQL_Query = pd.read_sql_query(sql=text(query), con=conn.connect())
                df = pd.DataFrame(SQL_Query, columns=['DATAHORA','ACCX','ACCY','ACCZ'])
                data = df[["ACCX", "ACCY", "ACCZ"]]
                last_row = data.tail(1)
                last_minute_data = data.tail(60)
                last_minute = df.tail(60)
                fig1 = px.line(df, x="DATAHORA", y=data.columns,
                    labels={
                        "DATAHORA": "Data e Hora",
                        "value" : "Valor",
                        "variable" : "Legenda"
                    },
                    title='x, y and z axis accelerometer sensor values')

                fig1.update_xaxes(showgrid=True, ticks="inside")
                fig1.update_layout({"uirevision": "foo"}, overwrite=True)

                fig2 = px.line(last_minute, x="DATAHORA", y=last_minute_data.columns,
                    labels={
                        "DATAHORA": "Data e Hora",
                        "value" : "Valor",
                        "variable" : "Legenda"
                    },
                    title='x, y and z axis accelerometer sensor values (last minute)')

                fig2.update_xaxes(showgrid=True, ticks="inside")
                fig2.update_layout({"uirevision": "foo"}, overwrite=True)

                with grafico1lastMin.container():
                    st.plotly_chart(fig2, use_container_width=True)

                with label_pressure.container():
                    accx = last_row["ACCX"]
                    accy = last_row["ACCY"]
                    accz = last_row["ACCZ"]
                    st.metric(label="Accelerometer Sensor x axis", value=accx)
                    st.metric(label="Accelerometer Sensor y axis", value=accy)
                    st.metric(label="Accelerometer Sensor z axis", value=accz)

                with grafico1Todo.container():
                    st.plotly_chart(fig1, use_container_width=True)

        time.sleep(ts)

    while page == "Strain":
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
                query = 'SELECT DATAHORA,DEF FROM '+select_test+';'
                SQL_Query = pd.read_sql_query(sql=text(query), con=conn.connect())
                df = pd.DataFrame(SQL_Query, columns=['DATAHORA','DEF'])
                data = df[["DEF"]]
                last_row = data.tail(1)
                last_minute_data = data.tail(60)
                last_minute = df.tail(60)
                fig1 = px.line(df, x="DATAHORA", y=data.columns,
                    labels={
                        "DATAHORA": "Data e Hora",
                        "value" : "Valor",
                        "variable" : "Legenda"
                    },
                    title='Strain sensor value')

                fig1.update_xaxes(showgrid=True, ticks="inside")
                fig1.update_layout({"uirevision": "foo"}, overwrite=True)

                fig2 = px.line(last_minute, x="DATAHORA", y=last_minute_data.columns,
                    labels={
                        "DATAHORA": "Data e Hora",
                        "value" : "Valor",
                        "variable" : "Legenda"
                    },
                    title='Strain sensor value (last minute)')

                fig2.update_xaxes(showgrid=True, ticks="inside")
                fig2.update_layout({"uirevision": "foo"}, overwrite=True)

                with grafico1lastMin.container():
                    st.plotly_chart(fig2, use_container_width=True)

                with label_pressure.container():
                    strain = last_row["DEF"]
                    st.metric(label="Strain Sensor 1#", value=strain)

                with grafico1Todo.container():
                    st.plotly_chart(fig1, use_container_width=True)

        time.sleep(ts)



