import unittest
from code.evallib import precision

# TODO: consider using metaclasses to ensure that all tests are written in the form: test_<x>

class TestPrecision(unittest.TestCase):

    '''
    Precision tests
    precision accepts two document sets (relevent and retrieved)
    It returns the value of: |(relevent INTERSECTION retrieved)| / |retrieved|
    '''

    def test_expected_precision(self):
        relevent_documents = {1, 2}
        retrieved_documents = {2, 3, 4}
        self.assertEqual(precision(relevent_documents, retrieved_documents), (float(1)/float(3)))

    def test_return_type(self):
        relevent_documents = {1, 2}
        retrieved_documents = {2, 3, 4}
        self.assertIsInstance(precision(relevent_documents, retrieved_documents), float)

    def test_divide_by_zero(self):
        relevent_documents = {1, 2}
        retrieved_documents = {}
        with self.assertRaises(ZeroDivisionError):
            precision(relevent_documents, retrieved_documents)

    def test_floating_point(self):
        """precision itself doesn't care about the labels that documents use"""
        relevent_documents = {0.11, 0.23}
        retrieved_documents = {1, 3, 0.23, 4}
        self.assertEqual(precision(relevent_documents, retrieved_documents), (float(1)/float(4)))

    def test_invalid_arguments(self):
        """using lists instead of sets should cause problems"""
        relevent_documents = [1, 2]
        retrieved_documents = [2, 3, 4]
        with self.assertRaises(AttributeError):
            precision(relevent_documents, retrieved_documents)

    def test_no_arguments(self):
        with self.assertRaises(TypeError):
            precision()

    def test_expects_zero(self):
        """casting a dict to a set is a thing, so we can expect zero"""
        relevent_documents = {1, 2}
        retrieved_documents = {'a':'b','c':'d'}
        self.assertEqual(precision(relevent_documents, retrieved_documents), float(0))

if __name__ == '__main__':
    unittest.main()