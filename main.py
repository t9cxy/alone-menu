import os
import re
import requests
import random
import json
import time
from datetime import datetime
from urllib.parse import quote
from bs4 import BeautifulSoup
import subprocess

# Your Telegram Bot Info
BOT_TOKEN = "6770850573:AAFUCCzKlKrekJU5GtNFqdnqwMSAsnTBIc0"
CHAT_ID   = "1241769879"

# Color codes
class Colors:
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKCYAN    = '\033[96m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def print_colored(msg, color):
    print(f"{color}{msg}{Colors.ENDC}")

def send_telegram_log(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data, timeout=5)
    except:
        pass

def log_and_notify(action):
    ts = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    msg = f"[•] {action} | {ts}"
    send_telegram_log(msg)
    print_colored(msg, Colors.OKCYAN)

# --- FEATURES ---

def proxy_options():
    clear_screen()
    print_colored("[•] Proxy Options", Colors.OKCYAN)
    # Example: fetch a list and save to proxy.txt
    try:
        res = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http")
        proxies = res.text.strip().splitlines()
        with open("proxy.txt","w") as f:
            for p in proxies:
                f.write(p+"\n")
        log_and_notify(f"Fetched {len(proxies)} proxies")
        print_colored(f"[•] Saved {len(proxies)} proxies to proxy.txt", Colors.OKGREEN)
    except Exception as e:
        print_colored(f"[!] Error: {e}", Colors.FAIL)
    input("[•] Press Enter to return...")

def user_agent_generator():
    clear_screen()
    print_colored("[•] User-Agent Generator", Colors.OKCYAN)
    uas = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
        "Mozilla/5.0 (Linux; Android 10)..."
    ]
    with open("ug.txt","w") as f:
        for ua in uas:
            f.write(ua+"\n")
    log_and_notify("Generated sample User-Agents")
    print_colored("[•] Saved sample UAs to ug.txt", Colors.OKGREEN)
    input("[•] Press Enter to return...")

def send_http_request():
    clear_screen()
    print_colored("[•] Send HTTP Request", Colors.OKCYAN)
    url = input("[•] Target URL: ").strip()
    try:
        r = requests.get(url, timeout=5)
        log_and_notify(f"Requested {url} => {r.status_code}")
        print_colored(f"[•] Status: {r.status_code}", Colors.OKGREEN)
    except Exception as e:
        print_colored(f"[!] Error: {e}", Colors.FAIL)
    input("[•] Press Enter to return...")

def look_ip_info():
    clear_screen()
    print_colored("[•] Look IP Info", Colors.OKCYAN)
    ip = input("[•] IP Address: ").strip()
    try:
        info = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        for k,v in info.items():
            print_colored(f"{k}: {v}", Colors.OKBLUE)
        log_and_notify(f"IP lookup {ip}")
    except:
        print_colored("[!] Failed to fetch IP info", Colors.FAIL)
    input("[•] Press Enter to return...")

def facebook_ids_extractor():
    clear_screen()
    print_colored("[•] Facebook IDs Extractor", Colors.OKCYAN)
    target = input("[•] Profile URL or ID: ").strip()
    # Placeholder recursive extractor
    seen = set()
    def extract(uid):
        url = f"https://mbasic.facebook.com/profile.php?id={uid}&v=friends"
        r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
        bs = BeautifulSoup(r.text,"html.parser")
        for a in bs.find_all("a", href=True):
            m = re.search(r"profile\.php\?id=(\d+)", a["href"])
            if m:
                fid = m.group(1)
                name = a.text
                if fid not in seen:
                    seen.add(fid)
                    print_colored(f"{fid} | {name}", Colors.OKGREEN)
                    with open("ids.txt","a") as f:
                        f.write(f"{fid}|{name}\n")
                    extract(fid)
    extract(target)
    log_and_notify(f"Extracted {len(seen)} FB IDs")
    input("[•] Press Enter to return...")

def group_member_dumper():
    clear_screen()
    print_colored("[•] Group Member ID Dumper", Colors.OKCYAN)
    group = input("[•] Group URL: ").strip()
    cookie = input("[•] Your FB Cookie: ").strip()
    headers = {"User-Agent":"Mozilla/5.0", "Cookie":cookie}
    m = re.search(r"groups/(\d+)", group)
    if not m:
        print_colored("[!] Invalid group URL", Colors.FAIL)
        input("[•] Press Enter to return..."); return
    gid = m.group(1)
    url = f"https://mbasic.facebook.com/groups/{gid}/members"
    seen = []
    while url:
        r = requests.get(url, headers=headers)
        bs = BeautifulSoup(r.text,"html.parser")
        for a in bs.find_all("a", href=True):
            m2 = re.search(r"profile\.php\?id=(\d+)", a["href"])
            if m2:
                fid=a["href"].split("id=")[1]
                name=a.text
                if fid not in seen:
                    seen.append(fid)
                    print_colored(f"{fid} | {name}", Colors.OKGREEN)
                    with open("groupids.txt","a") as f:
                        f.write(f"{fid}|{name}\n")
        nxt = bs.find("a", string="See More")
        url = "https://mbasic.facebook.com" + nxt["href"] if nxt else None
    log_and_notify(f"Dumped {len(seen)} group members")
    input("[•] Press Enter to return...")

def encrypt_code():
    clear_screen()
    print_colored("[•] Encrypt File", Colors.OKCYAN)
    fn = input("[•] Filename: ").strip()
    if not os.path.isfile(fn):
        print_colored("[!] File not found", Colors.FAIL)
        input("[•] Press Enter..."); return
    with open(fn,"r") as f:
        code = f.read()
    out = "encrypted_" + os.path.basename(fn)
    with open(out,"w") as f:
        f.write(code[::-1])
    log_and_notify(f"Encrypted {fn} -> {out}")
    print_colored(f"[•] Saved to {out}", Colors.OKGREEN)
    input("[•] Press Enter to return...")

def rerun_update():
    clear_screen()
    print_colored("[•] Fetching and Running Latest Tool (github.py)...", Colors.OKGREEN)
    subprocess.run(["python3","github.py"])
    exit()

# --- MAIN MENU ---

def main_menu():
    while True:
        clear_screen()
        print_colored("█████╗ ██╗      ██████╗ ███╗   ██╗███████╗", Colors.OKCYAN)
        print_colored("██╔══██╗██║     ██╔═══██╗████╗  ██║██╔════╝", Colors.OKCYAN)
        print_colored("███████║██║     ██║   ██║██╔██╗ ██║█████╗  ", Colors.OKCYAN)
        print_colored("██╔══██║██║     ██║   ██║██║╚██╗██║██╔══╝  ", Colors.OKCYAN)
        print_colored("██║  ██║███████╗╚██████╔╝██║ ╚████║███████╗", Colors.OKCYAN)
        print_colored("╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝", Colors.OKCYAN)
        print()
        print_colored("[1] Proxy Options", Colors.OKGREEN)
        print_colored("[2] User-Agent Generator", Colors.OKGREEN)
        print_colored("[3] Send HTTP Request", Colors.OKGREEN)
        print_colored("[4] Look IP Info", Colors.OKGREEN)
        print_colored("[5] Facebook IDs Extractor", Colors.OKGREEN)
        print_colored("[6] Group Member ID Dumper", Colors.OKGREEN)
        print_colored("[7] Encrypt Code", Colors.OKGREEN)
        print_colored("[8] Rerun Tool (Auto-Update)", Colors.OKGREEN)
        print_colored("[0] Exit", Colors.FAIL)
        choice = input("\n[?] Choose an option: ").strip()
        if   choice=="1": proxy_options()
        elif choice=="2": user_agent_generator()
        elif choice=="3": send_http_request()
        elif choice=="4": look_ip_info()
        elif choice=="5": facebook_ids_extractor()
        elif choice=="6": group_member_dumper()
        elif choice=="7": encrypt_code()
        elif choice=="8": rerun_update()
        elif choice=="0": break
        else:
            print_colored("[!] Invalid choice", Colors.FAIL)
            time.sleep(1)

if __name__ == "__main__":
    main_menu()