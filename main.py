import time
import random
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService

def setup_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")  # Avoid sandboxing for Termux
    chrome_options.add_argument("--disable-dev-shm-usage")  # Disable /dev/shm usage
    
    # Path to chromedriver
    driver_path = '/data/data/com.termux/files/usr/bin/chromedriver'
    
    # Set up the service for the Chrome driver
    service = ChromeService(executable_path=driver_path)
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def get_facebook_ids(target_url):
    driver = setup_chrome_driver()

    driver.get(f'https://www.facebook.com/{target_url}')
    time.sleep(2)

    # Extract Friends' IDs (recursively)
    ids = []
    try:
        friends_section = driver.find_element(By.XPATH, "//a[contains(@href, '/friends')]")
        friends_section.click()
        time.sleep(2)
        
        # Extract IDs of friends
        friend_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/profile.php?id=')]")
        for link in friend_links:
            id = link.get_attribute('href').split('id=')[1]
            name = link.text
            ids.append(f'{id} | {name}')

        # Extract IDs of Friends' Friends
        friends_friends = driver.find_elements(By.XPATH, "//a[contains(@href, '/profile.php?id=')]")
        for friend in friends_friends:
            id = friend.get_attribute('href').split('id=')[1]
            name = friend.text
            if f'{id} | {name}' not in ids:
                ids.append(f'{id} | {name}')

    except Exception as e:
        print(f'[ERROR] {str(e)}')

    # Save IDs to ids.txt
    with open('ids.txt', 'w') as f:
        for item in ids:
            f.write(f"{item}\n")

    print(f'[INFO] IDs extracted and saved to ids.txt')

def main():
    print("Welcome to Facebook ID Extractor")
    target_url = input("Enter the target profile ID or URL: ").strip()

    get_facebook_ids(target_url)

    print("[ ! ] Extraction completed. Check ids.txt for results.")
    input("[Enter] to go back to the menu...")

if __name__ == "__main__":
    main()