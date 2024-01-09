from datetime import datetime

import pandas
import pandas as pd

from User import User
from db.records_handler import RecordsDbConnector
from google_fit_tools.google_fit import GoogleFit
from google_fit_tools.google_fit_utils import get_data_and_save_in_db, get_bpm_from_google_fit
import matplotlib.pyplot as plt


class UiBack:
    users_list: list[User] = []
    user_id_list: list[str] = []
    google_fit = GoogleFit()

    def __init__(self):
        self.recordsDbConnector = RecordsDbConnector()
        with open("google_fit_tools/tokens.json", "r") as tokens:
            lines = tokens.readlines()
        for line in lines:
            if line.split(":")[0] in self.user_id_list:
                break
            self.add_user(line.split(":")[0])

    def add_user(self, name: str):
        self.users_list.append(User(name, self.google_fit))
        self.user_id_list.append(name)

    # get all registered users
    def get_users(self) -> list:
        return self.users_list

    def get_user_by_id(self, id: str):
        print(f"id:{id}")
        for u in self.users_list:
            print (u.userID)
            if u.userID is id:
                return u

    def get_all_users_data_from_google(self, from_time: datetime, to_time):
        data = []
        for user in self.users_list:
            data += get_data_and_save_in_db(user, from_time, to_time, self.recordsDbConnector)
            # data += get_bpm_from_google_fit(user, from_time, to_time)
        return data

    def get_user_data_from_google_and_save_in_db(self, user: User, from_time: datetime, to_time):
        return get_data_and_save_in_db(user, from_time, to_time, self.recordsDbConnector)

    def get_user_data_from_google(self, user: User, from_time: datetime, to_time):
        return get_bpm_from_google_fit(user, from_time, to_time)

    def get_records_data_from_db(self, selected_user, from_date: datetime, to_date: datetime, from_time: str, to_time: str):
        return self.recordsDbConnector.get_records_from_db(from_date, to_date, from_time, to_time, selected_user)

    def get_combined_data(self, selected_user, from_date: datetime, to_date: datetime, from_time: str, to_time: str):
        meta_data = self.__prepare_meta_data(self.get_meta_data())
        fitness_data = self.get_records_data_from_db(selected_user, from_date, to_date, from_time, to_time)
        self.plot_conmined(meta_data, fitness_data, from_date)
        return self.__combine_data(meta_data, fitness_data)

    def get_meta_data(self) -> pandas.DataFrame:
        return pd.read_excel('./assets/meta_data.xlsx')

    def __prepare_meta_data(self, meta_data):
        # combine fill time with new time
        meta_data['date'].fillna(pd.to_datetime(meta_data["fill_date"]).dt.date, inplace=True)
        # Replace 'שעון מעורר' with 'alarm_clock' in the 'wake_up_type' column
        meta_data['wake_up_type'] = meta_data['wake_up_type'].replace('שעון מעורר', 'alarm_clock', regex=False)
        # Replace 'יקיצה טבעית' with 'alarm_clock' in the 'natural_wakeup' column
        meta_data['wake_up_type'] = meta_data['wake_up_type'].replace('יקיצה טבעית', 'natural_wakeup', regex=False)
        return meta_data

    def __combine_data(self, meta_data, record_data) -> pandas.DataFrame:
        df_merged = pd.merge(meta_data, record_data, on='date', how='left')
        df_merged.loc[df_merged['time'] == df_merged['wakeup time'], 'line_type'] = 'blue'
        df_merged.loc[df_merged['time'].isin(df_merged.iloc[:, -11:-1].values.flatten()), 'line_type'] = 'red'

        # Separate data for wakeup time and alarm  clock time
        df_wake_up_time = df_merged[df_merged['line_type'] == 'blue']
        df_alarm_clock_time = df_merged[df_merged['line_type'] == 'red']

    def plot_conmined(self, df_metadata, df_records, plot_date):
        # df_records['time'] = pd.to_datetime(df_records['time']).dt.time
        # # df_metadata['wake_up_time'] = pd.to_datetime(df_metadata['wake_up_time']).dt.time
        # df_metadata['wake_up_time'] = pd.to_datetime(df_metadata['wake_up_time'].astype(str)).dt.time
        df_records['time'] = pd.to_datetime(df_records['time']).dt.hour * 3600 + pd.to_datetime(
            df_records['time']).dt.minute * 60 + pd.to_datetime(df_records['time']).dt.second

        # Convert the 'wakeup time' column in df_metadata to total seconds since midnight
        df_metadata['wake_up_time'] = pd.to_timedelta(df_metadata['wake_up_time'].astype(str)).dt.total_seconds()
        # Convert the 'clock_1' to 'clock_6' columns in df_metadata to total seconds since midnight
        for i in range(1, 6):
            df_metadata[f'clock_{i}'] = pd.to_timedelta(df_metadata[f'clock_{i}'].astype(str)).dt.total_seconds()

        # Step 1: Plot the data for each user_id in different colors
        unique_user_ids = df_records['user_id'].unique()

        plt.figure(figsize=(12, 8))

        # Plot data for each user_id in different colors
        for user_id in unique_user_ids:
            user_data = df_records[
                (df_records['user_id'] == user_id) & (df_records['date'] == plot_date.strftime('%Y-%m-%d'))]
            plt.plot(user_data['time'], user_data['bpm'], label=f'User {user_id}', marker='o')
            user_metadata = df_metadata[(df_metadata['date'] == plot_date) & (df_metadata['user_id'] == user_id)]

            # Step 2: Plot blue lines for wakeup time and add labels
            for _, row in user_metadata.iterrows():
                plt.axvline(x=row['wake_up_time'], color='blue', linestyle='--')
                plt.text(row['wake_up_time'], 200, row['wake_up_type'], rotation=90, color='blue', ha='right', va='bottom')

            # Step 3: Plot yellow lines for alarm_clocks 1 to 6
            for _, row in user_metadata.iterrows():
                for i in range(1, 6):
                    if pd.notnull(row[f'clock_{i}']):
                        plt.axvline(x=row[f'clock_{i}'], color='yellow', linestyle='--')

        plt.xlabel('Time')
        plt.ylabel('BPM')
        plt.title('BPM vs. Time with Wakeup and Alarm Clocks')
        plt.grid(True)
        plt.legend()
        plt.show()

