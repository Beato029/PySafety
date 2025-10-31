import json
import requests

def readData():
    try:
        with open("settings.json", "r") as file:
            data = json.load(file)
    except:
        with open("settings.json", "w") as file:
            data = {
                "host_default": "127.0.0.1",
                "port_default": "8080",
                "check_update": True
            }
            data_json = json.dumps(data)
            json.dump(data_json, file, indent=4, ensure_ascii=True)

    with open("settings.json", "r") as file:
        data = json.load(file)

    return data


def checkForUpdate():
    TYPE = "beta"
    VERSION = "1"

    req = requests.get("https://raw.githubusercontent.com/Beato029/PySafety/refs/heads/main/version.json")
    data = req.json()

    type_version = data.get("type_version")
    latest_version = data.get("latest_version")

    