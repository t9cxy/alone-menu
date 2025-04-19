#!/usr/bin/env python3

-- coding: utf-8 --

import os import sys import time import json import requests import re from bs4 import BeautifulSoup from datetime import datetime from urllib.parse import urlencode

Colors

R = '\033[1;31m' G = '\033[1;32m' Y = '\033[1;33m' B = '\033[1;34m' M = '\033[1;35m' C = '\033[1;36m' W = '\033[0;37m' RESET = '\033[0m'

ASCII Art Logo

logo = f""" {R} █████╗ ██╗      ██████╗ ███╗   ██╗███████╗ ██╔══██╗██║     ██╔═══██╗████╗  ██║██╔════╝ ███████║██║     ██║   ██║██╔██╗ ██║█████╗
██╔══██║██║     ██║   ██║██║╚██╗██║██╔══╝
██║  ██║███████╗╚██████╔╝██║ ╚████║███████╗ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝{RESET} """

def clear(): os.system('clear' if os.name != 'nt' else 'cls')

def save_to_file(filename, data): with open(filename, 'a', encoding='utf-8') as f: f.write(data + '\n')

def extract_group_members(token, cookie, group_url): headers = { 'Authorization': f'Bearer {token}' if token else '', 'Cookie': cookie if cookie else '', 'User-Agent': 'Mozilla/5.0 (Linux; Android 10)'  # Facebook mobile UA } session = requests.Session() session.headers.update(headers)

group_id = ''
if 'groups/' in group_url:
    try:
        group_id = re.search(r"groups/(.*?)(/|$)", group_url).group(1)
    except:
        print(f"{R}[!] Invalid group URL format.{RESET}")
        return
else:
    print(f"{R}[!] Invalid group URL.{RESET}")
    return

print(f"{Y}[•] Extracting members from group: {group_id}{RESET}")
members_dumped = 0
next_cursor = ''

while True:
    url = f"https://graph.facebook.com/v18.0/{group_id}/members?fields=id,name&limit=1000"
    if next_cursor:
        url += f"&after={next_cursor}"

    try:
        response = session.get(url)
        data = response.json()

        if 'data' not in data:
            print(f"{R}[!] Failed to extract or access denied.{RESET}")
            break

        for member in data['data']:
            print(f"{G}{member['id']} | {member['name']}{RESET}")
            save_to_file('groupids.txt', f"{member['id']} | {member['name']}")
            members_dumped += 1

        if 'paging' in data and 'next' in data['paging'] and 'cursors' in data['paging']:
            next_cursor = data['paging']['cursors'].get('after')
            if not next_cursor:
                break
        else:
            break

    except Exception as e:
        print(f"{R}[!] Error: {e}{RESET}")
        break

print(f"{C}[✓] Extraction complete. Total IDs: {members_dumped}{RESET}")

def main_menu(): while True: clear() print(logo) print(f"{Y}[ 1 ]{C} Facebook Group Member Dump (with Cookie or Token){RESET}") print(f"{Y}[ 0 ]{C} Exit{RESET}\n") choice = input(f"{B}Choose: {RESET}")

if choice == '1':
        method = input(f"{M}[?] Use Cookie or Token? (c/t): {RESET}").strip().lower()
        cookie = ''
        token = ''

        if method == 'c':
            cookie = input(f"{C}[•] Enter your Facebook Cookie: {RESET}")
        elif method == 't':
            token = input(f"{C}[•] Enter your Facebook Token: {RESET}")
        else:
            print(f"{R}[!] Invalid choice.{RESET}")
            input("Press Enter to return...")
            continue

        group_url = input(f"{Y}[•] Enter Facebook Group URL: {RESET}")
        extract_group_members(token, cookie, group_url)
        input(f"\n{Y}[•] Press Enter to return to menu...{RESET}")

    elif choice == '0':
        print(f"{G}Exiting...{RESET}")
        break
    else:
        print(f"{R}[!] Invalid choice.{RESET}")
        time.sleep(1)

if name == 'main': try: main_menu() except Exception as err: print(f"{R}[ ! ] Error while running the script: {err}{RESET}")

