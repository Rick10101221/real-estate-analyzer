import json

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/drive"]


def fileUpload(fileName, filePath, driveService, config):
    file_metadata = {
      'name': 'MyFile.txt',  
      'parents': [config["folder_id"]]  # ID of the folder where you want to upload
    }
    media = MediaFileUpload(filePath, mimetype='text/plain')
    _ = driveService.files().create(body=file_metadata, media_body=media, fields='id').execute()

def main():
    with open('credentials.json') as json_file:
      credsDict = json.load(json_file)
      config = { 'folder_id': credsDict['folder_id'] }

    # retrieve driver service
    creds = service_account.Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    driveService = build('drive', 'v3', credentials=creds)

    # Upload file
    fileUpload("MyFile.txt", "test.txt", driveService, config)
    

if __name__ == "__main__":
  main()