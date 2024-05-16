# This script automates the web game "Cookie Clicker" using Selenium Webdriver and Google Chrome.

# Download "ChromeDriver win64" from https://googlechromelabs.github.io/chrome-for-testing/#stable.
# Extract the file and place the chromedriver.exe to the same folder as this file.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import time
import sys
import os

GAME_URL = "https://orteil.dashnet.org/cookieclicker/"
WEBDRIVER_PATH = "chromedriver.exe"

if ( os.path.isfile(WEBDRIVER_PATH) ) == False:
    print('\nERROR: ChromeDriver.exe could not be found.')
    print('\nPlease download "ChromeDriver win64" from https://googlechromelabs.github.io/chrome-for-testing/#stable. Extract the file and place the chromedriver.exe to the same folder as this python file.\n\n')
    quit()

# Set up the webdriver service.
SERVICE = Service(executable_path=WEBDRIVER_PATH)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")
DRIVER = webdriver.Chrome(service=SERVICE, options=chrome_options)

def main(): 
    DRIVER.get(GAME_URL)
    DRIVER.set_window_size(1200,1000)
    DRIVER.set_window_position(0,0)
    
    time.sleep(5)


if __name__ == '__main__':
    main()
    
DRIVER.quit()