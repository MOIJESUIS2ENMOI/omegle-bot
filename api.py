import requests 
import os, sys, json, time
import string, random
import threading
from datetime import datetime
from colorama import Fore, Back, init
init(convert=True)

from tor import *

class OmegleAPI:
    def __init__(self, tormode, port, message, start_time):
        self.start_time = start_time
        self.message = message
        self.user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"] #, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36", "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/108.0.5359.112 Mobile/15E148 Safari/604.1", "Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.128 Mobile Safari/537.36", "Mozilla/5.0 (Linux; Android 10; LM-X420) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.128 Mobile Safari/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36", "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1", "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15", "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.1; rv:108.0) Gecko/20100101 Firefox/108.0", "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:108.0) Gecko/20100101 Firefox/108.0", "Mozilla/5.0 (Android 13; Mobile; rv:68.0) Gecko/68.0 Firefox/108.0"
        
        self.headers = {
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://www.omegle.com",
            "pragma": "no-cache",
            "referer": "https://www.omegle.com/",
            "TE": "trailers",
            "user-agent": random.choice(self.user_agents),    
        }
        if tormode:
            self.proxies= {
                'http': f'socks5://127.0.0.1:{port}',
                'https': f'socks5://127.0.0.1:{port}'
            }
        else:
            self.proxies = {
            'http': 'http://moijesuis:NPsZ8JVOcWuG2DVb_country-France@proxy.packetstream.io:31112',
            'https': 'http://moijesuis:NPsZ8JVOcWuG2DVb_country-France@proxy.packetstream.io:31112'
        }
            
        #self.proxies = {
        #    'http': 'http://moijesuis:NPsZ8JVOcWuG2DVb_country-France@proxy.packetstream.io:31112',
        #    'https': 'http://moijesuis:NPsZ8JVOcWuG2DVb_country-France@proxy.packetstream.io:31112'
        #}
        #stats 
        
        self.total_sent = 0
        self.count = 0
    
    def monitorOmegleData(self):

        try:
            r = requests.post("https://omegle.com/status")
            if r.status_code == 200:
                self.count = r.json()['count']
        except Exception as err:
            self.count = self.count
        time.sleep(5)
    
    #generate a random id, seems like a strong security, but called "random" ;)???
    def genRandomId(self):
        self.random_id = ""
        for i in range(8):
            self.random_id = self.random_id + random.choice(string.ascii_uppercase + string.digits) 
        self.headers['cookies'] = f"randid={self.random_id}; uselikes=1; topiclist=%5B%5D;"
    
    
    #get the check id, seems like a verification from the omegle API.
    def getCheckId(self):
        url = f"https://waw{str(random.randint(1,4))}.omegle.com/check"
        
        headers = {
            "User-Agent": random.choice(self.user_agents),
            "Accept": "*/*",
            "cookies": f"randid={self.random_id}; uselikes=1; topiclist=%5B%5D;",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Origin": "https://www.omegle.com",
            "Connection": "keep-alive",
            "Referer": "https://www.omegle.com/",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            }
        
        try:
            r = requests.post(url, headers=headers, proxies=self.proxies, timeout=10)
            if r.status_code == 200:
                self.check_id = r.text
        except Exception as err:
            pass
            #print(err)
    
    # gen the server id we will use to reach the maximum number of people
    def genServerId(self):
        self.server_id = str(random.randint(1,48))
    
    
    
    #######################################################################
    #                                                                     #
    #                   API INTERACTIONS FOR MESSAGES                     #
    #                                                                     #
    #######################################################################
    
    # ici toutes les interactions permettant de gerer l'application texte du
    # site. 
    
    def openCon(self):
        url = f"https://front{self.server_id}.omegle.com/start?caps=recaptcha2,t3&firstevents=1&spid=&randid={self.random_id}&cc={self.check_id}&lang=fr"
        try:
            r = requests.post(url, headers=self.headers, proxies=self.proxies, timeout=10)
            if r.status_code == 200:
                if "error" not in r.text:
                    if "antinudeBanned" not in r.text:
                        if "recaptchaRequired" not in r.text:
                            self.client_id = r.json()["clientID"]
                            #print(r.json())
                            for i in range(3):
                                self.getEvents()
                                time.sleep(1)
                            self.total_sent = self.total_sent + 1
                            return True
                        #print(r.json())
                        #print(r.status_code)
                        return False
                    #print(r.json())
                    #print(r.status_code)
                    return False
                #print(r.json())
                #print(r.status_code)
                return False
            #print(r.json())
            #print(r.status_code)
            return False
        except Exception as err:
            pass
            #print(err)
    
    def getEvents(self):
        rdata = {
            "id": self.client_id,
        }
        try:
            r2 = requests.post(url=f"https://front{self.server_id}.omegle.com/events", headers=self.headers, proxies=self.proxies, data=rdata, timeout=10)
            print(r2.content)
        except Exception as err:
            pass
            #print(err)
            
    def typing(self):
    
        rdata = {
            "id": self.client_id,
        }
        url = f"https://front{self.server_id}.omegle.com/typing"
        
        try:
            r = requests.post(url, headers=self.headers, data=rdata, proxies=self.proxies, timeout=10)
        except Exception as err:
            pass
            #print(err)
        
    def sendMessage(self):
        
        headers = self.headers
        headers['accept'] = "text/javascript, text/html, application/xml, text/xml, */*"
        rdata = {
            "msg": self.message,
            "id": self.client_id
        }
        url = f"https://front{self.server_id}.omegle.com/send"
        
        try:
            r = requests.post(url, headers=headers, data=rdata, proxies=self.proxies, timeout=10)
            if r.status_code == 200 and r.text == 'win':
                print(f"{Fore.LIGHTBLUE_EX}{Back.MAGENTA}[{threading.current_thread().name}]{Back.RESET} ==> | {Fore.RESET}{Fore.LIGHTBLUE_EX}Message sent:{Fore.RESET} {Fore.LIGHTGREEN_EX}{self.client_id} {Fore.LIGHTBLUE_EX}| Total Sent: {Fore.RESET}{Fore.LIGHTGREEN_EX}{self.total_sent} {Fore.LIGHTBLUE_EX}| Active users:{Fore.RESET} {Fore.LIGHTGREEN_EX}{self.count} {Fore.LIGHTBLUE_EX}| Iterations: {Fore.RESET} {Fore.LIGHTGREEN_EX}{round((self.total_sent/(time.time()-self.start_time))*60, 1)} it/min{Fore.RESET} {Fore.LIGHTBLUE_EX} |")
                for i in range(10):
                    self.getEvents()
                    time.sleep(1)
        except Exception as err:
            pass
            #print(err)
        
    def closeCon(self):
        
        rdata = {
            "id": self.client_id,
        }
        url = f"https://front{self.server_id}.omegle.com/disconnect"
        
        try:
            r = requests.post(url, headers=self.headers, data=rdata, proxies=self.proxies, timeout=10)  
        except Exception as err:
            pass
            #print(err)
