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
    if readData()["check_update"]:
        TYPE = "beta"
        VERSION = "1"
    
        req = requests.get("https://raw.githubusercontent.com/Beato029/PySafety/refs/heads/main/version.json")
        data = req.json()

        type_version = data.get("type_version")
        latest_version = data.get("latest_version")


        # Da beta a beta
        if type_version == "beta" and TYPE == "beta" and latest_version > VERSION: 
            print(f"Beta {str(latest_version)} Disponibile (NON si consiglia l'installazione delle versioni beta, perchè potrebbero contenere bug)")
            print("Scaricala da qui: https://github.com/Beato029/PySafety")
            return True

        # da beta a pubblica
        elif type_version == "public" and TYPE == "beta":
            print(f"Versione {str(latest_version)} Disponibile (si consiglia di aggiornare dalla versione di Beta per correggere eventuali bug)")
            print("Scaricala da qui: https://github.com/Beato029/PySafety")
            return True

        # da pubblica a pubblica
        elif type_version == "public" and TYPE == "public" and latest_version > VERSION:
            print(f"Versione {str(latest_version)} Disponibile (Si consiglia di aggiornare per correggere eventuali bug)")
            print("Scaricala da qui: https://github.com/Beato029/PySafety")
            return True

        # da pubblica a beta
        elif type_version == "beta" and TYPE == "public":
            print(f"Beta {str(latest_version)} Disponibile (NON si consiglia di passare da una versione pubblica a una Beta, perchè l'aggiornamento potrebbe causare bug)")
            print("Scaricala da qui: https://github.com/Beato029/PySafety")
            return True

        else:
            print("Nessun aggiornamento disponibile")       
            return False
    
checkForUpdate()