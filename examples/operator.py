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

class operator:

    __slots__ = ("m1","m2")
    def __new__(cls: type[Self], m1:MultyPolinomial, m2:MultyPolinomial|Number, print_all:bool=True) -> Self:
        if not isinstance(m1,MultyPolinomial) or not isinstance(m2,MultyPolinomial|Number):
            raise TypeError("this method has to be used only with MultyPolinomial or eventually Numbers")

        return super().__new__(cls)
        
    @overload
    def __init__(self, m1:MultyPolinomial, m2:MultyPolinomial|Number) -> Self:
        "Given a MultyPolinomial, it prints all the operations between m1 and m2"
        
    @overload
    def __init__(self, m1:MultyPolinomial, m2:MultyPolinomial|Number, print_all:bool=True) -> None:
        "Given a MultyPolinomial, it prints all the operations between m1 and m2 if print_all is True"
        
    def __init__(self, m1:MultyPolinomial, m2:MultyPolinomial|Number, print_all:bool=True) -> None:
        
        self.m1 = m1
        self.m2 = m2

        if print_all:
            self.beautiful_print()

    def eq_add(self) -> bool:
        "m1+m2 == (m1+=m2)"

        s = self.m1+self.m2
        t=self.m1.copy()
        t+=self.m2
        return s==t

    def eq_sub(self) -> bool:
        "m1-m2 == (m1-=m2)"

        s = self.m1-self.m2
        t=self.m1.copy()
        t-=self.m2
        return s==t

    def eq_mul(self) -> bool:
        "m1*m2 == (m1*=m2)"

        s = self.m1*self.m2
        t=self.m1.copy()
        t*=self.m2
        return s==t

    def eq_pow(self):
        "m1**3 == (m1**=3)"

        s = self.m1**2
        t=self.m1.copy()
        t**=2
        return s==t


    def eq_div(self) -> bool:
        "m1//m2==(m1//=m2)"

        s = self.m1//self.m2
        t=self.m1.copy()
        t//=self.m2
        return s==t

    def eq_mod(self) -> bool:
        "m1%m2 == (m1%=m2)"

        s = self.m1%self.m2
        t=self.m1.copy()
        t%=self.m2
        return s==t

    def eq_divmod(self) -> bool:
        "q,r = m1.divmod(m1,m2)\n(m2*q) + r == m1"

        q,r = self.m1.divmod(self.m2)
        return self.m2*q+r==self.m1

    def aeq_divmod(self) -> bool:
        "q,r = m1.divmod(m1,m2)\n(m2*q) + r ~= m1"

        q,r = self.m1.divmod(self.m2)
        return self.m1.almost_equal(self.m2*q+r)


    def beautiful_print(self) -> None:
        "It sets everything to have a beautiful rectangular shape print"
        self._print_rect(self.eq_add, self.eq_sub, self.eq_mul, self.eq_pow, self.eq_div, self.eq_mod, self.eq_divmod, self.aeq_divmod)

    @staticmethod
    def _start() -> str:
        "It returns a raw of #"
        return "="*40

    @staticmethod
    def _border(func:Callable[[],str]|None=None) -> str:
        "it returns the border to continue the print"
        if not func:
            return "# "
        s='\n'
        return f"# {func.__doc__.replace(s,f'{s}# ')}:\t{func()}"

    def _print_rect(self, *what:Callable[[],str]) -> None:
        "It prints the actual rect"
        print(f'{self._border()}{self._start()}')
        for arg in what:
            print(self._border())
            print(self._border(arg))
            
        print(self._border())
        print("\n")

if __name__ == "__main__":
    a = MultyPolinomial({"3-5-4":1/3,"5-4-3":1/5,"6-3-2":1/7},("x","y","z"))
    b = MultyPolinomial({"2-1-0":1/3,"1-0-1":1/5,"0-0-2":1/7},("x","y","z"))
    operator(a,b)