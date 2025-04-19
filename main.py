import requests
import random
import os
import json
from datetime import datetime
from colorama import Fore, Style, init
from urllib.parse import urlparse

# Initialize colorama
init(autoreset=True)

# Configuration
BOT_TOKEN = '6770850573:AAFUCCzKlKrekJU5GtNFqdnqwMSAsnTBIc0'
CHAT_ID = '1241769879'

# Header ASCII art
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

# Utility functions
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

# Feature: Generate and check proxies
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

# Feature: Generate user-agents
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

# Feature: Send requests to URL
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

# Feature: Look IP Info
def look_ip_info():
    clear()
    print(Fore.MAGENTA + HEADER)
    ip = input(Fore.YELLOW + "Enter IP to lookup: ")
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
    input(Fore.YELLOW + "Press Enter to go back...")

# Feature: Send feedback
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

# Feature: Facebook ID Extractor
def facebook_ids_extractor():
    clear()
    print(Fore.MAGENTA + HEADER)
    target = input(Fore.YELLOW + "Enter Facebook profile URL or ID: ")
    ids = set()
    extracted = 0

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
                if extracted % 50 == 0:  # Periodic extraction
                    print(f"[ {extracted} ] IDs extracted so far...")
        except Exception as e:
            print(f"Error extracting friends: {e}")

    extract_friends(target)
    print(f"Extraction complete. Total IDs extracted: {len(ids)}")
    input(Fore.YELLOW + "Press Enter to go back...")

# Menu loop
def menu():
    clear()
    print(Fore.MAGENTA + HEADER)
    print(Fore.YELLOW + "[1] Generate and Check Proxies")
    print(Fore.YELLOW + "[2] Generate User-Agents")
    print(Fore.YELLOW + "[3] Send Requests to URL")
    print(Fore.YELLOW + "[4] Look IP Info")
    print(Fore.YELLOW + "[5] Send Feedback")
    print(Fore.YELLOW + "[6] Facebook ID Extractor")
    print(Fore.YELLOW + "[7] Exit")
    choice = input(Fore.YELLOW + "Choose an option: ")

    if choice == '1':
        generate_proxies()
    elif choice == '2':
        generate_useragents()
    elif choice == '3':
        send_requests()
    elif choice == '4':
        look_ip_info()
    elif choice == '5':
        send_feedback()
    elif choice == '6':
        facebook_ids_extractor()
    elif choice == '7':
        exit()
    else:
        print(Fore.RED + "Invalid option, try again.")
        menu()

if __name__ == "__main__":
    menu()