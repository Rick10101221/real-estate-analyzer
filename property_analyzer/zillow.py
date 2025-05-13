import requests
import utils

from bs4 import BeautifulSoup
from html import unescape
from json import loads
from re import compile


REGEX_SPACE = compile(r"[\s ]+")


def main(url):
    header = utils.getRequestHeader()
    print(header)
    print('Fetching data from Zillow...')
    response = requests.get(url, headers=header)
    utils.handleResponseErrors(response, header)
    body = parseBody(response.content)
    propertyDict = getPropertyDataFromBody(body)
    addDataToPropertyDict(propertyDict, url)
    return propertyDict


def addDataToPropertyDict(propertyDict: dict[str, any], url) -> None:
    """
    Add additional data to the property dictionary
    :param propertyDict: dictionary containing property data
    :return: None
    """
    location = propertyDict['city'] + ', ' + propertyDict['state'] + ' ' + propertyDict['zipcode']
    propertyDict['location'] = location
    fullAddress = propertyDict['streetAddress'] + ', ' + location
    propertyDict['fullAddress'] = fullAddress
    propertyDict['url'] = url
    propertyDict['crimeGrade'], propertyDict['crimeGradeUrl'] = utils.getCrimeGrade(propertyDict['city'], propertyDict['state'])
    if propertyDict['monthlyHoaFee'] == None:
        propertyDict['monthlyHoaFee'] = 0
    return


def getPropertyDataFromBody(body: dict[str, any]) -> dict[str, any]:
    cache = body['gdpClientCache']
    cache = cache[cache.index('{\"property\"'):].replace('\\\\"', '').replace('\\\'', '').rstrip('\'')[:-1]
    propertyDict = loads(cache)
    return propertyDict['property']


def parseBody(body: bytes) -> dict[str, any]:
    """
    https://github.com/johnbalvin/pyzill/blob/main/src/pyzill/parse.py
    parse HTML content to retrieve JSON data

    Args:
        body (bytes): HTML content of web page

    Returns:
        dict[str, any]: parsed property information
    """
    soup = BeautifulSoup(body, "html.parser")
    selection = soup.select_one("#__NEXT_DATA__")
    if selection:
        htmlData = selection.getText()
        htmlData = removeSpace(unescape(htmlData))
        data = loads(htmlData)
        return getNestedValue(data,"props.pageProps.componentProps")


def removeSpace(value: str) -> str:
    return REGEX_SPACE.sub(" ", value.strip())


def getNestedValue(dic, key_path, default=None):
    keys = key_path.split(".")
    current = dic
    for key in keys:
        current = current.get(key, {})
        if current == {} or current is None:
            return default
    return current


if __name__ == "__main__":
    main()