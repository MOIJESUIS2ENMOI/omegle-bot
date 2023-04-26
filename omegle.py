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
 
proxies = None
 


proxie = {
    'http': f'socks5://127.0.0.1:9050',
    'https': f'socks5://127.0.0.1:9050'
}

        
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


timestart = time.time()
max_threads = 100
def spam():
    message = "Salut! C'est Aline 16 ans." 
    while True:
        
        while threading.active_count() <= max_threads:
            threading.Thread(target=resquestsBloc, args=(message,)).start()
            time.sleep(0.1)
        else: 
            time.sleep(1)
            
def requestsThreadCanal():
    message = "Salut! C'est Aline 16 ans. " 
    for i in range(max_threads):
        threading.Thread(target=resquestsBloc, args=(message,)).start()
        time.sleep(0.1)
     

#create_tor()
message = "Salut! C'est Aline 16 ans." 

resquestsBloc(message)
