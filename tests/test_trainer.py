from tokenizer.trainer import get_tags, get_chunk_positions
import unittest


class TrainerTest(unittest.TestCase):

    def testGetTags(self):
        self.assertEqual(get_tags(['a', 'bc', 'def']), ['1', '1', '0', '1', '0', '0'])

    def testGetTagsEmpty(self):
        self.assertEqual(get_tags([]), [])

    def testGetChunkPositions(self):
        self.assertEqual(list(get_chunk_positions('1a fff 111')), [(0, 2)])
