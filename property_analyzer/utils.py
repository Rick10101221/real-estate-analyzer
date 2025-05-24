# library imports
import datetime
import os
import random
import time
from selenium import webdriver

# file imports
from bs4 import BeautifulSoup
import onehome
import zillow

OS = "Windows"

def getOSCompatibleUserAgents(excludeWebKit = False) -> list[str]:
    """
    Get a list of user agents compatible with the current OS
    :return: list of user agents
    """
    compatibleAgents = []
    with open('user_agents.txt') as f:
        for line in f:
            if OS not in line: continue
            if excludeWebKit and 'AppleWebKit' in line: continue
            compatibleAgents.append(line.strip()) 

    return compatibleAgents


def getRequestHeader(excludeWebKit = False) -> dict[str, str]:
    compatibleAgents = getOSCompatibleUserAgents(excludeWebKit)

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
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; FunWebProducts; rv:11.0) like Gecko',#random.choice(compatibleAgents),
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
    while True:
        url = input('Provide a property URL: ')
        print()
        if url.startswith('https://www.zillow.com/homedetails/'):
            # Call the Zillow function here
            return zillow.main(url)  
        elif url.startswith('https://portal.onehome.com/en-US/property/'):
            # Call the OneHome function here
            return onehome.main(url)
        elif url == 'quit':
            return None
        else:
            print('Invalid URL. Please provide a valid property URL.')


def getCrimeGrade(city, state):
    city, state = city.lower().strip().replace(' ', '-'), state.lower().strip()
    url = f'https://crimegrade.org/safest-places-in-{city}-{state}/'

    soup = getSoupWithSelenium(url)
    overallCrimeGrade = soup.find('p', class_='overallGradeLetter').text.strip()
    return overallCrimeGrade, url


def getSoupWithSelenium(url):
    # Set up Selenium WebDriver
    userAgents = getOSCompatibleUserAgents()
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--enable-unsafe-swiftshader')
    options.add_argument(f'--user-agent={random.choice(userAgents)}')
    driver = webdriver.Chrome(options=options)
    if driver == None:
        raise ValueError("Selenium WebDriver is not initialized.")

    driver.get(url)
    print('Waiting for page to load...')
    time.sleep(5)  # Wait for the page to load
    
    # Use BeautifulSoup to Parse
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return soup