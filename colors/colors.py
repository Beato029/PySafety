import colorama
from colorama import Fore

def Colors():
    colorama.init(autoreset=True)

    BOLD = '\033[1m'

    red = BOLD + Fore.LIGHTRED_EX
    green = BOLD + Fore.LIGHTGREEN_EX
    blue = BOLD + Fore.LIGHTBLUE_EX
    yellow = BOLD + Fore.LIGHTYELLOW_EX
    magenta = BOLD + Fore.LIGHTMAGENTA_EX
    cyan = BOLD + Fore.LIGHTCYAN_EX

    RESET = BOLD + Fore.LIGHTWHITE_EX


    return red, green, blue, yellow, magenta, cyan, RESET