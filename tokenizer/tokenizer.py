import pycrfsuite
import regex as re
from itertools import chain
from typing import Iterator, List


def get_feature(left: str, right: str) -> List[str]:
    """generate single feature given string to left and right"""
    return list(chain(
        (f'c{-i}:{char}' for char, i in zip(left, reversed(range(1, len(left)+1)))),
        (f'c{i}:{char}' for char, i in zip(right, range(len(right))))
    ))


def apply_labels(labels: str, string: str) -> Iterator[str]:
    """split string at every label position, where there is '1'"""
    return (
        string[begin:end] for begin, end in map(lambda match: match.span(), re.finditer('10*', labels))
    )


def get_spans(start: int, finish: int, left_span: int = 5, right_span: int = 3) -> Iterator[List[int]]:
    """for each index, get number of characters to left and right used to generate features"""
    return (
        [index, index-left_span if index > left_span else 0, index+right_span] for index in range(start, finish)
    )


def tag(string: str, start: int, finish: int) -> List[str]:
    """use tagger to predict label at each index"""
    return tagger.tag([
        get_feature(string[to_left:index], string[index:to_right])
        for index, to_left, to_right in get_spans(start, finish)
    ])


def homogeneous(string: str) -> re.match:
    """determine if string is made up of similar types of characters"""
    return re.match('(^\p{L}+$|^\p{Z}+$|^\p{N}+$)', string)


def get_labels(string: str, start: int, finish: int) -> Iterator[str]:
    """returns string of '0' and '1', where '1' specifies start of new token"""
    return chain('1', (
        '0' if homogeneous(string[index-1:index+1]) else tag(string, index, index+1)[0]
        for index in range(start+1, finish))
    )


def process(string: str, chunk: re.match) -> Iterator[str]:
    """splits chunk into tokens"""
    return apply_labels(
        ''.join(get_labels(string, *chunk.span())), chunk.group()
    )


def tokenize(string: str) -> List[str]:
    """splits string into tokens"""
    return list(chain.from_iterable(
        (chunk.group(), ) if homogeneous(chunk.group()) else process(string, chunk)
        for chunk in re.finditer('[^\p{Z}\n]+', string)
    ))


tagger = pycrfsuite.Tagger()
tagger.open('resources/lt-model.crfsuite')
