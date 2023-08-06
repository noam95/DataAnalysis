
class User:

    def __init__(self, name, google_fit_instance):
        self.name = name
        self.userID = name
        self.fit_creds = None
        self.fit_instance = self.__init_fit_instance(google_fit_instance)

    def __repr__(self):
        return f"User(name='{self.name}')"

    def __init_fit_instance(self, google_fit_instance):
        with open("google_fit_tools/tokens.json", "r") as tokens:
            for line in tokens:
                if self.userID in line:
                    self.fit_creds = google_fit_instance.create_credentials(line.strip(f'{self.userID}:'))
                    break
        if not self.fit_creds or not self.fit_creds.valid:
            self.fit_creds = google_fit_instance.initial_token(creds=self.fit_creds, user_id=self.userID)
        return google_fit_instance.build_user_fit(self.fit_creds)
