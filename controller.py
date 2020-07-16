import lang_data
import parse
import sys
from tests import knowledge_tests
from query import query
from colorama import Fore, Style, init
from utils import iinput

# Initializes colorama
init()

MARTINE_TADY_JE_TEN_LIMIT = 5

def welcome():
    print(Fore.LIGHTYELLOW_EX + "Welcome to the english dictionary!" + Style.RESET_ALL)
    

def test(lang, type_of_test):

    print(Fore.LIGHTYELLOW_EX + "Do you want to test any particular package?"
                                " (type yes or no): " + Style.RESET_ALL, end="")
    package_will = input()
    if package_will == 'yes' or package_will == 'y':
        print(Fore.LIGHTYELLOW_EX + "Type in the name of the package: " + Style.RESET_ALL, end="")
        package = iinput()
    else:
        package = 'default'
    mode = 'def'
    if lang == 'EN':
        print(Fore.LIGHTYELLOW_EX + "Do you want to test by translations (t) or definitions (d)?"
                                    ": " + Style.RESET_ALL, end="")
        if iinput() == 't':
            mode = 'tr'
    else:
        mode = 'tr'

    print(Fore.LIGHTYELLOW_EX + "How many words do you want in the test: " + Style.RESET_ALL, end="")
    number_of_tests = int(iinput())
    if type_of_test == 'random':
        knowledge_tests.random_test(number_of_tests, lang, mode, package)
    if type_of_test == 'smart':
        knowledge_tests.smart_test(number_of_tests, lang, mode, package)
    sys.exit()


def translation_mode():
    if '-tr' in sys.argv and '-def' in sys.argv:
        return 'TRA+DEF'
    elif '-tr' in sys.argv or '-cz' in sys.argv:
        return 'TRA'
    elif '-def' in sys.argv:
        return 'DEF'
    return 'TRA+DEF'


def help():
    print("There are two main modes: normal for translating words and test mode")
    print("Normal mode:")
    print("     Normal mode is used for translating words. If you want to translate english word, you can get czech translation, english definition or both.")
    print("     To translate czech word, type -cz.")
    print("     To translate english word, type -en or nothing. You will get definition and translation.")
    print("         To get only translation, type -tr.")
    print("         To get only definition, type -def.")
    print("     After you define what you want, you will enter insert state. Write word you want to translate. Then, you have many options what to write next:")
    print("         next word to be translated")
    print("         'q' to quit the program")
    print("         'd' to delete the last found word")
    print("         'number' to save the appropriate word")
    print("         'n' to list all definitions (you can choose one of them to be saved)")
    print("         'p' and '+' to increase priority of the word or '-' to decrease")
    print("         'cz' or 'en' to change language")
    print("     Packages")
    print("         When you start program, you can add '-p name_of_package' to previous parameters to define in what package will the words be stored. If not specified, the package is 'default'.")
    print("Test mode:")
    print("     Martín napíše")
    print("Add word:")
    print("     You can add you own words and translations.")
    print("     Start program with -add (and other optional parameters like -p or -cz). Then, type the word and its translation. When you want to quit, type 'q' and enter.")
    print("Other commands:")
    print("     '-pp name' (print package): Lists all words in the package")
    print("         write '-pp name > file_name.txt' to save it in file")
    print("     '-dp name' (delete package): Deletes all words in the package")


def color_print(sentence, color):
    if color == 'yellow':
        print(Fore.YELLOW + sentence + Style.RESET_ALL, end="")
    if color == 'lcyan':
        print(Fore.LIGHTCYAN_EX + sentence + Style.RESET_ALL, end="")
    if color == 'lyeallow':
        print(Fore.LIGHTYELLOW_EX + sentence + Style.RESET_ALL, end="")


def color_print_n(sentence, color):
    color_print(sentence, color)
    print()


def print_words(from_word, words):
    translation = query.get_saved_translation(from_word, lang)
    print("->", end=" ")
    len_words = len(words)
    match = False
    last = len_words-1 #min( , MARTINE_TADY_JE_TEN_LIMIT-1)
    for i in range(last):
        color = 'lcyan'
        if words[i] == translation:
            color = 'yellow'
            match = True
        color_print(words[i], color)
        print(" ({0}), ".format(i + 1), end='')
    color = 'lcyan'
    if words[last] == translation:
        color = 'yellow'
        match = True
    color_print(words[last], color)
    # todo Jada: if the last word is the added, it prints word (number) which it should't
    print(" ({0})".format(last+1), end='')
    # the word is user-defined
    if not match:
        print(", ", end="")
        color_print(translation, 'yellow')
    print(".")


def print_arrow():
    print("->", end=" ")


lang = 'CZ' if '-cz' in sys.argv else 'EN'


if '-test' in sys.argv:
    if '-smart' in sys.argv:
        test(lang, 'smart')
    else:
        test(lang, 'random')


if '-help' in sys.argv:
    help()
    sys.exit()

# delete package
if '-dp' in sys.argv:
    index = sys.argv.index('-dp')
    package = sys.argv[index + 1]
    records = query.delete_package(lang, package)
    sys.exit("Deleted {0} package.".format(package))

# print package
if '-pp' in sys.argv:
    index = sys.argv.index('-pp')
    package = sys.argv[index + 1]
    records = query.retrieve_package_records(lang, package)
    for record in records:
        print(record[0])
        if record[1] != '':
            print('     Definition: ' + record[1])
        if record[2] != '':
            print('     Translation: ' + record[2])
    sys.exit()

# print all packages
if '-ap' in sys.argv:
    print("Your packages: ")
    for package in query.get_all_packages(lang):
        print(package, end=', ')
    print()

# should recode to be more intuitive, this was coded just in a few minutes
# rename packages
if '-rp' in sys.argv:
    index = sys.argv.index('-rp') + 1
    old = sys.argv[index]
    new = sys.argv[index + 1]
    query.rename_package(new, old, lang)
    print("Renamed")

# join packages
if '-jp' in sys.argv:
    index = sys.argv.index('-jp') + 1

    new_package = sys.argv[index]
    index += 1

    packages = []

    while index < len(sys.argv):
        packages.append(sys.argv[index])
        index += 1

    query.join_packages(new_package, packages, lang)
    print("Joined")


package = 'default'
if '-p' in sys.argv:
    index = sys.argv.index('-p')
    package = sys.argv[index + 1]


# add word
if '-add' in sys.argv:
    while True:
        print("Word: ", end='')
        word = input()
        if word == 'q':
            sys.exit()
        print("Translation: ", end='')
        translation = input()
        if translation == 'q':
            sys.exit()
        query.add_word(word, translation, lang, package)

original_mode = translation_mode()
mode = original_mode

welcome()


# todo Jada: too much from_word = input()
# todo Jada: Zkratit nejdelsi funkci ever, co to je za necistoty
# not todo Blahec: Co mi do toho kecas, moje kody, moje decisions
from_word = iinput()
n = 1
while from_word != 'q':

    words = []
    if from_word == 'cz':
        print("Changed source language to czech.")
        lang = "CZ"
        mode = 'TRA'
        from_word = input()
    elif from_word == 'en':
        print("Changed source language to english.")
        lang = "EN"
        mode = original_mode
        from_word = input()

    if mode == 'TRA':
        found = (parse.get_translation(from_word, lang))
        saved = query.get_saved_translation(from_word, lang)
        words = []

        if found is not None:
            words.extend(found[:MARTINE_TADY_JE_TEN_LIMIT])

        if saved is not None and (found is None or saved not in found):
            words.append(saved)

        if len(words) != 0:
            if saved is None:
                query.add_word(from_word, words[0], lang, package)
            print_words(from_word, words)
        new_word = iinput()
        # if change word
        if new_word.isdigit():
            # todo: choice is in range
            query.edit_word(from_word, words[int(new_word) - 1], lang)
            print(Fore.LIGHTMAGENTA_EX + "Added " +
                  from_word + " - " + words[int(new_word) - 1] + Style.RESET_ALL)
            new_word = iinput()
        #print("-> " + Fore.LIGHTCYAN_EX + words[0] + Style.RESET_ALL)
    elif mode == 'DEF':
        definition = parse.get_definition(from_word,n)
        if definition:
            query.add_definition(from_word, definition, package)
            if (definition == "-1"):
                print("-> " + Fore.LIGHTRED_EX + "That's it! " + Style.RESET_ALL)
            else:
                print("-> " + Fore.LIGHTBLUE_EX + definition + Style.RESET_ALL)
        new_word = iinput()
    elif mode == 'TRA+DEF':
        found = (parse.get_translation(from_word, lang))
        saved = query.get_saved_translation(from_word, lang)
        words = []

        if found is not None:
            words.extend(found[:MARTINE_TADY_JE_TEN_LIMIT])

        if saved is not None and (found is None or saved not in found):
            words.append(saved)

        definition = parse.get_definition(from_word,n)

        # both
        if definition and len(words) != 0:
            query.add_both(from_word, words[0], definition, package)
            print("-> " + Fore.LIGHTBLUE_EX + definition + Style.RESET_ALL, end='')
            input()
            #print("->", end=" ")
            #color_print(words[0], "yellow")
        # just definitions
        elif definition:
            query.add_definition(from_word, definition, package, lang)
            print("-> " + Fore.LIGHTBLUE_EX + definition + Style.RESET_ALL)
        # just translations
        elif len(words) != 0:
            if saved is None:
                query.add_word(from_word, words[0], lang, package)
        # all translations
        if len(words) != 0:
            print_words(from_word, words)
            new_word = iinput()
            # if change word
            if new_word.isdigit():
                # todo: choice is in range
                query.edit_word(from_word, words[int(new_word) - 1], lang)
                print(Fore.LIGHTMAGENTA_EX + "Added " + from_word + " - " +
                      words[int(new_word) - 1] + Style.RESET_ALL)
                new_word = iinput()
        else:
            #print("Could not find the translation in the dictionary!")
            new_word = iinput()

    
    # Delete last record
    if new_word == 'd':
        lang_data.delete(from_word, lang)
        new_word = iinput()
    if new_word == 'p':
        print("decrease priority \'-\' or increase \'+\':", end=" ")
        priority = input()
        query.change_priority(from_word, priority, lang)
        new_word = iinput()
    
    # Next definition
    if new_word == 'n':
        n = n+1
        new_word = from_word  
    else: n = 1

    from_word = new_word
