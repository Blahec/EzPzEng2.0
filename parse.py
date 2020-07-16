# Martin

import urllib.request
from urllib.parse import quote
import json
import sys
import re
from colorama import Fore, Style, init



dictionary = None


def set_dictionary(address):
    global dictionary
    dictionary = address


# Calls all the functions needed for obtaining the package, then returns it in form of
# Returns string - the translation
def get_translation(word, language):
    data = get_json(word, language)
    package = create_package_for_database(data, word)
    if package == []:
        print(Fore.LIGHTRED_EX + "Could not find the translation in the dictionary!" + Style.RESET_ALL)
        return None
    return package

# Returs definition in form of a string
def get_definition(word, n):
    set_dictionary("https://dictionary.cambridge.org/dictionary/english/")
    data = get_source_code(word)
    definition = parse_source_code_cambridge(word, data, n)
    return definition


'''
# Connects to url and returns the json got by looking up word
def get_json(word, language):
    API_KEY = "trnsl.1.1.20180504T182025Z.531fc9f4bc67ce19.982233f7c25d7d7e0ffa0645ac2056f5e6c2269d"
    if language == "CZ":
        lang_param = "cs-en"
        word = eliminate_czech_characters(word)
    elif language == "EN":
        lang_param = "en-cs"
    else:
        sys.stderr.write("No or wrong language set!")
        sys.exit()
    URL = "https://translate.yandex.net/api/v1.5/tr.json/translate?key={0}" \
          "&text={1}&lang={2}".format(API_KEY, word, lang_param)
    data = urllib.request.urlopen(URL).read()
    return data
'''


def get_json(word, language):
    langs = ('cs', 'eng') if language == 'CZ' else ('eng', 'cs')
    URL = "https://glosbe.com/gapi/translate?from={0}&dest={1}&format=json&phrase={2}"\
        .format(langs[0], langs[1], quote(word).replace(" ", "%20"))

    data = urllib.request.urlopen(URL).read()
    return data


# Returns tuple: (original word, translated word)
# Argument of a function is a json object
def create_package_for_database(json_data, word):
    parsed = json.loads(json_data)
    translated_words = [record['phrase']['text'] for record in parsed['tuc'] if 'phrase' in record]
    return translated_words


def to_ascii(letter):
    non_ascii = ('á', 'č', 'ď', 'é', 'ě', 'í', 'ó', 'ř', 'š', 'ť', 'ú', 'ů', 'ý', 'ž')
    if letter == non_ascii[0]:
        return 'a'
    if letter == non_ascii[1]:
        return 'c'
    if letter == non_ascii[2]:
        return 'd'
    if letter == non_ascii[3] or letter == non_ascii[4]:
        return 'e'
    if letter == non_ascii[5]:
        return 'i'
    if letter == non_ascii[6]:
        return 'o'
    if letter == non_ascii[7]:
        return 'r'
    if letter == non_ascii[8]:
        return 's'
    if letter == non_ascii[9]:
        return 't'
    if letter == non_ascii[10] or letter == non_ascii[11]:
        return 'u'
    if letter == non_ascii[12]:
        return 'y'
    if letter == non_ascii[13]:
        return 'z'


def eliminate_czech_characters(word):
    non_ascii = ('á', 'č', 'ď', 'é', 'ě', 'í', 'ó', 'ř', 'š', 'ť', 'ú', 'ů', 'ý', 'ž')
    for letter in word:
        if letter in non_ascii:
            word = word.replace(letter, to_ascii(letter))
    return word


# Finds a word on a webpage dictionary and returns the source code of the result
def get_source_code(word):
    data = urllib.request.urlopen("{0}{1}".format(dictionary, word)).read()
    return data

# finds n-th definition
def parse_source_code_cambridge(word, data, n):
    #pattern = r"{0} definition: (?P<definition>[a-zA-Z,\.1\-\)\(\= ]*)".format(word)
    pattern = r"\"{0} definition: (?P<definition>[a-zA-Z1-9,\.;&:\-\)\(\= ]*)\"".format(word)
    definition = re.search(pattern, str(data))
    if not definition:
        print(Fore.LIGHTRED_EX + "Could not find the definition in the dictionary!\n" + Style.RESET_ALL)
        return None
    definition = definition.group("definition")
    if not ("{0}".format(n) in definition):
        return "-1"
    definition = definition.split("{0}. ".format(n))
    definition = (definition[1] if (len(definition) > 1) else definition[0])

    if (not ("{0}".format(n+1) in definition)) and "&hellip" in definition:
    	definition = definition.split("&hellip")
    	definition = definition[0]
    
    if ":" in definition:
        definition = definition.split(":")
        definition = definition[0]


    return definition
