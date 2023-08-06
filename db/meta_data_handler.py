from db.db_connector import DbConnector


class RecordMetadata:
    def __init__(self, user_id=None, DATE=None, alarm_clock_time=None, type_of_awake=None, point_of_awakening=None,
                 fall_asleep_time=None):
        self.user_id = user_id
        self.DATE = DATE
        self.alarm_clock_time = alarm_clock_time
        self.type_of_awake = type_of_awake
        self.point_of_awakening = point_of_awakening
        self.fall_asleep_time = fall_asleep_time


class MetaDataDbConnector(DbConnector):
    def __init__(self):
        super().__init__()
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
        mycursor.execute(meta_data_table_query)
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

    def get_meta_data(self, user_id=None):
        mycursor = self.mydb.cursor()
        if user_id:
            sql = "SELECT * FROM records_metadata WHERE user_id = %s"
            pk_value = (user_id,)
            mycursor.execute(sql, pk_value)
        else:
            sql = "SELECT * FROM records_metadata"
            mycursor.execute(sql)
        result = mycursor.fetchall()
        print(result)
        mycursor.close()
