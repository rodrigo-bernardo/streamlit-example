import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

try:
    # Connect to database
    cnx = mysql.connector.connect(
        host = "sql7.freesqldatabase.com",
        user = "sql7589569",
        password = "NTLDAUBVuH",
        database = "sql7589569"
    )
    # Create a function to plot the data
    def plot_data():
        try:
            # Get data from the database
            df = pd.read_sql("SELECT * FROM molde1", cnx)
            # Plot the data
            plt.clf() # clear the previous plot
            plt.plot(df['x'], df['y'])
            plt.xlabel('X')
            plt.ylabel('Y')
            st.pyplot()
        except mysql.connector.Error as error:
            st.error(f"Error: {error}")
    # Create a Streamlit app
    st.title('Real-time Data Plot')
    st.markdown("Data will auto-refresh every 5 seconds.")
    # Add auto-refresh
    while True:
        plot_data()
        st.sleep(5)
finally:
    if cnx.is_connected():
        cnx.close()
        st.success("Connection closed.")
