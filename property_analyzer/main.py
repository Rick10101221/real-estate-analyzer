import config
import sheet
import utils

from gspread.utils import ValueRenderOption


def main():
    #introMsg()
    #print()

    propertyDict = utils.getAndResolveUrl()
    if propertyDict == None:
        return
    driveService, sheetService, configDict = config.main()

    print('Copying analyzer sheet and writing data from property page...')
    newAnalyzerSheetId = sheet.writeToAnalyzerSheet(driveService, sheetService, configDict, propertyDict)

    analyzerSheetData = sheet.getDataFromAnalyzerSheet(sheetService, newAnalyzerSheetId)

    print('Writing data to prospective properties sheet...')
    sheet.writeDataToProspectivePropsSheet(sheetService, configDict, propertyDict, analyzerSheetData, newAnalyzerSheetId)

    print()
    print('Done! Thanks for using Rickesh\'s Property Analyzer!')
    print('Check Google Drive for results.')


def introMsg():
    print('Welcome to Rickesh\'s Property Analyzer!')
    print('This program will analyze a property from Zillow.com or OneHome.com.')
    print('Please provide a valid URL for the property you want to analyze.')
    print('The URL should be in the format: https://www.zillow.com/homedetails/ or https://portal.onehome.com/en-US/property/')
    print('The program will then fetch the property data and analyze it.')
    print('Note that the program may take a few minutes to fetch the data, depending on the property and your internet connection.')


if __name__ == "__main__":
    main()