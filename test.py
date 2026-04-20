RELEASE = "beta"
VERSION = 1.0

import requests

def check_for_update():
    url = "https://raw.githubusercontent.com/Beato029/PySafety/main/Version/version.json"

    req = requests.get(url).json()

    release = req["release"]
    verison = req["version"]

    return [release, verison]