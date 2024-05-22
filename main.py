# This script automates the web game "Cookie Clicker" using Selenium Webdriver and Google Chrome.

# Download "ChromeDriver win64" from https://googlechromelabs.github.io/chrome-for-testing/#stable.
# Extract the file and place the chromedriver.exe to the same folder as this file.

# TODO: Add save/load game functionality.
# TODO: Add NewGame+ functionality, to enable ascending to the next level.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import os

print("Auto Cookie Clicker running...\n")

GAME_URL = "https://orteil.dashnet.org/cookieclicker/"
WEBDRIVER_PATH = "chromedriver.exe"
SAVE_FILE_PATH = "savefile.txt"

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
ACTIONS = ActionChains(DRIVER)

def close_notification_popups():
    popup_class = "notes"
    try:
        notifications = DRIVER.find_elements(By.ID, popup_class)
        for note in notifications:
            note_title = note.find_element(By.TAG_NAME, 'h3').text
            note.find_element(By.CLASS_NAME, 'close').click()
            # print(f'Closed {note_title} notification.')
    except:
        return

def export_save_game():
    try:
        option_button = WebDriverWait(DRIVER, 5).until(
            EC.element_to_be_clickable((By.ID, "prefsButton"))
        )
        option_button.click()

        try:
            export_save_button = WebDriverWait(DRIVER, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="menu"]/div[3]/div/div[4]/a[1]'))
            )
            export_save_button.click()
            save_game_text = DRIVER.find_element(By.ID, 'textareaPrompt').text

            try:
                save_file = open(SAVE_FILE_PATH, "w")
                save_file.write(save_game_text)
                save_file.close()
                # print("Exported save.")

            except Exception as exc:
                print(f'ERROR Opening savefile: {exc}')
            
            close_textarea_button = DRIVER.find_element(By.ID, 'promptOption0')
            close_textarea_button.click()

        except Exception as exc:
            print(f'ERROR Finding Export button: {exc}')

        # Close options menu
        option_button.click()

    except Exception as exc:
        print(f'ERROR Finding Options button: {exc}')


def import_save_game():
    try:
        ACTIONS.reset_actions()
        ACTIONS.key_down(Keys.CONTROL).send_keys('O').key_up(Keys.CONTROL)
        ACTIONS.perform()

        try:
            save_file = open(SAVE_FILE_PATH, "r")
            save_file_contents = save_file.read()
            
            WebDriverWait(DRIVER, 5).until(
                EC.visibility_of_element_located((By.ID, 'textareaPrompt'))
            )

            script = f"document.getElementById('textareaPrompt').value = `{save_file_contents}`;"
            DRIVER.execute_script(script)
            save_file.close()
            # print("Imported save.")

        except Exception as exc:
            print(f'ERROR opening savefile: {exc}')

        load_button = DRIVER.find_element(By.ID, 'promptOption0')
        load_button.click()

    except Exception as exc:
        print(f'ERROR opening Import dialog: {exc}')



def main(): 
    DRIVER.get(GAME_URL)
    DRIVER.set_window_size(1200,1000)
    DRIVER.set_window_position(50,50)

    try:
        WebDriverWait(DRIVER, 5).until(
            EC.element_to_be_clickable((By.ID, "langSelect-EN"))
        ).click()
    except Exception as exc:
        print(f'ERROR: {exc}')
        quit()
    
    # Wait for page reload.
    time.sleep(5)

    # Hide ads
    DRIVER.execute_script("document.getElementById('support').style.display = 'none';")
    DRIVER.execute_script("document.getElementById('smallSupport').style.display = 'none';") 

    # Close webpage cookies popup banner
    try:
        webpage_cookies_popup = WebDriverWait(DRIVER, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "cc_btn.cc_btn_accept_all"))
        )
        webpage_cookies_popup.click()
    except Exception as exc:
        print(f'ERROR: {exc}')
        quit()

    close_notification_popups()

    # Load the save file if it exists.
    try:
        save_file_size = os.stat(SAVE_FILE_PATH).st_size
        if(save_file_size > 0):
            import_save_game()
    except:
        pass

    is_playing_game = True
    clicked_product = False
    clicked_upgrade = False
    has_saved_game = False

    while is_playing_game:
        try:
            # Golden Cookie appears on top of big cookie and needs to be checked first.
            golden_cookie_element = DRIVER.find_element(By.CLASS_NAME, "goldenCookie")
            golden_cookie_element.click()
        except:
            pass

        try:
            big_cookie_element = WebDriverWait(DRIVER, 5).until(
                EC.element_to_be_clickable((By.ID, "bigCookie"))
            )
            big_cookie_element.click()
        except Exception as exc:
            print(f'ERROR with BigCookie: {exc}')
            is_playing_game = False

        close_notification_popups()
        
        # Products
        # Buys a product, the cheapest product will be bought.
        try:
            product = DRIVER.find_element(By.CLASS_NAME, "product.unlocked.enabled")
            product_name = product.find_element(By.CLASS_NAME, 'title.productName').text
            product_amount_owned = product.find_element(By.CLASS_NAME, 'title.owned').text

            if not product.is_displayed:
                ACTIONS.reset_actions()
                ACTIONS.scroll_to_element(product).perform()

            if not clicked_product:
                product.click()
                clicked_product = True
                # print(f'Bought product: {product_name}, Owned: {product_amount_owned}')
        except:
            clicked_product = False
        
        # Upgrades
        # Buys an upgrade, the cheapest upgrade will be bought.
        try:
            upgrade_button = DRIVER.find_element(By.CLASS_NAME, "crate.upgrade.enabled")
            ACTIONS.reset_actions()
            ACTIONS.move_to_element(upgrade_button).perform()
            try: 
                tooltip = DRIVER.find_element(By.ID, "tooltip")
                upgrade_name = tooltip.find_element(By.CLASS_NAME, 'name').text
            except:
                pass

            if not upgrade_button.is_displayed:
                ACTIONS.reset_actions()
                ACTIONS.scroll_to_element(upgrade_button).perform()

            if not clicked_upgrade:
                upgrade_button.click()
                clicked_upgrade = True
                # print(f"Bought upgrade: {upgrade_name}")
        except:
            clicked_upgrade = False

        # TODO: Sugar lumps, check if ripe then do something.



        # TODO Prestige / Ascension / Heavenly Chip upgrades



        # Auto save the game every minute.
        t = time.localtime()
        current_time = time.strftime("%S", t)
        if int(current_time) == 00:
            if not has_saved_game:
                export_save_game()
                has_saved_game = True
        else:
            has_saved_game = False


    DRIVER.quit()

if __name__ == '__main__':
    main()
    