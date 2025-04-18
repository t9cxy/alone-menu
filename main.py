import requests
import random
import os
import re
import json
from datetime import datetime
from colorama import Fore, Style, init
from urllib.parse import urlparse

init(autoreset=True)

BOT_TOKEN = '6770850573:AAFUCCzKlKrekJU5GtNFqdnqwMSAsnTBIc0'
CHAT_ID   = '1241769879'

HEADER = f"""
  █████╗ ██╗      ██████╗ ███╗   ██╗███████╗
██╔══██╗██║     ██╔═══██╗████╗  ██║██╔════╝
███████║██║     ██║   ██║██╔██╗ ██║█████╗  
██╔══██║██║     ██║   ██║██║╚██╗██║██╔══╝  
██║  ██║███████╗╚██████╔╝██║ ╚████║███████╗
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
                                           
[ • ] Telegram: @i4mAlone
[ • ] Date: {datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}
"""

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def send_log(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={'chat_id': CHAT_ID, 'text': msg}
        )
    except:
        pass

def check_telegram_username(username):
    u = username.lstrip('@')
    try:
        r = requests.get(f"https://t.me/{u}", timeout=5)
        return r.status_code == 200 and 'tgme_page_title' in r.text
    except:
        return False

def get_random_proxy():
    sources = [
        "https://www.proxy-list.download/api/v1/get?type=https",
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=1000&country=all",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt"
    ]
    proxies = []
    for src in sources:
        try:
            r = requests.get(src, timeout=5)
            if r.status_code == 200:
                proxies += r.text.strip().split('\n')
        except:
            pass
    return list(set(proxies))

def get_random_useragent():
    return random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
        "Mozilla/5.0 (Linux; Android 10)..."
    ])

def check_proxy_by_file():
    clear()
    print(Fore.MAGENTA + HEADER)
    file_path = input(Fore.YELLOW + "Enter file path containing proxies: ")
    try:
        with open(file_path, 'r') as f:
            proxies = f.readlines()
        valid_proxies = []
        for proxy in proxies:
            proxy = proxy.strip()
            try:
                r = requests.get('https://httpbin.org/ip', proxies={'http': f'http://{proxy}', 'https': f'http://{proxy}'}, timeout=5)
                if r.status_code == 200:
                    valid_proxies.append(proxy)
                    print(Fore.GREEN + f"Valid Proxy: {proxy}")
                else:
                    print(Fore.RED + f"Invalid Proxy: {proxy}")
            except:
                print(Fore.RED + f"Invalid Proxy: {proxy}")
        print(Fore.CYAN + f"Valid proxies found: {len(valid_proxies)}")
    except FileNotFoundError:
        print(Fore.RED + "File not found.")

def check_proxy_from_url():
    clear()
    print(Fore.MAGENTA + HEADER)
    url = input(Fore.YELLOW + "Enter URL containing proxies (GitHub, PasteBin, etc.): ")
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            proxies = r.text.splitlines()
            valid_proxies = []
            for proxy in proxies:
                try:
                    r = requests.get('https://httpbin.org/ip', proxies={'http': f'http://{proxy}', 'https': f'http://{proxy}'}, timeout=5)
                    if r.status_code == 200:
                        valid_proxies.append(proxy)
                        print(Fore.GREEN + f"Valid Proxy: {proxy}")
                    else:
                        print(Fore.RED + f"Invalid Proxy: {proxy}")
                except:
                    print(Fore.RED + f"Invalid Proxy: {proxy}")
            print(Fore.CYAN + f"Valid proxies found: {len(valid_proxies)}")
        else:
            print(Fore.RED + "Failed to fetch proxies from URL.")
    except:
        print(Fore.RED + "Failed to fetch data from URL.")

def generate_and_check_proxies():
    clear()
    print(Fore.MAGENTA + HEADER)
    amt = int(input(Fore.YELLOW + "How many proxies do you want to generate and check? > "))
    ok = 0
    bad = 0
    while ok < amt:
        for px in get_random_proxy():
            try:
                r = requests.get('https://httpbin.org/ip', proxies={'http': f'http://{px}', 'https': f'http://{px}'}, timeout=5)
                if r.status_code == 200:
                    ok += 1
                    print(Fore.GREEN + f"Valid Proxy: {px}")
                else:
                    bad += 1
                    print(Fore.RED + f"Invalid Proxy: {px}")
            except:
                bad += 1
                print(Fore.RED + f"Invalid Proxy: {px}")
            if ok >= amt:
                break
    print(Fore.CYAN + f"Generation and checking complete: {ok} valid, {bad} invalid proxies.")

def proxy_options():
    clear()
    print(Fore.MAGENTA + HEADER)
    print(Fore.CYAN + "[1] Check Proxy By File")
    print(Fore.CYAN + "[2] Check From URL (GitHub, PasteBin, etc.)")
    print(Fore.CYAN + "[3] Generate and Check Proxy")
    print(Fore.CYAN + "[0] Back to Menu\n")
    choice = input(Fore.YELLOW + "Choose an option: ")
    if choice == '1':
        check_proxy_by_file()
    elif choice == '2':
        check_proxy_from_url()
    elif choice == '3':
        generate_and_check_proxies()
    elif choice == '0':
        return
    else:
        print(Fore.RED + "Invalid option. Try again.")

def main():
    clear(); print(Fore.MAGENTA + HEADER)
    global username
    username = input(Fore.YELLOW + "Telegram user (no @): ").strip()
    if not check_telegram_username(username):
        print(Fore.RED + "Invalid or not found."); return
    info = requests.get('https://ipinfo.io/json').json()
    ua = requests.get('https://httpbin.org/user-agent').json().get('user-agent')
    log = (f"~~~ NEW LOGS ~~~\n"
           f"[ # ] User: @{username}\n"
           f"[ IP ] {info.get('ip')}\n"
           f"[ Loc ] {info.get('city')}, {info.get('region')} ({info.get('country')})\n"
           f"[ ISP ] {info.get('org')}\n"
           f"[ UA ] {ua}\n"
           f"[ ⏰ ] {datetime.now():%Y-%m-%d %I:%M:%S %p}")
    send_log(log)
    print(Fore.GREEN + f"Welcome @{username}\n")
    while True:
        print(Fore.MAGENTA + "[1]" + Fore.CYAN + " Send Requests")
        print(Fore.MAGENTA + "[2]" + Fore.CYAN + " Generate Proxies")
        print(Fore.MAGENTA + "[3]" + Fore.CYAN + " Generate UAs")
        print(Fore.MAGENTA + "[4]" + Fore.CYAN + " Look IP Info")
        print(Fore.MAGENTA + "[5]" + Fore.CYAN + " Send Feedback")
        print(Fore.MAGENTA + "[6]" + Fore.CYAN + " Proxy Options")
        print(Fore.MAGENTA + "[0]" + Fore.CYAN + " Exit\n")
        ch = input(Fore.YELLOW + "Choose: ")
        if ch == '1': send_requests()
        elif ch == '2': generate_proxies()
        elif ch == '3': generate_useragents()
        elif ch == '4': look_ip_info()
        elif ch == '5': send_feedback()
        elif ch == '6': proxy_options()
        elif ch == '0': break
        else: print(Fore.RED + "Invalid, try again.")

if __name__ == "__main__":
    main()
