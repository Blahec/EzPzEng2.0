from tests import test_results_data
import lang_data
import random
import utils
from query import query_utils
from tests import test_utils


'''
def add_word(word, to, package, lang):
    record = (word,  {'to': to, 'definition': '', 'searches': 1, 'dates': [utils.today_to_array()], 'priority': 2, 'packages': [package]})
'''


def get_all_packages(language):
    records = lang_data.load_records(language)
    packages = []
    for record in records.values():
        for package in record['packages']:
            if package not in packages:
                packages.append(package)
    return packages


def rename_package(new_package, old_package, language):
    records = lang_data.load_records(language)
    for record in records.values():
        if old_package in record['packages']:
            index = record['packages'].index(old_package)
            record['packages'][index] = new_package
    lang_data.save_records(records, language)


def join_packages(new_package, packages, language):
    records = lang_data.load_records(language)
    for record in records.values():
        if len(set(record['packages']) & set(packages)) >= 1: # intersection
            if new_package not in record['packages']:
                record['packages'].append(new_package)
    lang_data.save_records(records, language)


# Return array [word, def, to] only with words with the package
def retrieve_package_records(language, package):
    records = lang_data.load_records(language)
    filtred_records = query_utils.filter_package(records, package)
    return [[word, record['definition'], record['to']] for (word, record) in filtred_records.items()]


def delete_package(language, package):
    records = lang_data.load_records(language)
    records_without_package = query_utils.filter_without_package(records, package)
    lang_data.save_records(records_without_package, language)


# Retrieves random words, ignoring packages and priorities
# Returns them in form of ('Apple', record of apple in database)
def retrieve_random_records(language, number_of_records, mode, package):
    data = lang_data.load_records(language)
    data = query_utils.filter_mode(data, mode)
    if package != 'default':
        data = query_utils.filter_package(data, package)
    length = len(data)
    if number_of_records > length:
        number_of_records = length
    indexes = random.sample(range(0, length), number_of_records)
    test_records = {}
    list_of_records = list(data)
    for index in indexes:
        test_records[list_of_records[index]] = data[list_of_records[index]]
    return test_records


# Returns list of words with the biggest values according to the function in calculations_on_data
def retrieve_smartly_records(language, number_of_records, mode, package):
    data = lang_data.load_records(language)
    if package != 'default':
        data = query_utils.filter_package(data, package)
    data = query_utils.filter_mode(data, mode)
    length = len(data)
    if number_of_records > length:
        number_of_records = length
    test_data = test_results_data.load_records(language)
    values = test_utils.give_value_to_words(data, test_data)
    values = sorted(values, key=values.get, reverse=True)
    result = {}
    for word in values:
        if number_of_records == 0:
            break
        result[word] = data[word]
        number_of_records -= 1

    return result


# Lang DB:
# record = {to lang, definition, # of searches, [[24, 11, 2018], ...], priority, packages}

def new_record(definition, package, translation=''):
    return {'definition': definition, 'to': translation, 'searches': 1,
            'date': [utils.today_to_array()], 'priority': 2, 'packages': [package]}


def add_package(record, package):
    if package not in record['packages']:
        record['packages'].append(package)


def edit_word(from_word, to_word, language):
    records = lang_data.load_records(language)

    records[from_word]['to'] = to_word
    lang_data.save_records(records, language)


def edit_definition(from_word, definition, language):
    records = lang_data.load_records(language)
    records[from_word]['definition'] = definition


def get_saved_translation(from_word, language):
    records = lang_data.load_records(language)
    if from_word in records:
        return records[from_word]['to']
    return None


# dict = own dict or default
def add_word(from_word, to_word, language, package='default'):
    records = lang_data.load_records(language)

    if from_word in records:
        if records[from_word]['to'] == '':
            records[from_word]['to'] = to_word
        records[from_word]['searches'] += 1
        records[from_word]['date'].append(utils.today_to_array())
        records[from_word]['to'] = to_word  # !! Rewrites the word, whereas add_both not !! (works but it's really mess)

        add_package(records[from_word], package)
    else:
        record = new_record("", package, to_word)
        records[from_word] = record

    lang_data.save_records(records, language)


def add_definition(from_word, definition, package='default', lang='EN'):
    records = lang_data.load_records(lang)

    if from_word in records:
        if records[from_word]['definition'] == '':
            records[from_word]['definition'] = definition
        records[from_word]['searches'] += 1
        records[from_word]['date'].append(utils.today_to_array())
        add_package(records[from_word], package)
    else:
        records[from_word] = new_record(definition, package)

    lang_data.save_records(records, lang)


def add_both(from_word, to_word, definition, package='default', lang='EN'):
    records = lang_data.load_records(lang)

    if from_word in records:
        if records[from_word]['definition'] == '':
            records[from_word]['definition'] = definition
        if records[from_word]['to'] == '':
            records[from_word]['to'] = to_word
        records[from_word]['searches'] += 1
        records[from_word]['date'].append(utils.today_to_array())
        add_package(records[from_word], package)
    else:
        records[from_word] = new_record(definition, package, to_word)

    lang_data.save_records(records, lang)


def change_priority(word, sign, language):
    records = lang_data.load_records(language)
    records[word]['priority'] = (1 if sign == '-' else 3)
    lang_data.save_records(records, language)