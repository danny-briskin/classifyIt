import typing

from typing import Tuple


def spring_splitter_by_chunks(number_of_chunks: int, string_to_split: str) -> typing.List[str]:
    """
    Splits string into a number of chunks specified
    :param number_of_chunks: number of chunks
    :param string_to_split: string_to_split
    :return: list of strings
    """
    pieces = string_to_split.split()
    return list(
        (" ".join(pieces[i:i + number_of_chunks]) for i in range(0, len(pieces), number_of_chunks)))


def select_maximum_value_in_list_of_tuples(list_of_tuples: typing.List[Tuple[int, float]]) \
        -> typing.List[Tuple[int, float]]:
    """
    Calculates maximum probability in category. Groups incoming list by first tuple value and
        determines maximum value of second value
    :param list_of_tuples: list of probabilities per category :
                        [(1,0.23),(1,0.34),(2,0.56),(2,0.78)]
    :return: a list of maximum probabilities per category
        [(1,0.34),(2,0.78)]
    """
    _tuple = {i: 0 for i, v in list_of_tuples}
    for key, value in list_of_tuples:
        if value >= _tuple[key]:
            _tuple[key] = value
            # using map
    return list(map(tuple, _tuple.items()))


def is_list_of_strings(lst) -> bool:
    """
    Verifies that given parameter is a list of strings
    :param lst: list
    :return: True if parameter is list of strings
    """
    if lst and isinstance(lst, list):
        return all(isinstance(elem, str) for elem in lst)
    else:
        return False


def is_valid_url(url) -> bool:
    """
    Validates if given image is an URL
    :param url: string URL
    :return: True if given string is an URL
    """
    import re
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)
