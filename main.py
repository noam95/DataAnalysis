import os
import subprocess
from datetime import datetime, timedelta

from data_plotting.streamlit_data_plot import draw_histogram, plotly_histogram
import streamlit as st
from ui_back import UiBack


def initial_values(backend_instance):
    user_id = "noam95@gmail.com"
    backend_instance.add_user(user_id)
    #define parametrs which will be defined by user
    datetime_str = '2024-01-01 00:00:00' # 11/07/2023 - 07/08/2023
    from_date = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    from_date.timestamp() * 1000
    to_date = from_date + timedelta(days=120)
    start_time = "01:00:00"
    end_time = "19:00:00"
    backend_instance.get_all_users_data_from_google(from_date, to_date)
    backend_instance.get_records_data_from_db(backend_instance.get_user_by_id(user_id), from_date, to_date, start_time,
                                              end_time)
    # backend_instance.get_combined_data(backend_instance.get_user_by_id(user_id), from_date, to_date, start_time, end_time)

def init_system():
    #init main istances
    backend_instance = UiBack()
    st.title('Good morning Data plots')

    # Section to add a new user
    st.header("Add a New User")
    new_user_name = st.text_input("Enter the name of the new user:")
    if st.button("Add User"):
        if new_user_name:
            backend_instance.add_user(new_user_name)
            st.success(f"User '{new_user_name}' added successfully!")

    # Let the user choose a user from the list
    selected_user = st.selectbox("Choose a user:", backend_instance.get_users())

    # Section to choose start time and number of days
    st.header("Choose Start Time and Number of Days")
    datetime_str = st.text_input("Enter the start time in format 'YYYY-MM-DD HH:MM:SS':", "2023-07-22 00:00:00")
    num_days = st.number_input("Enter the number of days:", min_value=1, max_value=365, value=1)
    start_time = st.text_input("Enter the hour in the morning to start plot from. format:HH:MM:SS ", "05:00:00")
    end_time = st.text_input("Enter the hour in the morning to end plot in. format:HH:MM:SS ", "09:00:00")
    # Google API phase
    if st.button("Get Data From User API"):
        if datetime_str and selected_user and num_days:
            from_date = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
            to_date = from_date + timedelta(days=num_days)
            backend_instance.get_user_data_from_google_and_save_in_db(selected_user, from_date, to_date)

    # Plot from SQL DB
    if st.button("Plot records_data from SQL DB"):
        data_load_state = st.text('Loading records_data...')
        if datetime_str and selected_user and num_days and start_time and end_time:
            from_date = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
            to_date = from_date + timedelta(days=num_days)
            records_data = backend_instance.get_records_data_from_db(selected_user, from_date, to_date, start_time,
                                                                     end_time)

            data_load_state.text('Loading records_data...done!')
            # draw_histogram(records_data)
            plotly_histogram(records_data)
    initial_values(backend_instance)
if __name__ == '__main__':
    init_system()


