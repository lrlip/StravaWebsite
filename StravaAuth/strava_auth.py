import os
from dotenv import load_dotenv
import requests
import json
import time

load_dotenv()

BASENAME = os.path.dirname(__file__)
class StravaAuth:

    def __init__(self):

        self.strava_token_json = os.path.join(BASENAME, 'strava_tokens.json')
        self.__strava_client_id = os.getenv('STRAVA_CLIENT_ID')
        self.__strava_client_secret = os.getenv('STRAVA_CLIENT_SECRET')



    def get_first_acces_code_DONT_RUN_WHEN_NOT_NEEDED(self):
        """
        Used to get the access_code the first time a connection with strava is made.
        Returns:

        """
        response = requests.post(
            url='https://www.strava.com/oauth/token',
            data={
                'client_id': self.__strava_client_id,
                'client_secret': self.__strava_client_secret,
                'code': '95bebd8409a53d080f0f4dff325324171475b88f',
                'grant_type': 'authorization_code'
            })
        # Save json response as a variable
        strava_tokens = response.json()
        print(strava_tokens)
        # Save tokens to file
        with open('strava_tokens.json', 'w') as outfile:
            json.dump(strava_tokens, outfile)
        # Open JSON file and print the file contents
        # to check it's worked properly
        with open('strava_tokens.json') as check:
            data = json.load(check)
            print(data)

    def _read_strava_tokens_json(self):
        """
        Read the strava tokens from json
        Returns:

        """
        with open(self.strava_token_json) as json_file:
            self._strava_tokens = json.load(json_file)

    def _write_strava_tokens_json(self):
        """
        Write strava tokens a json file """
        with open(self.strava_token_json, 'w') as outfile:
            json.dump(self._strava_tokens, outfile)

    def _update_strava_tokens(self):
        """
        Updates strava tokens using the client_id, client_secret and the refreshtoken
        stores the tokens in _strava_tokens and writes them to a file.
        Returns:

        """
        response = requests.post(
            url='https://www.strava.com/oauth/token',
            data={
                'client_id': self.__strava_client_id,
                'client_secret': self.__strava_client_secret,
                'grant_type': 'refresh_token',
                'refresh_token':
                    self._strava_tokens['refresh_token']
            }
        )
        self._strava_tokens = response.json()
        self._write_strava_tokens_json()

    def get_strava_tokens(self):
        """
        Retrieves the strava tokens:
        Read strava tokens from json, if they are expired, updates the strava tokens
        Returns:

        """
        self._read_strava_tokens_json()
        if self._strava_tokens['expires_at'] < time.time():
            self._update_strava_tokens()

    def strava_tokens(self):
        """
        function to retrieve the strava tokens
        First checks the expiration using get_strava_tokens()
        Returns:

        """
        self.get_strava_tokens()
        return self._strava_tokens


if __name__ == "__main__":
    StravaAuth().get_first_acces_code_DONT_RUN_WHEN_NOT_NEEDED()
    strava_tokens = StravaAuth().strava_tokens()
    print(strava_tokens)

()