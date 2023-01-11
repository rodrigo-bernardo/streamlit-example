from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import mysql.connector
from mysql.connector import Error
import datetime
import numpy as np
from UliEngineering.SignalProcessing.Simulation import sine_wave, cosine_wave
from matplotlib import pyplot as plt
from datetime import datetime


def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

# Configure the properties of the sine wave here
frequency = 0.01 # 10 Hz sine / cosine wave
samplerate = 1 # 10 kHz
nseconds = 120 # Generate 1 second of data
sine = sine_wave(frequency=frequency, samplerate=samplerate, length=nseconds)
cosine = cosine_wave(frequency=frequency, samplerate=samplerate, length=nseconds)
nsamples = len(sine) # How many values we have in the data arrays

print(nsamples)

start_timestamp = pd.Timestamp('now')

timedelta = pd.Timedelta(1/samplerate, 'seconds')
timestamps =  [start_timestamp + i * timedelta for i in range(nsamples)]

df = pd.DataFrame(index=timestamps, data={
    "Sine": sine,
    "Cosine": cosine
})
df.index.name = 'Timestamp'

print(df.index[0].date())
print(df.index[0].time().replace(microsecond=0))

# Use nice plotting style
plt.style.use("ggplot")
# Plot dataset
df.plot()
# Make figure larger
plt.gcf().set_size_inches(10, 5)

plt.show()

#connection = create_connection("sql7.freesqldatabase.com", "sql7589569", "NTLDAUBVuH","sql7589569")
#
#sqlCursor = connection.cursor()
#
#date = datetime.date(2023,1,10)
#hour = datetime.time(15,45,30)
##INSERT INTO molde1 (DATA, HORA, P1, T1) VALUES ('2023-01-10','15:45:10','11','15')
#query = "INSERT INTO molde1 (DATA, HORA, P1, T1) VALUES ('"+date.strftime('%Y-%m-%d')+"','"+hour.strftime('%H:%M:%S')+"','12'"+",'15')"
#print(query)
#sqlCursor.execute(query)
#
#connection.commit()
#
#sqlCursor.execute("SELECT * FROM molde1;")
#
#myresult = sqlCursor.fetchall()
#
#for x in myresult:
#  print(x)
#
#connection.close()

"""
# Welcome to 
# Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:pip install mysql-connector-python

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""


#with st.echo(code_location='below'):
#    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
#    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)
#
#    Point = namedtuple('Point', 'x y')
#    data = []
#
#    points_per_turn = total_points / num_turns
#
#    for curr_point_num in range(total_points):
#        curr_turn, i = divmod(curr_point_num, points_per_turn)
#        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
#        radius = curr_point_num / total_points
#        x = radius * math.cos(angle)
#        y = radius * math.sin(angle)
#        data.append(Point(x, y))
#
#    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
#        .mark_circle(color='#0068c9', opacity=0.5)
#        .encode(x='x:Q', y='y:Q'))
