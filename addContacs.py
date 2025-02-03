from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_contacts(file_path, column_name):
    """
    Load phone numbers from an Excel file.
    :param file_path: Path to the Excel file.
    :param column_name: Column name containing phone numbers.
    :return: List of phone numbers as strings.
    """
    try:
        df = pd.read_excel(file_path)
        return df[column_name].astype(str).tolist()
    except Exception as e:
        logging.error(f"Error loading contacts: {e}")
        return []

def add_to_whatsapp_community(driver, community_name):
    """
    Automates adding all visible contacts to a WhatsApp community.
    :param driver: Selenium WebDriver.
    :param community_name: Name of the WhatsApp community.
    """
    driver.get("https://web.whatsapp.com/")
    logging.info("Please scan the QR code to log in to WhatsApp.")
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]'))
    )

    try:
        # Search for the community
        search_box_xpath = '//div[@role="textbox" and @contenteditable="true"]'
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, search_box_xpath))
        )
        search_box.send_keys(community_name)
        time.sleep(2)

        community_xpath = f'//span[@title="{community_name}"]'
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, community_xpath))
        ).click()
        time.sleep(2)

        # Open the menu
        menu_button_xpath = '//div[@data-testid="menu"]'
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, menu_button_xpath))
        ).click()

        # Click "Announcement Info"
        announcement_info_xpath = '//div[text()="Announcement Info"]'
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, announcement_info_xpath))
        ).click()
        time.sleep(2)

        # Click "Add Members"
        add_members_xpath = '//div[text()="Add Members"]'
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, add_members_xpath))
        ).click()
        time.sleep(2)

        # Select all visible contacts
        contact_list_xpath = "//div[contains(@class, '_ak72') and contains(@class, '_ak73') and contains(@class, '_ak75')]"
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, contact_list_xpath))
        )

        contacts = driver.find_elements(By.XPATH, contact_list_xpath)
        for contact in contacts:
            try:
                contact.click()
                logging.info("Contact selected.")
            except Exception as e:
                logging.error(f"Could not select contact: {e}")

        # Click the "Next" button
        next_button_xpath = '//div[text()="Next"]'
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, next_button_xpath))
        ).click()
        time.sleep(2)
        logging.info("Next button clicked. Proceeding to the next step.")

        # Click the "Confirm" button
        confirm_button_xpath = '//div[text()="Confirm"]'
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, confirm_button_xpath))
        ).click()
        time.sleep(10)
        logging.info("Confirm button clicked. Contacts have been added to the community.")

        # Click the "Invite to Group" button
        invite_button_xpath = '//div[text()="Invite to Group"]'
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, invite_button_xpath))
        ).click()
        time.sleep(10)
        logging.info("Invite button clicked. Invitation sent to the selected contacts.")

    except Exception as e:
        logging.error(f"Error selecting contacts: {e}")

if __name__ == "__main__":
    # Path to the Excel file and configuration
    excel_file = r'C:\Users\user\Documents\whatsappAutomatization\googleContacts.xlsx'
    column_name = "mobitel"
    community_name = "GIT trgovina"

    # Set up WebDriver with a persistent profile
    profile_path = r'C:\Users\user\Documents\whatsappAutomatization\chrome_profile'
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={profile_path}")

    driver = webdriver.Chrome(
        service=webdriver.chrome.service.Service(
            r"C:\Users\user\Documents\whatsappAutomatization\chromedriver-win64\chromedriver.exe"
        ),
        options=options
    )

    try:
        add_to_whatsapp_community(driver, community_name)
    finally:
        driver.quit()
