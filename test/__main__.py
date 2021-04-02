import unittest
from py_expression.core import Parser

parser = Parser()

class TestExpression(unittest.TestCase):

    def test_arithmetic(self):
        self.assertEqual(parser.solve('1+1'),1+1)
        self.assertEqual(parser.solve('3+2-1'),3+2-1) 
        self.assertEqual(parser.solve('3*4-1'),3*4-1)
        self.assertEqual(parser.solve('1+4*2'),1+4*2)
        self.assertEqual(parser.solve('4+4+2+50+600'),4+4+2+50+600)
        self.assertEqual(parser.solve('1-2-5'),1-2-5)
        self.assertEqual(parser.solve('(1+4)*2'),(1+4)*2)
        self.assertEqual(parser.solve('(2+3)*2'),(2+3)*2)
        self.assertEqual(parser.solve('2*(3+2)'),2*(3+2))
        self.assertEqual(parser.solve('2*(3+2)*(2+2)'),2*(3+2)*(2+2))
        self.assertEqual(parser.solve('1+2*3*4'),1+2*3*4)  
        self.assertEqual(parser.solve('2*3+4*5'),2*3+4*5)
        self.assertEqual(parser.solve('(1+(2**3)*4'),(1+(2**3)*4))
        self.assertEqual(parser.solve('1+2**3*4'),1+2**3*4) 
        self.assertEqual(parser.solve('1+2**(3*4)'),1+2**(3*4))

    def test_comparisons(self):         
        self.assertEqual(parser.solve('3>2'),3>2)
        self.assertEqual(parser.solve('3>2*2'),3>2*2)
        self.assertEqual(parser.solve('-3>2*2'),-3>2*22)
        self.assertEqual(parser.solve('4>=2*2'),4>=2*2)
        self.assertEqual(parser.solve('3<=2*2'),3<=2*2)
        self.assertEqual(parser.solve('3!=2*2'),3!=2*2)
        self.assertEqual(parser.solve('4!=2*2'),4!=2*2)
        self.assertEqual(parser.solve('-4!=2*2'),-4!=2*2)
        self.assertEqual(parser.solve('-4==-2*2'),-4==-2*2)
        self.assertEqual(parser.solve('-4==-(2*2)'),-4==-(2*2))

    def test_variables(self):
        self.assertEqual(parser.solve('a>b',{"a":1,"b":2}),False)
        self.assertEqual(parser.solve('a+b',{"a":1,"b":2}),3)
        self.assertEqual(parser.solve('-a*b',{"a":1,"b":2}),-2)
        self.assertEqual(parser.solve('a*3==b+1',{"a":1,"b":2}),True)
        self.assertEqual(parser.solve('(a*b)+(2*a+2*b)',{"a":1,"b":2}),8)
        self.assertEqual(parser.solve('2**b+a',{"a":1,"b":2}),5) 
        self.assertEqual(parser.solve('c.b',{"a":"1","b":2,"c":{"a":4,"b":5}}),5)

    def test_strings(self):
        self.assertEqual(parser.solve('"a"'),"a") 
        self.assertEqual(parser.solve('"a"<"b"'),"a"<"b") 
        self.assertEqual(parser.solve('"a ""b"" "<"b"'),"a ""b"" "<"b") 

    def test_assigments(self):
        context = {"a":"1","b":2,"c":{"a":4,"b":5}}
        parser.solve('a=8',context)
        self.assertEqual(context['a'],8)
        parser.solve('c.a=1',context)
        self.assertEqual(context['c']['a'],1)

    def test_functions(self):
        self.assertEqual(parser.solve('nvl(a,b)',{"a":None,"b":2}),2) 
        self.assertEqual(parser.solve('a.capitalize()',{"a":"aaa","b":2}),"Aaa")  
        self.assertEqual(parser.solve('"aaa".capitalize()'),"Aaa") 
        self.assertEqual(parser.solve('a.count("a")',{"a":"aaa"}),3)
        self.assertEqual(parser.solve('a.count("b")',{"a":"aaa"}),0) 
        self.assertEqual(parser.solve('a.upper()',{"a":"aaa"}),"AAA") 

    def test_enums(self):
        parser.addEnum('ColorConversion',{"BGR2GRAY":6
                                  ,"BGR2HSV":40
                                  ,"BGR2RGB":4
                                  ,"GRAY2BGR":8
                                  ,"HSV2BGR":54
                                  ,"HSV2RGB":55
                                  ,"RGB2GRAY":7
                                  ,"RGB2HSV":41})

        self.assertEqual(parser.solve('ColorConversion.GRAY2BGR'),8)

        

def test():
    unittest.main()