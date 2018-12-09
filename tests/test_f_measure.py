import unittest
from code.evallib import f_measure

class TestFMeasure(unittest.TestCase):

    def test_expected_f_measure(self):
        beta = float(2)
        relevent_documents = {1, 2, 3}
        retrieved_documents = {2, 3, 4, 5}
        expected_value = (float(5) * float(0.5) * (float(2) / float(3)) / (float(4) * float(0.5) + (float(2) / float(3))))
        self.assertEqual(f_measure(relevent_documents, retrieved_documents, beta), expected_value)

    def test_return_type(self):
        beta = float(2)
        relevent_documents = {1, 2, 3}
        retrieved_documents = {2, 3, 4, 5}
        test_score = f_measure(relevent_documents, retrieved_documents, beta)
        self.assertIsInstance(test_score, float)

    def test_invalid_hyper_param(self):
        relevent_documents = [1, 2, 3]
        retrieved_documents = {1, 2, 3, 4}
        with self.assertRaises(TypeError):
            f_measure(relevent_documents, retrieved_documents, 'abc') 

    def test_invalid_arguments(self):
        relevent_documents = [1, 2, 3]
        retrieved_documents = {1, 2, 3, 4}
        with self.assertRaises(AttributeError):
            f_measure(relevent_documents, retrieved_documents, 5) 

    def test_no_relevent_docs(self):
        relevent_documents = {}
        retrieved_documents = {1, 2, 3, 4}
        with self.assertRaises(AttributeError):
            f_measure(relevent_documents, retrieved_documents, 2)

    def test_no_retrieved_docs(self):
        relevent_documents = {2, 3}
        retrieved_documents = {}
        with self.assertRaises(ZeroDivisionError):
            f_measure(relevent_documents, retrieved_documents, 1)

    def test_no_arguments(self):
        with self.assertRaises(TypeError):
            f_measure()

if __name__ == '__main__':
    unittest.main()