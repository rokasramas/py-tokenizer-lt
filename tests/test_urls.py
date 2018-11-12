from tokenizer.urls import get_url_indexes, add_url_features
import unittest


class UrlsTest(unittest.TestCase):

    def testGetUrlIndexes(self):
        self.assertEqual(
            get_url_indexes('vcv http://www.www.lt ggg'), set(range(4, 21))
        )

    def testAddUrlFeatures(self):
        self.assertEqual(
            list(add_url_features({0, 1, 2}, [[], ['c0:0'], ['c0:0', 'c1:1'], []])),
            [['u:1'], ['u:1', 'c0:0'], ['u:1', 'c0:0', 'c1:1'], []]
        )
