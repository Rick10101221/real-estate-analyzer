import config
import zillow

from gspread.utils import ValueRenderOption

def main():
    driveService, sheetService, configDict = config.main()
    propertyDict = zillow.main()


    #create duplicate of analyzer file in analyzer parent folder
    fileMetadata = {
        'name': f'Analyzer - {propertyDict['fullAddress']}',
        'parents': [configDict["analyzerFolderId"]],
    }
    sheetResponse = driveService.files().copy(body=fileMetadata, fileId=configDict["analyzerSourceSheetId"]).execute()

    #get analyzer worksheet reference
    newAnalyzerSheetId = sheetResponse['id']
    webViewLink = sheetResponse.get('webViewLink', None)
    if not webViewLink: print("No webViewLink found in the response.")
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

    # get monthly amount
    monthlyAmt = round(analyzerWorksheet.get("T94:U94", value_render_option=ValueRenderOption.unformatted)[0][0],2)

    #get prospective properties worksheet reference
    prospectivePropsSheet = sheetService.open_by_key(configDict["prospectivePropsSheetId"])
    prospectivePropsWorksheet = prospectivePropsSheet.get_worksheet(0)
    newRowIdx = len(prospectivePropsWorksheet.col_values(2)) + 1

    #write location
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
    dimensionStr = f'{propertyDict['resoFacts']['bedrooms']}x{propertyDict['resoFacts']['bathrooms']}'
    prospectivePropsWorksheet.update([[propertyDict['price'], monthlyAmt, propertyDict['livingArea'], dimensionStr]], f'C{newRowIdx}:F{newRowIdx}')
    if not webViewLink:
        webViewLink = f'https://docs.google.com/spreadsheets/d/{newAnalyzerSheetId}'
    if webViewLink:
        analyzerLink = f'=HYPERLINK("{webViewLink}","Link")'
        prospectivePropsSheet.values_update(
            f'Sheet1!G{newRowIdx}',
            params={
                'valueInputOption': 'USER_ENTERED'
            },
            body={
                'values': [[analyzerLink]]
            }
        )
    

if __name__ == "__main__":
    main()