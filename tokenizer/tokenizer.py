import pycrfsuite
import regex as re
from itertools import chain
from typing import Iterator, List


TAGGER = pycrfsuite.Tagger()
TAGGER.open('resources/lt-model.crfsuite')


def homogeneous(string: str) -> re.match:
    """determine if string is made up of similar types of characters"""
    return re.match("(^\p{L}+$|^\p{Z}+$|^\p{N}+$|^\.+$|^\[?!]+$|^\,+$)", string)


def get_feature(to_left: str, to_right: str) -> List[str]:
    """generate single feature given string to left and right"""
    return ['h:1'] if homogeneous(to_left[-1:]+to_right[:1]) else list(chain(
        (f'c{-i}:{char}' for char, i in zip(to_left, reversed(range(1, len(to_left)+1)))),
        (f'c{i}:{char}' for char, i in zip(to_right, range(len(to_right))))
    ))


def apply_labels(tags: str, string: str) -> Iterator[str]:
    """split string at every position, where there is '1'"""
    return (
        string[begin:end] for begin, end in (instance.span() for instance in re.finditer('10*', tags))
    )


def get_features(string: str, start: int, finish: int, left_span: int, right_span: int) -> Iterator[List[str]]:
    """prepare string features in given range"""
    return (
        get_feature(string[max(0, index-left_span):index], string[index:index+right_span])
        for index in range(start, finish)
    )


def tag(string: str, tagger: pycrfsuite.Tagger, start: int, finish: int, left_span: int, right_span: int) -> str:
    """splits chunk into tokens"""
    return '1' + ''.join(
        tagger.tag(list(get_features(string, start+1, finish, left_span, right_span)))
    )


def tokenize(string: str, tagger: pycrfsuite.Tagger = TAGGER, left_span: int = 12, right_span: int = 12) -> List[str]:
    """splits string into tokens"""
    return list(chain.from_iterable(
        (chunk.group(), ) if homogeneous(chunk.group()) else apply_labels(
            tag(string, tagger, *chunk.span(), left_span, right_span), chunk.group()
        ) for chunk in re.finditer('[^\p{Z}\n\r\t]+|[\p{Z}\n\r\t]+', string)
    ))
