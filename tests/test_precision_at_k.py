import unittest
from code.evallib import precision_at_k
from code.evallib import precision

class TestPrecisionAtK(unittest.TestCase):

    '''
    precision_at_k tests
    precision_at_k accepts two document lists and a 'cut-off' value @ k
    both lists are assumed to be ranked
    it returns the same as precision, but limits the number of docs in
    the retrieved list to the first K documents.
    '''

    def test_basic_precision_at_k(self):
        self.assertEqual(precision_at_k([0, 1, 2], [4, 3, 2], 2), 0)

    # this test will pass assuming that the set of relevent documents is not truncated
    # else, this test will fail
    def test_basic_precision_at_k_assuming_the_rel_docs_have_not_been_truncated(self):
        p_at_k_rel_docs = [0, 1, 2]
        p_at_k_ret_docs = [2, 3, 4]
        k = 2
        # as k = 2, we're limiting our ret docs to be truncated @ 2
        pre_rel_docs = [0, 1, 2]
        pre_ret_docs = [2, 3]
        result_check = precision(set(pre_rel_docs), set(pre_ret_docs))
        # print(precision_at_k(p_at_k_rel_docs, p_at_k_ret_docs, 2))
        # print(result_check)
        self.assertEqual(precision_at_k(p_at_k_rel_docs, p_at_k_ret_docs, 2), result_check)

    def test_divide_by_zero(self):
        relevent_documents = [0, 1, 2]
        retrieved_documents = [0, 1, 3]
        k = 0
        with self.assertRaises(ZeroDivisionError):
           precision_at_k(relevent_documents, retrieved_documents, k)

    def test_return_type(self):
        relevent_documents = [2, 3]
        retrieved_documents = [1, 2]
        k = 2
        result = precision_at_k(relevent_documents, retrieved_documents, k)
        self.assertIsInstance(result, float)

    # precision_at_k will accept a list of relevent documents, as I'm not 100% sure
    # to truncate the list of relevent documents, or to not
    def test_input_works_with_rel_set_not_list(self):
        relevent_documents = {2, 3}
        retrieved_documents = [1, 2]
        k = 2
        result = precision_at_k(relevent_documents, retrieved_documents, k)
        self.assertEqual(result, float(0.5))

    # precision_at_k will accept a list of relevent documents, as I'm not 100% sure
    # to truncate the list of relevent documents, or to not
    def test_ret_docs_as_set_throws_exception(self):
        relevent_documents = [2, 3]
        retrieved_documents = {1, 2}
        k = 2
        with self.assertRaises(TypeError):
            precision_at_k(relevent_documents, retrieved_documents, k)

    def test_no_arguments(self):
        with self.assertRaises(TypeError):
            precision_at_k()

    def test_out_of_bounds_is_not_thrown(self):
        relevent_documents = [2, 3, 4, 9225]
        retrieved_documents = [3]
        k = 10
        result = precision_at_k(relevent_documents, retrieved_documents, k)
        self.assertEqual(result, (float(1) / float(10)))

if __name__ == '__main__':
    unittest.main()