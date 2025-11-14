import colorama
from colorama import Fore

def Colors():
    colorama.init(autoreset=True)

    red = Fore.LIGHTRED_EX
    green = Fore.LIGHTGREEN_EX
    blue = Fore.LIGHTBLUE_EX
    yellow = Fore.LIGHTYELLOW_EX
    magenta = Fore.LIGHTMAGENTA_EX
    cyan = Fore.LIGHTCYAN_EX

    RESET = Fore.RESET

    return red, green, blue, yellow, magenta, cyan, RESET