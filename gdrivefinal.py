# import the required libraries
from __future__ import print_function
import pickle
import os.path
import io
import shutil
import requests
from mimetypes import MimeTypes
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import logging

''' run below commands first '''
'''pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib'''

logging.basicConfig(filename ='drivelog.log',format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

maindir = '.'
if 'drivefiles' not in os.listdir(maindir):
    os.mkdir('drivefiles')

def FileDownload(file_id, file_name , creds):
        service = build('drive', 'v3', credentials= creds)
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()

        # Initialise a downloader object to download the file
        downloader = MediaIoBaseDownload(fh, request, chunksize=204800)
        done = False

        try:
            # Download the data in chunks
            while not done:
                status, done = downloader.next_chunk()

            fh.seek(0)
            filePath = os.path.join(maindir, 'drivefiles', file_name)

            # Write the received data to the file
            with open(filePath, 'wb') as f:
                shutil.copyfileobj(fh, f)

            print("File Downloaded")
            # Return True if file Downloaded successfully
            return True
        except:

            # Return False if something went wrong
            print("Something went wrong.")
            return False


class DriveAPI:
    global SCOPES
    global items

    # Define the scopes
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def __init__(self):

        # Variable self.creds will
        # store the user access token.
        # If no valid token found
        # we will create one.
        self.creds = None

        # The file token.pickle stores the
        # user's access and refresh tokens. It is
        # created automatically when the authorization
        # flow completes for the first time.

        # Check if file token.pickle exists
        if os.path.exists('token.pickle'):

            # Read the token from the file and
            # store it in the variable self.creds
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        # If no valid credentials are available,
        # request the user to log in.
        if not self.creds or not self.creds.valid:

            # If token is expired, it will be refreshed,
            # else, we will request a new one.
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)

            # Save the access token in token.pickle
            # file for future usage
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        # Connect to the API service
        self.service = build('drive', 'v3', credentials=self.creds)

        # request a list of first N files or
        # folders with name and id from the API.
        results = self.service.files().list(
            pageSize=100, fields="files(id, name, size)").execute()
        items = results.get('files', [])

        # print a list of files

        #print("Here's a list of files: \n")
        #print(*items, sep="\n", end="\n\n")
        logging.info(items)

        for i in items:
            #print(i)
            if 'size' in i.keys():
                FileDownload(i["id"], i["name"], self.creds)
                logging.info(i["id"] + ' ' + i["name"]) 
            else:
                print("folder" + i["name"])
 


if __name__ == "__main__":
    obj = DriveAPI() 
    print('process completed')
