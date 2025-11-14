import platform
import os
from logo import *

def clear():    
    # Rilevamento semplificato
    so = platform.system().lower()
    if so == "darwin":
        os.system("clear")
    elif so == "windows":
        os.system("cls")
    elif so == "linux":
        os.system("clear")
    else:
        pass


    Logo()