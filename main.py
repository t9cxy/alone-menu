#!/usr/bin/env python3

import os import re import json import time import requests import random from bs4 import BeautifulSoup from datetime import datetime from urllib.parse import quote

Colors

R = '\033[1;91m' G = '\033[1;92m' Y = '\033[1;93m' B = '\033[1;94m' P = '\033[1;95m' C = '\033[1;96m' W = '\033[1;97m' N = '\033[0m'

Logo

LOGO = f""" {R} █████╗ ██╗      ██████╗ ███╗   ██╗███████╗ ██╔══██╗██║     ██╔═══██╗████╗  ██║██╔════╝ ███████║██║     ██║   ██║██╔██╗ ██║█████╗
██╔══██║██║     ██║   ██║██║╚██╗██║██╔══╝
██║  ██║███████╗╚██████╔╝██║ ╚████║███████╗ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝ {W}"""

Menu

MENU = f""" {C}1.{W} Proxy Tools {C}2.{W} User-Agent Generator {C}3.{W} Send Requests with Proxy & UA {C}4.{W} Look IP Info {C}5.{W} Facebook IDs Extractor {C}6.{W} Group Member Dump IDs {C}7.{W} Send Feedback {C}0.{W} Exit """

def clear(): os.system('clear')

def main_menu(): clear() print(LOGO) print(MENU) choice = input(f"{C}Choose:{W} ") if choice == '1': proxy_menu() elif choice == '4': look_ip_info() elif choice == '5': facebook_ids_extractor() elif choice == '6': group_member_dump() elif choice == '0': exit() else: input(f"{R}Invalid choice!{W} Press Enter...") main_menu()

def proxy_menu(): clear() print(f"{Y}Proxy Tools Options:{W}") print(f"{C}1.{W} Check Proxy by File") print(f"{C}2.{W} Check From URL (Pastebin, GitHub, etc)") print(f"{C}3.{W} Generate and Check Proxy") choice = input(f"{C}Choose:{W} ") if choice == '3': generate_and_check_proxies() else: input(f"{R}This option is not yet implemented.{W} Press Enter...") main_menu()

def generate_and_check_proxies(): total = int(input(f"{C}How many valid proxies you want? {W}")) good = 0 bad = 0 open('proxy.txt', 'w').write('') print() while good < total: ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}:{random.randint(1000,9999)}" try: r = requests.get("http://example.com", proxies={"http": f"http://{ip}"}, timeout=1) with open('proxy.txt', 'a') as f: f.write(ip + '\n') good += 1 except: bad += 1 clear() print(f"{G}{ip}{W}") print(f"{G}[ GOOD ] {good}/{total} {W}|{R} [ BAD ] {bad}{W}") input(f"{G}Done! Press Enter to return...{W}") main_menu()

def look_ip_info(): clear() ip = input(f"{C}Enter IP to lookup:{W} ") try: r = requests.get(f"http://ip-api.com/json/{ip}").json() print(f"\n{G}IP Info:{W}") for key in ['query','country','regionName','city','isp','org']: print(f"{C}{key.capitalize()}: {W}{r.get(key, 'N/A')}") except Exception as e: print(f"{R}Error: {e}{W}") input(f"\n{C}Press Enter to return to menu...{W}") main_menu()

def facebook_ids_extractor(): clear() link = input(f"{C}Enter Facebook profile link or ID:{W} ") print(f"{Y}Extracting friends and friends of friends...{W}") # Dummy output - you will need a working method here open('ids.txt', 'w').write("100001 | John Doe\n100002 | Jane Smith\n") print(f"{G}Saved to ids.txt{W}") input(f"\n{C}Press Enter to return to menu...{W}") main_menu()

def group_member_dump(): clear() print(f"{C}Choose Auth Type:{W}\n1. Cookie\n2. Token") auth = input(f"{C}Your choice:{W} ") if auth == '1': cookie = input(f"{C}Enter your Facebook Cookie:{W} ") headers = {'cookie': cookie, 'user-agent': 'Mozilla/5.0'} elif auth == '2': token = input(f"{C}Enter your Facebook Token:{W} ") headers = {'Authorization': f'Bearer {token}'} else: main_menu() link = input(f"{C}Enter Facebook Group Link:{W} ") print(f"{Y}Fetching group members...{W}") # Dummy output - real method needs mobile API or scraping open('groupids.txt', 'w').write("100011 | Member One\n100022 | Member Two\n") print(f"{G}Saved to groupids.txt{W}") input(f"\n{C}Press Enter to return to menu...{W}") main_menu()

if name == 'main': main_menu()

