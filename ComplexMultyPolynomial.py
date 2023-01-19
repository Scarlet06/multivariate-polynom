from __future__ import annotations
from MultyPolynomial import MultyPolinomial, Iterable, Generator, LenghtError, Self, Any, Never, overload, floor, ceil, prod, randint
import re 

Number = int|float|complex
Powers = dict[str,Number]
Unknowns = tuple[str,...]
Integrals = dict[str,list[str|Number]]

class ComplexMultyPolynomial(MultyPolinomial):

    __slots__ = ()
    
    @classmethod
    def fromMulty(cls: type[Self], m:MultyPolinomial) -> Self:
        return cls(m._pcoef,m._unkn,m._icoef)

    @overload
    @classmethod
    def fromText(cls: type[Self], text:str) -> Self:
        """
        Given a string of text it tries to create the polinom.
        the string has to be formatted, writing every multiplication *, even between coef and unknown. The exponential has to be written with ^.
        The only way to add a complex number is by placing it in parenthesis, the complex part has to be set to j.
        More complex form have to be created by applaying math operation between multiple MultyPolinomial
        """

    @overload
    @classmethod
    def fromText(cls: type[Self], text:str, unknown:Unknowns=()) -> Self:
        """
        Given a string of text it tries to create the polinom.
        the string has to be formatted, writing every multiplication *, even between coef and unknown. The exponential has to be written with ^.
        The only way to add a complex number is by placing it in parenthesis, the complex part has to be set to j.
        More complex form have to be created by applaying math operation between multiple MultyPolinomial

        If a unknown str tuple is given, it will add these if are not present in the given text
        """

    @overload
    @classmethod
    def fromText(cls: type[Self], text:str, unknown:Unknowns=(), integrals_coefficients:Integrals={}) -> Self:
        """
        Given a string of text it tries to create the polinom.
        the string has to be formatted, writing every multiplication *, even between coef and unknown. The exponential has to be written with ^.
        The only way to add a complex number is by placing it in parenthesis, the complex part has to be set to j.
        More complex form have to be created by applaying math operation between multiple MultyPolinomial

        If a unknown str tuple is given, it will add these if are not present in the given text

        integrals_coefficients have to with each key by the right lenght and in the right format. It is better to not give anything
        If it is really needed, if unknown = ('x', 'y', 'q'), each item has to be: '0-2-1': ['C0',5] -> 5*C0*y^2*q
        """

    @classmethod
    def fromText(cls: type[Self], text:str, unknown:Unknowns=(), integrals_coefficients:Integrals={}) -> Self:
        unknown = list(unknown)
        t = {}

        pattern = r'(\(([+-]?\d+(\.\d+)?)?([+-]?(\d+)?(\.\d+)?j)?\))'
        match = re.finditer(pattern, text)
        replacer = "{}"
        complexes = []
        for m in match:
            text = text.replace(m[0],replacer)
            complexes.append(complex(m[0]))
        
        text = text.replace("-","+-")
        if text.startswith("+"):
            text = text[1:]
        for part in text.split("+"):
            power = ["0"]*len(unknown)
            coef = "1"
            for p in part.split("*"):

                if not p:
                    continue

                if p.startswith("-"):
                    coef+=f"*(-1)"
                    p=p[1:]

                if "^" in p:

                    if p[:p.index("^")].isalpha():
                        i, val = p.split("^")

                        if i in unknown:
                            power[unknown.index(i)]+=f"+{val}"
                            continue

                        unknown.append(i)
                        t = {po+"-0":co for po,co in t.items()}
                        power.append('0')
                        power[unknown.index(i)]+=f"+{val}"
                        continue

                    if replacer in p:
                        _, val = p.split("^")
                        coef+=f"*({complexes.pop(0)}**{val})"
                        continue
                    
                    coef+=f"*({i}**{val})"
                    continue

                if p.isalpha():

                    if p in unknown:
                        power[unknown.index(p)]+=f"+{1}"
                        continue

                    unknown.append(p)
                    t = {po+"-0":co for po,co in t.items()}
                    power.append('0')
                    power[unknown.index(p)]+=f"+{1}"
                    continue

                if replacer in p:
                    coef+=f"*{complexes.pop(0)}"
                    continue

                coef+=f"*{p}"

            power = "-".join(map(lambda x: str(eval(x)),power))
            coef = eval(coef)

            if power in t:
                t[power] += coef
                continue
            
            t[power] = coef

        if integrals_coefficients:
            l = len(unknown)
            if any((len(ic.split("-"))!=l for ic in integrals_coefficients)):
                raise LenghtError("all keys in 'integrals_coefficients' have to be len('unknown')")

        return cls(t,tuple(unknown), integrals_coefficients)


    ## SOME INTERESTING METHODS ##
    def is_real(self) -> bool:
        "It returns True if it is a real polynomial"
        return not (any(isinstance(coef,complex) for coef in self._pcoef.values()) or any(isinstance(coef[1],complex) for coef in self._pcoef.values()))
        
    def toMulty(self) -> MultyPolinomial:
        "It convert this complex multivariative polynomial into a real one"
        return MultyPolinomial({power:coef if not isinstance(coef,complex) else coef.real for power,coef in self._pcoef.items()},self._unkn,{power:coef[1] if not isinstance(coef,complex) else coef[1].real for power,coef in self._icoef.items()})
    
    def is_a_float_number(self) -> bool:
        """
        Retruns True if and only if there is not integration's constants and all the coef which degree is greater than 0 are 0 and the other is int
        """

        return self.is_a_number() and isinstance(self._pcoef[self._get_key_0(len(self._unkn))],float)

    def is_a_int_number(self) -> bool:
        """
        Retruns True if and only if there is not integration's constants and all the coef which degree is greater than 0 are 0 and the other is float
        """

        return self.is_a_number() and isinstance(self._pcoef[self._get_key_0(len(self._unkn))],int)

    def is_a_complex_number(self) -> bool:
        """
        Retruns True if and only if there is not integration's constants and all the coef which degree is greater than 0 are 0 and the other is complex
        """

        return self.is_a_number() and isinstance(self._pcoef[self._get_key_0(len(self._unkn))],complex)

    def __complex__(self) -> complex:
        "returns the 0 degree coef as complex"

        return complex(self._pcoef.get(self._get_key_0(len(self._unkn)),0))

    def __int__(self) -> int:
        "returns the 0 degree coef as int"

        coef = self._pcoef.get(self._get_key_0(len(self._unkn)),0)
        if isinstance(coef,complex):
            return int(coef.real)

        return int(coef)

    def __float__(self) -> float:
        "returns the 0 degree coef as float"

        coef = self._pcoef.get(self._get_key_0(len(self._unkn)),0.0)
        if isinstance(coef,complex):
            return float(coef.real)

        return float(coef)


    ## STRING METHODS ##
    def __str__(self) -> str:
        """
        string of the MultyPolinomial

        if this MultyPolinomial has any Integrals, it will raise an error if used for fromText()
        Before to do so, is best practice to check if Integrals are present with has_integrals_const() or by passing 'i' at __format__()
        """
        
        s = ""

        # _ = sorted(self._pcoef.keys(),reverse=True)

        for power,coef in sorted(self._pcoef.items(),key=lambda x:x[0],reverse=True):
            # coef = self._pcoef[power]

            if not coef:
                continue

            t = tuple(map(int,power.split("-")))

            if isinstance(coef,complex):
                s+="+("
                if coef.real:
                    s+=f"{coef.real:+}"
                if coef.imag:
                    s+=f"{coef.imag:+}j"
                s+=")"
            else:
                s+=f"{coef:+}"

            if not any(t):
                continue

            for p,i in zip(self._unkn,t):
                
                if not i:
                    continue

                s+=f"*{p}"

                if i>=2:
                    s+=f"^{i}"
                
        for power in sorted(self._icoef.keys(),reverse=True):
            coef = self._icoef[power]

            if not coef[1]:
                continue

            t = tuple(map(int,power.split("-")))

            if isinstance(coef[1],complex):
                s+="+("
                if coef[1].real:
                    s+=f"{coef[1].real:+}"
                if coef[1].imag:
                    s+=f"{coef[1].imag:+}j"
                s+=f")*{coef[0]}"
            else:
                s+=f"{coef[1]:+}*{coef[0]}"

            if not any(t):
                continue

            for p,i in zip(self._unkn,t):
                
                if not i:
                    continue

                s+=f"*{p}"

                if i>=2:
                    s+=f"^{i}"

        if not s:
            s = "0"

        return s.strip("+")

    def __format__(self, __format_spec: str) -> str:
        """
        The __format_spec can format individually the polynomial coef individually and the whole polynomial object,
        it is olso possible to format it without the integration parts. To get this, the formatting moda has to follow this:

        '[integrals][numbers][!!monomials][;;[polinomial]]'
        - integrals, if 'i' is given, integrals will be ignored. other formatting modes will be given to numbers
        - numbers, are the formatting spec for the numbers, following the standard formatting for numbers
        - monomials, are the formatting spec for the monomials as string
        - MultyPolinomial, are the formatting spec for the MultyPolinomials as string 
        """

        if __format_spec.startswith("i"):
            numbers = __format_spec[1:]
            breaker = True
        else:
            numbers = __format_spec
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
        ks = ""
        
        for power in sorted(self._pcoef.keys(),reverse=True):
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

            t = tuple(map(int,power.split("-")))

            if any(t):

                for p,i in zip(self._unkn,t):
                    
                    if not i:
                        continue

                    ks+=f"*{p}"

                    if i>=2:
                        ks+=f"^{i}"

            ks= f'{ks:{monomials}}'
            s+=f'{"+"*(not ks.startswith(h))}{ks}'

        if breaker:
            if not s:
                return f"""{f"{f'{0:{numbers}}':{monomials}} ":{polynomial}}""".strip("+")
            return f"{s:{polynomial}}".strip("+")

        for power in sorted(self._icoef.keys(),reverse=True):
            coef = self._icoef[power]

            if not coef[1]:
                continue

            t = tuple(map(int,power.split("-")))

            if isinstance(coef,complex):
                ks+="+("
                if coef.real:
                    ks+=f"{coef.real:{numbers}}"
                if coef.imag:
                    ks+=f"{coef.imag:{numbers}}j"
                ks+=f")*{coef[0]}"
            else:
                ks+=f"{coef[1]:{numbers}}*{coef[0]}"

            if any(t):

                for p,i in zip(self._unkn,t):
                    
                    if not i:
                        continue
                    
                    ks+=f"*{p}"

                    if i>=2:
                        ks+=f"^{i}"
                    
            ks= f'{ks:{monomials}}'
            s+=f'{"+"*(not ks.startswith(h))}{ks}'

        if not s:
            return f"""{f"{f'{0:{numbers}}':{monomials}} ":{polynomial}}""".strip("+")
        return f"{s:{polynomial}}".strip("+")


    ## TRASNFORMATIONS ##
    @overload
    def __round__(self) -> Self:
        """
        It returns a new ComplexMultyPolynomial with each coef rounded to the closer integer
        """
    
    @overload
    def __round__(self, __n:int|None = None) -> Self:
        """
        It returns a new ComplexMultyPolynomial with each coef in the given position
        """
    
    def __round__(self, __n:int|None = None) -> Self:

        return self.__class__({power:complex(round(coef.real,__n),round(coef.imag,__n)) if isinstance(coef,complex) else round(coef,__n) for power,coef in self._pcoef.items()}, self._unkn, {power:[coef[0],complex(round(coef[1].real,__n),round(coef[1].imag,__n))] if isinstance(coef[1],complex) else [coef[0],round(coef[1],__n)] for power,coef in self._icoef.items()})

    def __floor__(self) -> Self:
        "It returns the ComplexMultyPolynomial with all the coefs floored"

        return self.__class__({power:complex(floor(coef.real),floor(coef.imag)) if isinstance(coef,complex) else floor(coef) for power,coef in self._pcoef.items()}, self._unkn, {power:[coef[0],complex(floor(coef[1].real),floor(coef[1].imag))] if isinstance(coef[1],complex) else [coef[0],floor(coef[1])] for power,coef in self._icoef.items()})

    def __ceil__(self) -> Self:
        "It returns the ComplexMultyPolynomial with all the coefs ceiled"

        return self.__class__({power:complex(ceil(coef.real),ceil(coef.imag)) if isinstance(coef,complex) else ceil(coef) for power,coef in self._pcoef.items()}, self._unkn, {power:[coef[0],complex(ceil(coef[1].real),ceil(coef[1].imag))] if isinstance(coef[1],complex) else [coef[0],ceil(coef[1])] for power,coef in self._icoef.items()})


    ## OPERATION WITH MULTIVARIATIVE POLYNOMIALS ##
    @staticmethod
    def _check__is_Number(__o:Any, error:str="{}"):
        "This function raises a TypeError if the given __o is not a Number"
        if not isinstance(__o, Number):
            raise TypeError(error.format(type(__o)))

    def divmod(self, __o:Never) -> None:
        "Doesn't work here"

        raise TypeError("complex floor-divide module nor be floor-divided")

    def __floordiv__(self, __o:Never) -> None:
        "Doesn't work here"

        raise TypeError("complex floor-divide module nor be floor-divided")

    def __rfloordiv__(self,__o:Never) -> None:
        "Doesn't work here"

        raise TypeError("complex floor-divide module nor be floor-divided")

    def __ifloordiv__(self, __o:Never) -> None:
        "Doesn't work here"

        raise TypeError("complex floor-divide module nor be floor-divided")

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
    c:ComplexMultyPolynomial = ComplexMultyPolynomial.fromText("(j)",("x"))
    j:ComplexMultyPolynomial = ComplexMultyPolynomial.random(3,"x")
    print(3*(c*2+j)==(2*c- (-j))*3)
