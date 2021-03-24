import unittest
from expression.core import exp

class TestExpression(unittest.TestCase):

    def test_arithmetic(self):
        self.assertEqual(exp.solve('1+1'),1+1)
        self.assertEqual(exp.solve('3+2-1'),3+2-1) 
        self.assertEqual(exp.solve('3*4-1'),3*4-1)
        self.assertEqual(exp.solve('1+4*2'),1+4*2)
        self.assertEqual(exp.solve('4+4+2+50+600'),4+4+2+50+600)
        self.assertEqual(exp.solve('1-2-5'),1-2-5)
        self.assertEqual(exp.solve('(1+4)*2'),(1+4)*2)
        self.assertEqual(exp.solve('(2+3)*2'),(2+3)*2)
        self.assertEqual(exp.solve('2*(3+2)'),2*(3+2))
        self.assertEqual(exp.solve('2*(3+2)*(2+2)'),2*(3+2)*(2+2))
        self.assertEqual(exp.solve('1+2*3*4'),1+2*3*4)  
        self.assertEqual(exp.solve('2*3+4*5'),2*3+4*5)
        self.assertEqual(exp.solve('(1+(2**3)*4'),(1+(2**3)*4))
        self.assertEqual(exp.solve('1+2**3*4'),1+2**3*4) 
        self.assertEqual(exp.solve('1+2**(3*4)'),1+2**(3*4))

    def test_comparisons(self):         
        self.assertEqual(exp.solve('3>2'),3>2)
        self.assertEqual(exp.solve('3>2*2'),3>2*2)
        self.assertEqual(exp.solve('-3>2*2'),-3>2*22)
        self.assertEqual(exp.solve('4>=2*2'),4>=2*2)
        self.assertEqual(exp.solve('3<=2*2'),3<=2*2)
        self.assertEqual(exp.solve('3!=2*2'),3!=2*2)
        self.assertEqual(exp.solve('4!=2*2'),4!=2*2)
        self.assertEqual(exp.solve('-4!=2*2'),-4!=2*2)
        self.assertEqual(exp.solve('-4==-2*2'),-4==-2*2)
        self.assertEqual(exp.solve('-4==-(2*2)'),-4==-(2*2))

    def test_variables(self):
        self.assertEqual(exp.solve('a>b',{"a":1,"b":2}),False)
        self.assertEqual(exp.solve('a+b',{"a":1,"b":2}),3)
        self.assertEqual(exp.solve('-a*b',{"a":1,"b":2}),-2)
        self.assertEqual(exp.solve('a*3==b+1',{"a":1,"b":2}),True)
        self.assertEqual(exp.solve('(a*b)+(2*a+2*b)',{"a":1,"b":2}),8)
        self.assertEqual(exp.solve('2**b+a',{"a":1,"b":2}),5)        

    def test_strings(self):
        self.assertEqual(exp.solve('"a"'),"a") 
        self.assertEqual(exp.solve('"a"<"b"'),"a"<"b") 
        self.assertEqual(exp.solve('"a ""b"" "<"b"'),"a ""b"" "<"b") 

    def test_functions(self):
        self.assertEqual(exp.solve('nvl(a,b)',{"a":None,"b":2}),2) 
        self.assertEqual(exp.solve('a.capitalize()',{"a":"aaa","b":2}),"Aaa")  
        self.assertEqual(exp.solve('"aaa".capitalize()'),"Aaa") 
        self.assertEqual(exp.solve('a.count("a")',{"a":"aaa"}),3)
        self.assertEqual(exp.solve('a.count("b")',{"a":"aaa"}),0) 
        self.assertEqual(exp.solve('a.upper()',{"a":"aaa"}),"AAA") 

        

        

def test():
    unittest.main()