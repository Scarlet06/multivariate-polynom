from __future__ import annotations
from MultyPolynomial import MultyPolinomial, LenghtError, Self, Any, Never, Number, overload, findall, match,floor, ceil, randint

Unknowns = str
Powers = dict[int,Number]
Integrals = dict[int,list[str|Number]]

class SinglePolynomial(MultyPolinomial):

    __slots__ = ()

    ## SOME INITIALIZATION && CLASSMETHODS ##
    def __new(self, powers_coefficients:Powers, unknown:Unknowns, integrals_coefficients:Integrals={}) -> None:
        """
        Before creating the object, it checks that every argument is given in the right format
        """

        if type(unknown) is not Unknowns and len(unknown)!=1:
            raise TypeError("'unknown' has to be a string of lenght 1")

        if type(powers_coefficients) is not Powers.__origin__ :
            raise TypeError("'powers_coefficients' has to be a dict")

        if type(integrals_coefficients) is not Integrals.__origin__ :
            raise TypeError("'integrals_coefficients' has to be a dict")

        if not all(isinstance(q,int) for q in powers_coefficients|integrals_coefficients):
            raise LenghtError("All the key used in both 'powers_coefficients' and 'integrals_coefficients' have to be numbers of type int")

        for coef in powers_coefficients.values():
            self._check__is_Number(coef,"All the value used in 'powers_coefficients' have to be a Number")
        for coef in integrals_coefficients.values():
            self._check__is_Number(coef[1],"All the value used in 'integrals_coefficients' have to be list[str,Number]")

    @overload
    def __init__(self, powers_coefficients:Powers, unknown:Unknowns) -> None:
        """
        It creates the Polinoms giving to it a dictionary for the coefficient for each needed combination on power to each unknown:
        - powers = {'0':1,'1':-1,'3':3} -> 1*x^0-1*x^1+3*x^3
        
        a string for the unknowns:
        - unknown = 'x'
        """
    
    @overload
    def __init__(self, powers_coefficients:Powers, unknown:Unknowns, integrals_coefficients:Integrals={}) -> None:
        """
        It creates the Polinoms giving to it a dictionary for the coefficient for each needed combination on power to each unknown:
        - powers = {'0':1,'1':-1,'3':3} -> 1*x^0-1*x^1+3*x^3
        
        a string for the unknowns:
        - unknown = 'x'

        and eventually a dictonary for the "integral coefficient" dictionary:
        - integrals_coefficients = {'1':[C0,3]} -> 3*C0*x
        """
    
    def __init__(self, powers_coefficients:Powers, unknown:Unknowns, integrals_coefficients:Integrals={}) -> None:
        self.__new(powers_coefficients,unknown,integrals_coefficients)

        self._pcoef = powers_coefficients
        self._unkn = unknown
        self._icoef = integrals_coefficients

    @classmethod
    def fromMulty(cls: type[Self], m:MultyPolinomial) -> Self:
        """
        Given another MultyPolinomial it creates a new SinglePolynomial with the same informations
        """

        if len(m._unkn) !=1:
            raise LenghtError(f"{m!r} has too many Unknowns: {m.unknown}")
        
        return cls({int(power):coef for power,coef in m._pcoef},m._unkn,{int(p):c.copy() for p,c in m._icoef.items()})

    @overload
    @classmethod
    def fromText(cls: type[Self], text:str) -> Self:
        """
        Given a string of text it tries to create the polinom.
        the string has to be formatted, writing every multiplication *, even between coef and unknown. The exponential has to be written with ^. It doesn't understand parenthesis
        More complex form can be achieved by applaying math operation between multiple SinglePolynomial
        """

    @overload
    @classmethod
    def fromText(cls: type[Self], text:str, unknown:Unknowns="x") -> Self:
        """
        Given a string of text it tries to create the polinom.
        the string has to be formatted, writing every multiplication *, even between coef and unknown. The exponential has to be written with ^. It doesn't understand parenthesis
        More complex form can be achieved by applaying math operation between multiple SinglePolynomial

        If a unknown str is given, it will be used when not present in text
        """

    @overload
    @classmethod
    def fromText(cls: type[Self], text:str, unknown:Unknowns="", integrals_coefficients:Integrals={}) -> Self:
        """
        Given a string of text it tries to create the polinom.
        the string has to be formatted, writing every multiplication *, even between coef and unknown. The exponential has to be written with ^. It doesn't understand parenthesis
        More complex form can be achieved by applaying math operation between multiple SinglePolynomial

        If a unknown str is given, it will be used when not present in text

        integrals_coefficients have to be in the right format.
        if unknown = "z", each item has to be: 3: ['C0',5] -> 5*C0*z^3
        """

    @classmethod
    def fromText(cls: type[Self], text:str, temp_unknown:Unknowns="x", integrals_coefficients:Integrals={}) -> Self:

        num = r'^[+-]?(?:(?:\d+)?(?:\.)?(?:\d+)?)$'

        unknown = ""
        t = {}
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
                    i, val = p.split("^")

                    x = match(num,i)
                    if x:
                        coef+=f"*({i}**{val})"
                        continue

                    if i == unknown:
                        power+=f"+{val}"
                        continue
                    
                    elif unknown:
                        raise ValueError("Too many Unknowns for this SinglePolynomial")
                    unknown=i
                    power=f"{val}"
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
                unknown=i
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

    @overload
    @classmethod
    def one(cls: type[Self]) -> Self:
        """
        This classmethod creates a MultyPolinomial with only the coef 1
        """

    @overload
    @classmethod
    def one(cls: type[Self], unknowns:Unknowns="x") -> Self:
        """
        This classmethod creates a MultyPolinomial with only the coef 1
        If unknowns are given, it initializes it with it
        """

    @classmethod
    def one(cls: type[Self], unknowns:Unknowns="x") -> Self:

        return cls({0:1},unknowns,{})

    @overload
    @classmethod
    def zero(cls: type[Self]) -> Self:
        """
        This classmethod creates a MultyPolinomial with only the coef 0
        """

    @overload
    @classmethod
    def zero(cls: type[Self], *unknowns:str) -> Self:
        """
        This classmethod creates a MultyPolinomial with only the coef 0
        If unknowns are given, it initializes it with these, else it won't have any
        """

    @classmethod
    def zero(cls: type[Self], *unknowns:str) -> Self:

        if not unknowns:
            unknowns = ("x",)
        
        return cls({cls._get_key_0(len(unknowns)):0},unknowns,{})

    @overload
    @classmethod
    def random(cls: type[Self], maxdeg:int) -> Self:
        """
        This classmethod creates a random MultyPolinomial with at maximum the given degree to every monom. It is a lil' junk

        The unknown will be 'x'
        """

    @overload
    @classmethod
    def random(cls: type[Self], maxdeg:int, *unknowns:str) -> Self:
        """
        This classmethod creates a random MultyPolinomial with at maximum the given degree to every monom. It is a lil' junk

        it will use the given unknowns
        """

    @overload
    @classmethod
    def random(cls: type[Self], maxdeg:int, *unknowns:str, **maxunknowns:tuple[str:int]) -> Self:
        """
        This classmethod creates a random MultyPolinomial with at maximum the given degree to every monom. It is a lil' junk

        it will use the given unknowns but also the unknown used as key for maxunknowns

        if kwargs are given, the int will be the max power for its key-unknown
        """

    @classmethod
    def random(cls: type[Self], maxdeg:int, *unknowns:str, **maxunknowns:tuple[str:int]) -> Self:
        
        if maxunknowns:
            unknowns=tuple(set(unknowns)|set(maxunknowns.keys()))

        elif not unknowns:
            unknowns = ("x",)

        t={}
        l = len(unknowns)
        s=tuple(min(maxdeg,maxunknowns.get(u,maxdeg)) for u in unknowns)
        k = ['0']*l
        m = max(5,maxdeg,*s)
        v = randint(randint(0,min(l,m-1)),m)
        for i in range(v):
            x=0
            for j in range(l):
                n = randint(0,max(0,s[j]-x))
                k[j]=str(n)
                x+=n
            u="-".join(k)
            if u in t:
                t[u]-=randint(-m,m)*(-1)**i+l
            else:
                t[u] = randint(-v,v)*(-1)**i

        if not t:
            t[cls._get_key_0(l)] = 0
        return cls(t,unknowns,{})


    ## SOME PROPERTIES TO ACCESS VARIABLES QUICKLY ##
    @property
    def unknown(self) -> Unknowns:
        "tuple of the unknown"
        return self._unkn

    @unknown.setter
    def unknown(self, unknowns:Unknowns) -> None:
        "tuple of the unknown"
        if not isinstance(unknowns, Unknowns) or len(unknowns)!=1:
            raise TypeError("'unknown' has to be a string of lenght 1")
        self._unkn = unknowns

    @property
    def powers(self) -> Powers:
        "dictionary of the coefficients"
        return self._pcoef

    @powers.setter
    def powers(self, powers_coefficients:Powers) -> None:
        "dictionary of the coefficients"
        if not isinstance(powers_coefficients, Powers.__origin__):
            raise TypeError("'powers_coefficients' has to be a dict")
        if not all(isinstance(p,int) for p in powers_coefficients):
            raise LenghtError("The lenght of all the keys inthe given Powers has to be the same as unknown")
        self._pcoef = powers_coefficients

    @property
    def integrals(self) -> Integrals:
        "dictionary of the integrals costants"
        return self._icoef

    @integrals.setter
    def integrals(self, integrals_coefficients:Integrals) -> None:
        "dictionary of the coefficients"

        if not isinstance(integrals_coefficients, Integrals.__origin__):
            raise TypeError("'integrals_coefficients' has to be a dict")
        elif not all(isinstance(p,int) for p in integrals_coefficients):
            raise LenghtError("The lenght of all the keys inthe given Integrals has to be the same as unknown")
        self._icoef = integrals_coefficients


    ## STRING METHODS ##

    def __str__(self) -> str:
        """
        string of the MultyPolinomial

        if this MultyPolinomial has any Integrals, it will raise an error if used for fromText()
        Before to do so, is best practice to check if Integrals are present with has_integrals_const() or by passing 'i' at __format__()
        """
        
        s = ""
        h = ("+","-")
        
        for power,coef in sorted(self._pcoef.items(),key=lambda x:x[0],reverse=True):

            if not coef:
                continue

            if coef == floor(coef):
                coef = floor(coef)

            if power and abs(coef)==1:
                if coef> 0:
                    s+="+"
                else:
                    s+="-"
            else:
                s+=f"{coef:+}"

            if not power:
                continue

            if not s[-1] in h:
                s+=f"*{self._unkn}"
            else:
                s+=f"{self._unkn}"

            if power>=2:
                s+=f"^{power}"
        
        for power,coef in sorted(self._icoef.items(),key=lambda x:x[0],reverse=True):

            if not coef[1]:
                continue
            
            if coef[1] == floor(coef[1]):
                coef[1] = floor(coef[1])

            if abs(coef[1])==1:
                if coef[1]> 0:
                    s+="+"
                else:
                    s+="-"
            else:
                s+=f"{coef[1]:+}*"
            s+=coef[0]

            if not power:
                continue

            if not s[-1] in h:
                s+=f"*{self._unkn}"
            else:
                s+=f"{self._unkn}"

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

            ks = f"{coef:{numbers}}"
                    
            if not power:
                continue

            ks+=f"*{self._unkn}"

            if power>=2:
                ks+=f"^{power}"

            ks= f'{ks:{monomials}}'
            s+=f'{"+"*(not ks.startswith(h))}{ks}'

        if breaker:
            if not s:
                return f"""{f"{f'{0:{numbers}}':{monomials}} ":{polynomial}}"""
            return f"{s.strip('+'):{polynomial}}"

        for power in sorted(self._icoef.keys(),reverse=True):
            coef = self._icoef[power]

            if not coef[1]:
                continue

            ks = f"{coef[1]:{numbers}}*{coef[0]}"
                    
            if not power:
                continue

            ks+=f"*{self._unkn}"

            if power>=2:
                ks+=f"^{power}"
                    
            ks= f'{ks:{monomials}}'
            s+=f'{"+"*(not ks.startswith(h))}{ks}'

        if not s:
            return f"""{f"{f'{0:{numbers}}':{monomials}} ":{polynomial}}"""
        return f"{s.strip('+'):{polynomial}}"

    @staticmethod
    def _get_key_0(__len:int = 0) -> str:
        """
        it returns a string used as key for _pcoef or _icoef.
        it is a 0 sequence of lenght as __mod is 0-0-0-...-0
        """
        
        if __len:
            return ("0-"*__len)[:-1]
        return ("0-"*__len)

print(f'{SinglePolynomial.fromText("3*y^2-y+y^5*2*5*y"):+!!^15;;_^100}')