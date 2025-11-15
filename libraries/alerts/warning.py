from colors import Colors

yellow = Colors()[3]
RESET = Colors()[6]

def Warning(text):
    print(yellow + f"[-] {text}" + RESET)