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
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
C = '\033[96m'
W = '\033[97m'
RESET = '\033[0m'

# Logo
logo = f"""{G}
 █████╗ ██╗      ██████╗ ███╗   ██╗███████╗
██╔══██╗██║     ██╔═══██╗████╗  ██║██╔════╝
███████║██║     ██║   ██║██╔██╗ ██║█████╗  
██╔══██║██║     ██║   ██║██║╚██╗██║██╔══╝  
██║  ██║███████╗╚██████╔╝██║ ╚████║███████╗
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
{RESET}"""

# Clear screen
def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

# Main menu
def main_menu():
    clear()
    print(logo)
    print(f"""{B}
[1] Proxy Options
[2] User-Agent Generator
[3] Send HTTP Request
[4] Look IP Info
[5] Facebook IDs Extractor
[6] Group Member ID Dumper
[7] Send Feedback
[0] Exit{RESET}
""")
    choice = input(f"{Y}[?] Choose an option: {RESET}")
    if choice == "1":
        proxy_options()
    elif choice == "2":
        user_agent_generator()
    elif choice == "3":
        send_http_request()
    elif choice == "4":
        ip_lookup()
    elif choice == "5":
        facebook_id_extractor()
    elif choice == "6":
        group_member_dumper()
    elif choice == "7":
        send_feedback()
    elif choice == "0":
        exit()
    else:
        print(f"{R}[!] Invalid option!{RESET}")
        time.sleep(1)
        main_menu()

# Proxy Options
def proxy_options():
    clear()
    print(logo)
    print(f"{Y}[•] Proxy Options{RESET}")
    print(f"{B}[1] Check Proxy By File{RESET}")
    print(f"{B}[2] Check From URL (GitHub, PasteBin, etc.){RESET}")
    print(f"{B}[3] Generate and Check Proxy{RESET}")
    choice = input(f"{Y}[?] Choose an option: {RESET}")
    if choice == "1":
        check_proxy_by_file()
    elif choice == "2":
        check_proxy_from_url()
    elif choice == "3":
        generate_and_check_proxy()
    else:
        print(f"{R}[!] Invalid option!{RESET}")
        time.sleep(1)
        proxy_options()

# Option 4: Look IP Info
def ip_lookup():
    clear()
    print(logo)
    print(f"{Y}[•] IP Lookup Tool{RESET}\n")
    ip = input(f"{C}Enter IP to lookup: {RESET}")
    if not ip:
        input(f"{Y}[!] No IP entered. Press Enter to return...{RESET}")
        main_menu()
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}").json()
        print(f"\n{G}[•] IP Info for: {ip}{RESET}")
        print(f"{W}Country: {C}{response['country']}")
        print(f"{W}Region: {C}{response['regionName']}")
        print(f"{W}City: {C}{response['city']}")
        print(f"{W}ZIP: {C}{response['zip']}")
        print(f"{W}ISP: {C}{response['isp']}")
        print(f"{W}Org: {C}{response['org']}")
        print(f"{W}AS: {C}{response['as']}")
        print(f"{W}Lat/Lon: {C}{response['lat']}, {response['lon']}{RESET}")
    except Exception as e:
        print(f"{R}[!] Failed to fetch IP info: {e}{RESET}")
    input(f"\n{Y}[•] Press Enter to return...{RESET}")
    main_menu()

# Option 5: Facebook ID Extractor
def facebook_id_extractor():
    clear()
    print(logo)
    print(f"{Y}[•] Facebook ID Extractor{RESET}\n")
    target = input(f"{C}Enter Facebook profile URL or ID: {RESET}")
    if not target:
        input(f"{Y}[!] No target entered. Press Enter to return...{RESET}")
        main_menu()
    try:
        extracted = set()
        def extract_friends(user_id):
            url = f"https://mbasic.facebook.com/profile.php?id={user_id}&v=friends"
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(url, headers=headers)
            matches = re.findall(r'href="/profile.php\?id=(\d+)[^"]+">([^<]+)</a>', res.text)
            for uid, name in matches:
                entry = f"{uid} | {name}"
                if entry not in extracted:
                    extracted.add(entry)
                    print(f"{G}[+] {entry}{RESET}")
                    with open("ids.txt", "a") as f:
                        f.write(entry + "\n")
                    extract_friends(uid)

        extract_friends(target)
    except Exception as e:
        print(f"{R}[!] Error extracting friends: {e}{RESET}")
    input(f"\n{Y}[•] Press Enter to return...{RESET}")
    main_menu()

# Option 6: Group Member Dumper
def group_member_dumper():
    clear()
    print(logo)
    print(f"{Y}[•] Facebook Group Member Dumper{RESET}\n")
    method = input(f"{C}[1] Use Cookie\n[2] Use Token\nChoose method: {RESET}")
    auth = input(f"{C}Enter Cookie or Token: {RESET}")
    group_url = input(f"{C}Enter Facebook Group URL: {RESET}")
    if not auth or not group_url:
        input(f"{Y}[!] Missing inputs. Press Enter to return...{RESET}")
        main_menu()

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": auth if method == "1" else ""
    }

    try:
        if method == "1":
            res = requests.get(group_url, headers=headers)
            members = re.findall(r'data-ntid="(\d+)"', res.text)
        else:
            group_id = re.findall(r'groups/(\d+)', group_url)
            if group_id:
                api_url = f"https://graph.facebook.com/{group_id[0]}/members?access_token={auth}"
                res = requests.get(api_url).json()
                members = [f"{m['id']} | {m['name']}" for m in res.get("data", [])]
            else:
                members = []

        with open("groupids.txt", "w") as f:
            for m in members:
                line = f"{m if isinstance(m, str) else f'{m} | Unknown'}"
                f.write(line + "\n")
                print(f"{G}[+] {line}{RESET}")

    except Exception as e:
        print(f"{R}[!] Error dumping members: {e}{RESET}")

    input(f"\n{Y}[•] Press Enter to return...{RESET}")
    main_menu()

# Placeholder functions
def proxy_options():
    print(f"{Y}[•] Proxy options not implemented here.{RESET}")
    input(f"\n{Y}[•] Press Enter to return...{RESET}")
    main_menu()

def user_agent_generator():
    print(f"{Y}[•] User-Agent Generator not implemented here.{RESET}")
    input(f"\n{Y}[•] Press Enter to return...{RESET}")
    main_menu()

def send_http_request():
    print(f"{Y}[•] Send HTTP Request option not implemented here.{RESET}")
    input(f"\n{Y}[•] Press Enter to return...{RESET}")
    main_menu()

def send_feedback():
    print(f"{Y}[•] Send Feedback option not implemented here.{RESET}")
    input(f"\n{Y}[•] Press Enter to return...{RESET}")
    main_menu()

def main():
    main_menu()

if __name__ == "__main__":
    main()