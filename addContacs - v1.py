from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import pandas as pd  # Dodan import za pandas
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Logging setup
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='whatsapp_automation.log', filemode='w')

def wait_and_click(driver, xpath, timeout=10):
    """Waits for an element to be clickable and clicks it."""
    logging.debug(f"Waiting for element: {xpath}")
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
    logging.debug(f"Clicked element: {xpath}")

def load_contacts(file_path, column_name):
    """Load phone numbers from an Excel file."""
    try:
        df = pd.read_excel(file_path)
        return df[column_name].astype(str).tolist()
    except Exception as e:
        logging.error(f"Error loading contacts: {e}")
        return []

def add_to_whatsapp_community(driver, community_name):
    """Automates adding all visible contacts to a WhatsApp community."""
    logging.info("Navigating to WhatsApp Web")
    driver.get("https://web.whatsapp.com/")
    print("Please scan the QR code to log in to WhatsApp.")
    
    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]'))
        )
        logging.info("WhatsApp Web loaded successfully.")
    except Exception as e:
        logging.error(f"Failed to load WhatsApp Web: {e}")
        return

    try:
        logging.info("Searching for community")
        search_box_xpath = '//div[@role="textbox" and @contenteditable="true"]'
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, search_box_xpath))
        )
        search_box.send_keys(community_name)
        time.sleep(2)

        community_xpath = f'//span[@title="{community_name}"]'
        wait_and_click(driver, community_xpath)
        time.sleep(2)

        logging.info("Opening menu")
        menu_button_xpath = '/html/body/div[1]/div/div/div[3]/div/div[4]/div/header/div[3]/div/div[3]'
        wait_and_click(driver, menu_button_xpath)
        
        logging.info("Accessing Announcement Info")
        announcement_info_xpath = '/html/body/div[1]/div/div/span[5]/div/ul/div/div/li[1]'
        wait_and_click(driver, announcement_info_xpath)
        time.sleep(2)

        logging.info("Clicking Add Members")
        add_members_xpath = '/html/body/div[1]/div/div/div[3]/div/div[5]/span/div/span/span/div/div/section/div[1]/div/div[4]/button[2]'
        wait_and_click(driver, add_members_xpath)
        time.sleep(2)

        logging.info("Selecting contacts")
        contact_list_xpath = "//div[contains(@class, '_ak72') and contains(@class, '_ak73') and contains(@class, '_ak75')]"
        contacts = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, contact_list_xpath))
        )

        logging.debug(f"Found {len(contacts)} contacts to add.")
        for contact in contacts:
            try:
                contact.click()
                logging.debug("Contact selected.")
            except Exception as e:
                logging.error(f"Could not select contact: {e}")

        logging.info("Confirming addition of contacts")
        confirm_button_xpath = '/html/body/div[1]/div/div/span[2]/div/span/div/div/div/div/div/div/span[2]/div/div/div'
        wait_and_click(driver, confirm_button_xpath)
        time.sleep(2)

        logging.info("Handling additional confirmation steps")
        additional_confirmation_button_xpath = '/html/body/div[1]/div/div/span[2]/div/span/div/div/div/div/div/div[2]/div/button[2]'
        wait_and_click(driver, additional_confirmation_button_xpath)
        time.sleep(2)

        logging.info("Handling group invitation step")
        invite_to_group_button_xpath = '/html/body/div[1]/div/div/span[2]/div/span/div/div/div/div/div/div[2]/div/button[2]'
        wait_and_click(driver, invite_to_group_button_xpath)
        time.sleep(2)

        invitation_xpath = '/html/body/div[1]/div/div/span[2]/div/span/div/div/div/div/div/div/div/span/div'
        wait_and_click(driver, invitation_xpath)
        time.sleep(1000)
        logging.info("All steps completed successfully.")
    
    except Exception as e:
        logging.error(f"Error during process: {e}")

if __name__ == "__main__":
    # Path to the Excel file and configuration
    excel_file = r'C:\Users\user\Documents\whatsappAutomatization\googleContacts.xlsx'
    column_name = "mobitel"
    community_name = "GIT trgovina"

    # Set up WebDriver with a persistent profile
    profile_path = r'C:\Users\user\Documents\whatsappAutomatization\chrome_profile'
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={profile_path}")

    try:
        # Automatski preuzima ispravnu verziju ChromeDriver-a
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # Pokreće automatizaciju
        add_to_whatsapp_community(driver, community_name)
    except Exception as e:
        logging.error(f"Failed to start WebDriver: {e}")
    finally:
        driver.quit()
