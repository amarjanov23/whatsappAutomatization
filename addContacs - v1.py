from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os

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
        print(f"Error loading contacts: {e}")
        return []

def add_to_whatsapp_community(driver, community_name):
    """
    Automates adding all visible contacts to a WhatsApp community.
    :param driver: Selenium WebDriver.
    :param community_name: Name of the WhatsApp community.
    """
    driver.get("https://web.whatsapp.com/")
    print("Please scan the QR code to log in to WhatsApp.")
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
        menu_button_xpath = '/html/body/div[1]/div/div/div[3]/div/div[4]/div/header/div[3]/div/div[3]'
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, menu_button_xpath))
        ).click()

        # Click "Announcement Info"
        announcement_info_xpath = '/html/body/div[1]/div/div/span[5]/div/ul/div/div/li[1]'
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, announcement_info_xpath))
        ).click()
        time.sleep(2)

        # Click "Add Members"
        add_members_xpath = '/html/body/div[1]/div/div/div[3]/div/div[5]/span/div/span/span/div/div/section/div[1]/div/div[4]/button[2]'
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, add_members_xpath))
        ).click()
        time.sleep(2)

        # Select all visible contacts by new class
        contact_list_xpath = "//div[contains(@class, '_ak72') and contains(@class, '_ak73') and contains(@class, '_ak75')]"
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, contact_list_xpath))
        )

        contacts = driver.find_elements(By.XPATH, contact_list_xpath)
        for contact in contacts:
            try:
                contact.click()
                print("Contact selected.")
            except Exception as e:
                print(f"Could not select contact: {e}")

        # Confirm adding contacts
        confirm_button_xpath = '//div[@data-testid="done"]'
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, confirm_button_xpath))
        ).click()
        print("All contacts have been added to the community.")
    except Exception as e:
        print(f"Error selecting contacts: {e}")

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
