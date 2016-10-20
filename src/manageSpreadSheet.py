from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

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

  def createNewSheet(self,name):
    requests = []
    requests.append({
        'addSheet': {
            'properties': {
                'title': name
            },
        }
    })

    body = {
        'requests': requests
    }

    result = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId,body=body).execute()
    
    return result['replies'][0]['addSheet']['properties']['sheetId']

  def clearSheet(self,sheetId):
    requests = []
    requests.append({
        "updateCells": {
          "range": {
            "sheetId": sheetId
          },
          "fields": "userEnteredValue"
        }
    })
    body = {
        'requests': requests
    }

    result = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId,body=body).execute()   

  def getSheetId(self,name):
    result = self.service.spreadsheets().get(spreadsheetId=self.spreadsheetId).execute()

    sheetId=-1
    for i in result['sheets']:
      title = i['properties']['title']
      if title==name:
        sheetId=i['properties']['sheetId']

    return sheetId

  def writeValues(self,values,sheet,line):
    body = {
      'values': values
    }

    range_name=sheet + '!A' + str(line)
    value_input_option='USER_ENTERED'
    result = self.service.spreadsheets().values().update(spreadsheetId=self.spreadsheetId, range=range_name,
      		valueInputOption=value_input_option, body=body).execute()

  def appendValues(self,values,sheet):
    body = {
      'values': values
    }

    range_name=sheet + '!A1'
    value_input_option='USER_ENTERED'

    result = self.service.spreadsheets().values().append(spreadsheetId=self.spreadsheetId,  range=range_name,
    valueInputOption=value_input_option, body=body).execute()


  def getEmail(self):
    return self.email

  def readSheet(self,sheet):
    range_names = sheet
    result = self.service.spreadsheets().values().batchGet(spreadsheetId=self.spreadsheetId, ranges=range_names).execute()

    return result['valueRanges'][0]['values']


  def protectSheet(self,name,sheetId):
    editors={
      "users": [
        name
      ],
      "domainUsersCanEdit": False,
    }
    protectedRange ={
      #"protectedRangeId": number,
      "range": {
        "sheetId": sheetId,
      },
      ##"namedRangeId": string,
      "description": name+ " Sheet",
      "warningOnly": False,
      "requestingUserCanEdit": True,
      "editors": editors
    }

    requests = []
    requests.append({
        "addProtectedRange": {
          "protectedRange": protectedRange
        }
    })

    body = {
        'requests': requests
    }

    result = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId,body=body).execute()
    print(result)
    
    return 


