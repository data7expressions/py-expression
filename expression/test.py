import unittest
from expression.core import exp

class TestExpression(unittest.TestCase):

    def test_arithmetic(self):
        self.assertEqual(exp.solve('1+1'),2)
        self.assertEqual(exp.solve('3+2-1'),4) 
        self.assertEqual(exp.solve('3*4-1'),11)
        self.assertEqual(exp.solve('1+4*2'),9)        

unittest.main()