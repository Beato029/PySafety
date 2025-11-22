import json

# def readJson(file):
#     with open(file, "r") as file:
#         file = json.load(file)

#     return file


# readJson("settings.json")


def readJson(file):
    with open(file, "r") as file:
        file = json.load(file)

        return file
