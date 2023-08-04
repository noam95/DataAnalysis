from datetime import datetime, timedelta

import mysql.connector

# run docker image command
# docker run -d -p 3306:3306 --name mysql-docker-container -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=testDB -e MYSQL_USER=admin -e MYSQL_PASSWORD=password mysql
class RecordMetadata:
    def __init__(self, user_id=None, DATE=None, alarm_clock_time=None, type_of_awake=None, point_of_awakening=None,
                 fall_asleep_time=None):
        self.user_id = user_id
        self.DATE = DATE
        self.alarm_clock_time = alarm_clock_time
        self.type_of_awake = type_of_awake
        self.point_of_awakening = point_of_awakening
        self.fall_asleep_time = fall_asleep_time


class DbConnector:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="password",
            database="testDB"
        )
        self.__init_tables()

    def __init_tables(self):
        mycursor = self.mydb.cursor()
        # Define the SQL query to create the table if it does not exist
        meta_data_table_query = '''CREATE TABLE IF NOT EXISTS records_metadata (
                                      id INT AUTO_INCREMENT PRIMARY KEY,
                                      user_id VARCHAR(255) NOT NULL,
                                      date DATE NOT NULL,
                                      alarm_clock_time TIME,
                                      type_of_awake VARCHAR(255),
                                      point_of_awakening VARCHAR(255),
                                      fall_asleep_time TIME
                                    );'''
        measurs_table_query = "CREATE TABLE IF NOT EXISTS records (" \
                              "id INT AUTO_INCREMENT PRIMARY KEY," \
                              "user_id VARCHAR(255) NOT NULL, " \
                              "date DATE, " \
                              "time TIME, " \
                              "bpm INT)"
        # Execute the SQL query using the cursor's execute() method
        mycursor.execute(meta_data_table_query)
        mycursor.execute(measurs_table_query)
        # Commit the changes to the database
        self.mydb.commit()
        # Close the cursor and the database connection
        mycursor.close()

    def add_night_recording(self, user_id, date, time, bpm):
        query = "INSERT INTO records (user_id, date, time, bpm) VALUES (%s, %s, %s, %s)"
        val = (user_id,
               date,
               time,
               bpm)
        mycursor = self.mydb.cursor()
        mycursor.execute(query, val)
        self.mydb.commit()
        mycursor.close()

    def add_day_meta_data(self, metadata: RecordMetadata):
        query = "INSERT INTO records_metadata (" \
                "user_id," \
                "date, " \
                "alarm_clock_time, " \
                "type_of_awake, " \
                "point_of_awakening, " \
                "fall_asleep_time) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (metadata.user_id,
               metadata.DATE,
               metadata.alarm_clock_time,
               metadata.type_of_awake,
               metadata.point_of_awakening,
               metadata.fall_asleep_time)
        mycursor = self.mydb.cursor()
        mycursor.execute(query, val)
        self.mydb.commit()
        mycursor.close()

    def get_user_recordings(self,user_id=None, date=None):
        mycursor = self.mydb.cursor()
        if date and user_id:
            sql = "SELECT * FROM records WHERE user_id = %s AND date = %s"
            pk_value = (user_id, date)
            mycursor.execute(sql, pk_value)
        elif user_id:
            sql = "SELECT * FROM records WHERE user_id = %s"
            pk_value = (user_id, )
            mycursor.execute(sql, pk_value)
        elif date:
            sql = "SELECT * FROM records WHERE date = %s"
            pk_value = (date,)
            mycursor.execute(sql, pk_value)
        else:
            sql = "SELECT * FROM records_metadata"
            mycursor.execute(sql)
        result = mycursor.fetchall()
        print(result)
        mycursor.close()
        return result


    def get_meta_data(self, user_id = None):
        mycursor = self.mydb.cursor()
        if user_id:
            sql = "SELECT * FROM records_metadata WHERE user_id = %s"
            pk_value = (user_id, )
            mycursor.execute(sql, pk_value)
        else:
            sql = "SELECT * FROM records_metadata"
            mycursor.execute(sql)
        result = mycursor.fetchall()
        print(result)
        mycursor.close()


# connector = DbConnector()
# metadata = RecordMetadata(
#     'noam',
#     datetime.now(),
#     datetime.now() + timedelta(hours=1),
#     'regular_alarm',
#     datetime.now() + timedelta(hours=8),
#     fall_asleep_time=datetime.now())
# connector.add_day_meta_data(metadata)
# connector.get_meta_data()
# connector.add_night_recording('noam', datetime.now(), datetime.now(), bpm=85)
# connector.get_meta_data()
# connector.mydb.close()
