__author__ = 'dandrade'
import re


def write_vision_types(char_name, vision_name):
    file = open('_vision-types.txt', '+a')
    file.write('CharName   : %s\n'
               'VisionName : %s\n\n' % (char_name, vision_name))
    file.close()

def clean_name(name):
    name = str.replace(str(name), " (combat trained) ", "")
    name = str.replace(name, " (combat trained)", "")
    name = str.replace(name, "(combat trained)", "")
    name = re.sub(r'([^\s\w]|_)+', '', name)
    name = str.replace(name, "  ", " ")

    return name


def pretty_html(text):
    text = str.replace(text, '\n', '<br>')
    text = str.replace(text, 'Benefit:', '<b>Benefit:</b>')
    text = str.replace(text, 'Benefits:', '<b>Benefits:</b>')
    text = str.replace(text, 'Special:', '<b>Special:</b>')
    text = str.replace(text, 'Requirement:', '<b>Requirement:</b>')
    text = str.replace(text, 'Requirements:', '<b>Requirements:</b>')
    text = str.replace(text, 'Prerequisite:', '<b>Prerequisite:</b>')
    text = str.replace(text, 'Prerequisites:', '<b>Prerequisites:</b>')
    text = str.replace(text, 'Normal:', '<b>Normal:</b>')
    return text


def html_sanitize(html):
    """
    Replaces all special characters, which are known to cause problems with maptool. This function replaces
    special characters with the correct 'escaped html' entity.

    Thanks to http://www.htmlescape.net/htmlescape_tool.html website

    :param html: html string to be escaped
    :return: 'escaped html' entity for given 'html' string
    """
    map = {"\&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;", "'": "&#x00b4;", "\n": "&lt;br&gt;\n"}
    escaped = replace_all(html, map)
    return escaped


def replace_all(text, dic):
    """
    Replaces all occurrences of provided dictionary 'key' by dictionary 'key value' in given str

    :param str: the given str to be replaced
    :param dic: dictionary containing key to search and value to replace
    :return: a copy of the str with all occurrences of 'dic' keys replaced by dic 'values'

    Example:
    <code>
        # our text the replacement will take place
        my_text = 'Hello everybody.'

        # our dictionary with our key:values.
        # we want to replace 'H' with '|-|'
        # 'e' with '3' and 'o' with '0'
        reps = {'H':'|-|', 'e':'3', 'o':'0'}

        # bind the returned text of the method
        # to a variable and print it
        txt = replace_all(my_text, reps)
        print txt    # it prints '|-|3ll0 3v3ryb0dy'

        # of course we can print the result
        # at once with:
        # print replace_all(my_text, reps)
    </code>
    """
    for k, v in dic.items():
        text = str.replace(text, k, v)
    return text
