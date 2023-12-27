# Py Expression

Py-expression is an extensible expression evaluator and parser.
Besides the operators, functions, variables, objects and arrays that are supported; it is possible to extend it with your own functions, operators, etc.

## Features

- Parse and evaluate
  - Arithmetic operators
  - assignment operators
    - comparison operators
    - Logical operators
    - Bitwise Operators
    - Variables
    - Constants
    - Functions
    - Objects
    - Arrays
    - Enums
- Simplify math operations where operands are constant
- It allows to extend the model by adding or overwriting operators, functions and enums
- Supports multiline expressions using the semicolon character to separate them
- The evaluation receives the context where the variables will be read, written, and created. This context must be a dictionary or a class derived from a dictionary
- When parsing a string that contains expression, an expression object is returned, which can be reused to evolve the expression with different contexts, in this way the performance is notably improved.
- You can create a new expression object using expression objects and combining them with operators

## Wiki

[Home](https://github.com/FlavioLionelRita/py-expression/wiki)

## Use

### Exp

Exp is the main class of the library that contains the methods to parse, evaluate, get info of expression, etc . In order to use the library you need to create an instance of this class:

```python
from py_expression.core import Exp
exp = Exp()
```

### Parse

```python
from py_expression.core import Exp
exp = Exp()
operand =exp.parse('a+4')
```

### Eval

```python
from py_expression.core import Exp

exp = Exp()
operand =exp.parse('a+4')
result = exp.eval(operand,{"a":2})
```

```python
from py_expression.core import Exp

exp = Exp()
operand =exp.parse('a+4')
result = operand.eval({"a":2})
```

```python
from py_expression.core import Exp

exp = Exp()
result =exp.parse('a+4').eval({"a":2})
```

### Work with expressions

reuse the parsed expression:

```python
from py_expression.core import Exp

exp = Exp()
op = exp.parse('sin(x)') 
xs=[]
ys=[] 
for x in range(-100,100):
    y=op.eval({"x":x})
    xs.append(x)
    ys.append(y)  
```

create a new expression based on two or more parsed expressions:

```python
from py_expression.core import Exp

exp = Exp()
op1 = exp.parse('a+1')
op2 = exp.parse('b')
op3 = (op1+op2)*(op1-op2) >= (op1*2)

result1= op3.eval({"a":1,"b":2})
result2= op3.eval({"a":5,"b":9})

print(result1)
print(result2)
```

## Project Examples

### Test Graph

In this project, the py-expression library is used to parse and evaluate expressions that a variable uses (in this case x) and the result is assigned to y.
then the point (x,y) is shown in a diagram.
In this example x takes the values from -100 to 100

- [github](https://github.com/FlavioLionelRita/py-expression-test-graph)

### Lib Opencv

Extend the expression library by adding enums and related functions to opencv

- [github](https://github.com/FlavioLionelRita/py-expression-lib-opencv)

### Test Opencv

In this project, the expression library and an opencv library that adds enums and functions is used to execute multi-line expressions that transform an image

- [github](https://github.com/FlavioLionelRita/py-expression-test-opencv)
