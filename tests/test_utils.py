import math
import utils


# Returns dictionary in form {'Apple': value, ...}, where value says how much it is appropriate to test the word
# data comes in the same form as in the database
def give_value_to_words(data, test_data):
    values = {}
    for record in data:
        if not record in test_data:
            values[record] = calculate_value(process_data(record, data[record], None))
        else:
            values[record] = calculate_value(process_data(record, data[record],  test_data[record]))
    return values


# Returns tuple: (lookups, last_lookup, priority, number_of_tests, last_test, score)
# data and test_data are for the particular word only
def process_data(record, data, test_data):
    word = record
    lookups = data['searches']
    last_lookup = data['date'][-1]
    #priority = data['priority']
    priority = 0
    if not test_data:
        number_of_tests = 0
        last_test = None
        score = None
    else:
        number_of_tests = 0
        fails = 0
        last_test = [1000, 0, 0]
        for date in test_data['test_results']:
            array_date = utils.string_to_array(date)
            if utils.is_later(array_date, last_test):
                last_test = array_date
            for score in test_data['test_results'][date]:
                number_of_tests += 1
                if score == 0:
                    fails += 1
        score = (number_of_tests - fails)/number_of_tests
    return [lookups, last_lookup, priority, number_of_tests, last_test, score]


# parameters: lookups, last_lookup, priority, number_of_tests, last_test, score
def calculate_value(parameters):
    today_date = utils.today_to_array()
    if not parameters[3]:
        parameters[3] = 0
        parameters[4] = today_date
        parameters[5] = 0
    return 10*parameters[2] - (parameters[5]**2)*parameters[3]*3 + 5*parameters[0] + utils.date_distance(today_date, parameters[4]) \
           + math.fabs(utils.date_distance(today_date, parameters[1]) - 5)

