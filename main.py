import os
import re
import time
import json
import requests
import random
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import quote

# Your Telegram Bot Info
BOT_TOKEN = "6770850573:AAFUCCzKlKrekJU5GtNFqdnqwMSAsnTBIc0"
CHAT_ID = "1241769879"

# Color codes for better output readability
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Function to clear the screen based on the OS
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to send logs to Telegram
def send_telegram_log(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={quote(message)}"
    try:
        requests.get(url)
    except Exception as e:
        print(f"[•] Error sending log to Telegram: {e}")

# Function to print colorful and styled messages
def print_colored(message, color):
    print(color + message + Colors.ENDC)

# Function to log and notify via Telegram about each action
def log_and_notify(action):
    message = f"[•] {action} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    send_telegram_log(message)
    print_colored(f"[•] {action}", Colors.OKCYAN)

# Encrypt Code Function
def encrypt_code():
    print_colored("[•] Welcome to the Code Encryptor!", Colors.OKCYAN)
    print_colored("[•] Please enter the file name to encrypt:", Colors.OKBLUE)
    file_name = input("[•] File Name: ")

    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            code = f.read()
        encrypted_code = f"Encrypted Code: {code[::-1]}"  # Simple reverse encryption for example
        encrypted_file_name = f"encrypted_{file_name}"

        with open(encrypted_file_name, "w") as f:
            f.write(encrypted_code)
        
        log_and_notify(f"Encrypted file: {file_name} -> {encrypted_file_name}")
        print_colored(f"[•] Code encrypted successfully and saved as {encrypted_file_name}", Colors.OKGREEN)
    else:
        print_colored("[•] File does not exist!", Colors.FAIL)

    input("[•] Press Enter to return to the main menu...")

# Proxy Options function
def proxy_options():
    print_colored("[•] Proxy Options", Colors.OKCYAN)
    print_colored("[1] Check Proxy by File", Colors.OKBLUE)
    print_colored("[2] Check from URL (GitHub, PasteBin, etc)", Colors.OKBLUE)
    print_colored("[3] Generate and Check Proxy", Colors.OKBLUE)
    choice = input("[?] Choose an option: ")
    
    if choice == "1":
        file = input("[•] Enter proxy file path: ")
        check_proxies_from_file(file)

    elif choice == "2":
        url = input("[•] Enter URL to fetch proxies: ")
        check_proxies_from_url(url)

    elif choice == "3":
        print_colored("[•] Generating proxies...", Colors.OKCYAN)
        generate_and_check_proxies()

    else:
        print_colored("[•] Invalid option! Returning to main menu...", Colors.FAIL)

    input("[•] Press Enter to return to the main menu...")

# Placeholder functions (to be expanded)
def check_proxies_from_file(file):
    print_colored(f"[•] Checking proxies from file: {file}", Colors.OKCYAN)

def check_proxies_from_url(url):
    print_colored(f"[•] Checking proxies from URL: {url}", Colors.OKCYAN)

def generate_and_check_proxies():
    print_colored("[•] Generating and checking proxies...", Colors.OKCYAN)

# Main menu options
def main_menu():
    clear_screen()
    print_colored(" █████╗ ██╗      ██████╗ ███╗   ██╗███████╗", Colors.OKCYAN)
    print_colored("██╔══██╗██║     ██╔═══██╗████╗  ██║██╔════╝", Colors.OKCYAN)
    print_colored("███████║██║     ██║   ██║██╔██╗ ██║█████╗  ", Colors.OKCYAN)
    print_colored("██╔══██║██║     ██║   ██║██║╚██╗██║██╔══╝  ", Colors.OKCYAN)
    print_colored("██║  ██║███████╗╚██████╔╝██║ ╚████║███████╗", Colors.OKCYAN)
    print_colored("╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝", Colors.OKCYAN)

    print_colored("\n[1] Proxy Options", Colors.OKGREEN)
    print_colored("[2] User-Agent Generator", Colors.OKGREEN)
    print_colored("[3] Send HTTP Request", Colors.OKGREEN)
    print_colored("[4] Look IP Info", Colors.OKGREEN)
    print_colored("[5] Facebook IDs Extractor", Colors.OKGREEN)
    print_colored("[6] Group Member ID Dumper", Colors.OKGREEN)
    print_colored("[7] Encrypt Code", Colors.OKGREEN)
    print_colored("[0] Exit", Colors.FAIL)
    
    choice = input("[?] Choose an option: ")

    if choice == "1":
        proxy_options()
    elif choice == "2":
        print_colored("[•] User-Agent Generator not implemented here.", Colors.WARNING)
        input("[•] Press Enter to return to the main menu...")
    elif choice == "3":
        print_colored("[•] Send HTTP Request not implemented here.", Colors.WARNING)
        input("[•] Press Enter to return to the main menu...")
    elif choice == "4":
        print_colored("[•] Look IP Info not implemented here.", Colors.WARNING)
        input("[•] Press Enter to return to the main menu...")
    elif choice == "5":
        print_colored("[•] Facebook IDs Extractor not implemented here.", Colors.WARNING)
        input("[•] Press Enter to return to the main menu...")
    elif choice == "6":
        print_colored("[•] Group Member ID Dumper not implemented here.", Colors.WARNING)
        input("[•] Press Enter to return to the main menu...")
    elif choice == "7":
        encrypt_code()
    elif choice == "0":
        print_colored("[•] Exiting...", Colors.FAIL)
        exit()
    else:
        print_colored("[•] Invalid option! Returning to main menu...", Colors.FAIL)
        input("[•] Press Enter to return to the main menu...")

# Run the main menu
if __name__ == "__main__":
    while True:
        main_menu()