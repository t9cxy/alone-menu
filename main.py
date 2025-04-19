import os import re import requests import random import json import time from datetime import datetime from urllib.parse import quote, urlparse from bs4 import BeautifulSoup

Telegram Bot Info

BOT_TOKEN = "6770850573:AAFUCCzKlKrekJU5GtNFqdnqwMSAsnTBIc0" CHAT_ID = "1241769879"

GitHub Raw URL for auto-update

github_url = "https://raw.githubusercontent.com/t9cxy/alone-menu/main/main.py"

Color codes

def color(code): return f"\033[{code}m" class C: HEADER = color('95') OKBLUE = color('94') OKCYAN = color('96') OKGREEN = color('92') WARNING = color('93') FAIL = color('91') ENDC = color('0') BOLD = color('1') UNDERLINE = color('4')

Utility

def clear(): os.system('clear')

def printc(msg, col=C.ENDC): print(f"{col}{msg}{C.ENDC}")

def send_telegram_log(msg): url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage" data = {'chat_id': CHAT_ID, 'text': msg} try: requests.post(url, data=data, timeout=5) except: pass

def log_and_notify(action): timestamp = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p') msg = f"[•] {action} | {timestamp}" send_telegram_log(msg) printc(msg, C.OKCYAN)

Auto-update

def check_update(): try: r = requests.get(github_url, timeout=5) if r.status_code == 200: remote = r.text with open(file, 'r') as f: local = f.read() if remote.strip() != local.strip(): printc('[•] Update found. Applying...', C.WARNING) with open(file, 'w') as f: f.write(remote) printc('[•] Restarting... ', C.OKGREEN) os.execv(file, ['python3'] + sys.argv) except: pass

Features

def encrypt_code(): clear() printc('[•] Code Encryptor', C.OKCYAN) fn = input('[•] File to encrypt: ').strip() if not os.path.isfile(fn): printc('[•] File not found!', C.FAIL) input('[•] Enter to return...') return with open(fn) as f: code = f.read() enc = code[::-1] out = 'encrypted_' + os.path.basename(fn) with open(out, 'w') as f: f.write(enc) log_and_notify(f'Encrypted {fn} -> {out}') printc(f'[•] Saved as {out}', C.OKGREEN) input('[•] Enter to return...')

Proxy Options

def fetch_proxies(): urls = [ 'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt', 'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt' ] ps = set() for u in urls: try: r = requests.get(u, timeout=5) ps.update(r.text.splitlines()) except: pass return list(ps)

def proxy_options(): clear() printc('[•] Proxy Options', C.OKCYAN) ps = fetch_proxies() if not ps: printc('[•] No proxies fetched', C.FAIL) input('[•] Enter to return...') return with open('proxy.txt','w') as f: for p in ps: f.write(p+'\n') log_and_notify(f'Fetched {len(ps)} proxies') printc(f'[•] Wrote {len(ps)} proxies to proxy.txt', C.OKGREEN) input('[•] Enter to return...')

UA Generator

def user_agent_generator(): clear() printc('[•] User-Agent Generator', C.OKCYAN) uas = [ 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)', 'Mozilla/5.0 (X11; Linux x86_64)' ] with open('ug.txt','w') as f: for ua in uas: printc(ua, C.OKGREEN) f.write(ua+'\n') log_and_notify('Generated user-agent list') input('[•] Enter to return...')

HTTP Request

def send_http_request(): clear() printc('[•] Send HTTP Request', C.OKCYAN) url = input('[•] URL: ').strip() use_p = input('[•] Use proxy? (y/N): ').lower()=='y' use_ua = input('[•] Use UA? (y/N): ').lower()=='y' pr = None hd = {} if use_p: ps = open('proxy.txt').read().splitlines() pr = {'http':f'http://{random.choice(ps)}','https':f'http://{random.choice(ps)}'} if use_ua: uas = open('ug.txt').read().splitlines() hd['User-Agent']=random.choice(uas) try: r = requests.get(url, proxies=pr, headers=hd, timeout=5) printc(f'Status: {r.status_code}', C.OKGREEN) log_and_notify(f'Request to {url} status {r.status_code}') except Exception as e: printc(f'Error: {e}', C.FAIL) input('[•] Enter to return...')

IP Lookup

def look_ip_info(): clear() printc('[•] IP Lookup', C.OKCYAN) ip = input('[•] IP: ').strip() try: r = requests.get(f'http://ip-api.com/json/{ip}',timeout=5).json() for k,v in r.items(): printc(f'{k}: {v}', C.OKBLUE) log_and_notify(f'IP lookup {ip}') except: printc('[•] Failed', C.FAIL) input('[•] Enter to return...')

Facebook IDs Extractor

def facebook_ids_extractor(): clear() printc('[•] FB IDs Extractor', C.OKCYAN) uid = input('[•] Profile ID or URL: ').strip() if 'facebook.com' in uid: m = re.search(r'id=(\d+)',uid) if m: uid=m.group(1) seen=set() def ext(u): url=f'https://mbasic.facebook.com/profile.php?id={u}&v=friends' headers={'User-Agent':'Mozilla/5.0'} r=requests.get(url,headers=headers) bs=BeautifulSoup(r.text,'html.parser') for a in bs.find_all('a',href=True): m=re.search(r'profile.php?id=(\d+)',a['href']) if m: fid=m.group(1) name=a.text if fid not in seen: seen.add(fid) printc(f'{fid} | {name}',C.OKGREEN) with open('ids.txt','a') as f: f.write(f'{fid}|{name}\n') ext(fid) ext(uid) log_and_notify(f'Extracted {len(seen)} IDs') input('[•] Enter to return...')

Group Member Dumper

def group_member_dumper(): clear() printc('[•] Group Member Dumper', C.OKCYAN) url=input('[•] Group URL: ').strip() cookie=input('[•] Enter Facebook cookie: ').strip() headers={'User-Agent':'Mozilla/5.0','Cookie':cookie} m=re.search(r'groups/(\d+)',url) if not m: printc('Invalid group URL',C.FAIL); input(); return gid=m.group(1) page=f'https://mbasic.facebook.com/groups/{gid}/members' seen=[] while page: r=requests.get(page,headers=headers) bs=BeautifulSoup(r.text,'html.parser') for a in bs.find_all('a',href=True): m2=re.search(r'profile.php?id=(\d+)',a['href']) if m2: fid=m2.group(1) name=a.text if fid not in seen: seen.append(fid) printc(f'{fid} | {name}',C.OKGREEN) with open('groupids.txt','a') as f: f.write(f'{fid}|{name}\n') nxt=bs.find('a',string='See More') page='https://mbasic.facebook.com'+nxt['href'] if nxt else None log_and_notify(f'Dumped {len(seen)} group members') input('[•] Enter to return...')

Main Menu

def main_menu(): while True: clear() check_update() printc('█████╗ ██╗      ██████╗ ███╗   ██╗███████╗',C.OKCYAN) printc('██╔══██╗██║     ██╔═══██╗████╗  ██║██╔════╝',C.OKCYAN) printc('███████║██║     ██║   ██║██╔██╗ ██║█████╗  ',C.OKCYAN) printc('██╔══██║██║     ██║   ██║██║╚██╗██║╚════██║',C.OKCYAN) printc('██║  ██║███████╗╚██████╔╝██║ ╚████║███████║',C.OKCYAN) printc('╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝',C.OKCYAN) printc("\n[1] Proxy Options",C.OKGREEN) printc("[2] User-Agent Generator",C.OKGREEN) printc("[3] Send HTTP Request",C.OKGREEN) printc("[4] Look IP Info",C.OKGREEN) printc("[5] Facebook IDs Extractor",C.OKGREEN) printc("[6] Group Member ID Dumper",C.OKGREEN) printc("[7] Encrypt Code",C.OKGREEN) printc("[8] Exit",C.FAIL) choice=input('[?] Choose: ').strip() if choice=='1': proxy_options() elif choice=='2': user_agent_generator() elif choice=='3': send_http_request() elif choice=='4': look_ip_info() elif choice=='5': facebook_ids_extractor() elif choice=='6': group_member_dumper() elif choice=='7': encrypt_code() elif choice=='8': break else: printc('Invalid choice',C.FAIL) time.sleep(1)

if name=='main': main_menu()

