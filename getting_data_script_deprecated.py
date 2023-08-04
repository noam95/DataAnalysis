# from datetime import datetime, timedelta
#
# import db
#
#
# # initialize db instance
# db_connector = db.DbConnector()
#
# # init google fit instance
# google_fit_instance = GoogleFit()
#
# # init users
# user1 = User(28, "noam", google_fit_instance)
# # user2 = User(30, "Hallel", google_fit_instance)
#
# # script
# datetime_str = '2023-05-01 00:00:00'
# start_time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
# start_time.timestamp() * 1000
# end_time = start_time + timedelta(days=5)
# bpm_data = google_fit_utils.get_bpm_from_google_fit(user1, start_time, end_time)
# google_fit_utils.save_data_to_db(user1, bpm_data, db_connector)


# smoothins(db_connector)
# Retrieve the data using SQL query
# df = pd.read_sql("SELECT * FROM records", con=db_connector.mydb)
# data = db_connector.get_user_recordings('noam')
# Plot the data using matplotlib
# df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
# df = df.set_index('time')
# df = df.resample('1H').mean()
# df = df.interpolate()
# df['is_night'] = ((df.index.hour >= 20) | (df.index.hour <= 6)).astype(int)
# sns.lineplot(data=df, x=df.index, y='bpm', hue='is_night', palette=['blue', 'orange'])
# plt.xlabel('Date')
# plt.ylabel('BPM')
# plt.title('Night/Wake-up Process')
# plt.show()
#
# df.plot(kind='line', x='time', y='bpm')
# plt.show()