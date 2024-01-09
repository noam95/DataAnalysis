from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json
import google.auth.transport.requests


class GoogleFit:
    def __init__(self):
        self.scopes = ["https://www.googleapis.com/auth/fitness.activity.read",
                       "https://www.googleapis.com/auth/fitness.heart_rate.read",
                       "https://www.googleapis.com/auth/fitness.sleep.read",
                       "https://www.googleapis.com/auth/fitness.activity.write",
                       "https://www.googleapis.com/auth/fitness.sleep.write"]


    def initial_token(self, user_id, creds=None) -> Credentials:
        """
        write token to json file based on credentials
        """
        if creds and creds.expired and creds.refresh_token:
            request = google.auth.transport.requests.Request()
            creds.refresh(request)
        else:
            flow = InstalledAppFlow.from_client_secrets_file("google_fit_tools/credentials.json", self.scopes)
            creds = flow.run_local_server(port=3000)
            #TODO: Enable it and fix the missing field 'refresh token"
            # with open("google_fit_tools/tokens.json", "a") as token:
            #     token.write(f'{user_id}: {creds.to_json()}\n')
        return creds

    def create_credentials(self, token):
        token_as_dict = json.loads(token)
        return Credentials.from_authorized_user_info(token_as_dict, self.scopes)

    def build_user_fit(self, fit_creds):
        return build('fitness', 'v1', credentials=fit_creds)
