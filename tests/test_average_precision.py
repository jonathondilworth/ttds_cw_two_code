import unittest
from code.evallib import average_precision

# TODO: abstract out QuerySet & Query

class QuerySet():

    def __init__(self, queries):
        self.queries = queries

class Query():
    
    def __init__(self, rel_docs, ret_docs, total_rel_docs=None):
        self.rel_docs = rel_docs
        self.ret_docs = ret_docs
        if total_rel_docs is None:
            self.total_rel_docs = len(self.rel_docs)
        else:
            self.total_rel_docs = total_rel_docs

# something cool to think about - query generator - TODO

class TestAVGPrecision(unittest.TestCase):

    ''' AP_1 = 3.04 / 4 = 0.76, AP_2 = 0.62 / 3, AP_3 = 1.275 / 7 = 0.182 '''

    def test_exp_avg_pre_one(self):

        query_one = Query(rel_docs = [1, 2, 5, 9],
                          ret_docs = [1, 2, 3, 4, 5, 6, 7, 8, 9])

        test_score = average_precision(query_one.rel_docs, query_one.ret_docs)

        expected_score = (float(1) + float(1) + (float(3) / float(5)) + (float(4) / float(9))) / float(4)

        self.assertEqual(test_score, expected_score)


    def test_exp_avg_pre_two(self):

        query_two = Query(rel_docs = [3, 7],
                          ret_docs = [1, 2, 3, 4, 5, 6, 7, 8],
                          total_rel_docs = 3)

        test_score = average_precision(query_two.rel_docs, query_two.ret_docs, query_two.total_rel_docs)

        expected_score = ((float(1) / float(3)) + (float(2) / float(7))) / float(3)

        self.assertEqual(test_score, expected_score)


    def test_exp_avg_pre_three(self):

        query_three = Query(rel_docs = [2, 5, 8],
                            ret_docs = [1, 2, 3, 4, 5, 6, 7, 8, 9],
                            total_rel_docs = 7)

        test_score = average_precision(query_three.rel_docs, query_three.ret_docs, query_three.total_rel_docs)

        expected_score = ((float(1) / float(2)) + (float(2) / float(5)) + (float(3) / float(8))) / float(7)

        self.assertEqual(test_score, expected_score)

if __name__ == '__main__':
    unittest.main()
