import argparse
from tokenizer.tokenizer import tokenize


def tokenize_file(input_path: str, output_path: str):
    with open(input_path, 'r', encoding='utf-8') as input_file, open(output_path, 'a', encoding='utf-8') as output:
        for line in input_file:
            output.write('\n'.join(tokenize(line)) + '\n')


parser = argparse.ArgumentParser(
    description='Tokenize text file.'
)
parser.add_argument(
    'text_file', metavar='text_file', type=str, nargs=1, help='path to file containing text'
)
parser.add_argument(
    'output_path', metavar='output_path', type=str, nargs=1, help='path where tokenized text will be stored'
)

args = parser.parse_args()

tokenize_file(args.text_file[0], args.output_path[0])
