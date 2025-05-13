import datetime

from gspread.utils import ValueRenderOption


ANALYZER_PROP_INFO_START_ROW = 10


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
    listingLink = f'=HYPERLINK("{propertyDict["url"]}","{propertyDict["streetAddress"]}")'
    newAnalyzerSheet.values_update(
        f'Analyzer!E{ANALYZER_PROP_INFO_START_ROW}:G{ANALYZER_PROP_INFO_START_ROW}',
        params={
            'valueInputOption': 'USER_ENTERED'
        },
        body={
            'values': [[listingLink]]
        }
    )
    for key in ['location', 'homeType', 'livingArea', 'yearBuilt']:
        coreInfo.append([propertyDict.get(key, ''), '', ''])
    analyzerWorksheet.update(coreInfo, f'E{ANALYZER_PROP_INFO_START_ROW+1}:G{ANALYZER_PROP_INFO_START_ROW + len(coreInfo)}')
    crimeGradeLink = f'=HYPERLINK("{propertyDict["crimeGradeUrl"]}","{propertyDict["crimeGrade"]}")'
    newAnalyzerSheet.values_update(
        f'Analyzer!E24:G24',
        params={
            'valueInputOption': 'USER_ENTERED'
        },
        body={
            'values': [[crimeGradeLink]]
        }
    )

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


def getCrimeDataByCitySheetData(sheetService, configDict, city):
    #get crime data worksheet reference
    crimeDataSheet = sheetService.open_by_key(configDict["crimeByCitySheetId"])
    crimeDataWorksheet = crimeDataSheet.get_worksheet(1)

    cities = crimeDataWorksheet.col_values(1)
    try:
        queryCityRow = cities.index(city) + 1
    except:
        return None
    
    cityRowData = crimeDataWorksheet.row_values(queryCityRow)
    crimeByCityData = {}
    crimeByCityData['city'] = cityRowData[0]
    crimeByCityData['county'] = cityRowData[1]
    crimeByCityData['population'] = cityRowData[2]
    crimeByCityData['populationDensity'] = cityRowData[3]
    crimeByCityData['violentCrime'] = cityRowData[4]
    crimeByCityData['violentCrimeRate'] = cityRowData[5]
    crimeByCityData['propertyCrime'] = cityRowData[6]
    crimeByCityData['propertyCrimeRate'] = cityRowData[7]

    return crimeByCityData


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

    # write crime data
    crimeByCityData = getCrimeDataByCitySheetData(sheetService, configDict, propertyDict['city'])
    crimeGradeLink = f'=HYPERLINK("{propertyDict["crimeGradeUrl"]}","{propertyDict["crimeGrade"]}")'
    prospectivePropsSheet.values_update(
        f'Sheet1!H{newRowIdx}',
        params={
            'valueInputOption': 'USER_ENTERED'
        },
        body={
            'values': [[crimeGradeLink]]
        }
    )
    if crimeByCityData:
        prospectivePropsWorksheet.update_acell(f'I{newRowIdx}', crimeByCityData['propertyCrimeRate'])

    prospectivePropsWorksheet.update([['Available', f'{datetime.datetime.now().strftime("%m/%d/%y")}']], f'J{newRowIdx}:K{newRowIdx}', 'Available')

    

if __name__ == "__main__":
    main()