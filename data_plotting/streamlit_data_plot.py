import streamlit as st
import pandas as pd
import numpy as np
import db_connector
import plost


#
# def run_streamlit(db_connector):
#     st.title('Good morning Data plots')
#     # run from command line- streamlit run uber_pickups.py
#     data_load_state = st.text('Loading data...')
#     # Load 10,000 rows of data into the dataframe.
#     data = get_data_from_db(db_connector)
#     # Notify the reader that the data was successfully loaded.
#     data_load_state.text('Loading data...done!')
#     draw_histogram(data)
#

def draw_histogram(data):
    st.subheader('Raw data')
    st.subheader('Number of pickups by hour')
    st.dataframe(data)
    # hist_values = np.histogram(
    #     data['datetime']  , bins=24, range=(0, 24))[0]
    # st.bar_chart(hist_values)
    plost.line_chart(
        data,
        x='time',  # The name of the column to use for the x axis.
        y='bpm',  # The name of the column to use for the data itself.
        color='stock_name',  # The name of the column to use for the line colors.
    )


#
def plot_data_on_map(data):
    st.subheader('Map of all pickups')
    st.map(data)
    st.subheader('Map of all pickups')
    st.map(data)
    hour_to_filter = 17
    filtered_data = data[data['bpm'] == hour_to_filter]
    st.subheader(f'Map of all pickups at {hour_to_filter}:00')
    st.map(filtered_data)


#
def filter_resault_with_slider(data):
    hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h


#
#
def get_data_from_db(db_connector):
    cursor = db_connector.mydb.cursor()

    # execute a query to select the data from the table
    query = ("SELECT user_id, date, time, bpm FROM records "
             "WHERE time >= '05:00:00' AND time < '11:00:00' AND date >= '2023-05-01' AND date <= '2023-05-05'")

    cursor.execute(query)

    # fetch the results and store them in a Pandas DataFrame
    data = []
    for (user_id, date, time, bpm) in cursor:
        data.append({'user_id': user_id, 'date': str(date), 'time': str(time), 'bpm': bpm})

    df = pd.DataFrame(data)

    # close the cursor and the database connection
    cursor.close()
    return df


db = db_connector.DbConnector()
st.title('Good morning Data plots')
# run from command line- streamlit run uber_pickups.py
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = get_data_from_db(db)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')
draw_histogram(data)
