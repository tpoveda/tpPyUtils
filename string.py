#! /usr/bin/env python

"""
Module that contains utility functions related with strings
"""


from __future__ import print_function, division, absolute_import, unicode_literals


# region Imports
import re
import os
# endregion

# region Constants
iters = [list, tuple, set, frozenset]
class _hack(tuple): pass
iters = _hack(iters)
iters.__doc__ = """
A list of iterable items (like lists, but not strings). Includes whichever
of lists, tuples, sets, and Sets are available in this version of Python.
"""
# endregion


def _strips(direction, text, remove):
    """
    Strips characters on a certain direction
    :param direction: str, strip direction ("r", "R", "l" or "L")
    :param text: str, text so strip
    :param remove: variant<iter>, elements to remove
    :return:
    """
    if isinstance(remove, iters):
        for subr in remove:
            text = _strips(direction, text, subr)
        return text

    if direction == 'l' or direction == 'L':
        if text.startswith(remove):
            return text[len(remove):]
    elif direction == 'r' or direction == 'R':
        if text.endswith(remove):
            return text[:-len(remove)]
    else:
        raise ValueError("Direction needs to be r or l.")
    return text


def rstrips(text, remove):
    """
    Removes the string `remove` from the right of `text`
    >>> rstrips("foobar", "bar")
    'foo'
    """
    return _strips('r', text, remove)


def lstrips(text, remove):
    """
    Removes the string `remove` from the left of `text`
    >>> lstrips("foobar", "foo")
    'bar'
    >>> lstrips('http://foo.org/', ['http://', 'https://'])
    'foo.org/'
    >>> lstrips('FOOBARBAZ', ['FOO', 'BAR'])
    'BAZ'
    >>> lstrips('FOOBARBAZ', ['BAR', 'FOO'])
    'BARBAZ'
    """
    return _strips('l', text, remove)


def strips(text, remove):
    """
    removes the string `remove` from the both sides of `text`
    >>> strips("foobarfoo", "foo")
    'bar'
    """
    return rstrips(lstrips(text, remove), remove)


def normalize(string):
    """
    Replace all invalid characters with "_"
    :param string: str, string to normalize
    :return: str, normalize string
    """

    string = str(string)

    if re.match('^[0-9]', string):
        string = '_' + string

    return re.sub("[^A-Za-z0-9_-]", "_", str(string))


def remove_invalid_character(string, regex="[^A-Za-z0-9]"):
    """
    Remove all invalid character
    :param string: str, string to normalize
    :return: str, valid string
    """

    return re.sub(regex, "", str(string))


def clean_string(text):
    """
    Returns a cleaned version of a string - removes everything but alphanumeric and characters and dots
    :param text:  str, string to clean
    :return: str, cleaned string
    """

    return re.sub(r'[^a-zA-Z0-9\n\.]', '_', text)


def replace_sharp_with_padding(string, index):
    """
    Replace a list of # symbol with properly padded index (i.e, count_### > count_001)
    :param string: str, string set. Should include '#'
    :param index: int, index to replace
    :return: str, normalized string
    """

    if string.count("#") == 0:
        string += "#"

    digit = str(index)
    while len(digit) < string.count("#"):
        digit = "0" + digit

    return re.sub("#+", digit, string)


def extract(string, start='(', stop=')'):
    """
    Extract the string that is contained between start and stop strings
    :param string: str, string to process
    :param start: str, start string
    :param stop: str, stop string
    :return: str, extracted string
    """

    try:
        return string[string.index(start)+1:string.index(stop)]
    except:
        return string


def format_path(path):
    """
    Takes a path and format it to forward slashes
    :param path: str
    :return: str
    """

    return os.path.normpath(path).replace('\\', '/').replace('\t', '/t').replace('\n', '/n').replace('\a', '/a')


def format_path_join(path, *paths):
    """
    os.path.join wrapper that returns always a valid Python path
    :param path:  str
    :param paths: str
    :return: str
    """

    return format_path(os.path.join(path, *paths))


def strip_prefix(name, split='_'):
    """
    Strips prefix
    :param name: str, name to strip prefix of
    :param split: str, split character
    :return: str
    """

    if not name.count(split):
        return name

    return split.join(name.split(split)[1:])

def strip_suffix(name, split='_'):
    """
    Returns the portion of name minus the last element separated by the splitter character
    :param name: str, name to strip the suffix from
    :param split: str, split character
    :return: str
    """

    if not name.count(split):
        return name

    return name.replace(split+name.split(split)[-1], '')


def add_prefix(prefix, split, string):
    """
    Adds a prefix to the given string
    :param prefix: str, prefix to add to the string
    :param split: str, split character
    :param string: str, string to add prefix to
    :return: str
    """
    return split.join([prefix, string])


def get_prefix(string, split):
    """
    Returns the prefix of the given string
    :param string: str, string to get prefix of
    :param split: str, split character
    :return: str
    """
    return string.split(split)[0]


def camel_case_to_string(camel_case_string):
    """
    Converts a camel case string to a normal one
    testPath --> test Path
    :param camel_case_string: str
    :return: str
    """

    return re.sub("([a-z])([A-Z])", "\g<1> \g<2>", camel_case_string)


def string_to_camel_case(string):
    """
    Converts a string to a camel case one
    test path --> TestPath
    :param string: str
    :return: str
    """

    return ''.join(x for x in string.title() if not x.isspace())


def camel_case_to_lower_case_underscore(text):
    """
    Converts camel case string to underscore separate string
    :param text: str, string to convert
    :return: str
    """

    words = list()
    char_pos = 0
    for curr_char_pos, char in enumerate(text):
        if char.isupper() and char_pos < text:
            words.append(text[char_pos:curr_char_pos].lower())
            char_pos = curr_char_pos
    words.append(text[char_pos:].lower())
    return '_'.join(words)


def camel_case_to_title(text):
    """
    Split string by upper case letters and return a nice name
    :param text: str, string to convert
    :return: str
    """

    words = list()
    char_pos = 0
    for curr_char_pos, char in enumerate(text):
        if char.isupper() and char_pos < curr_char_pos:
            words.append(text[char_pos:curr_char_pos].title())
            char_pos = curr_char_pos
    words.append(text[char_pos:].title())
    return ' '.join(words)


def lower_case_underscore_to_camel_case(text):
    """
    Converts string or unicdoe from lower case underscore to camel case
    :param text: str, string to convert
    :return: str
    """

    # NOTE: We use string's class to work on the string to keep its type
    split_string = text.split('_')
    class_ = text.__class__
    return split_string[0] + class_.join('', map(class_.capitalize, split_string[1:]))


def get_trailing_number(input_string, as_string=False, number_count=-1):
    """
    Get the number at the very end of a string. If number not at the end of the string return None
    :param input_string: str
    :param as_string: bool
    :param number_count: int
    :return: varianht, str || None
    """

    if not input_string:
        return None

    number = '\d+'
    if number_count > 0:
        number = '\d' * number_count

    group = re.match('([a-zA-Z_0-9]+)(%s$)' % number, input_string)
    if group:
        number = group.group(2)
        if as_string:
            return number
        else:
            return int(number)


def get_string_index(index, padding=2):
    """
    Returns the string equivalent for the given integer index
    :param index: int, the index to get the string equivalent for
    :param padding: int, number of characters for the index string
    :return: str
    """

    str_ind = str(index)
    for i in range(padding-len(str_ind)):
        str_ind = '0'+str_ind

    return str_ind


def get_alpha(value, capital=False):
    """
    Convert an integer value to a character. a-z then double, aa-zz etc.
    @param value: int, Value to get an alphabetic character from
    @param capital: boolean: True if you want to get capital character
    @return: str, Character from an integer
    """

    # Calculate number of characters required
    base_power = base_start = base_end = 0
    while value >= base_end:
        base_power += 1
        base_start = base_end
        base_end += pow(26, base_power)
    base_index = value - base_start

    # Create alpha representation
    alphas = ['a'] * base_power
    for index in range(base_power - 1, -1, -1):
        alphas[index] = chr(97 + (base_index % 26))
        base_index /= 26

    if capital:
        return ''.join(alphas).upper()

    return ''.join(alphas)
