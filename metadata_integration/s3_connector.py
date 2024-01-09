import os
import subprocess

import boto3
from datetime import datetime
from collections import defaultdict
import json


class NightMetaData:
    morning_clock_time: datetime = None
    actions: list = []
    id: str = None


organized_data = {}


def download_and_organize_jsons(bucket_name, prefix):
    s3 = boto3.client('s3')
    organized_data = defaultdict(NightMetaData)
    # List all objects in the specified S3 bucket and prefix
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    for obj in response.get('Contents', []):
        key = obj['Key']
        timestamp = get_creation_timestamp(key)

        # Download the JSON file from S3
        json_content = download_json_from_s3(s3, bucket_name, key)
        user_id = json_content['id']
        # Add the JSON content to the organized_data dictionary
        organized_data = add_data_to_dict(json_content, timestamp, user_id, organized_data)
    return organized_data


def add_data_to_dict(data, timestamp, user_id, organized_data):
    entrance_key = f'{str(timestamp)}-{user_id}'
    if entrance_key not in organized_data:
        night_metadata = NightMetaData()
        organized_data[entrance_key] = night_metadata
    organized_data[entrance_key].id = user_id
    if 'payload' in data and 'connection established' not in data['payload']:
        if 'alarm_time' in data['payload']:
            if data['payload']['enabled'] == True:
                organized_data[entrance_key].morning_clock_time = data['payload']['alarm_time']
        else:
            organized_data[entrance_key].actions.append(data)
    return organized_data


def get_creation_timestamp(key):
    timestamp_milliseconds = key.split('/')[-1].split('.')[0]
    try:
        timestamp_seconds = int(timestamp_milliseconds) / 1000.0  # Convert milliseconds to seconds
        timestamp = datetime.utcfromtimestamp(timestamp_seconds)
        return timestamp.date()
    except:
        return None


def download_json_from_s3(s3, bucket_name, key):
    # Download the JSON content from S3
    response = s3.get_object(Bucket=bucket_name, Key=key)
    json_content = response['Body'].read().decode('utf-8')

    # Parse the JSON content
    json_data = json.loads(json_content)

    return json_data


def run_s3_scrapper():
    s3_bucket_name = 'mn-iot-core-user-data'
    s3_prefix = 'noam/'
    AWS_ACCESS_KEY_ID = "AKIAVBE26ZWLVLQHSVM6"
    AWS_SECRET_ACCESS_KEY = "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"
    # use bash to export AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
    os.environ['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
    os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY

    # Organize JSONs by date
    organized_data = download_and_organize_jsons(s3_bucket_name, s3_prefix)
    return organized_data
    # Print the organized data


if __name__ == "__main__":
    organized_data = run_s3_scrapper()
    for date, json_list in organized_data.items():
        print(f"Date: {date}")
        for json_data in json_list:
            print(json_data)
