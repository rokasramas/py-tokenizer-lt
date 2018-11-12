import regex as re
from itertools import chain
from typing import Iterator, List, Set


def get_url_indexes(string: str) -> Set[int]:
    """returns index numbers belonging to matched urls"""
    return set(chain.from_iterable(
        (list(range(*url.span()) for url in url_pattern.finditer(string)))
    ))


def add_url_features(indexes: Set[int], features: Iterator[List[str]]) -> Iterator[List[str]]:
    """attaches url feature to provided indexes"""
    return (
        list(chain(['u:1'], feature)) if index in indexes else feature
        for index, feature in enumerate(features)
    )


# @cowboy url pattern, found in https://mathiasbynens.be/demo/url-regex
with open('resources/url.regex', 'r') as file:
    url_pattern = re.compile(file.read())
    file.close()
