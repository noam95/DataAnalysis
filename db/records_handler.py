from datetime import datetime

import pandas as pd

from User import User
from db.db_connector import DbConnector


class RecordsDbConnector(DbConnector):
    def __init__(self):
        super().__init__()
        my_cursor = self.mydb.cursor()
        # Define the SQL query to create the table if it does not exist
        measurs_table_query = "CREATE TABLE IF NOT EXISTS records (" \
                              "id INT AUTO_INCREMENT PRIMARY KEY," \
                              "user_id VARCHAR(255) NOT NULL, " \
                              "date DATE, " \
                              "time TIME, " \
                              "bpm INT)"
        my_cursor.execute(measurs_table_query)
        self.mydb.commit()
        my_cursor.close()

    def add_record(self, user_id, date, time, bpm):
        query = "INSERT INTO records (user_id, date, time, bpm) VALUES (%s, %s, %s, %s)"
        val = (user_id, date, time, bpm)
        my_cursor = self.mydb.cursor()
        my_cursor.execute(query, val)
        self.mydb.commit()
        my_cursor.close()

    def get_records_from_db(self, from_date: datetime, to_date: datetime, start_time: str, end_time: str, user: User = None):
        cursor = self.mydb.cursor()
        if user:
            # sql = "SELECT * FROM records"
            # pk_value = (user.userID)
            sql = "SELECT user_id, date, time, bpm FROM records " \
                  "WHERE time >= %s AND time < %s AND date >= %s AND date <= %s AND user_id=%s"
            pk_value = (start_time,
                        end_time,
                        from_date.strftime('%Y-%m-%d'),
                        to_date.strftime('%Y-%m-%d'),
                        user.userID)
        else:
            sql = "SELECT user_id, date, time, bpm FROM records " \
                  "WHERE time >= %s AND time < %s AND date >= %s AND date <= %s"
            pk_value = (start_time,
                        end_time,
                        from_date.strftime('%Y-%m-%d'),
                        to_date.strftime('%Y-%m-%d'))
        cursor.execute(sql, pk_value)
        # fetch the results and store them in a Pandas DataFrame
        data = []
        for (user_id, date, time, bpm) in cursor.fetchall():
            data.append({'user_id': user_id, 'date': str(date), 'time': str(time), 'bpm': bpm})
        df = pd.DataFrame(data)
        # close the cursor and the database connection
        cursor.close()
        return df

    def get_user_recordings(self, user_id=None, date=None):
        my_cursor = self.mydb.cursor()
        if date and user_id:
            sql = "SELECT * FROM records WHERE user_id = %s AND date = %s"
            pk_value = (user_id, date)
            my_cursor.execute(sql, pk_value)
        elif user_id:
            sql = "SELECT * FROM records WHERE user_id = %s"
            pk_value = (user_id,)
            my_cursor.execute(sql, pk_value)
        elif date:
            sql = "SELECT * FROM records WHERE date = %s"
            pk_value = (date,)
            my_cursor.execute(sql, pk_value)
        else:
            sql = "SELECT * FROM records_metadata"
            my_cursor.execute(sql)
        result = my_cursor.fetchall()
        print(result)
        my_cursor.close()
        return result
