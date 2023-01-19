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
from collections.abc import Callable

class operator:

    __slots__ = ("m1","m2")
    def __new__(cls: type[Self], m1:MultyPolinomial, m2:MultyPolinomial|Number, print_all:bool=True) -> Self:
        if not isinstance(m1,MultyPolinomial) or not isinstance(m2,MultyPolinomial|Number):
            raise TypeError("These methods has to be used only with MultyPolinomial or eventually Numbers")

        return super().__new__(cls)
        
    @overload
    def __init__(self, m1:MultyPolinomial, m2:MultyPolinomial|Number) -> Self:
        "Given a MultyPolinomial, it prints all the operations with the second or a Number"
        
    @overload
    def __init__(self, m1:MultyPolinomial, m2:MultyPolinomial|Number, print_all:bool=True) -> None:
        "Given a MultyPolinomial, it prints all the operations with the second or a Number if print_all is True"
        
    def __init__(self, m1:MultyPolinomial, m2:MultyPolinomial|Number, print_all:bool=True) -> None:
        
        self.m1 = m1.clean()
        self.m2 = m2
        if isinstance(m2,MultyPolinomial):
            self.m2.clean_ip()

        if print_all:
            self.beautiful_print()

    def add(self) -> MultyPolinomial:
        "It applies the sum"
        
        return self.m1+self.m2

    def eq_add(self) -> tuple[str,bool]:
        "m1+m2 == (m1+=m2)"

        s = self.add()
        t=self.m1.copy()
        t+=self.m2
        return t.__format__('.2f'),s==t

    def sub(self) -> MultyPolinomial:
        "It applies the subtraction"
        
        return self.m1-self.m2

    def eq_sub(self) -> tuple[MultyPolinomial,bool]:
        "m1-m2 == (m1-=m2)"

        s = self.sub()
        t=self.m1.copy()
        t-=self.m2
        return t.__format__('.2f'),s==t

    def mul(self) -> MultyPolinomial:
        "It applies the multiplication"
        
        return self.m1*self.m2

    def eq_mul(self) -> tuple[MultyPolinomial,bool]:
        "m1*m2 == (m1*=m2)"

        s = self.mul()
        t=self.m1.copy()
        t*=self.m2
        return t.__format__('.2f'),s==t

    def pow(self) -> MultyPolinomial:
        "It raises to the power of 3"
        
        return self.m1**3

    def eq_pow(self):
        "m1**3 == (m1**=3)"

        s = self.pow()
        t=self.m1.copy()
        t**=3
        return t.__format__('.2f'),s==t

    def div(self) -> MultyPolinomial:
        "It applies the floor division"
        
        return self.m1//self.m2

    def eq_div(self) -> tuple[MultyPolinomial,bool]:
        "m1//m2==(m1//=m2)"

        s = self.div()
        t=self.m1.copy()
        t//=self.m2
        return t.__format__('.2f'),s==t

    def mod(self) -> MultyPolinomial:
        "It applies the modulation"
        
        return self.m1%self.m2

    def eq_mod(self) -> tuple[MultyPolinomial,bool]:
        "m1%m2 == (m1%=m2)"

        s = self.mod()
        t=self.m1.copy()
        t%=self.m2
        return t.__format__('.2f'),s==t

    def divmod(self) -> tuple[MultyPolinomial,MultyPolinomial]:
        "It applies the subtraction"
        
        return self.m1.divmod(self.m2)

    def eq_divmod(self) -> tuple[MultyPolinomial,bool]:
        "q,r = m1.divmod(m1,m2)\n(m2*q) + r == m1"

        q,r = self.divmod()
        return f"q={q}\tr={r}",self.m2*q+r==self.m1

    def aeq_divmod(self) -> tuple[MultyPolinomial,bool]:
        "q,r = m1.divmod(m1,m2)\n(m2*q) + r ~= m1"

        q,r = self.divmod()
        return f"q={q}\tr={r}",self.m1.round_equal(self.m2*q+r)

    def beautiful_print(self) -> None:
        "It sets everything to have a beautiful rectangular shape print"
        self._print_rect(self.eq_add, self.eq_sub, self.eq_mul, self.eq_pow, self.eq_div, self.eq_mod, self.eq_divmod, self.aeq_divmod)

    @staticmethod
    def _start(m1,m2) -> str:
        "It returns a raw of #"
        return f'### m1={m1} # m2={m2} ###'

    @staticmethod
    def _border(func:Callable[[],str]|None=None) -> str:
        "it returns the border to continue the print"
        if not func:
            return "# "
        s='\n'
        try:
            t = func()
            return f"# {t[0]}\n# {func.__doc__.replace(s,f'{s}# ')}:\t{t[1]}"
        except Exception as e:
            return f"% {func.__name__}:\t{e}"


    def _print_rect(self, *what:Callable[[],str]) -> None:
        "It prints the actual rect"
        print(f'{self._border()}{self._start(self.m1,self.m2)}')
        for arg in what:
            print(self._border())
            print(self._border(arg))
            
        print(self._border())
        print("\n")

if __name__ == "__main__":
    a = MultyPolinomial({"3-5-4":1/3,"5-4-3":1/5,"6-3-2":1/7},("x","y","z"))
    b = MultyPolinomial({"2-1-0":1/3,"1-0-1":1/5,"0-0-2":1/7},("x","y","z"))
    operator(a,b)
    