import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from matplotlib.ticker import MaxNLocator
from matplotlib.dates import AutoDateLocator

def smoothins(db_connector):
    # create a connection to the database
    # create a cursor object
    cursor = db_connector.mydb.cursor()

    # execute a query to select the data from the table
    query = ("SELECT user_id, date, time, bpm FROM records "
             "WHERE time >= '05:00:00' AND time < '14:00:00' AND date >= '2023-04-20' AND date <= '2023-04-20'")

    cursor.execute(query)

    # fetch the results and store them in a Pandas DataFrame
    data = []
    for (user_id, date, time, bpm) in cursor:
        data.append({'user_id': user_id, 'datetime': str(date) +' '+ str(time), 'bpm': bpm})

    df = pd.DataFrame(data)

    # close the cursor and the database connection
    cursor.close()
    df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d %H:%M:%S')
    df = df.drop(['user_id'], axis=1)
    df = df.set_index('datetime')


    # Use a 5-minute rolling mean to smooth the BPM data
    df['bpm_smooth'] = df['bpm'].rolling('10min').mean()

    # Create a line plot of the smoothed BPM data
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df['bpm_smooth'])

    # Set the x-axis label and format the x-axis tick labels
    ax.set_xlabel('Date')
    ax.tick_params(axis='x', rotation=45, labelsize=10)

    # Set the y-axis label and format the y-axis tick labels
    ax.set_ylabel('BPM')
    ax.tick_params(axis='y', labelsize=10)

    # Set the plot title
    ax.set_title('BPM Over Time', fontsize=10)

    # Show the plot
    plt.show()

