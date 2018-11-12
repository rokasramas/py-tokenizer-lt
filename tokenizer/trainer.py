import pycrfsuite
import regex as re
import os
from itertools import chain
from typing import Iterator, List, Tuple
from tokenizer.tokenizer import get_features, homogeneous


LEFT_SPAN = 12
RIGHT_SPAN = 12
NUMBER_OF_PARAGRAPHS = 1500000
TRAINING_DATA = 'resources/training.txt'


def get_params(c1: int = 1, c2: int= 1, max_iter: int = 200, num_memories : int = 12, epsilon : float = 1e-3,
               delta: float = 1e-2, linesearch: str = 'StrongBacktracking', max_linesearch: int = 20,
               possible_states: bool = True, possible_transitions: bool = True) -> dict:
    """returns model parameters"""
    return {
        'c1': c1,  # The coefficient for L1 regularization
        'c2': c2,  # The coefficient for L2 regularization
        'max_iterations': max_iter,  # The maximum number of iterations for L-BFGS optimization
        'num_memories': num_memories,  # The number of limited memories that L-BFGS uses for approximation
        'epsilon': epsilon,  # The epsilon parameter that determines the condition of convergence (1e-5)
        'delta': delta,  # The threshold for the stopping criterion
        'linesearch': linesearch,  # Available methods are: "MoreThuente", "Backtracking" and "StrongBacktracking"
        'max_linesearch': max_linesearch,  # The maximum number of trials for the line search algorithm

        # include transitions that are possible, but not observed
        'feature.possible_states': possible_states,
        'feature.possible_transitions': possible_transitions
    }


def get_model_name(c1: int, c2: int, max_iterations: int, num_memories: int, epsilon: float, delta: float,
                   linesearch: bool, max_linesearch: bool, **kwargs) -> str:
    """generates model name based on parameters"""
    ls = {'Backtracking': 'B', 'StrongBacktracking': 'SB', 'MoreThuente': 'MT'}
    return '_'.join([
        f'span_l{LEFT_SPAN}r{RIGHT_SPAN}',
        f'n_{NUMBER_OF_PARAGRAPHS}',
        f'maxiter_{max_iterations}',
        f'c1_{c1}_c2_{c2}',
        f'mem_{num_memories}',
        f'e_{epsilon}_d_{delta}',
        f'ls_{ls[linesearch]}',
        f'maxlsrch_{max_linesearch}.crfsuite'
    ])


def get_tags(tokens: List[str]) -> List[str]:
    """'1' for every token start, '0' for every other character"""
    return list(chain.from_iterable(
        (['1'] + ['0']*(len(token)-1) for token in tokens)
    ))


def get_chunk_positions(string: str) -> Iterator[Tuple[int, int]]:
    """returns chunk positions used for training"""
    return filter(None, (
        () if homogeneous(chunk.group()) else chunk.span()
        for chunk in re.finditer('[^\p{Z}\n\r\t]+', string)
    ))


def append_chunks(trainer: pycrfsuite.Trainer, tokens: List[str], left_span: int, right_span: int):
    """append training chunks based on provided tokens"""
    string = ''.join(tokens)
    tags = get_tags(tokens)
    for start, finish in get_chunk_positions(string):
        trainer.append(
            get_features(string, start, finish, left_span, right_span), tags[start:finish]
        )


def load_data(trainer: pycrfsuite.Trainer, path: str = TRAINING_DATA, n: int = NUMBER_OF_PARAGRAPHS,
              left_span: int = LEFT_SPAN, right_span: int = RIGHT_SPAN):
    """reads and loads training data, where each instance is
    split by double newline and every token by single newline"""
    with open(path, 'r', encoding='utf-8') as file:
        count = 0
        tokens = []
        for token in file:
            token = token.rstrip('\n')
            if token:
                tokens.append(token)
                continue
            append_chunks(trainer, tokens, left_span, right_span)
            count += 1
            tokens = []
            if n == count:
                break
        file.close()


def train(output_dir='output', verbose=True):
    """trains model and saves it in output directory"""
    trainer = pycrfsuite.Trainer(verbose=verbose)
    load_data(trainer)
    params = get_params()
    trainer.set_params(params)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    trainer.train(
        os.path.join(output_dir, get_model_name(**params))
    )
