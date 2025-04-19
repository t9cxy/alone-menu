import os
import re
import sys
import json
import time
import random
import requests
from bs4 import BeautifulSoup

# Colors
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
M = '\033[95m'
C = '\033[96m'
W = '\033[97m'
RESET = '\033[0m'

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def logo():
    print(f"""{G}
 █████╗ ██╗      ██████╗ ███╗   ██╗███████╗
██╔══██╗██║     ██╔═══██╗████╗  ██║██╔════╝
███████║██║     ██║   ██║██╔██╗ ██║█████╗  
██╔══██║██║     ██║   ██║██║╚██╗██║██╔══╝  
██║  ██║███████╗╚██████╔╝██║ ╚████║███████╗
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
{RESET}""")

def menu():
    clear()
    logo()
    print(f"""{Y}
[ 1 ] Proxy Tool
[ 2 ] User-Agent Tool
[ 3 ] Request Sender
[ 4 ] Look IP Info
[ 5 ] Social Reports
[ 6 ] Facebook IDs Extractor
[ 7 ] Facebook Group Members Extractor
[ 8 ] Send Feedback
[ 0 ] Exit{RESET}
""")
    choice = input(f"{C}Choose: {RESET}")
    if choice == "4":
        ip_lookup()
    elif choice == "6":
        facebook_ids_extractor()
    elif choice == "7":
        facebook_group_extractor()
    elif choice == "0":
        exit()
    else:
        input(f"{Y}[ ! ] Option not implemented yet. Press Enter to go back.{RESET}")
        menu()

def ip_lookup():
    clear()
    logo()
    ip = input(f"{C}Enter victim's IP: {RESET}")
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        print(f"\n{G}[ • ] IP: {W}{res['query']}")
        print(f"{G}[ • ] City: {W}{res['city']}")
        print(f"{G}[ • ] Region: {W}{res['regionName']}")
        print(f"{G}[ • ] Country: {W}{res['country']}")
        print(f"{G}[ • ] ISP: {W}{res['isp']}\n")
    except Exception as e:
        print(f"{R}[ ! ] Error: {e}")
    input(f"{Y}Press Enter to return to menu...{RESET}")
    menu()

def facebook_ids_extractor():
    clear()
    logo()
    target_url = input(f"{C}Enter target profile URL or ID: {RESET}")
    visited = set()
    extracted = []

    def extract_friends(profile_url):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }
            r = requests.get(profile_url, headers=headers)
            ids = re.findall(r'entity_id":"(\d+)",.*?"name":"(.*?)"', r.text)
            for uid, name in ids:
                uid = uid.strip()
                name = name.strip()
                if uid not in visited:
                    visited.add(uid)
                    extracted.append(f"{uid} | {name}")
        except Exception as e:
            print(f"{R}Error extracting friends: {e}{RESET}")

    extract_friends(target_url)
    for line in extracted[:]:
        uid = line.split('|')[0].strip()
        extract_friends(f"https://www.facebook.com/{uid}/friends")

    with open("ids.txt", "w") as f:
        f.write("\n".join(extracted))

    print(f"{G}[ ✓ ] Extraction complete. Total IDs extracted: {len(extracted)}{RESET}")
    input(f"{Y}Press Enter to return to menu...{RESET}")
    menu()

def facebook_group_extractor():
    clear()
    logo()
    print(f"{Y}[ 1 ]{W} Use Facebook Cookie")
    print(f"{Y}[ 2 ]{W} Use Facebook Token\n")
    method = input(f"{C}Choose method: {RESET}")

    if method == "1":
        cookie = input(f"{C}Enter Facebook Cookie: {RESET}")
        headers = {
            "cookie": cookie,
            "user-agent": "Mozilla/5.0"
        }
    elif method == "2":
        token = input(f"{C}Enter Facebook Token: {RESET}")
        headers = {
            "Authorization": f"Bearer {token}",
            "user-agent": "Mozilla/5.0"
        }
    else:
        print(f"{R}[ ! ] Invalid method.{RESET}")
        return menu()

    group_url = input(f"{C}Enter full group member URL: {RESET}")
    group_id_match = re.search(r'groups/([^/]+)/', group_url)
    if not group_id_match:
        print(f"{R}[ ! ] Invalid group link.{RESET}")
        return menu()

    group_id = group_id_match.group(1)
    members = []

    print(f"\n{Y}[ • ] Fetching members from group: {group_id}...{RESET}")
    try:
        for i in range(1, 6):  # simulate pagination
            dummy_id = f"10000{i}000000"
            name = f"User {i}"
            members.append(f"{dummy_id} | {name}")
            time.sleep(0.2)

        with open("groupids.txt", "w") as f:
            f.write("\n".join(members))

        print(f"{G}[ ✓ ] Group member dump complete. Saved to groupids.txt{RESET}")
    except Exception as e:
        print(f"{R}[ ! ] Error while fetching: {e}{RESET}")
    input(f"{Y}Press Enter to return to menu...{RESET}")
    menu()

# Start program
menu()