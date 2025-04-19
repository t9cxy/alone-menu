import os
import re
import time
import json
import requests
import random
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import quote

# Telegram Log Info
BOT_TOKEN = "6770850573:AAFUCCzKlKrekJU5GtNFqdnqwMSAsnTBIc0"
CHAT_ID = "1241769879"

# GitHub Auto-Updater URL
GITHUB_RAW_URL = "https://raw.githubusercontent.com/t9cxy/alone-menu/refs/heads/main/main.py"

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

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def print_colored(message, color):
    print(color + message + Colors.ENDC)

def send_telegram_log(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={quote(message)}"
        requests.get(url)
    except:
        pass

def log_and_notify(action):
    message = f"[•] {action} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    send_telegram_log(message)
    print_colored(f"[•] {action}", Colors.OKCYAN)

def encrypt_code():
    print_colored("[•] Welcome to the Code Encryptor!", Colors.OKCYAN)
    print_colored("[•] Please enter the file name to encrypt:", Colors.OKBLUE)
    file_name = input("[•] File Name: ").strip()

    if not os.path.isabs(file_name):
        file_name = os.path.abspath(file_name)

    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            code = f.read()

        encrypted_code = f"# ENCRYPTED FILE\n{code[::-1]}"
        encrypted_file_name = f"encrypted_{os.path.basename(file_name)}"

        with open(encrypted_file_name, "w") as f:
            f.write(encrypted_code)

        log_and_notify(f"Encrypted file: {file_name} -> {encrypted_file_name}")
        print_colored(f"[•] Code encrypted and saved as {encrypted_file_name}", Colors.OKGREEN)
    else:
        print_colored("[•] File does not exist!", Colors.FAIL)

    input("[•] Press Enter to return to the main menu...")

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

def check_proxies_from_file(file):
    print_colored(f"[•] Checking proxies from file: {file}", Colors.OKCYAN)

def check_proxies_from_url(url):
    print_colored(f"[•] Checking proxies from URL: {url}", Colors.OKCYAN)

def generate_and_check_proxies():
    print_colored("[•] Generating and checking proxies...", Colors.OKCYAN)

def update_and_restart():
    try:
        print_colored("\n[•] Checking for updates...", Colors.OKBLUE)
        req = requests.get(GITHUB_RAW_URL)
        if req.status_code == 200:
            with open("main.py", "w") as f:
                f.write(req.text)
            print_colored("[•] Update downloaded. Restarting...", Colors.OKGREEN)
            os.execv("/data/data/com.termux/files/usr/bin/python", ['python', 'main.py'])
        else:
            print_colored("[•] No update found or failed to fetch.", Colors.WARNING)
    except Exception as e:
        print_colored(f"[•] Update check failed: {e}", Colors.FAIL)

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
        print_colored("[•] User-Agent Generator not implemented yet.", Colors.WARNING)
        input("[•] Press Enter to return to the main menu...")
    elif choice == "3":
        print_colored("[•] Send HTTP Request not implemented yet.", Colors.WARNING)
        input("[•] Press Enter to return to the main menu...")
    elif choice == "4":
        print_colored("[•] Look IP Info not implemented yet.", Colors.WARNING)
        input("[•] Press Enter to return to the main menu...")
    elif choice == "5":
        print_colored("[•] Facebook IDs Extractor not implemented yet.", Colors.WARNING)
        input("[•] Press Enter to return to the main menu...")
    elif choice == "6":
        print_colored("[•] Group Member ID Dumper not implemented yet.", Colors.WARNING)
        input("[•] Press Enter to return to the main menu...")
    elif choice == "7":
        encrypt_code()
    elif choice == "0":
        print_colored("[•] Exiting...", Colors.FAIL)
        exit()
    else:
        print_colored("[•] Invalid option! Returning to main menu...", Colors.FAIL)
        input("[•] Press Enter to return to the main menu...")

    update_and_restart()

# Run the main menu
if __name__ == "__main__":
    while True:
        main_menu()
