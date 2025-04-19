import os
import sys
import time
import requests
import json
from datetime import datetime

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_colored(text, color=Colors.ENDC):
    print(f"{color}{text}{Colors.ENDC}")

def print_logo():
    logo = f"""{Colors.OKCYAN}
     █████╗ ██╗      ██████╗ ███╗   ██╗███████╗
    ██╔══██╗██║     ██╔═══██╗████╗  ██║██╔════╝
    ███████║██║     ██║   ██║██╔██╗ ██║█████╗  
    ██╔══██║██║     ██║   ██║██║╚██╗██║██╔══╝  
    ██║  ██║███████╗╚██████╔╝██║ ╚████║███████╗
    ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
    {Colors.ENDC}"""
    print(logo)

def log_and_notify(msg):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print_colored(f"[•] {now} - {msg}", Colors.OKBLUE)

def proxy_options():
    print_colored("[•] Proxy options will be here.", Colors.OKGREEN)
    input("[•] Press Enter to return to the main menu...")

def user_agent_generator():
    print_colored("[•] User-Agent Generator coming soon.", Colors.OKGREEN)
    input("[•] Press Enter to return to the main menu...")

def send_http_request():
    print_colored("[•] Send HTTP Request placeholder.", Colors.OKGREEN)
    input("[•] Press Enter to return to the main menu...")

def look_ip_info():
    ip = input("[•] Enter victim's IP address: ").strip()
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data["status"] == "success":
            print_colored(json.dumps(data, indent=2), Colors.OKCYAN)
        else:
            print_colored("[•] Invalid IP or failed to fetch info.", Colors.FAIL)
    except Exception as e:
        print_colored(f"[•] Error: {e}", Colors.FAIL)
    input("[•] Press Enter to return to the main menu...")

def facebook_ids_extractor():
    print_colored("[•] Facebook ID Extractor (placeholder).", Colors.OKGREEN)
    input("[•] Press Enter to return to the main menu...")

def group_member_id_dumper():
    print_colored("[•] Group Member ID Dumper (placeholder).", Colors.OKGREEN)
    input("[•] Press Enter to return to the main menu...")

def encrypt_code():
    print_colored("[•] Welcome to the Code Encryptor!", Colors.OKCYAN)
    file_name = input("[•] File Name: ").strip()

    # Check for exact match or relative path
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, file_name)

    if os.path.isfile(file_name):  # if exact filename matches
        file_path = file_name
    elif not os.path.isfile(file_path):
        print_colored(f"[•] File '{file_name}' does not exist!", Colors.FAIL)
        input("[•] Press Enter to return to the main menu...")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()

        encrypted_code = "# Encrypted file\n" + "".join(reversed(code))
        encrypted_name = f"encrypted_{os.path.basename(file_path)}"

        with open(encrypted_name, "w", encoding='utf-8') as f:
            f.write(encrypted_code)

        log_and_notify(f"Encrypted: {file_name} -> {encrypted_name}")
        print_colored(f"[•] Encrypted successfully as '{encrypted_name}'", Colors.OKGREEN)
    except Exception as e:
        print_colored(f"[•] Error: {e}", Colors.FAIL)

    input("[•] Press Enter to return to the main menu...")

def main_menu():
    while True:
        clear()
        print_logo()
        print(f"""{Colors.BOLD}{Colors.OKCYAN}
[1] Proxy Options
[2] User-Agent Generator
[3] Send HTTP Request
[4] Look IP Info
[5] Facebook IDs Extractor
[6] Group Member ID Dumper
[7] Encrypt Code
[0] Exit{Colors.ENDC}""")
        choice = input("[?] Choose an option: ").strip()

        if choice == "1":
            proxy_options()
        elif choice == "2":
            user_agent_generator()
        elif choice == "3":
            send_http_request()
        elif choice == "4":
            look_ip_info()
        elif choice == "5":
            facebook_ids_extractor()
        elif choice == "6":
            group_member_id_dumper()
        elif choice == "7":
            encrypt_code()
        elif choice == "0":
            print_colored("[•] Goodbye!", Colors.WARNING)
            sys.exit()
        else:
            print_colored("[•] Invalid option. Try again.", Colors.FAIL)
            time.sleep(1)

        os.system("python github.py")  # check for update every cycle

if __name__ == "__main__":
    main_menu()
