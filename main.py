import os
import re
import requests
import random
import json
import time
from datetime import datetime
from urllib.parse import quote, urlparse
from bs4 import BeautifulSoup
import base64
import ast
import zlib

# Colors for colorized output
class Colors:
    OKGREEN = '\033[92m'
    OKRED = '\033[91m'
    OKCYAN = '\033[96m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Function for colored printing
def print_colored(text, color=Colors.ENDC):
    print(f"{color}{text}{Colors.ENDC}")


# Welcome banner
def print_banner():
    print(f"""
    {Colors.OKCYAN}█████╗ ██╗      ██████╗ ███╗   ██╗███████╗
    ██╔══██╗██║     ██╔═══██╗████╗  ██║██╔════╝
    ███████║██║     ██║   ██║██╔██╗ ██║███████╗
    ██╔══██║██║     ██║   ██║██║╚██╗██║╚════██║
    ██║  ██║███████╗╚██████╔╝██║ ╚████║███████║
    ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
    {Colors.OKGREEN}A L O N E  T O O L{Colors.ENDC}
    """)


# Function to encrypt code with various methods
def encrypt_code():
    print_colored("[•] Welcome to the Code Encryptor!", Colors.OKCYAN)
    file_name = input(f"{Colors.YELLOW}[•] Please enter the file name to encrypt: {Colors.ENDC}")
    
    if not os.path.isfile(file_name):
        print_colored(f"{Colors.OKRED}[•] File does not exist!{Colors.ENDC}")
        return
    
    print_colored(f"{Colors.OKCYAN}[•] Choose an encryption method:{Colors.ENDC}")
    print(f"{Colors.YELLOW}[1] Base64 Encode{Colors.ENDC}")
    print(f"{Colors.YELLOW}[2] Lambda Function Obfuscation{Colors.ENDC}")
    print(f"{Colors.YELLOW}[3] Zlib Compression{Colors.ENDC}")
    
    encryption_method = input(f"{Colors.YELLOW}[•] Select an option (1/2/3): {Colors.ENDC}")
    
    with open(file_name, 'r') as file:
        file_content = file.read()

    if encryption_method == "1":
        # Base64 encoding
        encoded = base64.b64encode(file_content.encode('utf-8')).decode('utf-8')
        new_file_name = f"enc_{file_name}.py"
        with open(new_file_name, 'w') as new_file:
            new_file.write(f"import base64\nexec(base64.b64decode('{encoded}').decode('utf-8'))")
        print_colored(f"[•] File encrypted with Base64 and saved as {new_file_name}", Colors.OKGREEN)

    elif encryption_method == "2":
        # Lambda obfuscation
        obfuscated = f"lambda: exec('{file_content}')"
        new_file_name = f"enc_{file_name}.py"
        with open(new_file_name, 'w') as new_file:
            new_file.write(obfuscated)
        print_colored(f"[•] Code obfuscated with Lambda and saved as {new_file_name}", Colors.OKGREEN)

    elif encryption_method == "3":
        # Zlib compression
        compressed = zlib.compress(file_content.encode('utf-8'))
        compressed_data = base64.b64encode(compressed).decode('utf-8')
        new_file_name = f"enc_{file_name}.py"
        with open(new_file_name, 'w') as new_file:
            new_file.write(f"import zlib, base64\nexec(zlib.decompress(base64.b64decode('{compressed_data}')).decode('utf-8'))")
        print_colored(f"[•] File compressed and saved as {new_file_name}", Colors.OKGREEN)

    else:
        print_colored(f"{Colors.OKRED}[•] Invalid option selected.{Colors.ENDC}")


# Main menu
def main_menu():
    print_banner()
    while True:
        print_colored("[1] Proxy Options", Colors.YELLOW)
        print_colored("[2] User-Agent Generator", Colors.YELLOW)
        print_colored("[3] Send HTTP Request", Colors.YELLOW)
        print_colored("[4] Look IP Info", Colors.YELLOW)
        print_colored("[5] Facebook IDs Extractor", Colors.YELLOW)
        print_colored("[6] Group Member ID Dumper", Colors.YELLOW)
        print_colored("[7] Encrypt Code", Colors.YELLOW)
        print_colored("[0] Exit", Colors.OKRED)
        choice = input(f"{Colors.YELLOW}[•] Choose an option: {Colors.ENDC}")
        
        if choice == "1":
            print_colored("[•] Proxy Options (To be implemented)", Colors.OKRED)
        elif choice == "2":
            print_colored("[•] User-Agent Generator (To be implemented)", Colors.OKRED)
        elif choice == "3":
            print_colored("[•] Send HTTP Request (To be implemented)", Colors.OKRED)
        elif choice == "4":
            print_colored("[•] Look IP Info (To be implemented)", Colors.OKRED)
        elif choice == "5":
            print_colored("[•] Facebook IDs Extractor (To be implemented)", Colors.OKRED)
        elif choice == "6":
            print_colored("[•] Group Member ID Dumper (To be implemented)", Colors.OKRED)
        elif choice == "7":
            encrypt_code()
        elif choice == "0":
            print_colored("[•] Goodbye!", Colors.OKGREEN)
            break
        else:
            print_colored(f"{Colors.OKRED}[•] Invalid option selected!{Colors.ENDC}")


# Run the main menu
if __name__ == "__main__":
    main_menu()