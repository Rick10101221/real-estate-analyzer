import os
import random
import requests
import time
import utils

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup

def main(url):
    print('Fetching data from OneHome...')
    
    userAgents = utils.getOSCompatibleUserAgents()

    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument(f'--user-agent={random.choice(userAgents)}')
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    print('Waiting for page to load...')
    time.sleep(5)  # Wait for the page to load
    
    # Use BeautifulSoup to Parse
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    propertyDict = {}
    propertyDict['url'] = url
    propertyDict['price'] = soup.find('p', class_='price').text.replace('$', '').replace(',', '')
    propertyDict['fullAddress'] = soup.findAll('p', {'data-qa' : 'address-line1'})[0].text
    propertyDict['location'] = propertyDict['fullAddress'].split(',')[0]
    propertyDict['homeType'] = soup.select_one('li[data-qa=\'PropertySubTypeColon-feature\'] dd.detail').text
    propertyDict['yearBuilt'] = soup.select_one('li[data-qa=\'YearBuiltColon-feature\'] dd.detail').text
    propertyDict['livingArea'] = soup.findAll('span', {'data-qa' : 'sqft'})[0].text.replace('sqft', '').replace(',', '')
    propertyDict['resoFacts'] = {}
    propertyDict['resoFacts']['bedrooms'] = soup.findAll('span', {'data-qa' : 'beds'})[0].text
    propertyDict['resoFacts']['bathrooms'] = soup.findAll('span', {'data-qa' : 'baths'})[0].text

    driver.quit()

    return propertyDict


if __name__ == "__main__":
    main()