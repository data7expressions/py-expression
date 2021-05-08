import unittest
from py_expression.base import *
from py_expression.core import Exp,Token
from enum import Enum

exp = Exp()

class TestExpression(unittest.TestCase):

    def test_arithmetic(self):
        self.assertEqual(exp.run('1+1'),1+1)
        self.assertEqual(exp.run('3+2-1'),3+2-1) 
        self.assertEqual(exp.run('3*4-1'),3*4-1)
        self.assertEqual(exp.run('1+4*2'),1+4*2)
        self.assertEqual(exp.run('4+4+2+50+600'),4+4+2+50+600)
        self.assertEqual(exp.run('1-2-5'),1-2-5)
        self.assertEqual(exp.run('(1+4)*2'),(1+4)*2)
        self.assertEqual(exp.run('(2+3)*2'),(2+3)*2)
        self.assertEqual(exp.run('2*(3+2)'),2*(3+2))
        self.assertEqual(exp.run('2*(3+2)*(2+2)'),2*(3+2)*(2+2))
        self.assertEqual(exp.run('1+2*3*4'),1+2*3*4)  
        self.assertEqual(exp.run('2*3+4*5'),2*3+4*5)
        self.assertEqual(exp.run('(1+(2**3)*4'),(1+(2**3)*4))
        self.assertEqual(exp.run('1+2**3*4'),1+2**3*4) 
        self.assertEqual(exp.run('1+2**(3*4)'),1+2**(3*4))

    def test_comparisons(self):         
        self.assertEqual(exp.run('3>2'),3>2)
        self.assertEqual(exp.run('3>2*2'),3>2*2)
        self.assertEqual(exp.run('-3>2*2'),-3>2*22)
        self.assertEqual(exp.run('4>=2*2'),4>=2*2)
        self.assertEqual(exp.run('3<=2*2'),3<=2*2)
        self.assertEqual(exp.run('3!=2*2'),3!=2*2)
        self.assertEqual(exp.run('4!=2*2'),4!=2*2)
        self.assertEqual(exp.run('-4!=2*2'),-4!=2*2)
        self.assertEqual(exp.run('-4==-2*2'),-4==-2*2)
        self.assertEqual(exp.run('-4==-(2*2)'),-4==-(2*2))

    def test_variables(self):
        self.assertEqual(exp.run('a>b',{"a":1,"b":2}),False)
        self.assertEqual(exp.run('a+b',{"a":1,"b":2}),3)
        self.assertEqual(exp.run('-a*b',{"a":1,"b":2}),-2)
        self.assertEqual(exp.run('a*3==b+1',{"a":1,"b":2}),True)
        self.assertEqual(exp.run('(a*b)+(2*a+2*b)',{"a":1,"b":2}),8)
        self.assertEqual(exp.run('2**b+a',{"a":1,"b":2}),5) 
        self.assertEqual(exp.run('c.b',{"a":"1","b":2,"c":{"a":4,"b":5}}),5)

    def test_strings(self):
        self.assertEqual(exp.run('"a"'),"a") 
        self.assertEqual(exp.run('"a"<"b"'),"a"<"b") 
        self.assertEqual(exp.run('"a ""b"" "<"b"'),"a ""b"" "<"b") 

    def test_assigments(self):
        context = {"a":"1","b":2,"c":{"a":4,"b":5}}
        exp.run('a=8',context)
        self.assertEqual(context['a'],8)
        exp.run('c.a=1',context)
        self.assertEqual(context['c']['a'],1)

    def test_functions(self):
        self.assertEqual(exp.run('nvl(a,b)',{"a":None,"b":2}),2) 
        self.assertEqual(exp.run('capitalize(a)',{"a":"aaa","b":2}),"Aaa")  
        self.assertEqual(exp.run('capitalize("aaa")'),"Aaa") 
        self.assertEqual(exp.run('strCount(a,"a")',{"a":"aaa"}),3)
        self.assertEqual(exp.run('strCount(a,"b")',{"a":"aaa"}),0) 
        self.assertEqual(exp.run('upper(a)',{"a":"aaa"}),"AAA") 

    def test_enums(self):

        class TestEnumLib(Library):
            def __init__(self):
                super(TestEnumLib,self).__init__('testEnum')   
                self.initEnums()
            
            def initEnums(self):
                self.addEnum('ColorConversion',{"BGR2GRAY":6,"BGR2HSV":40,"BGR2RGB":4,"GRAY2BGR":8,"HSV2BGR":54
                                              ,"HSV2RGB":55,"RGB2GRAY":7,"RGB2HSV":41})

                class Color(Enum):
                    RED = 1
                    GREEN = 2
                    BLUE = 3 

                self.addEnum('Color',Color) 

        exp.addLibrary(TestEnumLib())
        
        self.assertEqual(exp.run('ColorConversion.GRAY2BGR'),8)
        self.assertEqual(exp.run('Color.GREEN'),2)  

    def test_multine(self):    
        text='a=4; '\
             'b=a+2; '\
            ' output=a*b; ' 
        context = {}
        exp.run(text,context)
        self.assertEqual(context['output'],24)

    def test_blockControl(self):        
        context = {}
        exp.run(('output=1;if(1==2){output=2}else {output=3}'),context)
        self.assertEqual(context['output'],3)

        exp.run('output=1;if(1==1){output=2;}else {output=3;}',context)
        self.assertEqual(context['output'],2)

        exp.run(('if(1==2){'
                   '    output=2'
                   '}else {'
                   '    output=3'
                   '}'),context)
        self.assertEqual(context['output'],3)
      
        exp.run(('i=0;'
                 'while(i<=6){'
                 '  output=i*2;'
                 '  i=i+1;'
                 '}'),context)
        self.assertEqual(context['output'],12)   

    def test_initializeLines(self):            
        text = ('rectangle = {"x":50,"y":50,"width":80,"height":60}; '
               'sleepSecs = 1;'
               'source=nvl(source,"data/source.jpg");')
        context = {}
        exp.run(text,context)
        self.assertEqual(context['rectangle']['x'],50)

    def test_arrowFunctions(self):            
        context = {"a":[1,2,3],"b":0}
        exp.run('a.foreach(p=>b=b+p)',context)
        self.assertEqual(context['b'],6) 
        context = {"a":[1,2,3,4,5],"b":0}
        exp.run('a.filter(p=> p<5).foreach(p => b=b+p)',context)
        self.assertEqual(context['b'],10) 
        context = {"a":[1,2,3,4,5],"b":0}
        self.assertEqual(exp.run('a.first(p => p%2==0)',context),2) 
        context = {"a":[1,2,3,4,5],"b":0}
        self.assertEqual(exp.run('a.last(p=> p%2==0)',context),4) 
        context = {"a":[1,2,3,4,5],"b":0}
        self.assertEqual(exp.run('a.filter(p=> p>1 && p<5).map(p=> p*2)',context),[4,6,8])
        context = {"a":[1,2,3,4,5],"b":0}
        self.assertEqual(exp.run('a.filter(p=> p>1 && p<5).reverse()',context),[4,3,2])
        context = {"a":[1,2,3,4,5],"b":0}
        self.assertEqual(exp.run('a.filter(p=> p>1 && p<5).map(p=> p*2).reverse()',context),[8,6,4])

    def test_token(self): 

        self.assertEqual(exp.run('2**b+a',{"a":1,"b":2},Token()),5) 
        self.assertEqual(exp.run('c.b',{"a":"1","b":2,"c":{"a":4,"b":5}},Token()),5)

        text='a=4; '\
             'b=a+2; '\
            ' output=a*b; ' 
        context = {}
        exp.run(text,context,Token())
        self.assertEqual(context['output'],24)

        context = {}
        exp.run(('if(1==2){'
                   '    output=2'
                   '}else {'
                   '    output=3'
                   '}'),context,Token())
        self.assertEqual(context['output'],3)

        
        context = {"a":[1,2,3,4,5],"b":0}
        self.assertEqual(exp.run('a.filter(p=> p>1 && p<5).reverse()',context,Token()),[4,3,2])
        context = {"a":[1,2,3,4,5],"b":0}
        self.assertEqual(exp.run('a.filter(p=> p>1 && p<5).map(p=> p*2).reverse()',context,Token()),[8,6,4]) 

    def test_info(self):
        node = exp.parse('strCount("expression","e")>= a+1')
        self.assertEqual(exp.vars(node),{'a': 'any'})
        self.assertEqual(exp.constants(node),{'expression': 'str', 'e': 'str', 1: 'int'})
        self.assertEqual(exp.operators(node),{'>=': 'comparison', '+': 'arithmetic'})
        self.assertEqual(exp.functions(node)['strCount']['signature'] ,'(self:str,x:str,start:int=None,end:int=None)->int' )  

        node = exp.parse('a-1')
        self.assertEqual(exp.vars(node), {'a': 'float'})
        node = exp.parse('a && true')
        self.assertEqual(exp.vars(node), {'a': 'bool'})
        node = exp.parse('a > 1')
        self.assertEqual(exp.vars(node), {'a': 'int'})
        node = exp.parse('a > "a"')
        self.assertEqual(exp.vars(node), {'a': 'str'})

        op = exp.compile('strCount("expression","e")>= a+1')
        self.assertEqual(exp.vars(op),{'a': 'any'})
        self.assertEqual(exp.constants(op),{'expression': 'str', 'e': 'str', 1: 'int'})
        self.assertEqual(exp.operators(op),{'>=': 'comparison', '+': 'arithmetic'})
        self.assertEqual(exp.functions(op)['strCount']['signature'] ,'(self:str,x:str,start:int=None,end:int=None)->int' ) 

        op = exp.compile('a-1')
        self.assertEqual(exp.vars(op), {'a': 'float'})
        op  = exp.compile('a && true')
        self.assertEqual(exp.vars(op ), {'a': 'bool'})
        op  = exp.compile('a > 1')
        self.assertEqual(exp.vars(op ), {'a': 'int'})
        op  = exp.compile('a > "a"')
        self.assertEqual(exp.vars(op ), {'a': 'str'})

    def test_serialize(self): 
        node =exp.parse(('i=0;'
                 'while(i<=6){'
                 '  output=i*2;'
                 '  i=i+1;'
                 '}'))
        serialized = exp.serialize(node)
        self.assertEqual(serialized,{'id': '0', 'n': 'block', 't': 'block', 'c': [{'id': '0.0', 'n': '=', 't': 'operator', 'c': [{'id': '0.0.0', 'n': 'i', 't': 'variable', 'c': []}, {'id': '0.0.1', 'n': 0, 't': 'constant', 'c': []}]}, {'id': '0.1', 'n': 'while', 't': 'while', 'c': [{'id': '0.1.0', 'n': '<=', 't': 'operator', 'c': [{'id': '0.1.0.0', 'n': 'i', 't': 'variable', 'c': []}, {'id': '0.1.0.1', 'n': 6, 't': 'constant', 'c': []}]}, {'id': '0.1.1', 'n': 'block', 't': 'block', 'c': [{'id': '0.1.1.0', 'n': '=', 't': 'operator', 'c': [{'id': '0.1.1.0.0', 'n': 'output', 't': 'variable', 'c': []}, {'id': '0.1.1.0.1', 'n': '*', 't': 'operator', 'c': [{'id': '0.1.1.0.1.0', 'n': 'i', 't': 'variable', 'c': []}, {'id': '0.1.1.0.1.1', 'n': 2, 't': 'constant', 'c': []}]}]}, {'id': '0.1.1.1', 'n': '=', 't': 'operator', 'c': [{'id': '0.1.1.1.0', 'n': 'i', 't': 'variable', 'c': []}, {'id':'0.1.1.1.1', 'n': '+', 't': 'operator', 'c': [{'id': '0.1.1.1.1.0', 'n': 'i', 't': 'variable', 'c': []}, {'id': '0.1.1.1.1.1', 'n': 1, 't': 'constant', 'c': []}]}]}]}]}]})
        node2= exp.deserialize(serialized,'Node')
        self.assertEqual(node2.children[0].type,'operator')  
        self.assertEqual(node2.children[0].name,'=')

        operand= exp.deserialize(serialized,'Operand')
        context = {}
        exp.run(operand,context)
        self.assertEqual(context['output'],12) 

# operand=exp.compile('(a+1)*(a-1)')
# context = {'a':3}
# token= Token()
# result = exp.run(operand,context,token)
# print(token.stack)

# context = {"a":"1","b":2,"c":{"a":4,"b":5}}
# exp.run('a=8',context)
# print(context['a'])

# print(exp.run('a>b',{"a":1,"b":2}))

# token= Token()
# context = {}
# exp.run(('i=0;'
#          'while(i<=6){'
#          '  output=i*2;'
#          '  if(output%2==0){ signal("signal_1"); }'
#          '  else { signal("signal_2"); }'
#          '  i=i+1;'
#          '}'),context,token)
# print(context['output'],12)
# print(token) 

# print(exp.run('3>2'),3>2)
# context = {"a":[1,2,3,4,5],"b":0}
# print(exp.run('a.filter(p=> p>1 && p<5).reverse()',context,Token()),[4,3,2])
unittest.main()

# operand=exp.compile('(a+1)*(a-1)')
# context = {'a':3}
# token= Token()
# result = exp.eval(operand,context,token)
# print(result)
# print(token.stack)
# exp.debug(operand,token,context)
# print(token.stack)
# print(token.value)
# exp.debug(operand,token,context)
# print(token.stack)
# print(token.value)
# exp.debug(operand,token,context)
# print(token.stack)
# print(token.value)
# exp.debug(operand,token,context)
# print(token.stack)
# print(token.value)
# exp.debug(operand,token,context)
# print(token.stack)
# print(token.value)
# exp.debug(operand,token,context)
# print(token.stack)
# print(token.value)


# op = exp.parse('"expression".count("e")>= a+1')
# print(op.functions())
# unittest.main()

