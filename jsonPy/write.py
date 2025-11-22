import json
from jsonPy import readJson

def writeJson(data, file):
    try:
        old_data = readJson(file)

        old_data.update(data)
    except:
        old_data = data

    with open(file, "w") as file:
        json.dump(old_data, file, ensure_ascii=4)


# data = {"paese": "italy"}