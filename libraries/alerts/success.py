from colors import Colors

green = Colors()[1]
RESET = Colors()[6]

def Success(text):
    print(green + f"[+] {text}" + RESET)