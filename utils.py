import datetime


def array_to_date(array):
    return datetime.date(array[2], array[1], array[0])


def today_to_array():
    today = datetime.date.today()
    return [today.day, today.month, today.year]


def array_to_string(array):
    arr = [str(number) for number in array]
    return '-'.join(arr)

def string_to_array(array):
    array = array.split('-')
    array = [int(element) for element in array]
    return array

# Approximate
def date_distance(array1, array2):
    return array1[2]*365 + array1[1]*30 + array1[0] - array2[2]*365 - array2[1]*30 - array2[0]

# returns True if the first date is later than the second one
def is_later(array1, array2):
    if array1[2] < array2[2]:
        return True
    if array1[1] < array2[1]:
        return True
    if array1[0] < array2[0]:
        return True
    return False


# Same as input but waits for non EOF non space input
def iinput():
    result = input()
    while result == '' or result == ' ':
        result = input()
    return result
