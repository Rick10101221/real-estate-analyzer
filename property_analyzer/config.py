import gspread
import json

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/drive", 
    "https://www.googleapis.com/auth/spreadsheets"
]

def main():
    with open('credentials.json') as json_file:
        credsDict = json.load(json_file)
        config = {
            'familyHousingFolderId': credsDict['familyHousingFolderId'],
            'analyzerFolderId': credsDict['analyzerFolderId'],
            'analyzerSourceSheetId': credsDict['analyzerSourceSheetId'],
            'prospectivePropsSheetId': credsDict['prospectivePropsSheetId'],
            'crimeByCitySheetId': credsDict['crimeByCitySheetId'],
            }

    # authorize and instantiate google cloud services
    creds = service_account.Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    driveService = build('drive', 'v3', credentials=creds)
    sheetService = gspread.authorize(creds)

    return driveService, sheetService, config