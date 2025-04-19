import os import requests import json import re import time from bs4 import BeautifulSoup from colorama import Fore, Style, init

init(autoreset=True)

Colors

R = Fore.RED G = Fore.GREEN Y = Fore.YELLOW B = Fore.BLUE C = Fore.CYAN M = Fore.MAGENTA W = Fore.WHITE

ASCII Logo

logo = f""" {R} ██████▆ ██▄      ██████▀ ███▉   ██▄█████▃ {R}██▄▄██▄██▄     ██▄▄▄▄▀ ████▂  ██▄██▄▄▄▄▀ {R}███████▄██▄     ██▄   ██▄██▄██▂▄ ██▄████▀ {R}██▄▄██▄██▄     ██▄   ██▄██▄▀██▄██▄▄▀ {R}██▄  ██▄█████▆▃██▄████▀ ██▄ ████▄█████▃ {R}▄▀  ▄▀▄▀▀▀▀▀▀▀▀ ▄▀  ▄▀▄▀▀▀▀▀▀ """

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def menu(): clear() print(logo) print(f"{Y}[ 1 ]{W} Proxy Tools") print(f"{Y}[ 2 ]{W} User-Agent Generator") print(f"{Y}[ 3 ]{W} Send HTTP Request") print(f"{Y}[ 4 ]{W} Look IP Info") print(f"{Y}[ 5 ]{W} Facebook IDs Extractor") print(f"{Y}[ 6 ]{W} Send Feedback") print(f"{Y}[ 0 ]{R}Exit") choice = input(f"\n{B}Choose: {W}") if choice == '4': victim_ip_info() elif choice == '5': facebook_ids_extractor() elif choice == '0': exit() else: input(f"{R}[ ! ] Not Implemented Yet. Press Enter to return.") menu()

def victim_ip_info(): clear() print(logo) ip = input(f"{C}[ ? ] Enter target IP: {W}") try: res = requests.get(f"http://ip-api.com/json/{ip}") data = res.json() print(f"\n{G}IP Info:") for key, value in data.items(): print(f"{B}{key.capitalize()}:{W} {value}") except Exception as e: print(f"{R}[ ! ] Error: {e}") input(f"\n{Y}[ * ] Press Enter to return to menu...") menu()

def facebook_ids_extractor(): clear() print(logo) target = input(f"{C}[ ? ] Enter target profile link or ID: {W}") visited = set() result = set()

def extract_ids(profile):
    if profile in visited:
        return
    visited.add(profile)
    try:
        url = f"https://mbasic.facebook.com/{profile}" if not profile.startswith('http') else profile
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        links = soup.find_all('a', href=True)
        for a in links:
            if '/friends' in a['href']:
                friends_url = 'https://mbasic.facebook.com' + a['href']
                rf = requests.get(friends_url, headers=headers)
                sf = BeautifulSoup(rf.text, 'html.parser')
                friend_links = sf.find_all('a', href=True)
                for link in friend_links:
                    if 'fref' in link['href'] or '/profile.php?' in link['href']:
                        name = link.text.strip()
                        href = link['href']
                        uid_match = re.search(r'id=(\d+)', href)
                        if uid_match:
                            uid = uid_match.group(1)
                            result.add(f"{uid} | {name}")
                            extract_ids(uid)
    except Exception as e:
        print(f"{R}[ ! ] Error while extracting: {e}")

extract_ids(target)
with open("ids.txt", "w", encoding="utf-8") as f:
    for line in result:
        f.write(line + "\n")

print(f"\n{G}[ + ] Extraction complete. Saved to ids.txt")
input(f"{Y}[ * ] Press Enter to return to menu...")
menu()

if name == 'main': menu()

