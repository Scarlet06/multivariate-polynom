from __future__ import annotations
from ComplexMultyPolynomial import ComplexMultyPolynomial, MultyPolinomial, findall,match, LenghtError, Self, Any, Never, overload, floor, ceil, Number
from SinglePolynomial import SinglePolynomial, Unknowns

Powers = dict[int,Number]
Integrals = dict[int,list[str|Number]]

class ComplexSinglePolynomial(SinglePolynomial,ComplexMultyPolynomial):
    "This object is used to create and match the needs for a polinomial in a single variable with complex coef"
    #it is settet this way 'couse SinglePolynomial methods overwrites over ComplexMultyPolynomial methods

    #the only variables used by the object
    __slots__ = ()

    ## SOME INITIALIZATION && CLASSMETHODS ##
    @classmethod
    def fromMulty(cls: type[Self], m:MultyPolinomial) -> Self:
        """
        Given another MultyPolinomial it creates a new ComplexSinglePolynomial with the same informations
        """

        return super().fromMulty(m)

    @classmethod
    def fromComplexMulty(cls: type[Self], m:ComplexMultyPolynomial) -> Self:
        """
        Given another ComplexMultyPolynomial it creates a new ComplexSinglePolynomial with the same informations
        """

        return super().fromMulty(m)

    @classmethod
    def fromSingle(cls: type[Self], s:SinglePolynomial) -> Self:
        """
        Given another SinglePolynomial it creates a new ComplexSinglePolynomial with the same informations
        """

        return super().fromSingle(s)

    @classmethod
    def fromComplexSingle(cls: type[Self], s:SinglePolynomial) -> Self:
        """
        Given another SinglePolynomial it creates a new ComplexSinglePolynomial with the same informations
        """

        return super().fromSingle(s)

    @overload
    @classmethod
    def fromText(cls: type[Self], text:str) -> Self:
        """
        Given a string of text it tries to create the polinom.
        the string has to be formatted, writing every multiplication *, even between coef and unknown. The exponential has to be written with ^. It doesn't understand parenthesis
        The only way to add a complex number is by placing it in parenthesis, the complex part has to be set to j.
        More complex forms can be achieved by applaying math operation between multiple SinglePolynomial
        """

    @overload
    @classmethod
    def fromText(cls: type[Self], text:str, unknown:Unknowns="x") -> Self:
        """
        Given a string of text it tries to create the polinom.
        the string has to be formatted, writing every multiplication *, even between coef and unknown. The exponential has to be written with ^. It doesn't understand parenthesis
        The only way to add a complex number is by placing it in parenthesis, the complex part has to be set to j.
        More complex form can be achieved by applaying math operation between multiple SinglePolynomial

        If a unknown str is given, it will be used when not present in text
        """

    @overload
    @classmethod
    def fromText(cls: type[Self], text:str, unknown:Unknowns="", integrals_coefficients:Integrals|None={}) -> Self:
        """
        Given a string of text it tries to create the polinom.
        the string has to be formatted, writing every multiplication *, even between coef and unknown. The exponential has to be written with ^. It doesn't understand parenthesis
        The only way to add a complex number is by placing it in parenthesis, the complex part has to be set to j.
        More complex form can be achieved by applaying math operation between multiple SinglePolynomial

        If a unknown str is given, it will be used when not present in text

        integrals_coefficients have to be in the right format.
        if unknown = "z", each item has to be: 3: ['C0',5] -> 5*C0*z^3
        """

    @classmethod
    def fromText(cls: type[Self], text:str, temp_unknown:Unknowns="x", integrals_coefficients:Integrals|None=None) -> Self:

        num = r'^[+-]?(?:(?:\d+)?(?:\.)?(?:\d+)?)$'

        unknown = ""
        t = {}

        replacer = "{}"
        complexes = []
        for m in findall(r'(\((?:(?:[+-]?\d+(?:\.\d+)?)?|(?:[+-]?(?:\d+)?(?:\.\d+)?j)?)+\))', text):
            text = text.replace(m,replacer)
            try:
                complexes.append(complex(m))
            except:
                complexes.append(complex(eval(m)))
        
        text = text.replace("-","+-")
        if text.startswith("+"):
            text = text[1:]

        for part in text.split("+"):
            power = "0"
            coef = "1"
            for p in part.split("*"):

                if not p:
                    continue

                if p.startswith("-"):
                    coef+=f"*(-1)"
                    p=p[1:]

                if "^" in p:

                    if replacer in p:
                        _, val = p.split("^")
                        coef+=f"*({complexes.pop(0)}**{val})"
                        continue

                    i, val = p.split("^")

                    x = match(num,i)
                    if x:
                        coef+=f"*({i}**{val})"
                        continue

                    if i == unknown:
                        power+=f"+{val}"
                        continue
                    
                    elif unknown:
                        raise ValueError("Too many Unknowns for this ComplexSinglePolynomial")
                    unknown=i
                    power=f"{val}"
                    continue
                    
                if replacer in p:
                    coef+=f"*{complexes.pop(0)}"
                    continue

                x = match(num,p)
                if x:
                    coef+=f"*{p}"
                    continue

                elif p == unknown:
                    power+="+1"
                    continue
                    
                elif unknown:
                    raise ValueError("Too many Unknowns for this SinglePolynomial")
                unknown=p
                power="1"

            power = eval(power)
            coef = eval(coef)

            if power in t:
                t[power] += coef
                continue
            
            t[power] = coef

        if not unknown:
            unknown = temp_unknown

        if integrals_coefficients:
            if not all(isinstance(p,int) for p in integrals_coefficients):
                raise LenghtError("All the key used in 'integrals_coefficients' have to be numbers of type int")

            return cls(t,unknown, integrals_coefficients)

        return cls(t,unknown, {})


    ## SOME INTERESTING METHODS ##
    def is_MultyPolynomial(self) -> bool:
        "It returns True if it is a real polynomial"
        return super().is_MultyPolynomial()

    def is_SinglePolynomial(self) -> bool:
        "It returns True if it is a real polynomial"
        return super().is_MultyPolynomial()

    def toMulty(self) -> MultyPolinomial:
        "It convert this complex single polynomial into a multy real one"
        return MultyPolinomial({str(power):coef if not isinstance(coef,complex) else coef.real for power,coef in self._pcoef.items()},(self._unkn,),{str(power):coef.copy() if not isinstance(coef[1],complex) else [coef[0],coef[1].real] for power,coef in self._icoef.items()})
    
    def toSingle(self) -> SinglePolynomial:
        "It convert this complex single polynomial into a single real one"
        return SinglePolynomial({power:coef if not isinstance(coef,complex) else coef.real for power,coef in self._pcoef.items()},self._unkn,{power:coef.copy() if not isinstance(coef[1],complex) else [coef[0],coef[1].real] for power,coef in self._icoef.items()})
    
    def toComplexMulty(self) -> ComplexMultyPolynomial:
        "It convert this complex single polynomial into a multy one"
        return ComplexMultyPolynomial({str(power):coef for power,coef in self._pcoef.items()},(self._unkn,),{str(power):coef.copy() for power,coef in self._icoef.items()})
    

    ## STRING METHODS ##
    def __str__(self) -> str:
        """
        string of the MultyPolinomial

        if this MultyPolinomial has any Integrals, it will raise an error if used for fromText()
        Before to do so, is best practice to check if Integrals are present with has_integrals_const() or by passing 'i' at __format__()
        """
        
        s = ""
        
        for power,coef in sorted(self._pcoef.items(),key=lambda x:x[0],reverse=True):

            if not coef:
                continue

            if isinstance(coef,complex):
                s+="+("
                if coef.real:
                    s+=f"{coef.real:+}"
                if coef.imag:
                    s+=f"{coef.imag:+}j"
                s+=")"
            else:
                s+=f"{coef:+}"

            if not power:
                continue

            s+=f"*{self._unkn}"

            if power>=2:
                s+=f"^{power}"
        
        for power,coef in sorted(self._icoef.items(),key=lambda x:x[0],reverse=True):

            if not coef[1]:
                continue

            if isinstance(coef[1],complex):
                s+="+("
                if coef[1].real:
                    s+=f"{coef[1].real:+}"
                if coef[1].imag:
                    s+=f"{coef[1].imag:+}j"
                s+=f")*{coef[0]}"
            else:
                s+=f"{coef[1]:+}*{coef[0]}"

            if not power:
                continue

            s+=f"*{self._unkn}"

            if power>=2:
                s+=f"^{power}"

        if not s:
            return "0"

        return s.lstrip("+")

    def __format__(self, __format_spec: str) -> str:
        """
        The __format_spec can format individually the polynomial coef individually and the whole polynomial object,
        it is olso possible to format it without the integration parts. To get this, the formatting moda has to follow this:

        '[integrals][numbers][!!monomials][;;[polinomial]]'
        - integrals, if 'i' is given, integrals will be ignored, wherealse if 'ii' is given, the non integral part wuill be ignored. other formatting modes will be given to numbers
        - numbers, are the formatting spec for the numbers, following the standard formatting for numbers
        - monomials, are the formatting spec for the monomials as string
        - MultyPolinomial, are the formatting spec for the MultyPolinomials as string 
        """

        if __format_spec.startswith("ii"):
            numbers = __format_spec[2:]
            starter = False
            breaker = True
        elif __format_spec.startswith("i"):
            numbers = __format_spec[1:]
            starter = True
            breaker = True
        else:
            numbers = __format_spec
            starter = True
            breaker = False
        polynomial=monomials=""

        if "!!" in numbers:
            numbers,monomials = numbers.split("!!")
        
        if ";;" in numbers:
            numbers,polynomial = numbers.split(";;")
        elif ";;" in monomials:
            monomials,polynomial = monomials.split(";;")
        
        h = ("+","-")
        s = ""
        
        if starter:
            for power in sorted(self._pcoef.keys(),reverse=True):

                ks = ""
                coef = self._pcoef[power]

                if not coef:
                    continue

                if isinstance(coef,complex):
                    ks+="+("
                    if coef.real:
                        ks+=f"{coef.real:{numbers}}"
                    if coef.imag:
                        ks+=f"{coef.imag:{numbers}}j"
                    ks+=")"
                else:
                    ks+=f"{coef:{numbers}}"
                        
                if not power:
                    s+=f'{"+"*(not ks.startswith(h))}{f"{ks:{monomials}}"}'
                    continue

                ks+=f"*{self._unkn}"

                if power>=2:
                    ks+=f"^{power}"

                ks= f'{ks:{monomials}}'
                s+=f'{"+"*(not ks.startswith(h))}{ks}'

            if breaker:
                if not s:
                    return f"""{f"{f'{0:{numbers}}':{monomials}}":{polynomial}}"""
                return f"{s.strip('+'):{polynomial}}"

        for power in sorted(self._icoef.keys(),reverse=True):
            ks = ""
            coef = self._icoef[power]

            if not coef[1]:
                continue

            if isinstance(coef,complex):
                ks+="+("
                if coef.real:
                    ks+=f"{coef.real:{numbers}}"
                if coef.imag:
                    ks+=f"{coef.imag:{numbers}}j"
                ks+=f")*{coef[0]}"
            else:
                ks+=f"{coef[1]:{numbers}}*{coef[0]}"
                    
            if not power:
                s+=f'{"+"*(not ks.startswith(h))}{f"{ks:{monomials}}"}'
                continue

            ks+=f"*{self._unkn}"

            if power>=2:
                ks+=f"^{power}"
                    
            ks= f'{ks:{monomials}}'
            s+=f'{"+"*(not ks.startswith(h))}{ks}'

        if not s:
            return f"""{f"{f'{0:{numbers}}':{monomials}}":{polynomial}}"""
        return f"{s.strip('+'):{polynomial}}"

    


    ## TRASNFORMATIONS ##
    @overload
    def __round__(self) -> Self:
        """
        It returns a new ComplexSinglePolynomial with each coef rounded to the closer integer
        """
    
    @overload
    def __round__(self, __n:int|None = None) -> Self:
        """
        It returns a new ComplexSinglePolynomial with each coef in the given position
        """
    
    def __round__(self, __n:int|None = None) -> Self:

        return super().__round__(__n)

    def __floor__(self) -> Self:
        "It returns the ComplexSinglePolynomial with all the coefs floored"

        return super().__floor__()
        
    def __ceil__(self) -> Self:
        "It returns the ComplexSinglePolynomial with all the coefs ceiled"

        return super().__ceil__()


    ## OPERATION WITH MULTIVARIATIVE POLYNOMIALS ##
    @staticmethod
    def _check__is_Number(__o:Any, error:str="{}"):
        "This function raises a TypeError if the given __o is not a Number"
        if not isinstance(__o, Number):
            raise TypeError(error.format(type(__o)))

    def __divmod__(self, __o:Never) -> None:
        "Doesn't work here"

        raise TypeError("complex cannot be moduled nor floor-divided")

    def __rdivmod__(self, __o:Never) -> None:
        "Doesn't work here"

        raise TypeError("complex cannot be moduled nor floor-divided")
        
    def __floordiv__(self, __o:Never) -> None:
        "Doesn't work here"

        raise TypeError("complex cannot floor-divide nor be floor-divided")

    def __rfloordiv__(self,__o:Never) -> None:
        "Doesn't work here"

        raise TypeError("complex cannot floor-divide nor be floor-divided")

    def __ifloordiv__(self, __o:Never) -> None:
        "Doesn't work here"

        raise TypeError("complex cannot floor-divide nor be floor-divided")

    def __mod__(self, __o:Never) -> None:
        "Doesn't work here"

        raise TypeError("complex cannot module nor be moduled")
        
    def __rmod__(self,__o:Never) -> None:
        "Doesn't work here"

        raise TypeError("complex cannot module nor be moduled")

    def __imod__(self, __o:Never) -> None:
        "Doesn't work here"

        raise TypeError("complex cannot module nor be moduled")


if __name__ == '__main__':
    m = MultyPolinomial.fromText("x+y")
    cm = ComplexMultyPolynomial.fromText("(j)*x+y")
    s = SinglePolynomial.fromText("1+x")
    cs = ComplexSinglePolynomial.fromText("-(1)*x")

    from itertools import product
    for i,j in product((m,cm,s,cs),repeat=2):
        try:
            print(f'{f"{i.__class__.__name__:<3}+{j.__class__.__name__:>3}":<10}\n{((k:=i+j)).__class__.__name__:>5} = {k:+;;>4}')
        except:
            print(f'{f"{i.__class__.__name__:<3}+{j.__class__.__name__:>3}":<10}\n{"ERROR":>12}')
