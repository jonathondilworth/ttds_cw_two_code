import unittest
from code.evallib import recall

class TestRecall(unittest.TestCase):

    '''
    Recall tests
    recall excepts two parameters: two document sets (relevent and retrieved)
    It returns the value of: |(relevent INTERSECTION retrieved)| / |relevent|
    '''

    def test_expected(self):
        relevent_documents = {3306, 3022, 1892, 100}
        retrieved_documents = {100, 3022, 3307, 3308, 3309, 1001, 202}
        self.assertEqual(recall(relevent_documents, retrieved_documents), (float(2)/float(4)))

    def test_return_type(self):
        relevent_documents = {3306, 3022, 1892, 100}
        retrieved_documents = {100, 3022, 3307, 3308, 3309, 1001, 202}
        self.assertIsInstance(recall(relevent_documents, retrieved_documents), float)

    def test_expecting_zero(self):
        relevent_documents = {22}
        retrieved_documents = {100, 3022, 3307, 3308, 3309, 1001, 202}
        self.assertEqual(recall(relevent_documents, retrieved_documents), float(0))

    def test_empty_relevent_set(self):
        relevent_documents = {}
        retrieved_documents = {100, 3022, 3307, 3308, 3309, 1001, 202}   
        with self.assertRaises(AttributeError):
            recall(relevent_documents, retrieved_documents)

    def test_invalid_arguments(self):
        relevent_documents = [1, 2]
        retrieved_documents = [2, 3, 4]
        with self.assertRaises(AttributeError):
            recall(relevent_documents, retrieved_documents)

    def test_no_arguments(self):
        with self.assertRaises(TypeError):
            recall()

    def test_expects_zero(self):
        """casting a dict to a set is a thing, so we can expect zero"""
        relevent_documents = {1, 2}
        retrieved_documents = {'a':'b','c':'d'}
        self.assertEqual(recall(relevent_documents, retrieved_documents), float(0))

if __name__ == '__main__':
    unittest.main()