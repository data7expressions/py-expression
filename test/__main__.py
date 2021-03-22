import unittest
from expression.core import expManager

class TestExpression(unittest.TestCase):

    def test_arithmetic(self):
        self.assertEqual(expManager.solve('1+1'),2)
        self.assertEqual(expManager.solve('3+2-1'),4) 
        self.assertEqual(expManager.solve('3*4-1'),11)
        self.assertEqual(expManager.solve('1+4*2'),9)        



unittest.main()