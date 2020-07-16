import sys
from colorama import Fore, Style
from query import query
from tests import test_results_data
from parse import eliminate_czech_characters


# Tested data should always be in the form analogical to the one in database:
# {'first word / definition to be tested': {'to': correct answer, additonal data}}
class Test:

    def __init__(self, words, language, mode='def', save=True):
        if words is None:
            sys.stderr.write("No words to test!")
            sys.exit()
        # Words are in the same form as in the database
        self.records = words
        self.language = language
        self.mode = mode
        self.save_to_database = save
        #!self.test_records =

    def test_the_user(self):
        failed_words = {}
        for record in self.records:
            if self.mode == 'tr':
                print(Fore.LIGHTBLUE_EX + record + Style.RESET_ALL + ":", end=" ")
            if self.mode == 'def':
                print(Fore.LIGHTBLUE_EX + self.records[record]['definition'] + Style.RESET_ALL + ":", end=" ")
            answer = input()
            self.process_answer(record, answer, failed_words)
        print(Fore.CYAN + "\n-------------------End of the test-------------------\n" + Style.RESET_ALL)
        print(Fore.LIGHTYELLOW_EX + 'Do you want to review the results (r) or take the test with failed words (t) '
                          'or end (q) ?' + Style.RESET_ALL)
        choice = input()
        if choice == 't':
            subtest = Test(failed_words, self.language, self.mode, save=False)
            subtest.test_the_user()
        if choice == 'r':
            for word in failed_words:
                if self.mode == 'def':
                    print(Fore.YELLOW + word + ' : ' + Fore.LIGHTBLUE_EX + self.records[word]['definition'] +
                          Style.RESET_ALL)
                if self.mode == 'tr':
                    print(Fore.YELLOW + word + ' : ' + Fore.YELLOW + self.records[word]['to'] +
                          Style.RESET_ALL)



# ! Maybe generalize for tr and def together
# Prints all the stuff, adds records to test db and adds word to failed_words if failed
# ! Maybe divide into more functions?
    def process_answer(self, record, answer, failed_words):
        result = None
        if self.mode == 'tr':
            if self.records[record]['to'] == answer or \
                            eliminate_czech_characters(self.records[record]['to']) == answer:
                print(Fore.GREEN + ' |OK| ' + Style.RESET_ALL)
                if self.save_to_database:
                    test_results_data.add_test_record(record, 1, self.language)
            else:
                print(Fore.LIGHTRED_EX + ' |' + self.records[record]['to']
                      + '|' + Style.RESET_ALL)
                if self.save_to_database:
                    test_results_data.add_test_record(record, 0, self.language)
                failed_words[record] = self.records[record]
        if self.mode == 'def':
            if record == answer:
                print(Fore.GREEN + ' |OK| ' + Style.RESET_ALL)
                if self.save_to_database:
                    test_results_data.add_test_record(record, 1, self.language)
            else:
                if self.save_to_database:
                    test_results_data.add_test_record(record, 0, self.language)
                print(Fore.LIGHTRED_EX + record + Style.RESET_ALL)
                failed_words[record] = self.records[record]


# mode: def or tr
def random_test(number_of_words, language, mode, package='default'):
    test_records = query.retrieve_random_records(language, number_of_words, mode, package)
    test = Test(test_records, language, mode)
    test.test_the_user()


def smart_test(number_of_words, language, mode, package='default'):
    test_records = query.retrieve_smartly_records(language, number_of_words, mode, package)
    if mode!='default':
        test = Test(test_records, language, mode)
    else:
        test = Test(test_records, language)
    test.test_the_user()

