import os
from datetime import datetime, timedelta

import pandas as pd
from google_fit_tools.google_fit_utils import save_data_as_file
from ui_back import UiBack

user_ids = ["hallelh@gmail.com", "noam95@gmail.com"]

for user_id in user_ids:
    backend_instance = UiBack()
    backend_instance.add_user(user_id)
    # define parametrs which will be defined by user
    datetime_str = '2023-07-11 00:00:00'
    from_date = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    to_date = from_date + timedelta(days=30)  # 11/07/2023 - 07/08/2023
    start_time = "04:00:00"
    end_time = "12:00:00"

    current_date = from_date
    folder_name = user_id.replace("@", "_").replace(".", "_")
    os.makedirs(folder_name, exist_ok=True)

    while current_date <= to_date:
        # Construct datetime objects for start and end times
        start_datetime = datetime.combine(current_date.date(), datetime.strptime(start_time, "%H:%M:%S").time())
        end_datetime = datetime.combine(current_date.date(), datetime.strptime(end_time, "%H:%M:%S").time())

        # Fetch user data for the current day within the specified time range
        user_data = backend_instance.get_user_data_from_google(backend_instance.get_user_by_id(user_id), start_datetime,
                                                               end_datetime)
        filename = f'{current_date.strftime("%Y-%m-%d")}.xlsx'
        filepath = os.path.join(folder_name, filename)
        save_data_as_file(pd.DataFrame(user_data),current_date, filepath)

        # Move to the next day
        current_date += timedelta(days=1)
