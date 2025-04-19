import os
import re
import requests
import random
import json
import time
from datetime import datetime
from urllib.parse import quote, urlparse
from bs4 import BeautifulSoup

# Telegram log info
BOT_TOKEN = "6770850573:AAFUCCzKlKrekJU5GtNFqdnqwMSAsnTBIc0"
CHAT_ID = "1241769879"

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
    OKRED = '\033[91m'
    OKYELLOW = '\033[93m'
    OKWHITE = '\033[97m'

def print_colored(text, color):
    print(f"{color}{text}{Colors.ENDC}")

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def send_telegram_log(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": message}
        requests.post(url, data=data)
    except Exception:
        pass

def auto_update():
    url = "https://raw.githubusercontent.com/t9cxy/alone-menu/main/main.py"
    try:
        r = requests.get(url)
        if r.status_code == 200:
            with open("main.py", "w") as f:
                f.write(r.text)
            print_colored("[•] Updated successfully. Running main.py...", Colors.OKGREEN)
            os.system("python main.py")
            exit()
        else:
            print_colored("[!] Failed to update from GitHub.", Colors.FAIL)
    except Exception as e:
        print_colored(f"[!] Update Error: {e}", Colors.FAIL)

def show_logo():
    clear_screen()
    print_colored(r"""
     █████╗ ██╗      ██████╗  ██████╗ ███╗   ██╗███████╗
    ██╔══██╗██║     ██╔═══██╗██╔════╝ ████╗  ██║██╔════╝
    ███████║██║     ██║   ██║██║  ███╗██╔██╗ ██║█████╗  
    ██╔══██║██║     ██║   ██║██║   ██║██║╚██╗██║██╔══╝  
    ██║  ██║███████╗╚██████╔╝╚██████╔╝██║ ╚████║███████╗
    ╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝
    """, Colors.OKCYAN)

def fetch_proxies():
    try:
        url = "https://api.proxyscrape.com/?request=getproxies&proxytype=http"
        proxies = requests.get(url).text.strip().split('\n')
        with open("proxy.txt", "w") as f:
            for proxy in proxies:
                f.write(proxy.strip() + "\n")
        print_colored(f"[•] {len(proxies)} proxies saved to proxy.txt", Colors.OKGREEN)
    except:
        print_colored("[!] Failed to fetch proxies", Colors.FAIL)

def generate_user_agents():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
        "Mozilla/5.0 (Linux; Android 10)...",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
    ]
    with open("ug.txt", "w") as f:
        for i in range(50):
            agent = random.choice(agents)
            f.write(agent + "\n")
    print_colored("[•] User-Agents written to ug.txt", Colors.OKGREEN)

def send_request():
    url = input("[•] Enter URL to request: ")
    try:
        r = requests.get(url)
        print_colored(f"[•] Status Code: {r.status_code}", Colors.OKCYAN)
        print_colored(f"[•] Response: {r.text[:200]}...", Colors.OKWHITE)
    except:
        print_colored("[!] Request failed", Colors.FAIL)

def ip_lookup():
    ip = input("[•] Enter IP to look up: ")
    try:
        info = requests.get(f"http://ip-api.com/json/{ip}").json()
        for k, v in info.items():
            print_colored(f"[{k}] {v}", Colors.OKYELLOW)
    except:
        print_colored("[!] Failed to fetch IP info", Colors.FAIL)

def extract_facebook_ids():
    target = input("[•] Enter Facebook profile URL or ID: ")
    print_colored("[!] This is a simulated extractor. Replace logic with real scraping.", Colors.WARNING)
    with open("ids.txt", "w") as f:
        for i in range(10):
            f.write(f"{1000000000+i} | Friend {i+1}\n")
    print_colored("[•] Saved to ids.txt", Colors.OKGREEN)

def group_member_dumper():
    group_url = input("[•] Enter Facebook Group URL: ")
    cookie = input("[•] Paste your Facebook cookie: ")
    print_colored("[!] Simulating group member dump...", Colors.WARNING)
    with open("groupids.txt", "w") as f:
        for i in range(10):
            f.write(f"{1000000000+i} | Member {i+1}\n")
    print_colored("[•] Group IDs saved to groupids.txt", Colors.OKGREEN)

def encrypt_code():
    filename = input("[•] Enter filename to encrypt: ")
    if not os.path.isfile(filename):
        print_colored("[!] File does not exist!", Colors.FAIL)
        input("[•] Press Enter to return...")
        return
    with open(filename, "r") as f:
        content = f.read()
    encrypted = ''.join(reversed(content))
    with open(f"{filename}.enc", "w") as f:
        f.write(encrypted)
    print_colored(f"[•] Encrypted version saved as {filename}.enc", Colors.OKGREEN)

def main_menu():
    while True:
        auto_update()
        show_logo()
        print_colored("[1] Proxy Options", Colors.OKCYAN)
        print_colored("[2] User-Agent Generator", Colors.OKCYAN)
        print_colored("[3] Send HTTP Request", Colors.OKCYAN)
        print_colored("[4] Look IP Info", Colors.OKCYAN)
        print_colored("[5] Facebook IDs Extractor", Colors.OKCYAN)
        print_colored("[6] Group Member ID Dumper", Colors.OKCYAN)
        print_colored("[7] Encrypt Code", Colors.OKCYAN)
        print_colored("[0] Exit", Colors.OKRED)
        choice = input("[?] Choose an option: ")
        if choice == '1':
            fetch_proxies()
        elif choice == '2':
            generate_user_agents()
        elif choice == '3':
            send_request()
        elif choice == '4':
            ip_lookup()
        elif choice == '5':
            extract_facebook_ids()
        elif choice == '6':
            group_member_dumper()
        elif choice == '7':
            encrypt_code()
        elif choice == '0':
            break
        else:
            print_colored("[!] Invalid option", Colors.FAIL)
        input("\n[•] Press Enter to return...")

if __name__ == "__main__":
    main_menu()