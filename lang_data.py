# Jada
import json
import os


def load(file_name, language):
    if not os.path.exists(file_name):
        if not os.path.exists("data"):
            os.makedirs("data")
        file_object = open(file_name, 'w')
        file_object.write("{}\n")
        file_object.close()
    with open(file_name, "r") as file:
        return json.load(file)


def load_records(language):
    file_name = "data/data" + language + ".json"
    return load(file_name, language)


def save_records(records, language):
    file_name = "data/data" + language + ".json"
    with open(file_name, "w") as file:
        json.dump(records, file)
        file.write("\n")


def delete(word, language):
    records = load_records(language)
    records.pop(word)
    save_records(records, language)


def load_own_dict(language):
    file_name = "data/your_dict" + language + ".json"
    return load(file_name, language)


def save_own_dict(records, language):
    file_name = "data/your_dict" + language + ".json"
    with open(file_name, "w") as file:
        json.dump(records, file)
