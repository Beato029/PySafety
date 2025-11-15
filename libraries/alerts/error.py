from colors import Colors

red = Colors()[0]
RESET = Colors()[6]

def Error(text):
    print(red + f"[-] {text}" + RESET)

