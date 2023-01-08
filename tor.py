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



class TorProxy:
    
    def __init__(self, i):
        
        self.base_port = 9050
        self.it_port = self.base_port + i
        self.tor_process = []
        
    def create_tor(self):

        self.SOCKS_PORT = self.it_port
        self.TOR_PATH = os.path.normpath(os.getcwd()+"\\tor\\tor.exe")
        self.tor_process.append(stem.process.launch_tor_with_config(
        config = {
        'SocksPort': str(self.SOCKS_PORT),
        },
        tor_cmd = self.TOR_PATH
        ))
        return self.SOCKS_PORT, self.tor_process
    
    def new_tor(self):
        self.tor_process.kill()
        self.SOCKS_PORT = self.create_tor()
        return self.SOCKS_PORT
    
    def kill_tor(self, i):
        self.tor_process[0].kill()