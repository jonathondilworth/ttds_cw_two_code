import unittest
from code.evallib import r_precision

class TestRPrecision(unittest.TestCase):

    def test_basic_r_precision(self):
        self.assertEqual(r_precision([0, 1, 2], [4, 3, 5], 3), 0)

    def test_basic_r_precision_implicit(self):
        self.assertEqual(r_precision([0, 1, 2], [4, 3, 5]), 0)

    '''
    since r_precision uses precision_at_k, all other tests are covered
    by test_precision_at_k.py
    '''

if __name__ == '__main__':
    unittest.main()