import colorama
from colorama import Fore
import pyfiglet
from Command import command
import sys
from clear import *
from CheckUpdate import check

colorama.init(autoreset=True)

red = Fore.LIGHTRED_EX
green = Fore.LIGHTGREEN_EX
yellow = Fore.LIGHTYELLOW_EX
blue = Fore.LIGHTBLUE_EX
cyan = Fore.LIGHTCYAN_EX
reset = Fore.RESET

def warning(text):
    print(yellow + f"[*] {text}")

def checkForUpdate():
    if check.checkForUpdate():
        warning("Nuovo aggiornamento disponiible")

def main():
    clear()
    command.commands()
    sys.exit()


if __name__ == "__main__":
    main()