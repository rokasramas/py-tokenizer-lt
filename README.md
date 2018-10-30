# py-tokenizer-lt
Simple tokenizer for Lithuanian language based on Conditional Random Fields

# Installation

Clone or download this repository, navigate to root folder and in terminal enter:

    pip install .
    

# Usage

    >>> from tokenizer import tokenize
    >>> tokenize("Lietuviškai šneka apie 3 mln. žmonių Lietuvoje, šiek tiek Baltarusijoje ir Lenkijos šiaurės rytuose.")
    ['Lietuviškai', 'šneka', 'apie', '3', 'mln.', 'žmonių', 'Lietuvoje', ',', 'šiek', 'tiek', 'Baltarusijoje', 'ir', 'Lenkijos', 'šiaurės', 'rytuose', '.']
    
# See also

[python-crfsuite](https://github.com/scrapinghub/python-crfsuite), a python binding to [CRFsuite](https://github.com/chokkan/crfsuite).


