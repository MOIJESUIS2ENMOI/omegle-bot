import requests 
import os, sys, json, time
import string, random
import threading
from colorama import Fore, init
init(convert=True)


import io
import os
import stem.process
from stem.control import Controller
from stem import Signal
import re
import urllib.request

total_sent = 0
count = 0

def create_tor(port:int = 0):
    global tor_process
    SOCKS_PORT = port
    TOR_PATH = os.path.normpath(os.getcwd()+"\\tor\\tor.exe")
    tor_process = stem.process.launch_tor_with_config(
    config = {
      'SocksPort': str(SOCKS_PORT),
    },
    init_msg_handler = lambda line: print(line) if re.search('Bootstrapped', line) else False,
    tor_cmd = TOR_PATH
  )
    return SOCKS_PORT
    
proxies = None
 
proxie = {
    'http': 'http://moijesuis:NPsZ8JVOcWuG2DVb_country-France@proxy.packetstream.io:31112',
    'https': 'http://moijesuis:NPsZ8JVOcWuG2DVb_country-France@proxy.packetstream.io:31112'
}
proxie = {
    'http': f'socks5://127.0.0.1:9050',
    'https': f'socks5://127.0.0.1:9050'
}

user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36", "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/108.0.5359.112 Mobile/15E148 Safari/604.1", "Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.128 Mobile Safari/537.36", "Mozilla/5.0 (Linux; Android 10; LM-X420) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.128 Mobile Safari/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36", "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1", "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15", "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.1; rv:108.0) Gecko/20100101 Firefox/108.0", "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:108.0) Gecko/20100101 Firefox/108.0", "Mozilla/5.0 (Android 13; Mobile; rv:68.0) Gecko/68.0 Firefox/108.0"]

def getCheckId():
    url = f"https://waw{str(random.randint(1,4))}.omegle.com/check"
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "no-cache",
        "origin": "https://www.omegle.com",
        "pragma": "no-cache",
        "referer": "https://www.omegle.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": random.choice(user_agents),
    }
    
    try:
        r = requests.post(url, headers=headers, proxies=proxies, timeout=10)
        if r.status_code == 200:
            return r.text
    except Exception as err:
        print(err)

def genRandomId():
    str = ""
    for i in range(8):
        str = str + random.choice(string.ascii_uppercase + string.digits) 
    return str

def getServerId():
    return str(random.randint(1,48))

def openCon(random_id:str='', check_id:str='', server_id:str=''):
    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://www.omegle.com",
        "pragma": "no-cache",
        "referer": "https://www.omegle.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": random.choice(user_agents),    }
    url = f"https://front{server_id}.omegle.com/start?caps=recaptcha2,t3&firstevents=1&spid=&randid={random_id}&cc={check_id}&lang=fr"
    try:
        r = requests.post(url, headers=headers, proxies=proxies, timeout=10)
        if r.status_code == 200:
            if "error" not in r.text :
                r = r.json()
                print(r)
                '''
                rdata = {
                    "id": r["clientID"]
                }
                time.sleep(1)
                r2 = requests.post(url=f"https://front{server_id}.omegle.com/events", headers=headers, proxies=proxies, data=rdata, timeout=10)
                print(r2.content)
                '''
                return r["clientID"]
            else: 
                return False
        else:
            print (r.status_code)
            print(r.json())
    except Exception as err:
        print(err)
        
def typing(server_id:str='', client_id:str=''):
    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://www.omegle.com",
        "pragma": "no-cache",
        "referer": "https://www.omegle.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": random.choice(user_agents),
    }
    rdata = {
        "id": client_id,
    }
    url = f"https://front{server_id}.omegle.com/typing"
    
    try:
        r = requests.post(url, headers=headers, data=rdata, proxies=proxies, timeout=10)
        if r.status_code == 200:
            return True
        else:
            print(r.status_code)
            print(r.content)
            return False
    except Exception as err:
        print(err)
    
def sendMessage(server_id:str='', client_id:str='', message:str='yo'):
    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://www.omegle.com",
        "pragma": "no-cache",
        "referer": "https://www.omegle.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": random.choice(user_agents),
    }
    rdata = {
        "msg": message,
        "id": client_id,
    }
    url = f"https://front{server_id}.omegle.com/send"
    
    try:
        r = requests.post(url, headers=headers, data=rdata, proxies=proxies, timeout=10)
        if r.status_code == 200:
            print(r.content)
            rdata = {
                "id": client_id,
            }
            r2 = requests.post(url=f"https://front{server_id}.omegle.com/events", headers=headers, proxies=proxies, data=rdata, timeout=10)
            print(r2.content)
            return True
        else:
            print(r.status_code)
            print(r.content)
            return False
    except Exception as err:
        print(err)
    
def closeCon(server_id:str='', client_id:str=''):
    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://www.omegle.com",
        "pragma": "no-cache",
        "referer": "https://www.omegle.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": random.choice(user_agents),
    }
    rdata = {
        "id": client_id,
    }
    url = f"https://front{server_id}.omegle.com/disconnect"
    
    try:
        r = requests.post(url, headers=headers, data=rdata, proxies=proxies, timeout=10)
        if r.status_code == 200:
            return True
        else:
            print(r.status_code)
            print(r.content)
    except Exception as err:
        print(err)
        
def resquestsBloc(message):
    global total_sent
    global count
    global timestart
    random_id = genRandomId()
    check_id = getCheckId()
    while True:
        for i in range(10):
            server_id = getServerId()
            client_id = openCon(random_id=random_id, check_id=check_id, server_id=server_id)
            if client_id is not False:
                time.sleep(round(random.uniform(0.1, 0.5), 1))
                typing(server_id=server_id, client_id=client_id)
                time.sleep(round(random.uniform(0.1, 0.5), 1))
                print(client_id)
                if sendMessage(server_id=server_id, client_id=client_id, message=message):
                    total_sent = total_sent + 1 
                    print(f"Message sent: {client_id} ! Total Sent: {total_sent} | Active users: {count} | Iterations: {total_sent/(time.time()-timestart)} it/s")
                time.sleep(round(random.uniform(0.1, 0.5), 1))
                closeCon(server_id=server_id, client_id=client_id)
        
        #tor_process.kill()
        #create_tor()

def monitorOmegleData():
    global count
    while True:
        r = requests.get("https://omegle.com/status")
        r = r.json()
        count = r['count']
        time.sleep(5)
    

timestart = time.time()
max_threads = 100

threading.Thread(target=monitorOmegleData).start()
time.sleep(10)
def spam():
    message = "Salut! C'est Aline 16 ans. Je nude(payant) sur snap : alinenog2023." 
    while True:
        
        while threading.active_count() <= max_threads:
            threading.Thread(target=resquestsBloc, args=(message,)).start()
            time.sleep(0.1)
        else: 
            time.sleep(1)
            
def requestsThreadCanal():
    message = "Salut! C'est Aline 16 ans. Je nude(payant) sur snap : alinenog2023." 
    for i in range(max_threads):
        threading.Thread(target=resquestsBloc, args=(message,)).start()
        time.sleep(0.1)
     

#create_tor()
message = "Salut! C'est Aline 16 ans. Je nude(payant) sur snap : alinenog2023." 

resquestsBloc(message)