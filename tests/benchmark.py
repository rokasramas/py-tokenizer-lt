from tokenizer.tokenizer import tokenize
from tokenizer.trainer import get_tags
import pycrfsuite
import regex as re
from datetime import datetime
import time
import os


TESTING_DATA = 'resources/testing.txt'


def test_outcomes(tagger: pycrfsuite.Tagger, path: str, left_span: int, right_span: int):
    outcomes = {'error_split': 0, 'correct_split': 0,
                'error_merge': 0, 'correct_merge': 0}
    with open(path, 'r', encoding='utf-8') as file:
        count = 0
        correct_instances = 0
        total_time = 0
        tokens = []
        for token in file:
            token = token.rstrip('\n')
            if token:
                tokens.append(token)
                continue
            string = ''.join(tokens)

            # measure time
            start = time.time()
            tokenized_string = tokenize(string, tagger, left_span, right_span)
            total_time += time.time() - start

            # compare at every index
            found_errors = False
            for prediction, label in zip(get_tags(tokenized_string), get_tags(tokens)):
                outcomes[{'10': 'error_split', '11': 'correct_split',
                          '01': 'error_merge', '00': 'correct_merge'}[prediction+label]] += 1
                if prediction+label in {'10', '01'}:
                    found_errors = True

            count += 1
            if not found_errors:
                correct_instances += 1
            tokens = []
        file.close()
    return get_result(
        count, correct_instances, total_time, **outcomes
    )


def get_result(count: int, correct_instances: int, total_time: float,
               correct_split: int, correct_merge: int, error_split: int, error_merge: int):
    return [
        ('Number of instances', count),
        ('Overall (%)', (correct_split+correct_merge)/(correct_split+error_split+correct_merge+error_merge)*100),
        ('Correct instances (%)', correct_instances/count*100),
        ('Split (%)', correct_split/sum([error_split, correct_split])*100),
        ('Merge (%)', correct_merge/sum([error_merge, correct_merge])*100),
        ('Average errors', sum([error_split, error_merge])/(count-correct_instances)),
        ('Total time (s)', total_time),
        ('Average time (s)', total_time/count)
    ]


def benchmark(model_path: str, left_span: int, right_span: int, testing_data: str = TESTING_DATA):
    tagger = pycrfsuite.Tagger()
    tagger.open(model_path)
    result = test_outcomes(tagger, testing_data, left_span, right_span)
    header = datetime.strftime(datetime.now(), f'*** (%m-%d %H:%M) "{model_path}" ***')
    output = '\n\n'.join([header, '\n'.join(map(lambda x: ': '.join(map(str, x)), result))]) + '\n\n'
    add_to_log(output)
    print(output)


def benchmark_all(output_dir: str = 'output', testing_data: str = TESTING_DATA):
    for model in filter(lambda file: name_pattern.match(file), os.listdir(output_dir)):
        left_span, right_span = map(int, name_pattern.match(model).groups()[0:2])
        benchmark(
            os.path.join(output_dir, model), left_span, right_span, testing_data
        )


def add_to_log(string: str, log_path: str = 'output/log.txt'):
    with open(log_path, 'a') as log:
        log.write(string)
        log.close()


name_pattern = re.compile('_'.join([
    'span_l([\d]+)r([\d]+)',
    'n_([\d]+)',
    'maxiter_([\d]+)',
    'c1_([\d.]+)_c2_([\d.]+)',
    'mem_([\d]+)',
    'e_([\d.]+)_d_([\d.]+)',
    'ls_([A-Za-z]+)',
    'maxlsrch_([\d]+).crfsuite'
]))
