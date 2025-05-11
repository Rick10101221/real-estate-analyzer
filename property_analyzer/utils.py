# library imports
import datetime
import os
import random

# file imports
import onehome
import zillow

OS = "Windows"

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


def handleResponseErrors(response, header = None):
    try:
        response.raise_for_status()
    except:
        filePath = os.path.join('errors', f'{datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}_error_log.txt')
        with open(filePath, 'w') as f:
            if header: f.write(f'{header}\n')
            f.write(f"{response.status_code} Request Error: {response.reason} for url: {response.url}")
        response.raise_for_status()


def getAndResolveUrl():
    print('Welcome to Rickesh\'s Property Analyzer!')
    print('This program will analyze a property from Zillow.com or OneHome.com.')
    print('Please provide a valid URL for the property you want to analyze.')
    print('The URL should be in the format: https://www.zillow.com/homedetails/ or https://portal.onehome.com/en-US/property/')
    print('The program will then fetch the property data and analyze it.')
    print('Note that the program may take a few minutes to fetch the data, depending on the property and your internet connection.')
    
    print()
    url = input('Provide a property URL: ')
    print()

    while True:
        if url.startswith('https://www.zillow.com/homedetails/'):
            # Call the Zillow function here
            return zillow.main(url)  
        elif url.startswith('https://portal.onehome.com/en-US/property/'):
            # Call the OneHome function here
            return onehome.main(url)
        else:
            print('Invalid URL. Please provide a valid property URL.')
    
    return None