import os
import re
import requests
import random
import json
import time
from datetime import datetime
from urllib.parse import quote
from bs4 import BeautifulSoup

# Telegram Info
BOT_TOKEN = "6770850573:AAFUCCzKlKrekJU5GtNFqdnqwMSAsnTBIc0"
CHAT_ID = "1241769879"

# Colors for styling
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

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def print_colored(text, color):
    print(color + text + Colors.ENDC)

def send_telegram_log(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={quote(msg)}"
    try:
        requests.get(url)
    except:
        pass

def log_and_notify(action):
    message = f"[•] {action} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    send_telegram_log(message)
    print_colored(f"[•] {action}", Colors.OKCYAN)

def encrypt_code():
    print_colored("[•] Welcome to the Code Encryptor!", Colors.OKCYAN)
    file = input("[•] File Name: ").strip()
    if not os.path.isfile(file):
        print_colored("[•] File does not exist!", Colors.FAIL)
        input("[•] Press Enter to return...")
        return

    with open(file, 'r') as f:
        code = f.read()
    encrypted = code[::-1]
    out = "encrypted_" + file
    with open(out, "w") as f:
        f.write(encrypted)
    log_and_notify(f"Encrypted: {file} -> {out}")
    print_colored(f"[•] Saved to {out}", Colors.OKGREEN)
    input("[•] Press Enter to return...")

# ---- PROXY MODULE ----

def fetch_proxies():
    sources = [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt"
    ]
    proxies = set()
    for url in sources:
        try:
            res = requests.get(url, timeout=5)
            proxies.update(res.text.strip().splitlines())
        except: continue
    return list(proxies)

def proxy_options():
    clear_screen()
    print_colored("[•] Proxy Options", Colors.OKCYAN)
    proxies = fetch_proxies()
    if not proxies:
        print_colored("[•] Failed to fetch proxies.", Colors.FAIL)
        input("[•] Press Enter to return...")
        return
    with open("proxy.txt", "w") as f:
        for p in proxies:
            f.write(p + "\n")
    log_and_notify(f"Fetched {len(proxies)} proxies")
    print_colored(f"[•] Saved {len(proxies)} proxies to proxy.txt", Colors.OKGREEN)
    input("[•] Press Enter to return...")

# ---- USER-AGENT MODULE ----

def user_agent_generator():
    uas = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
        "Mozilla/5.0 (Linux; Android 10; SM-G975F)...",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X)..."
    ]
    with open("ug.txt", "w") as f:
        for ua in uas:
            f.write(ua + "\n")
    log_and_notify("Generated sample User-Agents")
    print_colored("[•] Saved sample UAs to ug.txt", Colors.OKGREEN)
    input("[•] Press Enter to return...")

# ---- SEND REQUEST ----

def send_http_request():
    url = input("[