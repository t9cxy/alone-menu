import time
import re
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize Selenium WebDriver
driver = webdriver.Chrome()  # Ensure chromedriver is in your PATH

# -------------------------- ASCII Art --------------------------
def print_logo():
    print("""
█████╗ ██╗      ██████╗ ███╗   ██╗███████╗
██╔══██╗██║     ██╔═══██╗████╗  ██║██╔════╝
███████║██║     ██║   ██║██╔██╗ ██║█████╗  
██╔══██║██║     ██║   ██║██║╚██╗██║██╔══╝  
██║  ██║███████╗╚██████╔╝██║ ╚████║███████╗
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
    """)

# -------------------------- Proxy Generator --------------------------
def generate_proxies():
    # Proxy generation logic (simplified here)
    proxy_list = []
    for _ in range(10):  # Change to your desired proxy count
        proxy = "ip:port"
        proxy_list.append(proxy)
    return proxy_list

# -------------------------- Facebook ID Extractor --------------------------
def login_facebook(email, password):
    driver.get('https://www.facebook.com/')
    time.sleep(2)
    driver.find_element(By.ID, 'email').send_keys(email)
    driver.find_element(By.ID, 'pass').send_keys(password)
    driver.find_element(By.NAME, 'login').click()
    time.sleep(5)  # Wait for login to complete

def get_friends(profile_url):
    driver.get(profile_url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    friends = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        name = link.get_text()
        if '/profile.php?id=' in href:
            uid = re.search(r'id=(\d+)', href).group(1)
            friends.append((uid, name))
        elif href.startswith('/'):
            uid = href.strip('/').split('?')[0]
            friends.append((uid, name))
    return friends

def extract_ids(email, password, target_profile):
    login_facebook(email, password)
    first_level_friends = get_friends(target_profile)
    all_friends = set(first_level_friends)
    for uid, _ in first_level_friends:
        friend_profile = f'https://www.facebook.com/profile.php?id={uid}'
        friends_of_friend = get_friends(friend_profile)
        all_friends.update(friends_of_friend)
    with open('ids.txt', 'w', encoding='utf-8') as f:
        for uid, name in all_friends:
            f.write(f'{uid} | {name}\n')

# -------------------------- Menu Options --------------------------
def display_menu():
    print_logo()
    print("\n[1] Proxy Options")
    print("[2] Facebook ID Extractor")
    print("[3] Send Feedback")
    print("[4] Exit\n")

def proxy_menu():
    print("\n[1] Check Proxy By File")
    print("[2] Check From URL (GitHub, PasteBin, etc.)")
    print("[3] Generate and Check Proxy\n")

def facebook_ids_extractor():
    print("[*] Enter Facebook email and password:")
    email = input("Email: ")
    password = input("Password: ")
    target_profile = input("Enter Target Profile URL: ")
    print("[*] Extracting IDs...")

    extract_ids(email, password, target_profile)
    print("[*] Extraction complete. Results saved in 'ids.txt'")

def send_feedback():
    feedback = input("Enter your feedback: ")
    print("[*] Sending feedback...")  # Replace with your actual feedback handling code
    time.sleep(1)
    print("[*] Feedback sent successfully.")

def main():
    while True:
        display_menu()
        choice = input("Choose an option: ")

        if choice == '1':
            proxy_menu()
            proxy_choice = input("Choose proxy option: ")
            if proxy_choice == '1':
                print("[*] Check Proxy By File (Functionality to be implemented)")
            elif proxy_choice == '2':
                print("[*] Check Proxy From URL (Functionality to be implemented)")
            elif proxy_choice == '3':
                proxies = generate_proxies()
                print("\n[ GOOD ] Proxy Generation Results:")
                for proxy in proxies:
                    print(f"[ {proxy} ]")

        elif choice == '2':
            facebook_ids_extractor()

        elif choice == '3':
            send_feedback()

        elif choice == '4':
            print("[*] Exiting...")
            driver.quit()  # Close the Selenium WebDriver
            break

if __name__ == '__main__':
    main()