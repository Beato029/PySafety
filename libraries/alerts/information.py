from colors import Colors

blue = Colors()[2]
RESET = Colors()[6]

def Information(text):
    print(blue + f"[*] {text}" + RESET)