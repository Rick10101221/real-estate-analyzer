import utils

import datetime

def main(url):
    print('Fetching data from OneHome...')
    
    soup = utils.getSoupWithSelenium(url)
    
    propertyDict = {}
    
    # address information
    propertyDict['fullAddress'] = soup.findAll('p', {'data-qa' : 'address-line1'})[0].text.strip()
    stateZipSpaceIdx = propertyDict['fullAddress'].rfind(' ')
    propertyDict['zipcode'] = propertyDict['fullAddress'][stateZipSpaceIdx + 1:]
    propertyDict['state'] = propertyDict['fullAddress'][propertyDict['fullAddress'].rfind(' ', 0, stateZipSpaceIdx-1) + 1:stateZipSpaceIdx]
    dtMlsAreaMajor = soup.find('dt', string='MLS Area Major')
    mlsAreaMajor = dtMlsAreaMajor.find_next_sibling().text
    propertyDict['city'] = mlsAreaMajor.split(' - ')[1].strip()
    cityIdx = propertyDict['fullAddress'].find(propertyDict['city'])
    propertyDict['streetAddress'] = propertyDict['fullAddress'][:cityIdx].strip()
    propertyDict['location'] = propertyDict['fullAddress'][cityIdx:].strip()

    # price information
    propertyDict['price'] = int(soup.find('p', class_='price').text.replace('$', '').replace(',','').strip())
    try:
        hoaMonthlyStr = soup.select_one('li[data-qa=\'AssociationFeeColon-feature\'] dd.detail').text.strip()
        propertyDict['monthlyHoaFee'] = int(hoaMonthlyStr.split(' ')[0].replace('$', '').replace(',', '').strip())
    except:
        propertyDict['monthlyHoaFee'] = 0

    # miscellaneous information
    daysOnMarketSiblingSpan = soup.find('span', string='Days on OneHome')
    propertyDict['daysOnMarket'] = int(list(daysOnMarketSiblingSpan.find_next_sibling().children)[1].text.strip())
    propertyDict['listingDate'] = (datetime.date.today() - datetime.timedelta(days=propertyDict['daysOnMarket'])).strftime('%m/%d/%y')
    propertyDict['url'] = url
    propertyDict['homeType'] = soup.select_one('li[data-qa=\'PropertySubTypeColon-feature\'] dd.detail').text.strip()
    propertyDict['yearBuilt'] = int(soup.select_one('li[data-qa=\'YearBuiltColon-feature\'] dd.detail').text)
    propertyDict['livingArea'] = int(soup.findAll('span', {'data-qa' : 'sqft'})[0].text.replace('sqft', '').replace(',', '').strip())
    propertyDict['resoFacts'] = {}
    try:
        propertyDict['resoFacts']['bedrooms'] = int(soup.findAll('span', {'data-qa' : 'beds'})[0].text)
        propertyDict['resoFacts']['bathrooms'] = int(soup.findAll('span', {'data-qa' : 'baths'})[0].text)
    except:
        propertyDict['resoFacts']['bedrooms'] = 0
        propertyDict['resoFacts']['bathrooms'] = 0
    propertyDict['crimeGrade'], propertyDict['crimeGradeUrl'] = utils.getCrimeGrade(propertyDict['city'], propertyDict['state'])

    return propertyDict


if __name__ == "__main__":
    main()