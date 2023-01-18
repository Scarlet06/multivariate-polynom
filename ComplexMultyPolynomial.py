from __future__ import annotations
from MultyPolynomial import MultyPolinomial, Iterable, Generator, Self, Any, Never, overload, floor, ceil, prod, randint

Number = int|float|complex
Powers = dict[str,Number]
Unknowns = tuple[str,...]
Integrals = dict[str,list[str|Number]]

class ComplexMultyPolynomial(MultyPolinomial):
    

    
    ## OPERATION WITH MULTIVARIATIVE POLYNOMIALS ##
    @staticmethod
    def _check__is_Number(__o:Any, error:str="{}"):
        "This function raises a TypeError if the given __o is not a Number"
        if not isinstance(__o, Number):
            raise TypeError(error.format(type(__o)))
