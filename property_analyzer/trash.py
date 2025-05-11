from googleapiclient.http import MediaFileUpload

def findObjInFilesObj(filesObj, queries):
    if len(queries) == 0: return None

    for file in filesObj['files']:
        found = True
        for prop, op, val in queries:
            if op == "equals":
                check = lambda file: file[prop] == val
            elif op == "contains":
                check = lambda file: val in file[prop]
            if not check(file):
                found = False
                break
        if found:
            return file


def fileUpload(fileName, filePath, driveService, config):
    file_metadata = {
        'name': fileName,  
        'parents': [config["familyHousingFolderId"]]
    }
    media = MediaFileUpload(filePath, mimetype='text/plain')
    _ = driveService.files().create(body=file_metadata, media_body=media, fields='id').execute()


def sources():
    pass

    #https://medium.com/the-team-of-future-learning/integrating-google-drive-api-with-python-a-step-by-step-guide-7811fcd16c44


def main():
    pass

    # Upload file
    #fileUpload("MyFile.txt", "test.txt", driveService, config)

    # find analyzer template and parent folder using driveService
    # filesObj = driveService.files().list().execute()
    # analyzerObj = findObjInFilesObj(filesObj, [("name", "equals", "~Property Template and Analyzer")])
    # analyzerParent = findObjInFilesObj(filesObj, [("name", "equals", "Property Analyzing"), ("mimeType", "equals", "application/vnd.google-apps.folder")])
    # if analyzerObj is None or analyzerParent is None:
    #     print("Analyzer or Parent not found")
    #     return

    # atAGlanceFacts = propertyDict['atAGlanceFacts']
    # atAGlanceFactsDict = {factDict['factLabel']: factDict['factValue'] for factDict in atAGlanceFacts}