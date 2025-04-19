import os import re import time import json import random import requests from bs4 import BeautifulSoup from datetime import datetime from urllib.parse import quote

Colors

R = '\033[91m' G = '\033[92m' Y = '\033[93m' B = '\033[94m' C = '\033[96m' W = '\033[97m' RESET = '\033[0m'

Logo

logo = f"""{G} █████╗ ██╗      ██████╗ ███╗   ██╗███████╗ ██╔══██╗██║     ██╔═══██╗████╗  ██║██╔════╝ ███████║██║     ██║   ██║██╔██╗ ██║█████╗
██╔══██║██║     ██║   ██║██║╚██╗██║██╔══╝
██║  ██║███████╗╚██████╔╝██║ ╚████║███████╗ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝ {RESET}"""

Clear screen

def clear(): os.system('clear' if os.name == 'posix' else 'cls')

Main menu

def main_menu(): clear() print(logo) print(f"""{B} [1] Proxy Options [2] User-Agent Generator [3] Send HTTP Request [4] Look IP Info [5] Facebook IDs Extractor [6] Group Member ID Dumper [7] Send Feedback [0] Exit{RESET} """) choice = input(f"{Y}[?] Choose an option: {RESET}") if choice == "1": proxy_options() elif choice == "2": user_agent_generator() elif choice == "3": send_http_request() elif choice == "4": ip_lookup() elif choice == "5": facebook_id_extractor() elif choice == "6": group_member_dumper() elif choice == "7": send_feedback() elif choice == "0": exit() else: print(f"{R}[!] Invalid option!{RESET}") time.sleep(1) main_menu()

Option 1: Proxy Options

def proxy_options(): clear() print(logo) print(f"{Y}[•] Proxy Options{RESET}") proxy_list = input(f"{C}[?] Enter proxy list URL: {RESET}") try: res = requests.get(proxy_list) proxies = res.text.splitlines() valid = [] for proxy in proxies: try: r = requests.get("http://httpbin.org/ip", proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"}, timeout=5) valid.append(proxy) print(f"{G}[✓] {proxy} OK{RESET}") except: print(f"{R}[x] {proxy} BAD{RESET}") with open("proxy.txt", "w") as f: for p in valid: f.write(p + "\n") print(f"{G}[•] Saved valid proxies to proxy.txt{RESET}") except Exception as e: print(f"{R}[!] Error: {e}{RESET}") input(f"\n{Y}[•] Press Enter to return...{RESET}") main_menu()

Option 2: User-Agent Generator

def user_agent_generator(): clear() print(logo) print(f"{Y}[•] User-Agent Generator{RESET}") total = int(input(f"{C}[?] How many User-Agents to generate?: {RESET}")) uas = [] for _ in range(total): android_version = f"{random.randint(6, 13)}.0" device_model = random.choice(["SM-G930F", "Pixel 5", "Redmi Note 9", "OnePlus7T"]) browser_version = f"Chrome/{random.randint(70, 100)}.0.{random.randint(1000, 5000)}.{random.randint(10, 200)}" ua = f"Mozilla/5.0 (Linux; Android {android_version}; {device_model}) AppleWebKit/537.36 (KHTML, like Gecko) {browser_version} Mobile Safari/537.36" uas.append(ua) print(f"{G}[+] {ua}{RESET}") with open("ug.txt", "w") as f: for ua in uas: f.write(ua + "\n") print(f"\n{G}[•] Saved to ug.txt{RESET}") input(f"\n{Y}[•] Press Enter to return...{RESET}") main_menu()

Option 3: Send HTTP Request

def send_http_request(): clear() print(logo) print(f"{Y}[•] Send HTTP Request{RESET}") url = input(f"{C}[?] Enter URL: {RESET}") ua = input(f"{C}[?] Enter User-Agent or leave blank: {RESET}") proxy = input(f"{C}[?] Enter Proxy (IP:PORT) or leave blank: {RESET}") headers = {"User-Agent": ua} if ua else {} proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else {} try: res = requests.get(url, headers=headers, proxies=proxies, timeout=10) print(f"{G}[✓] Response Code: {res.status_code}{RESET}") print(res.text[:500]) except Exception as e: print(f"{R}[!] Request failed: {e}{RESET}") input(f"\n{Y}[•] Press Enter to return...{RESET}") main_menu()

Option 4: IP Lookup

def ip_lookup(): clear() print(logo) print(f"{Y}[•] IP Lookup{RESET}") ip = input(f"{C}[?] Enter IP Address: {RESET}") try: r = requests.get(f"http://ip-api.com/json/{ip}").json() for k, v in r.items(): print(f"{W}{k}: {C}{v}{RESET}") except Exception as e: print(f"{R}[!] Error: {e}{RESET}") input(f"\n{Y}[•] Press Enter to return...{RESET}") main_menu()

Option 5: Facebook ID Extractor

def facebook_id_extractor(): clear() print(logo) print(f"{Y}[•] Facebook ID Extractor{RESET}") target = input(f"{C}[?] Enter target profile ID or URL: {RESET}") # Placeholder functionality print(f"{G}[✓] Extracted from: {target} (demo only){RESET}") input(f"\n{Y}[•] Press Enter to return...{RESET}") main_menu()

Option 6: Group Member Dumper

def group_member_dumper(): clear() print(logo) print(f"{Y}[•] Group Member ID Dumper{RESET}") method = input(f"{C}[1] Cookie or [2] Token? {RESET}") auth = input(f"{C}[?] Enter Cookie/Token: {RESET}") group_url = input(f"{C}[?] Group URL: {RESET}") try: group_id = re.findall(r'groups/(\d+)', group_url) if not group_id: raise Exception("Invalid group link.") members = [f"10000{i} | Example Name {i}" for i in range(10)] with open("groupids.txt", "w") as f: for m in members: f.write(m + "\n") print(f"{G}[+] {m}{RESET}") print(f"\n{G}[✓] Saved to groupids.txt{RESET}") except Exception as e: print(f"{R}[!] Error: {e}{RESET}") input(f"\n{Y}[•] Press Enter to return...{RESET}") main_menu()

Option 7: Feedback

def send_feedback(): clear() print(logo) print(f"{Y}[•] Send Feedback{RESET}") msg = input(f"{C}[?] Your feedback: {RESET}") with open("feedback.txt", "a") as f: f.write(f"{datetime.now()} - {msg}\n") print(f"{G}[✓] Feedback saved. Thank you!{RESET}") input(f"\n{Y}[•] Press Enter to return...{RESET}") main_menu()

if name == "main": main_menu()

