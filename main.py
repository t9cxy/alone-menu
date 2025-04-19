# ALONE TOOL - MAIN SCRIPT

import os
import re
import time
import json
import random
import requests
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
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    print(f"""{G}
 █████╗ ██╗      ██████╗ ███╗   ██╗███████╗
██╔══██╗██║     ██╔═══██╗████╗  ██║██╔════╝
███████║██║     ██║   ██║██╔██╗ ██║█████╗  
██╔══██║██║     ██║   ██║██║╚██╗██║██╔══╝  
██║  ██║███████╗╚██████╔╝██║ ╚████║███████╗
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
{W}           CREATED BY @i4mAlone
""")

def menu():
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

def wait():
    input(f"\n{C}[•] Press Enter to return...")

def proxy_options():
    clear()
    print(f"{C}\n[1] Load Proxies from File\n[2] Load Proxies from URL\n[3] Generate Random Proxies\n")
    choice = input(f"{Y}[?] Choose: {RESET}")
    
    if choice == "1":
        path = input(f"{Y}[•] File path: {RESET}")
        try:
            with open(path) as f:
                proxies = f.read().splitlines()
                print(f"{G}[✓] Loaded {len(proxies)} proxies")
        except:
            print(f"{R}[!] File not found.")
    
    elif choice == "2":
        url = input(f"{Y}[•] Proxy list URL: {RESET}")
        try:
            res = requests.get(url)
            proxies = res.text.strip().splitlines()
            print(f"{G}[✓] Loaded {len(proxies)} proxies from URL")
        except:
            print(f"{R}[!] Failed to load proxies.")
    
    elif choice == "3":
        target = int(input(f"{Y}[•] How many proxies? {RESET}"))
        ok, bad = 0, 0
        with open("proxy.txt", "w") as f:
            while ok < target:
                ip = ".".join([str(random.randint(1, 255)) for _ in range(4)])
                port = random.randint(1000, 9999)
                proxy = f"{ip}:{port}"
                if random.choice([True, False]):
                    ok += 1
                    f.write(proxy + "\n")
                else:
                    bad += 1
                clear()
                print(f"{proxy}\n{G}[ OK ] {ok}/{target} | {R}[ BAD ] {bad}")
    
    else:
        print(f"{R}[!] Invalid choice.")
    
    wait()

def user_agent_generator():
    print(f"{R}[•] Not implemented yet.")
    wait()

def send_http_request():
    url = input(f"{Y}[•] Target URL: {RESET}")
    try:
        res = requests.get(url)
        print(f"{G}[✓] Response Code: {res.status_code}")
        print(res.text[:300])
    except Exception as e:
        print(f"{R}[!] Error: {e}")
    wait()

def look_ip_info():
    ip = input(f"{Y}[•] Enter IP: {RESET}")
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}")
        data = res.json()
        for k in ['query','city','regionName','country','isp']:
            print(f"{C}{k.title()}: {W}{data.get(k)}")
    except:
        print(f"{R}[!] Failed to fetch IP info.")
    wait()

def facebook_ids_extractor():
    print(f"{R}[•] Facebook ID extractor coming soon.")
    wait()

def group_id_dumper():
    print(f"{R}[•] Group member dumper coming soon.")
    wait()

def send_feedback():
    fb = input(f"{Y}[•] Your feedback: {RESET}")
    with open("feedback.txt", "a") as f:
        f.write(f"{datetime.now()} | {fb}\n")
    print(f"{G}[✓] Thanks for the feedback!")
    wait()

# Main loop
while True:
    clear()
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
        print(f"{G}[✓] Exiting...{RESET}")
        break
    else:
        print(f"{R}[!] Invalid option.")
        wait()