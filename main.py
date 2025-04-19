import requests import random import os import json import re from datetime import datetime from colorama import Fore, Style, init from urllib.parse import urlparse

init(autoreset=True)

BOT_TOKEN = '6770850573:AAFUCCzKlKrekJU5GtNFqdnqwMSAsnTBIc0' CHAT_ID = '1241769879'

HEADER = f""" █████╗ ██╗      ██████╗ ███╗   ██╗███████╗ ██╔══██╗██║     ██╔═══██╗████╗  ██║██╔════╝ ███████║██║     ██║   ██║██╔██╗ ██║█████╗
██╔══██║██║     ██║   ██║██║╚██╗██║██╔══╝
██║  ██║███████╗╚██████╔╝██║ ╚████║███████╗ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝

[ • ] Telegram: @i4mAlone [ • ] Date: {datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')} """

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def send_log(msg): try: requests.post( f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': msg} ) except: pass

def get_random_proxy(): sources = [ "https://www.proxy-list.download/api/v1/get?type=https", "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=1000&country=all", "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt", "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt" ] proxies = [] for src in sources: try: r = requests.get(src, timeout=5) if r.status_code == 200: proxies += r.text.strip().split('\n') except: pass return list(set(proxies))

def get_random_useragent(): return random.choice([ "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...", "Mozilla/5.0 (Linux; Android 10)..." ])

def facebook_ids_extractor(): clear() print(Fore.MAGENTA + HEADER) target = input(Fore.YELLOW + "Enter Facebook profile URL or ID: ") ids = set() extracted = 0

def extract_friends(user_id):
    nonlocal extracted
    url = f"https://www.facebook.com/{user_id}/friends"
    try:
        response = requests.get(url, timeout=5)
        friends = re.findall(r'profile_id=(\d+)', response.text)
        for friend_id in friends:
            if friend_id not in ids:
                ids.add(friend_id)
                extracted += 1
                with open('ids.txt', 'a') as f:
                    f.write(f"{friend_id} | {friend_id}\n")
            if extracted % 50 == 0:
                print(f"[ {extracted} ] IDs extracted so far...")
    except Exception as e:
        print(f"Error extracting friends: {e}")

extract_friends(target)
for uid in list(ids):
    extract_friends(uid)

print(Fore.GREEN + f"Extraction complete. Total IDs extracted: {len(ids)}")
input(Fore.YELLOW + "Press Enter to go back...")

def main_menu(): while True: clear() print(Fore.MAGENTA + HEADER) print(Fore.CYAN + "[ 1 ] Generate Proxies") print(Fore.CYAN + "[ 2 ] Generate User-Agents") print(Fore.CYAN + "[ 3 ] Send Requests to URL") print(Fore.CYAN + "[ 4 ] Look IP Info") print(Fore.CYAN + "[ 5 ] Facebook IDs Extractor") print(Fore.CYAN + "[ 6 ] Send Feedback") print(Fore.CYAN + "[ 0 ] Exit\n") choice = input(Fore.YELLOW + "Select option: ") if choice == '1': pass  # Add proxy generation logic here elif choice == '2': pass  # Add user-agent generation logic here elif choice == '3': pass  # Add request sending logic here elif choice == '4': pass  # Add IP lookup logic here elif choice == '5': facebook_ids_extractor() elif choice == '6': pass  # Add feedback logic here elif choice == '0': break else: print(Fore.RED + "Invalid option!") input("Press Enter...")

if name == "main": main_menu()

