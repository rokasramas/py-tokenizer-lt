from distutils.core import setup


def read(file):
    with open(file, 'r') as f:
        output = f.read()
        f.close()
    return output


setup(
    name='py-tokenizer-lt',
    version='1.0',
    description='Simple tokenizer for Lithuanian language based on Conditional Random Fields',
    long_description=read('README.md'),
    author='Rokas Ramanauskas',
    author_email='rokasramas@gmail.com',
    url='https://github.com/rokasramas/py-tokenizer-lt/',
    packages=['tokenizer'],
    package_data={'tokenizer': ['resources/lt-model.crfsuite']},
    include_package_data=True,
    install_requires=['python-crfsuite', 'regex']
)
