from gspread.utils import ValueRenderOption


def main():
    pass


def writeToAnalyzerSheet(driveService, sheetService, configDict, propertyDict):
    #create duplicate of analyzer file in analyzer parent folder
    fileMetadata = {
        'name': f'Analyzer - {propertyDict['fullAddress']}',
        'parents': [configDict["analyzerFolderId"]],
    }
    sheetResponse = driveService.files().copy(body=fileMetadata, fileId=configDict["analyzerSourceSheetId"]).execute()

    #get analyzer worksheet reference
    newAnalyzerSheetId = sheetResponse['id']
    newAnalyzerSheet = sheetService.open_by_key(newAnalyzerSheetId)
    analyzerWorksheet = newAnalyzerSheet.get_worksheet(0)

    #write core property information
    coreInfo = []
    for key in ['streetAddress', 'location', 'homeType', 'livingArea', 'yearBuilt']:
        coreInfo.append([propertyDict.get(key, ''), '', ''])
    analyzerWorksheet.update(coreInfo, f'E10:G{10 + len(coreInfo) - 1}')

    #write rates and percentages
    analyzerWorksheet.update([[propertyDict['price'], '']], 'F30:G30')

    #write unit breakdown
    analyzerWorksheet.update([[1, propertyDict['resoFacts']['bedrooms'], propertyDict['resoFacts']['bathrooms']]], 'S10:U10')

    return newAnalyzerSheetId


def getDataFromAnalyzerSheet(sheetService, newAnalyzerSheetId):
    analyzerSheetData = {}
    #get analyzer worksheet reference
    newAnalyzerSheet = sheetService.open_by_key(newAnalyzerSheetId)
    analyzerWorksheet = newAnalyzerSheet.get_worksheet(0)

    #get monthly amount
    analyzerSheetData['monthlyAmt'] = round(analyzerWorksheet.get("T94:U94", value_render_option=ValueRenderOption.unformatted)[0][0], 2)

    return analyzerSheetData


def writeDataToProspectivePropsSheet(sheetService, configDict, propertyDict, analyzerSheetData, newAnalyzerSheetId):
    #get prospective properties worksheet reference
    prospectivePropsSheet = sheetService.open_by_key(configDict["prospectivePropsSheetId"])
    prospectivePropsWorksheet = prospectivePropsSheet.get_worksheet(0)
    newRowIdx = len(prospectivePropsWorksheet.col_values(2)) + 1

    #write location with listing link
    locationLink = f'=HYPERLINK("{propertyDict["url"]}","{propertyDict["fullAddress"]}")'
    prospectivePropsSheet.values_update(
        f'Sheet1!B{newRowIdx}',
        params={
            'valueInputOption': 'USER_ENTERED'
        },
        body={
            'values': [[locationLink]]
        }
    )

    # write analyzer hyperlink
    webViewLink = f'https://docs.google.com/spreadsheets/d/{newAnalyzerSheetId}'
    analyzerLink = f'=HYPERLINK("{webViewLink}","Link")'
    prospectivePropsSheet.values_update(
        f'Sheet1!C{newRowIdx}',
        params={
            'valueInputOption': 'USER_ENTERED'
        },
        body={
            'values': [[analyzerLink]]
        }
    )

    # write remaining info (total price, monthly amount, living area, dimensions, etc.)
    dimensionStr = f'{propertyDict['resoFacts']['bedrooms']}x{propertyDict['resoFacts']['bathrooms']}'
    prospectivePropsWorksheet.update([[propertyDict['price'], analyzerSheetData['monthlyAmt'], propertyDict['livingArea'], dimensionStr]], f'D{newRowIdx}:G{newRowIdx}')


if __name__ == "__main__":
    main()