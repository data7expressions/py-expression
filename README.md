# py-expression


type        |pattern
------------|-------------
number      |##.##
variable    |xxx  xxx.xxx
string      |'xxx' "xxx" 'x"x"x' "x'x'x" 'x''x''x' "x""x""x"
function    |xxx() xxx.xxx()
object      | {} {x:'xxx',x:##.##,x:xxx}     

# TODO: 
- variables
- resolver precedencia de operadores (exp: * sobre +)
- uso de parentecis
- deteccion de funcionnes
- arrays
- dictionaries
- asignaciones de variables
- separacion por ;
- metodos reduce para resolver previamente las operaciones entre constantes y dejar un solo operando constante

# References
- [operants](https://www.w3schools.com/python/python_operators.asp)
- [unit test](https://docs.python.org/3/library/unittest.html)
- [example](https://stackoverflow.com/questions/13055884/parsing-math-expression-in-python-and-solving-to-find-an-answer)

# Info
https://github.com/maja42/goval
https://www.programiz.com/python-programming/operator-overloading
https://golang.org/src/go/parser/parser.go
https://github.com/alecthomas/participle
https://github.com/zdebeer99/goexpression
https://github.com/Knetic/govaluate
https://pypi.org/project/py-expression-eval/
https://axiacore.com/blog/mathematical-expression-evaluator-python-524/
https://github.com/Maldris/mathparse
https://github.com/google/cel-go
https://github.com/golang/go/blob/master/src/go/parser/parser.go


