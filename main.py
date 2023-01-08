from tor import *
from api import *

import requests 
import os, sys, json, time
import string, random
import threading
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Back, init
init(convert=True)


#var avant la config file#
message = 'Salut Aline 16, tu as quel age?' #cherche M pour n*de sur sN ap alinenog2023
message_per_identity = 100
max_threads = 1

def fakeUserThreadTor(message, i):
    print(f"{Fore.LIGHTBLUE_EX}{Back.BLUE}[{threading.current_thread().name}]{Back.RESET} ==> | {Fore.LIGHTGREEN_EX}Theard Started! {Fore.RESET}")
    while True:

        leave = False
        tor = TorProxy(i)
        port, tor_process = tor.create_tor()
        omegle = OmegleAPI(tormode=True, port=port, message=message, start_time=time.time())
        omegle.genRandomId()
        omegle.getCheckId()
        omegle.genServerId()
        for k in range(message_per_identity):
            if leave is not True:
                omegle.monitorOmegleData()
                if omegle.openCon():
                    time.sleep(random.uniform(1, 2))
                    #omegle.typing()
                    #time.sleep(random.uniform(0.1, 1))
                    omegle.sendMessage()
                    time.sleep(random.uniform(0.1, 1))
                    #omegle.closeCon()
                else:
                    leave = True
        tor.kill_tor(i)
        
def fakeUserThreadProxy(message):
    print(f"{Fore.LIGHTBLUE_EX}{Back.BLUE}[{threading.current_thread().name}]{Back.RESET} ==> | {Fore.LIGHTGREEN_EX}Theard Started! {Fore.RESET}")
    while True:

        leave = False
        omegle = OmegleAPI(tormode=False, port=None, message=message, start_time=time.time())
        omegle.genRandomId()
        omegle.getCheckId()
        omegle.genServerId()
        for k in range(message_per_identity):
            if leave is not True:
                omegle.monitorOmegleData()
                if omegle.openCon():
                    time.sleep(random.uniform(0.1, 1))
                    omegle.typing()
                    time.sleep(random.uniform(0.1, 1))
                    omegle.sendMessage()
                    time.sleep(random.uniform(0.1, 1))
                    omegle.closeCon()
                else:
                    leave = True

def fakeUserThreadNone(message, i):
    print(f"{Fore.LIGHTBLUE_EX}{Back.BLUE}[{threading.current_thread().name}]{Back.RESET} ==> | {Fore.LIGHTGREEN_EX}Theard Started! {Fore.RESET}")
    while True:

        leave = False
        omegle = OmegleAPI(tormode=None, port=None, message=message, start_time=time.time())
        omegle.genRandomId()
        omegle.getCheckId()
        omegle.genServerId()
        for k in range(message_per_identity):
            if leave is not True:
                omegle.monitorOmegleData()
                if omegle.openCon():
                    time.sleep(random.uniform(0.1, 1))
                    omegle.typing()
                    time.sleep(random.uniform(0.1, 1))
                    omegle.sendMessage()
                    time.sleep(random.uniform(0.1, 1))
                    omegle.closeCon()
                else:
                    leave = True

             
executor = ThreadPoolExecutor(max_workers=max_threads, thread_name_prefix='THREAD')

tormode = False

if tormode:
    for i in range(max_threads):
        executor.submit(fakeUserThreadTor, message, i)
        time.sleep(0.1)

else:
    for i in range(max_threads):
        executor.submit(fakeUserThreadProxy, message)
        time.sleep(0.1)
  

while True:
    time.sleep(1)