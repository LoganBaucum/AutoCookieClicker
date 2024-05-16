# This script automates the web game "Cookie Clicker" using Selenium Webdriver and Google Chrome.

# Download "ChromeDriver win64" from https://googlechromelabs.github.io/chrome-for-testing/#stable.
# Extract the file and place the chromedriver.exe to the same folder as this file.

# TODO: Add save/load game functionality.
# TODO: Add NewGame+ functionality, to enable ascending to the next level.


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import os

GAME_URL = "https://orteil.dashnet.org/cookieclicker/"
WEBDRIVER_PATH = "chromedriver.exe"

if ( os.path.isfile(WEBDRIVER_PATH) ) == False:
    print('\nERROR: ChromeDriver.exe could not be found.')
    print('\nPlease download "ChromeDriver win64" from https://googlechromelabs.github.io/chrome-for-testing/#stable. Extract the file and place the chromedriver.exe to the same folder as this python file.\n\n')
    quit()

# Set up the webdriver service.
SERVICE = Service(executable_path=WEBDRIVER_PATH)
CHROME_OPTIONS = webdriver.ChromeOptions()
CHROME_OPTIONS.add_argument("--window-size=800,600")
CHROME_OPTIONS.add_argument("--mute-audio")
DRIVER = webdriver.Chrome(service=SERVICE, options=CHROME_OPTIONS)

def close_notification_popups():
    popup_class = "notes"
    try:
        notifications = DRIVER.find_elements(By.ID, popup_class)
        for note in notifications:
            note_title = note.find_element(By.TAG_NAME, 'h3').text
            note.find_element(By.CLASS_NAME, 'close').click()
            print(f'Closed {note_title} notification.')
    except:
        return

def main(): 
    DRIVER.get(GAME_URL)
    DRIVER.set_window_size(1200,1000)
    DRIVER.set_window_position(50,50)

    try:
        WebDriverWait(DRIVER, 5).until(
            EC.presence_of_element_located((By.ID, "langSelect-EN"))
        ).click()
    except Exception as exc:
        print(f'ERROR: {exc}')
        quit()

    # ID = Loader, for the loading screen.
    # ID = Darken, for the page overlay.
    
    # Wait for page reload.
    time.sleep(5)

    # Hide ads
    DRIVER.execute_script("document.getElementById('support').style.display = 'none';")
    DRIVER.execute_script("document.getElementById('smallSupport').style.display = 'none';") 

    # Close webpage cookies popup notification
    try:
        webpage_cookies_popup = WebDriverWait(DRIVER, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "cc_btn.cc_btn_accept_all"))
        )
        webpage_cookies_popup.click()
    except Exception as e:
        print(f'Error occurred: {e}')
        quit()

    close_notification_popups()

    is_playing_game = True
    clicked_product = False
    clicked_upgrade = False

    while is_playing_game:
        try:
            big_cookie_element = WebDriverWait(DRIVER, 5).until(
                EC.presence_of_element_located((By.ID, "bigCookie"))
            )
        except Exception as exc:
            print(f'ERROR: {exc}')
            is_playing_game = False

        big_cookie_element.click()
    
        close_notification_popups()
        
        # Products
        # Buys a product, the cheapest product will be bought.
        # ID = Product#, for each product.
        # CLASS = Product.Unlocked.Enabled, for purchasable products
        try:
            product = DRIVER.find_element(By.CLASS_NAME, "product.unlocked.enabled")
            product_name = product.find_element(By.CLASS_NAME, 'title.productName').text
            product_amount_owned = product.find_element(By.CLASS_NAME, 'title.owned').text
            # product_name = product.text.split("\n")[0]
            # product_id = product.get_attribute("ID")
            # product_owned_id = "productOwned" + product_id.split("product")[1]
            # product_amount_owned = DRIVER.find_element(By.ID, product_owned_id).text

            if not clicked_product:
                product.click()
                clicked_product = True
                print(f'Bought product: {product_name}, Owned: {product_amount_owned}')
        except:
            clicked_product = False
        
        # Upgrades
        # Buys an upgrade, the cheapest upgrade will be bought.
        # ID = Upgrade#, for each upgrade.
        # CLASS = Crate.Upgrade.Enabled, for purchasable upgrades.
        try:
            upgrade_button = DRIVER.find_element(By.CLASS_NAME, "crate.upgrade.enabled")
            if not clicked_upgrade:
                upgrade_button.click()
                clicked_upgrade = True
                print(f"Bought upgrade: ")
        except:
            clicked_upgrade = False


    DRIVER.quit()

if __name__ == '__main__':
    main()
    