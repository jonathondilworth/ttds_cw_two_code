import unittest
from code.evallib import f1_score

class TestF1Score(unittest.TestCase):

    '''
    TODO: insert comment here.
    '''

    def test_expected_f1_score(self):
        relevent_documents = {2, 3}
        retrieved_documents = {1, 2}
        test_score = f1_score(relevent_documents, retrieved_documents)
        expected_score = float(1) / float(2)
        self.assertEqual(test_score, expected_score)

    def test_return_type(self):
        relevent_documents = {2, 3}
        retrieved_documents = {1, 2}
        test_score = f1_score(relevent_documents, retrieved_documents)
        self.assertIsInstance(test_score, float)

    def test_invalid_arguments(self):
        relevent_documents = [1, 2, 3]
        retrieved_documents = {1, 2, 3, 4}
        with self.assertRaises(AttributeError):
            f1_score(relevent_documents, retrieved_documents)

    def test_divide_by_zero(self):
        relevent_documents = {1, 2, 3, 4}
        retrieved_documents = {5, 6, 7, 8}
        with self.assertRaises(ZeroDivisionError):
            f1_score(relevent_documents, retrieved_documents)

    # test precision && || recall exception(s) raised

    def test_precision_recall_exceptions_thrown(self):
        relevent_documents = {}
        retrieved_documents = {1, 2, 3, 4}
        with self.assertRaises(AttributeError):
            f1_score(relevent_documents, retrieved_documents)

    def test_no_arguments(self):
        with self.assertRaises(TypeError):
            f1_score()

if __name__ == '__main__':
    unittest.main()