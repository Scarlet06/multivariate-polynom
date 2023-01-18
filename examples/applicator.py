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

from MultyPolynomial import MultyPolinomial,Self,overload,Number
from random import choices

class applicator:

    __slots__ = ("m", "a", "b", 'c')
    def __new__(cls: type[Self], m:MultyPolinomial, a:Number, b:Number, print_all:bool=True) -> Self:
        
        if not isinstance(m,MultyPolinomial):
            raise TypeError("m has to be a MultyPolinomial")
        
        if not isinstance(a,Number) or not isinstance(a,Number) or a>b:
            raise TypeError("a and b have to be Numbers where a is greater than b")

        return super().__new__(cls)
        
    def __init__(self: type[Self], m:MultyPolinomial, a:Number, b:Number) -> None:
        "Given a MultyPolinomial, it prints some applications using the given numbers"
        
    @overload
    def __init__(self, m:MultyPolinomial, a:Number, b:Number, print_all:bool=True) -> None:
        "Given a MultyPolinomial, it prints some applications using the given numbers if print_all is True"
        
    def __init__(self, m:MultyPolinomial, a:Number, b:Number, print_all:bool=True) -> None:
        
        self.m = m
        self.a = a
        self.b = b
        self.c=(b+a)/2

        if print_all:
            self.beautiful_print()

    def evaluate(self) -> bool:
        "this evaluates the MultyPolinomial in the median point in the first unknown"

        r = self.m.evaluate(self.c)
        s = self.m.copy()
        s.evaluate_ip(self.c)

        return str(r==s)

    def evaluate_all(self) -> bool:
        "this evaluates the MultyPolinomial in the median point in the first unknown"

        r = self.m.evaluate([self.c]*len(self.m))
        s = MultyPolinomial.fromText(str(self.m([self.c]*len(self.m),True)),self.m.unknown)

        t = self.m.copy()
        t.evaluate_ip([self.c]*len(self.m))

        return str(all((r==s,r==t,t==s)))

    def partial(self) -> bool:
        "this method applies a partial derivation"
        
        r = self.m.partial(self.m.unknown[0])
        s = self.m.copy()
        s.partial_ip(self.m.unknown[0])

        return str(r==s)

    def n_partial(self) -> bool:
        "this method applies a partial derivation to x, x and y"
        
        r = self.m.n_partial(*self.m._unkn)
        s = self.m.copy()
        s.n_partial_ip(*self.m._unkn)

        return str(r==s)

    def integral(self) -> bool:
        "this method applies a partial derivation"
        
        r = self.m.integral(self.m.unknown[0])
        s = self.m.copy()
        s.integral_ip(self.m.unknown[0])

        return str(r==s)

    def n_integral(self) -> bool:
        "this method applies a partial derivation to x, x and y"
        
        r = self.m.n_integral(*self.m._unkn)
        s = self.m.copy()
        s.n_integral_ip(*self.m._unkn)

        return str(r==s)

    def integral_AB(self) -> bool:
        "this method applies a partial derivation"
        
        r = self.m.integralAB(self.m.unknown[0],self.a,self.b)
        s = self.m.copy()
        s.integralAB_ip(self.m.unknown[0],self.a,self.b)

        return str(r==s)

    def n_integralAB(self) -> bool:
        "this method applies a partial derivation to x, x and y"

        k = {u:(self.a,self.b) for u in self.m._unkn}
        r = self.m.n_integralAB(**k)
        s = self.m.copy()
        s.n_integralAB_ip(**k)

        return str(r==s)

    def beautiful_print(self):
        m=self.m.clean()
        print(f"{chr(9487)}{chr(9473)*2} {m=}")
        print(f"{chr(9504)}{chr(9472)}{'evaluation:':<20}{self.evaluate()}")
        print(f"{chr(9504)}{chr(9472)}{'full evaluation:':<20}{self.evaluate_all()}")
        print(f"{chr(9504)}{chr(9472)}{'partial:':<20}{self.partial()}")
        print(f"{chr(9504)}{chr(9472)}{'n partial:':<20}{self.n_partial()}")
        print(f"{chr(9504)}{chr(9472)}{'integral:':<20}{self.integral()}")
        print(f"{chr(9504)}{chr(9472)}{'n integral:':<20}{self.n_integral()}")
        print(f"{chr(9504)}{chr(9472)}{'integral [a,b]:':<20}{self.integral_AB()}")
        print(f"{chr(9504)}{chr(9472)}{'n integral [a,b]:':<20}{self.n_integralAB()}")

if __name__ == "__main__":
    from creator import m_random_unkn
    applicator(m_random_unkn, 2, 5)
    