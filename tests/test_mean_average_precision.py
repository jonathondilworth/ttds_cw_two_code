import unittest
from code.evallib import mean_average_precision

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

class TestMAP(unittest.TestCase):

    ''' AP_1 = 3.04 / 4 = 0.76, AP_2 = 0.62 / 3, AP_3 = 1.275 / 7 = 0.182 '''
    ''' MAP = (0.76 + 0.62 + 0.182) / 3 = 0.383 '''

    def test_map(self):

        query_one = Query(rel_docs = [1, 2, 5, 9],
                          ret_docs = [1, 2, 3, 4, 5, 6, 7, 8, 9])

        query_two = Query(rel_docs = [3, 7],
                          ret_docs = [1, 2, 3, 4, 5, 6, 7, 8],
                          total_rel_docs = 3)

        query_three = Query(rel_docs = [2, 5, 8],
                            ret_docs = [1, 2, 3, 4, 5, 6, 7, 8, 9],
                            total_rel_docs = 7)

        all_queries = QuerySet([query_one, query_two, query_three])

        test_score = mean_average_precision(all_queries.queries)

        expected_score_1 = ((float(1) + float(1) + (float(3) / float(5)) + (float(4) / float(9))) / float(4))
        expected_score_2 = (((float(1) / float(3)) + (float(2) / float(7))) / float(3))
        expected_score_3 = (((float(1) / float(2)) + (float(2) / float(5)) + (float(3) / float(8))) / float(7))

        expected_score = (float(expected_score_1) + float(expected_score_2) + float(expected_score_3)) / 3

        self.assertEqual(test_score, expected_score)

if __name__ == '__main__':
    unittest.main()
