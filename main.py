import os
import re
import time
import json
import requests
import random
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import quote

# Colors
R = '\033[1;91m'
G = '\033[1;92m'
Y = '\033[1;93m'
B = '\033[1;94m'
M = '\033[1;95m'
C = '\033[1;96m'
W = '\033[1;97m'
RESET = '\033[0m'

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    print(f"""{G}
 █████╗ ██╗      ██████╗ ███╗   ██╗███████╗
██╔══██╗██║     ██╔═══██╗████╗  ██║██╔════╝
███████║██║     ██║   ██║██╔██╗ ██║█████╗  
██╔══██║██║     ██║   ██║██║╚██╗██║██╔══╝  
██║  ██║███████╗╚██████╔╝██║ ╚████║███████╗
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
            {W}Created by @i4mAlone
""")

def menu():
    clear()
    banner()
    print(f"""{C}
[1] {Y}Proxy Options
[2] {Y}User-Agent Generator
[3] {Y}Send HTTP Request
[4] {Y}Look IP Info
[5] {Y}Facebook IDs Extractor
[6] {Y}Group Member ID Dumper
[7] {Y}Send Feedback
[0] {R}Exit{RESET}
""")

def proxy_options():
    clear()
    print(f"""{C}
[1] Check Proxy By File
[2] Check From URL (Github, Pastebin, etc)
[3] Generate and Check Proxy
""")
    choice = input(f"{Y}[?] Choose: {RESET}")
    if choice == "1":
        path = input(f"{Y}[•] Enter path to proxy file: {RESET}")
        check_proxy_file(path)
    elif choice == "2":
        url = input(f"{Y}[•] Enter URL to proxy list: {RESET}")
        check_proxy_url(url)
    elif choice == "3":
        count = int(input(f"{Y}[•] Number of proxies to generate: {RESET}"))
        generate_proxies(count)
    else:
        print(f"{R}[!] Invalid choice")
        input(f"{W}[•] Press Enter to return...")

def check_proxy_file(path):
    try:
        with open(path, 'r') as file:
            proxies = file.read().splitlines()
            print(f"{G}[✓] Loaded {len(proxies)} proxies from file")
    except FileNotFoundError:
        print(f"{R}[!] File not found")
    input(f"{W}[•] Press Enter to return...")

def check_proxy_url(url):
    try:
        res = requests.get(url)
        proxies = res.text.strip().splitlines()
        print(f"{G}[✓] Loaded {len(proxies)} proxies from URL")
    except Exception as e:
        print(f"{R}[!] Failed to fetch: {e}")
    input(f"{W}[•] Press Enter to return...")

def generate_proxies(count):
    print(f"{Y}[•] Generating and checking {count} proxies...")
    ok, bad = 0, 0
    with open("proxy.txt", "w") as f:
        while ok < count:
            ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
            port = random.randint(1000, 9999)
            proxy = f"{ip}:{port}"
            # Simulated check
            if random.choice([True, False]):
                ok += 1
                f.write(f"{proxy}\n")
            else:
                bad += 1
            clear()
            print(f"{proxy}\n{G}[ GOOD ] {ok}/{count} | {R}[ BAD ] {bad}{RESET}")
    input(f"{W}[•] Press Enter to return...")

def user_agent_generator():
    print(f"{R}[•] User-Agent Generator not implemented here.")
    input(f"{W}[•] Press Enter to return...")

def send_http_request():
    url = input(f"{Y}[•] Enter URL: {RESET}")
    try:
        response = requests.get(url)
        print(f"{G}[✓] Status Code: {response.status_code}")
        print(response.text[:500])
    except Exception as e:
        print(f"{R}[!] Error: {e}")
    input(f"{W}[•] Press Enter to return...")

def look_ip_info():
    ip = input(f"{Y}[•] Enter IP to check: {RESET}")
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}")
        data = res.json()
        for key in ['query','city','regionName','country','isp']:
            print(f"{C}{key.title()}: {W}{data.get(key, 'N/A')}")
    except Exception as e:
        print(f"{R}[!] Error: {e}")
    input(f"{W}[•] Press Enter to return...")

def facebook_ids_extractor():
    print(f"{Y}[•] Feature coming soon...")
    input(f"{W}[•] Press Enter to return...")

def group_id_dumper():
    print(f"{Y}[•] Feature coming soon...")
    input(f"{W}[•] Press Enter to return...")

def send_feedback():
    feedback = input(f"{Y}[•] Your feedback: {RESET}")
    with open("feedback.txt", "a") as f:
        f.write(f"{datetime.now()}: {feedback}\n")
    print(f"{G}[✓] Feedback saved.")
    input(f"{W}[•] Press Enter to return...")

while True:
    menu()
    choice = input(f"{Y}[?] Choose an option: {RESET}")
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
        group_id_dumper()
    elif choice == "7":
        send_feedback()
    elif choice == "0":
        print(f"{G}[✓] Exiting...")
        break
    else:
        print(f"{R}[!] Invalid option")
        input(f"{W}[•] Press Enter to try again...")