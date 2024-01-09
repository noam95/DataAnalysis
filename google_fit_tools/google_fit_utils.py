import random
import time
from datetime import datetime
import xlsxwriter
import requests
from db.db_connector import DbConnector
from db.records_handler import RecordsDbConnector
from system_constants import DATA_SOURCE_BPM
from User import User


def get_bpm_from_google_fit(user, from_time: datetime, to_time):
    fit_instance = user.fit_instance
    start = int(time.mktime(from_time.timetuple()) * 1000000000)
    end = int(time.mktime(to_time.timetuple()) * 1000000000)
    data_set = "%s-%s" % (start, end)
    return fit_instance.users().dataSources().datasets().get(userId='me',
                                                             dataSourceId=DATA_SOURCE_BPM,
                                                             datasetId=data_set).execute()


def save_data_as_file(data, start_time, filepath):
    workbook_name = datetime.strftime(start_time, '%d.%m.%y %H:%M:%S').split(" ")[0]
    workbook = xlsxwriter.Workbook(filepath)
    worksheet = workbook.add_worksheet()

    # Start from the first cell.
    # Rows and columns are zero indexed.
    worksheet.write(0, 0, 'date')
    worksheet.write(0, 1, 'time')
    worksheet.write(0, 2, 'fpval')
    row_ind = 1
    column_ind = 0
    for row in data['point']:
        last = row['endTimeNanos']
        seconds = int(last) / 1000000000
        measure_date, measure_time = datetime.fromtimestamp(seconds).strftime("%m/%d/%y %H:%M:%S").split(" ")
        fpval = row['value'][0]['fpVal']
        worksheet.write(row_ind, column_ind, str(measure_date))
        worksheet.write(row_ind, column_ind + 1, str(measure_time))
        worksheet.write(row_ind, column_ind + 2, fpval)
        row_ind += 1
    workbook.close()


def save_data_to_db(user: User, data, db_connector: RecordsDbConnector):
    for row in data['point']:
        last = row['endTimeNanos']
        seconds = int(last) / 1000000000
        measure_date_time = datetime.fromtimestamp(seconds)
        fpval = row['value'][0]['fpVal']

        db_connector.add_record(user.userID, measure_date_time, measure_date_time, fpval)


def get_data_and_save_in_db(user: User, from_time: datetime, to_time, db_connector: RecordsDbConnector):
    data = get_bpm_from_google_fit(user, from_time, to_time)
    save_data_to_db(user, data, db_connector)
    return data


def set_session(start_time, end_time, creds, activity_type=0, session_id=random.randint(0, 100)):
    """
    create a new session
    :param creds: user creds
    :param start_time: define the start time of the session as datetime type
    :param end_time: define the end time of the session as datetime type
    :param activity_type: type of sport, In vehicle by default  # dont need?
    :param session_id: specific or random by default
    print if success else print the error message
    """
    start_time_in_mills = int(time.mktime(start_time.timetuple()) * 1000)
    end_time_in_mills = int(time.mktime(end_time.timetuple()) * 1000)
    # start_time_in_mills = start_time
    # end_time_in_mills = end_time
    token = creds.token
    session = {
        "activityType": activity_type,
        "application": {
            "name": ""
        },
        "endTimeMillis": end_time_in_mills,
        "id": str(session_id),
        "name": "",
        "startTimeMillis": start_time_in_mills
    }
    headers = {
        "Authorization": "Bearer {}".format(token),
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    url_session_update = "https://fitness.googleapis.com/fitness/v1/users/me/sessions/{}".format(session_id)
    session_create = requests.put(url_session_update, headers=headers, json=session)
    if session_create.status_code != 200:
        print("ERROR: status code {}, message: {}".format(session_create.status_code, session_create.text))
    else:
        print("request success with status code 200")
