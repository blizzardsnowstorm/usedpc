#barebones

import pwinput
import sys
import time
import random
import colorama
import os
import json
import shutil

def slowprint(text, delay=0.015):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
def clearscreen():
    os.system('cls' if os.name == 'nt' else 'clear')
def enterprompt(prompt="[Press ENTER to continue...]"):
    input(prompt)
    print("\n")

clearscreen()
slowprint("You found a shitty PC on the side of the road, in a nice suburb.")
slowprint("You plugged it into the outlet at your local library.")
slowprint("Are you ready to turn it on?")
enterprompt()
clearscreen()
#boot
print("[UEFI] Minimal Firmware Check V1.02")
time.sleep(3)
print("CPU: Intel Celeron N4000 @ 1.10 GHz (4MB cache)")
slowprint("Testing RAM: 4GB DDR4 24000MHz ... [OK]")
slowprint("HDD: Primary Master: 256GB SSD (SATA III) ... [OK]")
print("SystemD Boot Manager - [C A M E L O T]")
slowprint("Loading Kernel 5.4.0-lowpower...")
slowprint("Initializing disk cache ... [OK]")
slowprint("Waking LAN adapter ... [OK]")
slowprint("Starting Input Listener Service ... [RESTARTING]")
slowprint("Running [R E A P E R] integrity check ... [DONE]")
time.sleep(1)

username = input("Create a username: ")
password = input("create a password: ")
p2 = input("confirm password: ")
if p2 == password:
    print("password confirmed")
else:
    print("incorrect password")






