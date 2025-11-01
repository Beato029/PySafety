import colorama
from colorama import Fore
import pyfiglet

colorama.init(autoreset=True)

red = Fore.LIGHTRED_EX
green = Fore.LIGHTGREEN_EX
yellow = Fore.LIGHTYELLOW_EX
blue = Fore.LIGHTBLUE_EX
cyan = Fore.LIGHTCYAN_EX
reset = Fore.RESET

TYPE = "beta"
VERSION = "1"

def Logo():
    logo = pyfiglet.figlet_format("PySafety")
    print(green + logo)
    print(green + f"Versione: {TYPE} {VERSION}\n")