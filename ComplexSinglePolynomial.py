from __future__ import annotations
from ComplexMultyPolynomial import ComplexMultyPolynomial, MultyPolinomial, finditer, LenghtError, Self, Any, Never, overload, floor, ceil
from SinglePolynomial import SinglePolynomial

Number = int|float|complex
Powers = dict[str,Number]
Unknowns = tuple[str,...]
Integrals = dict[str,list[str|Number]]

class ComplexSinglePolynomial(ComplexMultyPolynomial,SinglePolynomial):
    ...