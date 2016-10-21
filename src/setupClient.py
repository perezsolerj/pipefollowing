#!/usr/bin/env python

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import spreadSheets

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

class SpreadSheetManager:

  def __init__(self,spreadSheet):

    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/uwsimBenchmarksUploader.json
    self.scopes = ['https://www.googleapis.com/auth/spreadsheets','email']
    self.clientSecretFile = 'client_secret.json'
    self.appName = 'UWSim Benchmarks results uploader'

    self.credentials=self.get_credentials()

    # Store the email as ID
    self.email=self.credentials.id_token['email']
    # Start the service
    http = self.credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?''version=v4')
    self.service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

    ##Other things:
    self.spreadsheetId = spreadSheet

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
    credential_path = os.path.join(credential_dir, 'uwsimBenchmarksUploader.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(self.clientSecretFile, self.scopes)
        flow.user_agent = self.appName
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


  def getEmail(self):
    return self.email

if __name__ == '__main__':

    SSnames=spreadSheets.spreadSheetsNames()
    SSname=SSnames.teleopBasic

    SSmanager=SpreadSheetManager(SSname)

    userEmail = SSmanager.getEmail()
    
    print (userEmail, "set up.")


