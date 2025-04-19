import requests
import random
import os
import re
import json
from datetime import datetime
from colorama import Fore, Style, init
from urllib.parse import urlparse
from bs4 import BeautifulSoup

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

# ————————————————————————————
# Facebook IDs Extractor
def facebook_ids_extractor():
    clear()
    print(Fore.MAGENTA + HEADER)
    target = input(Fore.YELLOW + "Enter profile URL or ID: ").strip()
    # Extract username or id from URL
    if 'facebook.com/' in target:
        path = urlparse(target).path.strip('/')
        username = path.split('?')[0]
    else:
        username = target

    base = "https://mbasic.facebook.com/"
    visited = set()
    queue = [(username, 0)]
    results = []

    # Prepare output file
    with open('ids.txt', 'w') as f:
        f.write("id | name\n")

    while queue:
        user, depth = queue.pop(0)
        if user in visited or depth > 2:
            continue
        visited.add(user)

        friends_url = f"{base}{user}/friends"
        try:
            r = requests.get(friends_url, timeout=5)
            soup = BeautifulSoup(r.text, 'html.parser')
            # Find friend entries
            for a in soup.find_all('a', href=True):
                href = a['href'].split('?')[0]
                # Match /profile.php?id=123... or /username
                m_id = re.match(r'/profile\.php\?id=(\d+)', href)
                if m_id:
                    fid = m_id.group(1)
                else:
                    # assume href like /username
                    fid = href.strip('/')
                name = a.get_text()
                if fid and fid not in visited:
                    results.append((fid, name))
                    with open('ids.txt', 'a') as f:
                        f.write(f"{fid} | {name}\n")
                    if depth < 1:
                        queue.append((fid, depth+1))
        except:
            pass

    clear()
    print(Fore.GREEN + f"Extracted {len(results)} unique IDs to ids.txt\n")
    input(Fore.CYAN + "Press Enter to return to menu...")

# (Other features omitted for brevity: generate_useragents, send_requests, etc.)

def main():
    clear()
    print(Fore.MAGENTA + HEADER)
    global username
    username = input(Fore.YELLOW + "Telegram user (no @): ").strip()
    if not check_telegram_username(username):
        print(Fore.RED + "Invalid or not found.")
        return

    # initial log...
    send_log(f"User @{username} started at {datetime.now():%Y-%m-%d %I:%M:%S %p}")

    while True:
        print(Fore.MAGENTA + "[1]" + Fore.CYAN + " Send Requests")
        print(Fore.MAGENTA + "[2]" + Fore.CYAN + " Generate Proxies")
        print(Fore.MAGENTA + "[3]" + Fore.CYAN + " Generate UAs")
        print(Fore.MAGENTA + "[4]" + Fore.CYAN + " Look IP Info")
        print(Fore.MAGENTA + "[5]" + Fore.CYAN + " Facebook IDs Extractor")
        print(Fore.MAGENTA + "[6]" + Fore.CYAN + " Send Feedback")
        print(Fore.MAGENTA + "[0]" + Fore.CYAN + " Exit\n")
        choice = input(Fore.YELLOW + "Choose: ")
        if   choice == '1': send_requests()
        elif choice == '2': proxy_options()
        elif choice == '3': generate_useragents()
        elif choice == '4': look_ip_info()
        elif choice == '5': facebook_ids_extractor()
        elif choice == '6': send_feedback()
        elif choice == '0': break
        else: print(Fore.RED + "Invalid, try again.")

if __name__ == "__main__":
    main()
