import requests
import random

from bs4 import BeautifulSoup
from html import unescape
from json import loads
from re import compile


OS = "Windows"
REGEX_SPACE = compile(r"[\s ]+")


def main():
    url = input("Provide a Zillow.com URL: ")
    if not url.startswith("https://www.zillow.com/homedetails/"):
        print("Invalid URL. Please provide a valid Zillow.com home details URL.")
        return
    
    header = getRequestHeader()
    print(header)
    response = requests.get(url, headers=header)
    response.raise_for_status()
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
    location = propertyDict['city'] + ', ' + propertyDict['state']
    propertyDict['location'] = location
    fullAddress = propertyDict['streetAddress'] + ', ' + location + ' ' + propertyDict['zipcode']
    propertyDict['fullAddress'] = fullAddress
    propertyDict['url'] = url
    return


def getOSCompatibleUserAgents() -> list[str]:
    """
    Get a list of user agents compatible with the current OS
    :return: list of user agents
    """
    compatibleAgents = []
    with open('user_agents.txt') as f:
        for line in f:
            if OS in line:
                compatibleAgents.append(line.strip()) 

    return compatibleAgents


def getRequestHeader() -> dict[str, str]:
    compatibleAgents = getOSCompatibleUserAgents()

    if not compatibleAgents:
        raise ValueError("No compatible user agents found for the current OS.")
    
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        "Cache-Control": "no-cache",
        'Connection': 'keep-alive',
        "Pragma": "no-cache",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        'User-Agent': random.choice(compatibleAgents),
        'TE': 'Trailers'
    }

    return headers


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