def prn(func):
    def low():
        
        lesbos = func().lower() + ' forever!!!'
        return lesbos
    return low

@prn
def second():
    return 'LESBOS'

# print(second())

import math

def cube(func):
    def c():
        a:int=math.pow(func(),4)
        
        return a
    return c

@cube
def num():
    return 4.1235

print(f'{num():.2f}')