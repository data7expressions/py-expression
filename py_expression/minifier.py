import re

class Minifier():
    def __init__(self):
       self.reAlphanumeric = re.compile('[a-zA-Z0-9_.]+$')

    def minify(self,expression)->str:
        isString=False
        quotes=None
        buffer = list(expression)
        length=len(buffer)
        result =[]
        i=0
        while i < length:
            p =buffer[i]        
            if isString and p == quotes: isString=False 
            elif not isString and (p == '\'' or p=='"'):
                isString=True
                quotes=p
            if isString:
                result.append(p)
            elif  p == ' ' :
                # solo deberia dejar los espacios cuando es entre caracteres alfanumericos. 
                # por ejemplo en el caso de "} if" no deberia quedar un espacio 
                if i+1 < length and self.reAlphanumeric.match(buffer[i-1]) and self.reAlphanumeric.match(buffer[i+1]):
                    result.append(p)                
            elif (p!='\n' and p!='\r' and p!='\t' ):
               result.append(p)
            i+=1   
        return result
 