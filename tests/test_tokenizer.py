from tokenizer.tokenizer import TAGGER, homogeneous, get_feature, apply_labels, get_features, tag, tokenize
import unittest


class TokenizerTest(unittest.TestCase):

    def testHomogeneousTrue(self):
        for string in ['ąbč', 'ĄBČ', 'Ąbč', '   ', '123', '...', '!!?', ',,,']:
            self.assertTrue(homogeneous(string))

    def testHomogeneousFalse(self):
        for string in ['1ab', '']:
            self.assertFalse(homogeneous(string))

    def testGetFeature(self):
        self.assertEqual(get_feature('abc', 'def'), ['h:1'])
        self.assertEqual(get_feature('dc', '12'), ['c-2:d', 'c-1:c', 'c0:1', 'c1:2'])

    def testApplyLabels(self):
        self.assertEqual(list(apply_labels('101010', 'abcdef')), ['ab', 'cd', 'ef'])
        self.assertEqual(list(apply_labels('1', 'a')), ['a'])

    def testGetFeatures(self):
        self.assertEqual(
            list(get_features('a12d', start=1, finish=3, left_span=1, right_span=1)), [['c-1:a', 'c0:1'], ['h:1']]
        )

    def testTag(self):
        for l in range(2, 100):
            self.assertEqual(
                len(tag(str(map(chr, range(l))), TAGGER, start=0, finish=l, left_span=1, right_span=1)), l
            )

    def testTagChar(self):
        for char in map(chr, range(100)):
            self.assertEqual(
                tag(char, TAGGER, start=0, finish=1, left_span=1, right_span=1), '1'
            )

    def testTokenize(self):
        chars = ''.join(map(chr, range(10000)))
        self.assertEqual(''.join(tokenize(chars)), chars)

    def testTokenizeEmptyString(self):
        self.assertEqual([], tokenize(''))
