import config
import sheet
import utils

from gspread.utils import ValueRenderOption


def main():
    propertyDict = utils.getAndResolveUrl()
    driveService, sheetService, configDict = config.main()

    print('Copying analyzer sheet and writing data from property page...')
    newAnalyzerSheetId = sheet.writeToAnalyzerSheet(driveService, sheetService, configDict, propertyDict)

    analyzerSheetData = sheet.getDataFromAnalyzerSheet(sheetService, newAnalyzerSheetId)

    print('Writing data to prospective properties sheet...')
    sheet.writeDataToProspectivePropsSheet(sheetService, configDict, propertyDict, analyzerSheetData, newAnalyzerSheetId)

    print('Done! Thanks for using Rickesh\'s Property Analyzer!')
    print('Check Google Drive for results.')

if __name__ == "__main__":
    main()