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



git add .
git commit -m "."
git push
git tag 0.0.2 -m "v0.0.2"
git push --tags origin main

python setup.py sdist upload -r pypi

pip install mgr

pip install mgr --upgrade
