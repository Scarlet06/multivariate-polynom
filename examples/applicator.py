if __name__ == '__main__':
    import sys
    import os

    # getting the name of the directory
    # where the this file is present.
    current = os.path.dirname(os.path.realpath(__file__))

    # Getting the parent directory name
    # where the current directory is present.
    parent = os.path.dirname(current)

    # adding the parent directory to
    # the sys.path.
    sys.path.append(parent)

from Polynomial import MultyPolinomial,Self,overload,Number
from collections.abc import Callable

class applicator:

    __slots__ = ("m1","a", "b")
    def __new__(cls: type[Self], m:MultyPolinomial, a:Number, b:Number, print_all:bool=True) -> Self:
        
        if not isinstance(m,MultyPolinomial):
            raise TypeError("m has to be a MultyPolinomial")
        
        if not isinstance(a,Number) or not isinstance(a,Number) or a>b:
            raise TypeError("a and b have to be Numbers where a is greater than b")

        return super().__new__(cls)
        
    @overload
    def __new__(self: type[Self], m:MultyPolinomial, a:Number, b:Number) -> None:
        "Given a MultyPolinomial, it prints some applications using the given numbers"
        
    @overload
    def __init__(self, m:MultyPolinomial, a:Number, b:Number, print_all:bool=True) -> None:
        "Given a MultyPolinomial, it prints some applications using the given numbers if print_all is True"
        
    def __init__(self, m:MultyPolinomial, a:Number, b:Number, print_all:bool=True) -> None:
        
        self.m = m
        self.a = a
        self.b = b

        if print_all:
            ...

if __name__ == "__main__":
    a = MultyPolinomial({"3-5-4":1/3,"5-4-3":1/5,"6-3-2":1/7},("x","y","z"))
    b = MultyPolinomial({"2-1-0":1/3,"1-0-1":1/5,"0-0-2":1/7},("x","y","z"))
    applicator(a,b)
    