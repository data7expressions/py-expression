"""Test expression"""
import unittest
from enum import Enum
from py_expression.core import Exp

exp = Exp()

class TestExpression(unittest.TestCase):
    """Test expression"""

    def test_arithmetic(self):
        """Test arithmetic expressions"""
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
        """Test comparison expressions"""  
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
        """Test variables"""
        self.assertEqual(exp.solve('a>b',{"a":1,"b":2}),False)
        self.assertEqual(exp.solve('a+b',{"a":1,"b":2}),3)
        self.assertEqual(exp.solve('-a*b',{"a":1,"b":2}),-2)
        self.assertEqual(exp.solve('a*3==b+1',{"a":1,"b":2}),True)
        self.assertEqual(exp.solve('(a*b)+(2*a+2*b)',{"a":1,"b":2}),8)
        self.assertEqual(exp.solve('2**b+a',{"a":1,"b":2}),5)
        self.assertEqual(exp.solve('c.b',{"a":"1","b":2,"c":{"a":4,"b":5}}),5)

    def test_strings(self):
        """Test strings"""
        self.assertEqual(exp.solve('"a"'),"a")
        self.assertEqual(exp.solve('"a"<"b"'),"a"<"b")
        self.assertEqual(exp.solve('"a ""b"" "<"b"'),"a ""b"" "<"b")

    def test_assignments(self):
        """Test assignments"""
        context = {"a":"1","b":2,"c":{"a":4,"b":5}}
        exp.solve('a=8',context)
        self.assertEqual(context['a'],8)
        exp.solve('c.a=1',context)
        self.assertEqual(context['c']['a'],1)

    def test_functions(self):
        """Test functions"""
        self.assertEqual(exp.solve('nvl(a,b)',{"a":None,"b":2}),2)
        self.assertEqual(exp.solve('a.capitalize()',{"a":"aaa","b":2}),"Aaa")
        self.assertEqual(exp.solve('"aaa".capitalize()'),"Aaa")
        self.assertEqual(exp.solve('a.count("a")',{"a":"aaa"}),3)
        self.assertEqual(exp.solve('a.count("b")',{"a":"aaa"}),0)
        self.assertEqual(exp.solve('a.upper()',{"a":"aaa"}),"AAA")

    def test_enums(self):
        """Test enums"""
        exp.addEnum('ColorConversion',{"BGR2GRAY":6
                                  ,"BGR2HSV":40
                                  ,"BGR2RGB":4
                                  ,"GRAY2BGR":8
                                  ,"HSV2BGR":54
                                  ,"HSV2RGB":55
                                  ,"RGB2GRAY":7
                                  ,"RGB2HSV":41})

        self.assertEqual(exp.solve('ColorConversion.GRAY2BGR'),8)

        class Color(Enum):
            """Color enum"""
            RED = 1
            GREEN = 2
            BLUE = 3

        exp.addEnum('Color',Color)
        self.assertEqual(exp.solve('Color.GREEN'),2)

    def test_info(self):
        """Test info"""
        op = exp.parse('"expression".count("e")>= a+1')
        self.assertEqual(op.vars(),{'a': 'any'})
        self.assertEqual(op.constants(),{'expression': 'str', 'e': 'str', 1: 'int'})
        self.assertEqual(op.operators(),{'>=': 'comparison', '+': 'arithmetic'})
        self.assertEqual(op.functions(),{'.count': {'isChild': True}} )

    def test_multiline(self):
        """Test multiline"""  
        text='a=4; '\
             'b=a+2; '\
            ' output=a*b; ' 
        expression = exp.parse(text)
        context = {}
        expression.eval(context)
        self.assertEqual(context['output'],24)

    def test_block_control(self):
        """Test block control"""      
        context = {}
        exp.solve(('output=1;if(1==2){output=2}else {output=3}'),context)
        self.assertEqual(context['output'],3)

        exp.solve('output=1;if(1==1){output=2;}else {output=3;}',context)
        self.assertEqual(context['output'],2)

        exp.solve(('if(1==2){'
                   '    output=2'
                   '}else {'
                   '    output=3'
                   '}'),context)
        self.assertEqual(context['output'],3)
        exp.solve(('i=0;'
                 'while(i<=6){'
                 '  output=i*2;'
                 '  i=i+1;'
                 '}'),context)
        self.assertEqual(context['output'],12)

    def test_initialize_lines(self):
        """Test initialize lines"""           
        text = ('rectangle = {"x":50,"y":50,"width":80,"height":60}; '
               'sleepSecs = 1;'
               'source=nvl(source,"data/source.jpg");')
        expression = exp.parse(text)
        context = {}
        expression.eval(context)
        self.assertEqual(context['rectangle']['x'],50)

    def test_lambda_functions(self):
        """Test lambda functions"""           
        context = {"a":[1,2,3],"b":0}
        exp.solve('a.foreach(p:b=b+p)',context)
        self.assertEqual(context['b'],6)
        context = {"a":[1,2,3,4,5],"b":0}
        exp.solve('a.filter(p: p<5).foreach(p: b=b+p)',context)
        self.assertEqual(context['b'],10)
        context = {"a":[1,2,3,4,5],"b":0}
        self.assertEqual(exp.solve('a.first(p: p%2==0)',context),2)
        context = {"a":[1,2,3,4,5],"b":0}
        self.assertEqual(exp.solve('a.last(p: p%2==0)',context),4)
        context = {"a":[1,2,3,4,5],"b":0}
        self.assertEqual(exp.solve('a.filter(p: p>1 && p<5).map(p: p*2)',context),[4,6,8])
        context = {"a":[1,2,3,4,5],"b":0}
        self.assertEqual(exp.solve('a.filter(p: p>1 && p<5).reverse()',context),[4,3,2])
        # context = {"a":[1,2,3,4,5],"b":0}
        # self.assertEqual(exp.solve('a.filter(p: p>1 && p<5).map(p: p*2).reverse()',context),[8,6,4])
    def test_serialize(self):
        """Test serialize"""
        operand =exp.parse(('i=0;'
                 'while(i<=6){'
                 '  output=i*2;'
                 '  i=i+1;'
                 '}'))
        serialized = exp.serialize(operand)
        self.assertEqual(serialized,{'n': 'block', 't': 'Block', 'c': [{'n': '=', 't': 'Assignment', 'c': [{'n': 'i', 't': 'Variable'}, {'n': 0, 't': 'Constant'}]}, {'n': 'while', 't': 'While', 'c': [{'n': '<=', 't': 'LessThanOrEqual', 'c': [{'n': 'i', 't': 'Variable'}, {'n': 6, 't': 'Constant'}]}, {'n': 'block', 't': 'Block', 'c': [{'n': '=', 't': 'Assignment', 'c': [{'n': 'output', 't': 'Variable'}, {'n': '*', 't': 'Multiplication', 'c': [{'n': 'i', 't': 'Variable'}, {'n': 2, 't': 'Constant'}]}]}, {'n': '=', 't': 'Assignment', 'c': [{'n': 'i', 't': 'Variable'}, {'n': '+', 't': 'Addition', 'c': [{'n': 'i', 't': 'Variable'}, {'n': 1, 't': 'Constant'}]}]}]}]}]})
        operand2= exp.deserialize(serialized)
        context = {}
        exp.eval(operand2,context)
        self.assertEqual(context['output'],12)

# context = {"a":"1","b":2,"c":{"a":4,"b":5}}
# exp.solve('a=8',context)
# print(context['a'])

# context = {"a":[1,2,3,4,5],"b":0}
# exp.solve('a.filter(p:p<5).foreach(p: b=b+p)',context)
# print(context['b'])

# context = {"a":[1,2,3,4,5],"b":0}
# print(exp.solve('a.filter(p: p>1 && p<5).map(p: p*2)',context))

# TODO: esta expression falla , hay que solucionarlo
# context = {"a":[1,2,3,4,5],"b":0}
# print(exp.solve('a.filter(p: p>1 && p<5).map(p: p*2).reverse()',context))


# operand =exp.parse(('i=0;'
#                  'while(i<=6){'
#                  '  output=i*2;'
#                  '  i=i+1;'
#                  '}'))

# serialized = exp.serialize(operand)
# print(serialized)
# operand2= exp.deserialize(serialized)
# context = {}
# exp.eval(operand2,context)
# print(context['output'])

unittest.main()

# operand=exp.parse('(a+1)*(a-1)')
# context = {'a':3}
# token= Token()
# exp.debug(operand,token,context)
# print(token.path)
# print(token.value)
# exp.debug(operand,token,context)
# print(token.path)
# print(token.value)
# exp.debug(operand,token,context)
# print(token.path)
# print(token.value)
# exp.debug(operand,token,context)
# print(token.path)
# print(token.value)
# exp.debug(operand,token,context)
# print(token.path)
# print(token.value)
# exp.debug(operand,token,context)
# print(token.path)
# print(token.value)
# exp.debug(operand,token,context)
# print(token.path)
# print(token.value)


# op = exp.parse('"expression".count("e")>= a+1')
# print(op.functions())
# unittest.main()
