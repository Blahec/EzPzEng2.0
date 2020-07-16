# Martin
# Database of all the records of tests

import json
import os
import utils


def load_records(language):
    file_name = "tests/tests_data" + language + ".json"
    if not os.path.exists(file_name):
        file_object = open(file_name, 'w')
        file_object.write("{}")
        file_object.close()
    with open(file_name, "r") as file:
        return json.load(file)


def save_records(records, language):
    file_name = "tests/tests_data" + language + ".json"
    with open(file_name, "w") as file:
        json.dump(records, file)


# score is either 0 in case of fail in test or 1 in case of success
# date_of_test is the date when the test was written
# database looks like: {'Apple':{'test_results':{(24, 05, 2018):[1,0]}}, 'Lemon':...}
def add_test_record(word, score, language):
    records = load_records(language)
    date = utils.today_to_array()
    date = utils.array_to_string(date)
    if word in records:
        if date in records[word]["test_results"]:
            records[word]["test_results"][date].append(score)
        else:
            records[word]["test_results"][date] = [score]
    else:
        records[word] = {}
        records[word]["test_results"] = {}
        records[word]["test_results"][date] = [score]
    save_records(records, language)