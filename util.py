__author__ = 'dandrade'


def html_sanitize(html):
    """
    Replaces all special characters, which are known to cause problems on a web  with maptool. This function replaces
    special characters with the correct 'escaped html' entity.

    Thanks to http://www.htmlescape.net/htmlescape_tool.html website

    :param html: html string to be escaped
    :return: 'escaped html' entity for given 'html' string
    """
    map = {"<": "&lt;", ">": "&gt;", "\&": "&amp;", "\"": "&quot;", "'": "&#x00b4;", "\n": "&lt;br&gt;\n"}
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
