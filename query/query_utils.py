# Return records with package
def filter_package(records, package):
    return {word: record for (word, record) in records.items() if package in record['packages']}


# Return records without package
def filter_without_package(records, package):
    return {word: record for (word, record) in records.items() if package not in record['packages']}


#! Will have to be changed after more definitions are added
def filter_mode(data, mode):
    if mode == 'def':
        return {word: record for (word, record) in data.items() if "" != record['definition']}
    if mode == 'tr':
        return {word: record for (word, record) in data.items() if "" != record['to']}
    return data
