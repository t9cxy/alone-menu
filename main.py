import os
import time
import json
import random
import requests
import subprocess
from datetime import datetime
from urllib.parse import quote

# Telegram Info (Do NOT remove)
BOT_TOKEN = "6770850573:AAFUCCzKlKrekJU5GtNFqdnqwMSAsnTBIc0"
CHAT_ID = "1241769879"

# Color Codes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    OKYELLOW = '\033[93m'
    OKRED = '\033[91m'   # <-- Added this to fix the crash
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear():
    os.system("clear")

def print_colored(text, color):
    print(color + text + Colors.ENDC)

def send_telegram_log(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={quote(msg)}"
    try:
        requests.get(url)
    except:
        pass

def log_and_notify(action):
    t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log = f"[•] {action} | {t}"
    send_telegram_log(log)
    print_colored(log, Colors.OKCYAN)

# Encrypt Code Option
def encrypt_code():
    clear()
    print_colored("[•] Welcome to the Code Encryptor!", Colors.OKCYAN)
    filename = input("[•] File Name: ")
    if not os.path.isfile(filename):
        print_colored("[•] File does not exist!", Colors.OKRED)
        input("[•] Press Enter to return...")
        return
    with open(filename, 'r') as f:
        code = f.read()
    encrypted = ''.join(chr(ord(c)+5) for c in code)
    output = f"encrypted_{filename}"
    with open(output, 'w') as f:
        f.write(encrypted)
    log_and_notify(f"Encrypted {filename} -> {output}")
    print_colored(f"[•] Encrypted and saved as {output}", Colors.OKGREEN)
    input("[•] Press Enter to return...")

# Rerun github.py (Auto Update)
def rerun_github():
    clear()
    print_colored("[•] Fetching and Running Latest Tool (github.py)...", Colors.OKCYAN)
    try:
        subprocess.run(["python3", "github.py"], check=True)
    except Exception as e:
        print_colored(f"[•] Failed to run github.py: {e}", Colors.OKRED)
    input("[•] Press Enter to return...")

# Placeholder Features
def proxy_options():
    clear()
    print_colored("[•] Proxy Options (To be implemented)", Colors.OKBLUE)
    input("[•] Press Enter to return...")

def user_agent_generator():
    clear()
    print_colored("[•] User-Agent Generator (To be implemented)", Colors.OKBLUE)
    input("[•] Press Enter to return...")

def send_http_request():
    clear()
    print_colored("[•] Send HTTP Request (To be implemented)", Colors.OKBLUE)
    input("[•] Press Enter to return...")

def look_ip_info():
    clear()
    print_colored("[•] Look IP Info (To be implemented)", Colors.OKBLUE)
    input("[•] Press Enter to return...")

def facebook_ids_extractor():
    clear()
    print_colored("[•] Facebook IDs Extractor (To be implemented)", Colors.OKBLUE)
    input("[•] Press Enter to return...")

def group_member_id_dumper():
    clear()
    print_colored("[•] Group Member ID Dumper (To be implemented)", Colors.OKBLUE)
    input("[•] Press Enter to return...")

# Main Menu
def main_menu():
    while True:
        clear()
        print_colored(" █████╗ ██╗      ██████╗ ███╗   ██╗███████╗", Colors.OKCYAN)
        print_colored("██╔══██╗██║     ██╔═══██╗████╗  ██║██╔════╝", Colors.OKCYAN)
        print_colored("███████║██║     ██║   ██║██╔██╗ ██║███████╗", Colors.OKCYAN)
        print_colored("██╔══██║██║     ██║   ██║██║╚██╗██║╚════██║", Colors.OKCYAN)
        print_colored("██║  ██║███████╗╚██████╔╝██║ ╚████║███████║", Colors.OKCYAN)
        print_colored("╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝", Colors.OKCYAN)
        print_colored("              A L O N E  T O O L", Colors.BOLD)

        print()
        print_colored("[1] Proxy Options", Colors.OKBLUE)
        print_colored("[2] User-Agent Generator", Colors.OKBLUE)
        print_colored("[3] Send HTTP Request", Colors.OKBLUE)
        print_colored("[4] Look IP Info", Colors.OKBLUE)
        print_colored("[5] Facebook IDs Extractor", Colors.OKBLUE)
        print_colored("[6] Group Member ID Dumper", Colors.OKBLUE)
        print_colored("[7] Encrypt Code", Colors.OKBLUE)
        print_colored("[8] Rerun Tool (Auto-Update)", Colors.OKGREEN)
        print_colored("[0] Exit", Colors.OKRED)

        choice = input("\n[?] Choose an option: ")

        if choice == "1": proxy_options()
        elif choice == "2": user_agent_generator()
        elif choice == "3": send_http_request()
        elif choice == "4": look_ip_info()
        elif choice == "5": facebook_ids_extractor()
        elif choice == "6": group_member_id_dumper()
        elif choice == "7": encrypt_code()
        elif choice == "8": rerun_github()
        elif choice == "0":
            print_colored("[•] Goodbye!", Colors.OKRED)
            break
        else:
            print_colored("[•] Invalid choice!", Colors.OKRED)
            input("[•] Press Enter to return...")

if __name__ == "__main__":
    main_menu()