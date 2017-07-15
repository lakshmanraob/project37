from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import datetime


class SpreadSheet:
    def __init__(self):
        try:
            import argparse

            self.flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            flags = None

        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/sheets.googleapis.com-python-quickstart.json
        self.SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
        self.CLIENT_SECRET_FILE = 'credentials/client_secret.json'
        self.APPLICATION_NAME = 'Google Sheets API Python Quickstart'

        """Shows basic usage of the Sheets API.

            Creates a Sheets API service object and prints the names and majors of
            students in a sample spreadsheet:
            https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
            """
        self.credentials = self.get_credentials()
        self.http = self.credentials.authorize(httplib2.Http())
        self.discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                             'version=v4')
        self.service = discovery.build('sheets', 'v4', http=self.http,
                                       discoveryServiceUrl=self.discoveryUrl)

        # spreadsheetId = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
        self.spreadsheetId = '1M-yIErYwdln-X9VWGKOrykz_B1oBR3b9nHIuD9xyeOs'
        # rangeName = 'Class Data!A2:E'
        # result = service.spreadsheets().values().get(
        #     spreadsheetId=spreadsheetId, range=rangeName).execute()

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'sheets.googleapis.com-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if self.flags:
                credentials = tools.run_flow(flow, store, self.flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def insert(self, values):
        
        body = {'values': values}
        rg = 'A1'

        self.service.spreadsheets().values().append(spreadsheetId=self.spreadsheetId, range=rg, body=body,
                                                    valueInputOption='RAW').execute()
        # values = result.get('values', [])

    print("update done")

    # if not values:
    #     print('No data found.')
    # else:
    #     print('Name, HomeState, Major:')
    #     for row in values:
    #         # Print columns A and E, which correspond to indices 0 and 4.
    #         print('%s, %s, %s' % (row[0], row[3], row[4]))


def create_values():
    emotionlist = ['happy', 'anger', 'disgust']

    values = []
    for j in range(0, 10):
        for index in range(0, 100):
            emotionIndex = ((j * 10) + index) % len(emotionlist)
            emotion = ['face {0}'.format((j * 10) + index), '{0}'.format(emotionlist[emotionIndex]),
                       'time {0}'.format(datetime.datetime.now())]
            values.append(emotion)

            # values = [
            #     ['face', 'emotion', 'timestamp'],
            #     ['face', 'emotion', 'timestamp']
            # ]
    return values


if __name__ == '__main__':
    speread_sheet = SpreadSheet()
    spread_sheet_id = '1M-yIErYwdln-X9VWGKOrykz_B1oBR3b9nHIuD9xyeOs'
    speread_sheet.insert(values=create_values())
    # main()
