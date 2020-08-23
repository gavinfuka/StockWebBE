
##Version = 2020-06-22
import pandas as pd
import json
import os
from termcolor import colored

def CLog(text=None):
    assert text != None
    if '[X]' in text or '[x]' in text:
        print(colored(text, 'red'))
    elif '[o]'  in text or '[O]'  in text:
        print(colored(text, 'green'))
    elif '[-]'  in text:
        print(colored(text,'grey',attrs= ['bold','blink']))
    elif '[!]'  in text:
        print(colored(text, 'yellow'))
    elif '[<]' in text:
        print(colored(text, 'cyan'))
    elif '[>]' in text:
        print(colored(text, 'cyan', attrs=['dark']))
    elif '[v]' in text or '[V]' in text:
        print(colored(text, 'magenta'))
    elif '[*]' in text:
        print(colored(text, 'yellow', attrs=['reverse']))
    elif '[h]' in text:
        print(colored(text, attrs=['reverse']))
    else:
        print(text)

GuideMenu = [
  '[-] Process Debug Log',
  '[o] Success',
  '[x] Error',
  '[!] Warning',
  '[>] Message Sent',
  '[<] Message Received',
  '[v] Finish Stage',
  '[*] Important',
  '[-] Object :: Message',
  '[<] Data << Receive Payload',
  '[>] Data >> Send Payload',
  '[!] Message $$ This is Highlighted [-]',
  '[!] Env !! DEV UAT PREPRD PRD',
  '[W][-] e1234 Error Code',
  '[W] Number : 4567 1234',
  '[!] URL https://www.google.com/',
  '[!] Pattern (4.01s)',
  '[x] Undefined Variable: ',
  '[h] Message is highlighted',
  '[Others]',
  '{Others}'
]

def Guide():
    for msg in GuideMenu:
        CLog(msg)


def CLogRed(text = None):
    assert text != None 
    print(colored(text, 'red'))

def CLogGreen(text = None):
    assert text != None 
    print(colored(text, 'green'))


