from __future__ import annotations
from MultyPolynomial import MultyPolinomial, LenghtError, Self, Any, Never, Generator, Number, overload, findall, match, floor, ceil,prod, randint,uniform

Unknowns = str
Powers = dict[int,Number]
Integrals = dict[int,list[str|Number]]

class SinglePolynomial(MultyPolinomial):
    "This object is used to create and match the needs for a polinomial in a single variable"

    #the only variables used by the object
    __slots__ = ()

    ## SOME INITIALIZATION && CLASSMETHODS ##
    def __new(self, powers_coefficients:Powers, unknown:Unknowns, integrals_coefficients:Integrals|None=None) -> None:
        """
        Before creating the object, it checks that every argument is given in the right format
        """

        #to not change furthermore these checks, integrals_coefficients is initialized as dict()
        if integrals_coefficients is None:
            integrals_coefficients={}

        if type(unknown) is not Unknowns:
            raise TypeError("'unknown' has to be a string")

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
    def __init__(self, powers_coefficients:Powers, unknown:Unknowns, integrals_coefficients:Integrals|None=None) -> None:
        """
        It creates the Polinoms giving to it a dictionary for the coefficient for each needed combination on power to each unknown:
        - powers = {'0':1,'1':-1,'3':3} -> 1*x^0-1*x^1+3*x^3
        
        a string for the unknowns:
        - unknown = 'x'

        and eventually a dictonary for the "integral coefficient" dictionary:
        - integrals_coefficients = {'1':['C0',3]} -> 3*C0*x
        """
    
    def __init__(self, powers_coefficients:Powers, unknown:Unknowns, integrals_coefficients:Integrals|None=None) -> None:
        self.__new(powers_coefficients,unknown,integrals_coefficients)

        self._pcoef = powers_coefficients
        self._unkn = unknown
        if integrals_coefficients is None:
            self._icoef = {}
        else:
            self._icoef = integrals_coefficients

    @classmethod
    def fromSingle(cls: type[Self], s:SinglePolynomial) -> Self:
        """
        Given another SinglePolynomial it creates a new SinglePolynomial with the same informations
        """

        return super().fromMulty(s)

    @classmethod
    def fromMulty(cls: type[Self], m:MultyPolinomial) -> Self:
        """
        Given another MultyPolinomial it creates a new SinglePolynomial with the same informations
        """

        if len(m._unkn) !=1:
            degs = tuple(m.degs())

            if sum(1 if i else 0 for i in degs)!=1:
                raise LenghtError(f"{m!r} has too many Unknowns: {m.unknown}")
            
            for pos,unkn,deg in zip(*zip(*enumerate(m._unkn)),degs):
                if not deg:
                    continue

                return cls({int(power.split("-")[pos]):coef for power,coef in m._pcoef.items() if coef},unkn,{int(p.split("-")[pos]):c.copy() for p,c in m._icoef.items() if c[1]})
        
        return cls({int(power):coef for power,coef in m._pcoef.items() if coef},m._unkn[0],{int(p):c.copy() for p,c in m._icoef.items() if c[1]})

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
    def fromText(cls: type[Self], text:str, unknown:Unknowns="", integrals_coefficients:Integrals|None={}) -> Self:
        """
        Given a string of text it tries to create the polinom.
        the string has to be formatted, writing every multiplication *, even between coef and unknown. The exponential has to be written with ^. It doesn't understand parenthesis
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

    @overload
    @classmethod
    def one(cls: type[Self]) -> Self:
        """
        This classmethod creates a SignlePolinomial with only the coef 1
        """

    @overload
    @classmethod
    def one(cls: type[Self], unknowns:Unknowns="x") -> Self:
        """
        This classmethod creates a SinglePolinomial with only the coef 1
        If unknowns are given, it initializes it with it
        """

    @classmethod
    def one(cls: type[Self], unknowns:Unknowns="x") -> Self:

        return cls({0:1},unknowns,{})

    @overload
    @classmethod
    def zero(cls: type[Self]) -> Self:
        """
        This classmethod creates a SinglePolinomial with only the coef 0
        """

    @overload
    @classmethod
    def zero(cls: type[Self], unknown:Unknowns="x") -> Self:
        """
        This classmethod creates a SinglePolinomial with only the coef 0
        If unknown is given, it initializes it with it
        """

    @classmethod
    def zero(cls: type[Self], unknown:Unknowns="x") -> Self:
        
        return cls({0:0},unknown,{})

    @overload
    @classmethod
    def random(cls: type[Self], maxdeg:int) -> Self:
        """
        This classmethod creates a random SinglePolinomial with at maximum the given degree to every monom. It is a lil' junk

        The unknown will be 'x'
        """

    @overload
    @classmethod
    def random(cls: type[Self], maxdeg:int, unknown:str="x") -> Self:
        """
        This classmethod creates a random SinglePolinomial with at maximum the given degree to every monom. It is a lil' junk

        it will use the given unknown
        """

    @classmethod
    def random(cls: type[Self], maxdeg:int, unknown:str="x") -> Self:
        
        t={}
        m = max(5,maxdeg)
        v = randint(randint(1,m-1),m+1)
        for i in range(v):
            u = randint(0,maxdeg)
            if u in t:
                t[u]-=uniform(-m,m)*(-1)**i
            else:
                t[u]=randint(-v,v)*(-1)**i

        if not t:
            t[0] = 0

        return cls(t,unknown,{})


    ## SOME PROPERTIES TO ACCESS VARIABLES QUICKLY ##
    @property
    def unknown(self) -> Unknowns:
        "tuple of the unknown"
        return self._unkn

    @unknown.setter
    def unknown(self, unknowns:Unknowns) -> None:
        "tuple of the unknown"
        if not isinstance(unknowns, Unknowns):
            raise TypeError("'unknown' has to be a string")
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


    ## SOME INTERESTING METHODS ##
    def toMulty(self) -> MultyPolinomial:
        "It convert this single polynomial into a multy one"
        return MultyPolinomial({str(power):coef for power,coef in self._pcoef.items()},(self._unkn,),{str(power):coef.copy() for power,coef in self._icoef.items()})
    
    def __len__(self) -> int:
        """
        return the number of unknowns 
        """
        return 1

    def deg(self) -> int:
        """
        it returns the maximum degree of the polynomial
        """
        return max(0,0,*tuple(power for power,coef in self._pcoef.items() if coef),*tuple(power for power,coef in self._icoef.items() if coef))
        
    def degs(self) -> int:
        """
        it returns the maximum degree of the polynomial
        """

        return self.deg()
        

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
                    return f"""{f"{f'{0:{numbers}}':{monomials}}":{polynomial}}"""
                return f"{s.strip('+'):{polynomial}}"

        for power in sorted(self._icoef.keys(),reverse=True):
            ks = ""
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
            return f"""{f"{f'{0:{numbers}}':{monomials}}":{polynomial}}"""
        return f"{s.strip('+'):{polynomial}}"

    @staticmethod
    def _get_key_0(__len:Never) -> int:
        """
        it returns just 0
        """
        
        return 0


    ## OPERATION OVER MULTIVARIATIVE POLYNOMIALS ##
    @overload
    def __call__(self, values:Number) -> tuple[Number,str]:
        """
        values can be a number if and only if Unknowns has only one element, and evaluate this polynomial in the given value
        To make only a partial evaluation, use evaluate or evaluate_ip methods

        It returns the number of the evaluation and the string representing the Integrals consts
        """

    @overload
    def __call__(self, values:Number, __ignore:bool=False) -> Number | tuple[Number,str]:
        """
        It returns the number of the evaluation and the string representing the Integrals consts

        if __ignore is give True, only the evaluation will be returned
        """

    def __call__(self, values:Number, __ignore:bool=False) -> Number | tuple[Number,str]:

        t = self.__format__("i")
        k = self.__format__("ii")

        if __ignore:
            return eval(t.replace(self._unkn,str(values)).replace("^","**"))

        t=t.replace(self._unkn,str(values))
        k=k.replace(self._unkn,str(values))
            
        return eval(t.replace("^","**")), k

    def evaluate(self, values:Number) -> Self:
        """
        It returns an evaluation as polynomial, its unknown will be kept
        """

        p = 0
        i = {}
        if self._icoef:
            i[0]=["C0",1]

        for power,coef in self._pcoef.items():
            p+=coef*values**power
        
        return self.__class__({0:p},self._unkn,i)

    def evaluate_ip(self, values:Number) -> None:
        """
        It updates itself evaluating in the given value as polynomial, its unknown will be kept
        """

        p = 0
        if self._icoef:
            self._icoef.clear()
            self._icoef[0]=["C0",1]

        for power,coef in self._pcoef.items():
            p+=coef*values**power
        
        self._pcoef.clear()
        self._pcoef[0]=p

    def derive(self) -> Self:
        "It derives the SinglePolynomial in its unknnown"

        return self.__class__({power-1:coef*power for power, coef in self._pcoef.items() if power and coef}, self._unkn, {power-1:[coef[0],coef[1]*power] for power, coef in self._icoef.items() if power and coef[1]})

    def derive_ip(self) -> None:
        "It derives the SinglePolynomial in its unknnown"

        p = {power-1:coef*power for power, coef in self._pcoef.items() if power and coef}
        i = {power-1:[coef[0],coef[1]*power] for power, coef in self._icoef.items() if power and coef[1]}
        self._pcoef.clear()
        self._pcoef.update(p)
        self._icoef.clear()
        self._icoef.update(i)

    def derive_n(self, __n:int=1) -> Self:
        "It derives the given number of times the SinglePolynomial in its unknnown"

        s = self.copy()

        for _ in range(__n):
            s.derive_ip()

        return s

    def derive_n_ip(self, __n:int=1) -> None:
        "It derives the given number of times the SinglePolynomial in its unknnown"

        for _ in range(__n):
            self.derive_ip()

    def partial(self, unknown:str) -> Self|MultyPolinomial:
        """
        It makes a partial derivation in the given unknown. If a different unknown is given, a MultyPolynomial will be returned
        """

        if unknown == self._unkn:
            return self.derive()

        return MultyPolinomial.zero(self._unkn,unknown)

    def partial_ip(self, unknown:str) -> None:
        """
        It makes a partial derivation in the given unknown
        """

        if unknown == self._unkn:
            return self.derive_ip()
        
        raise ValueError(f"the given unknown {unknown} doesn't match up with {self._unkn}. Consider convert this SinglePolynomial to MultyPolynomial before")

    @overload
    def partial_n(self, *unknown:str) -> Self|MultyPolinomial:
        """
        it makes sequentially all the partial derivations in the given unknown.

        If a different unknown is given, a MultyPolynomial will be returned
        """

    @overload
    def partial_n(self, **kwargs:int) -> Self|MultyPolinomial:
        """
        it makes sequentially all the partial derivations in the given unknown by the given number

        If a different unknown is given, a MultyPolynomial will be returned
        """

    @overload
    def partial_n(self, *unknown:str, **kwargs:int) -> Self|MultyPolinomial:
        """
        it makes sequentially all the partial derivations in the given unknown and by given unknown by the given number

        If a different unknown is given, a MultyPolynomial will be returned
        """

    def partial_n(self, *unknown:str, **kwargs:int) -> Self|MultyPolinomial:
        
        if all(u == self._unkn for u in unknown|kwargs.keys()):

            return self.derive_n(len(unknown)+kwargs.get(self._unkn,0))
            
        return self.toMulty().partial_n(*unknown, **kwargs)

    @overload
    def partial_n_ip(self, *unknown:str) -> None:
        """
        it makes sequentially all the partial derivations in the given unknown
        """

    @overload
    def partial_n_ip(self, **kwargs:int) -> None:
        """
        it makes sequentially all the partial derivations in the given unknown by the given number
        """

    @overload
    def partial_n_ip(self, *unknown:str, **kwargs:int) -> None:
        """
        it makes sequentially all the partial derivations in the given unknown and by given unknown by the given number
        """

    def partial_n_ip(self, *unknown:str, **kwargs:int) -> None:
        
        if all(u == self._unkn for u in unknown|kwargs.keys()):

            return self.derive_n_ip(len(unknown)+kwargs.get(self._unkn,0))
            
        raise ValueError(f"the given unknowns {unknown|kwargs.keys()} doesn't match up with {self._unkn}. Consider convert this SinglePolynomial to MultyPolynomial before")

    def integral(self) -> Self:
        """
        It integrates the SinglePolinomial
        """

        return self.__class__({power+1:coef*(power+1) for power, coef in self._pcoef.items() if power and coef}, self._unkn, {power+1:[coef[0],coef[1]*(power+1)] for power, coef in self._icoef.items() if coef[1]}|{0:[f"C{len(self._icoef)}",1]})

    def integral_ip(self) -> None:
        """
        It integrates the MultyPolinomial
        """

        icoef = self._icoef.copy()
        pcoef=self._pcoef.copy()
        self._pcoef.clear()
        self._icoef.clear()

        self._pcoef.update({power+1:coef/(power+1) for coef,power in pcoef.items() if coef})
        self._icoef.update({power+1:coef/(power+1) for coef,power in icoef.items() if coef}|{0:[f"C{len(icoef)}",1]})

    @overload
    def integral_n(self, *unknown:str) -> Self|MultyPolinomial:
        """
        it makes sequentially all the integrations in the given unknown

        If a different unknown is given, a MultyPolynomial will be returned
        """

    @overload
    def integral_n(self, **kwargs:int) -> Self|MultyPolinomial:
        """
        it makes sequentially all the integrations in the given unknown by the given number

        If a different unknown is given, a MultyPolynomial will be returned
        """

    @overload
    def integral_n(self, *unknown:str, **kwargs:int) -> Self|MultyPolinomial:
        """
        it makes sequentially all the integrations in the given unknown and by given unknown by the given number

        If a different unknown is given, a MultyPolynomial will be returned
        """

    def integral_n(self, *unknown:str, **kwargs:int) -> Self|MultyPolinomial:
        
        if all(u == self._unkn for u in unknown|kwargs.keys()):
            s = self.copy()

            for _ in range(len(unknown)+kwargs.get(self._unkn,0)):
                s.integral_ip()

            return s
            
        return self.toMulty().integral_n(*unknown, **kwargs)

    @overload
    def integral_n_ip(self, *unknown:str) -> None:
        """
        it makes sequentially all the integrations in the given unknown

        If a different unknown is given, a MultyPolynomial will be returned
        """

    @overload
    def integral_n_ip(self, **kwargs:int) -> None:
        """
        it makes sequentially all the integrations in the given unknown by the given number

        If a different unknown is given, a MultyPolynomial will be returned
        """

    @overload
    def integral_n_ip(self, *unknown:str, **kwargs:int) -> None:
        """
        it makes sequentially all the integrations in the given unknown and by given unknown by the given number

        If a different unknown is given, a MultyPolynomial will be returned
        """

    def integral_n_ip(self, *unknown:str, **kwargs:int) -> None:
        
        if all(u == self._unkn for u in unknown|kwargs.keys()):

            for _ in range(len(unknown)+kwargs.get(self._unkn,0)):
                self.integral_ip()

            return 
            
        raise ValueError(f"the given unknowns {unknown|kwargs.keys()} doesn't match up with {self._unkn}. Consider convert this SinglePolynomial to MultyPolynomial before")

    def integralAB(self, a:Number, b:Number) -> Self:
        """
        It integrates the MultyPolinomial in the given unknown in the [a,b] interval
        """

        if a>b:
            raise ValueError(f"'b':({b}) has to be greater than 'a':({a})")

        t = self.integral()

        return t.evaluate(b)-t.evaluate(a)

    def integralAB_ip(self, a:Number, b:Number) -> None:
        """
        It integrates the MultyPolinomial in the given unknown in the [a,b] interval
        """

        if a>b:
            raise ValueError(f"'b':({b}) has to be greater than 'a':({a})")

        self.integral_ip()
        t= self.copy()

        self.evaluate_ip(b)
        self-=t.evaluate(a)

    def integralAB_n(self, **kwargs:tuple[tuple[int,int],...]) -> Self|MultyPolinomial:
        """
        it makes sequentially all the integrations in the given unknown in its respective interval

        If a different unknown is given, a MultyPolynomial will be returned
        """


        if all(u == self._unkn for u in kwargs.keys()):
            t = self.copy()

            for unk, intervals in kwargs.items():
                for interval in intervals:
                    t.integralAB_ip(unk, *interval)

            return t
            
        return self.toMulty().integralAB_n(**kwargs)

    def integralAB_n_ip(self, **kwargs:tuple[tuple[int,int],...]) -> None:
        """
        it makes sequentially all the integrations in the given unknown in its respective interval
        """

        if all(u == self._unkn for u in kwargs.keys()):
            for unk, intervals in kwargs.items():
                for interval in intervals:
                    self.integralAB_ip(unk, *interval)
            
            return

        raise ValueError(f"the given unknowns {kwargs.keys()} doesn't match up with {self._unkn}. Consider convert this SinglePolynomial to MultyPolynomial before")


    ## TRASNFORMATIONS ##
    def __neg__(self) -> Self:
        """
        It returns a new SinglePolynomial with every coef negated
        """

        return super().__neg__()

    def __pos__(self) -> Self:
        """
        It returns a new SinglePolynomial
        """

        return super().__pos__()

    def __abs__(self) -> Self:
        """
        It returns a new SinglePolynomial with every coef positive
        """
        
        return super().__abs__()

    @overload
    def __round__(self) -> Self:
        """
        It returns a new SinglePolynomial with each coef rounded to the closer integer
        """
    
    @overload
    def __round__(self, __n:int|None = None) -> Self:
        """
        It returns a new SinglePolynomial with each coef in the given position
        """

    def __round__(self, __n:int|None = None) -> Self:

        return super().__round__(__n)

    def __floor__(self) -> Self:
        "It returns the SinglePolynomial with all the coefs floored"

        return super().__floor__()

    def __ceil__(self) -> Self:
        "It returns the SinglePolynomial with all the coefs ceiled"

        return super().__ceil__()

    def clear(self) -> None:
        """
        It transform itself to zero
        """
        
        self._pcoef.clear()
        self._pcoef[0]=0
        self._icoef.clear()

    def clean(self) -> Self:
        """
        It returns a new SinglePolynomial removing any unkown wich isn't used. It skips any zero coef
        """
        
        p = {power:coef for power,coef in self._pcoef.items() if coef}

        return self.__class__(p if p else {0:0},self._unkn,{power:coef.copy() for power,coef in self._icoef.items() if coef[1]})

    def clean_ip(self) -> None:
        """
        It updates this SinglePolynomial by removing any unkown wich isn't used. It removes any zero coef
        """

        for power,coef in self._pcoef.items():
            if not coef:
                del self._pcoef[power]

        if not self._pcoef:
            self._pcoef[0]=0

        for power,coef in self._icoef.items():
            if not coef[1]:
                del self._icoef[power]

    @overload
    def copy(self) -> Self:
        """
        It creates a copy of the current SinglePolynomial
        """

    @overload
    def copy(self, __ignore:bool=False) -> Self:
        """
        It creates a copy of the current SinglePolynomial
        if __ignore is True, the Integrals part will be ignored
        """

    def copy(self, __ignore:bool = False) -> Self:

        return super().copy(__ignore)

    @overload
    def translate(self, *args:Number) -> Self|MultyPolinomial:
        "by giving a number, one and only one, is possible to translate 'vertically' the polymoial"

    @overload
    def translate(self, **kwargs:Number) -> Self|MultyPolinomial:
        """
        for each given unknown, it translates the polynomial by the corrispective value.

        If a different unknown is given, a MultyPolynomial will be returned
        """

    @overload
    def translate(self, *args:Number, **kwargs:Number) -> Self|MultyPolinomial:
        """
        By giving a number, in args one and only one, is possible to translate 'vertically' the polymoial.
        For each given unknown in kwargs, it translates the polynomial by its corrispective value.
        
        If a different unknown is given, a MultyPolynomial will be returned
        """

    def translate(self, *args:Number, **kwargs:Number) -> Self|MultyPolinomial:

        if all(u == self._unkn for u in kwargs.keys()):
        
            if kwargs:
                p = self.zero(self._unkn)

                s = self.__class__({1:1,0:-kwargs.get(self._unkn,0)},self._unkn)
                trans = lambda power: s**power

                for power,coef in self._pcoef.items():
                    p+=trans(power)*coef
                
                s._icoef.update({1:['',1],0:['',1]})
                s._pcoef.clear()
                
                for power in self._icoef:
                    p+=trans(power)

                for i,coef in enumerate(p._icoef.values()):
                    coef[0] = f'C{i}'

                return p+sum(args)
            
            return self+sum(args)
        
        return self.toMulty().translate(*args, **kwargs)

    @overload
    def translate_ip(self, *args:Number) -> None:
        "by giving a number, one and only one, is possible to translate 'vertically' the polymoial"

    @overload
    def translate_ip(self, **kwargs:Number) -> None:
        """
        for each given unknown, it translates the polynomial by the corrispective value.
        """

    @overload
    def translate_ip(self, *args:Number, **kwargs:Number) -> None:
        """
        By giving a number, in args one and only one, is possible to translate 'vertically' the polymoial.
        For each given unknown in kwargs, it translates the polynomial by its corrispective value.
        """

    def translate_ip(self, *args:Number, **kwargs:Number) -> None:

        if all(u == self._unkn for u in kwargs.keys()):
            #if kwargs is eampty, all still enter here
        
            if kwargs:
                p = self.clean()
                self.clear()

                s = self.__class__({1:1,0:-kwargs.get(self._unkn,0)},self._unkn)
                trans = lambda power: s**power

                for power,coef in p._pcoef.items():
                    self+=trans(power)*coef
                
                s._icoef.update({1:['',1],0:['',1]})
                s._pcoef.clear()
                
                for power in p._icoef:
                    self+=trans(power)

                for i,coef in enumerate(self._icoef.values()):
                    coef[0] = f'C{i}'
            
            self+=sum(args)
            return

        raise ValueError(f"the given unknowns {kwargs.keys()} doesn't match up with {self._unkn}. Consider convert this SinglePolynomial to MultyPolynomial before")


    ## OPERATION WITH MULTIVARIATIVE POLYNOMIALS ##
    def __add__(self, __o: Number | Self) -> Self|MultyPolinomial:
        "Add a number or another MultyPolinomial to this SinglePolynomial"
        
        if isinstance(__o,MultyPolinomial):
            if isinstance(__o,SinglePolynomial):
                if __o._unkn==self._unkn:
                    t ={}
                    i=0
                    for power in self._icoef|__o._icoef:
                        coef=self._icoef.get(power,["",0])[1]
                        t[power] = [f"C{i}",coef+__o._icoef.get(power,["",0])[1]]
                        i+=1
                    return self.__class__({power:self._pcoef.get(power,0)+__o._pcoef.get(power,0) for power in self._pcoef|__o._pcoef},self._unkn,t)
                __o=__o.toMulty()
            return self.toMulty()+__o
        
        self._check__is_Number(__o,"{} cannot be added to a SinglePolinomial")

        t=self._pcoef.copy()
        if 0 in t:
            t[0]+=__o
        else:
            t[0] = __o

        return self.__class__(t,self._unkn, {power:coef.copy() for power,coef in self._icoef.items()})

    def __iadd__(self, __o: Number | Self) -> Self|MultyPolinomial:
        "Add a number or another MultyPolinomial to this SinglePolynomial"
        
        if isinstance(__o,MultyPolinomial):
            if isinstance(__o,SinglePolynomial):
                if __o._unkn==self._unkn:

                    for power, coef in __o._pcoef.items():
                        if power in self._pcoef:
                            self._pcoef[power]+=coef
                            continue
                        self._pcoef[power]=coef

                    i=0
                    for power, coef in __o._icoef.items():
                        if power in self._icoef:
                            self._icoef[power][1]+=coef
                            continue
                        self._icoef[power]=[f"C{i}",coef]
                        i+=1

                    return self

                __o=__o.toMulty()
            return self.toMulty()+__o
        
        self._check__is_Number(__o,"{} cannot be added to a SinglePolinomial")

        self._pcoef
        if 0 in self._pcoef:
            self._pcoef[0]+=__o
        else:
            self._pcoef[0] = __o

        return self

    def __sub__(self, __o: Number | Self) -> Self|MultyPolinomial:
        "subtract a number or another MultyPolinomial to this SinglePolynomial"

        if isinstance(__o,MultyPolinomial):
            if isinstance(__o,SinglePolynomial):
                if __o._unkn==self._unkn:
                    t ={}
                    i=0
                    for power in self._icoef|__o._icoef:
                        coef=self._icoef.get(power,["",0])[1]
                        t[power] = [f"C{i}",coef-__o._icoef.get(power,["",0])[1]]
                        i+=1
                    return self.__class__({power:self._pcoef.get(power,0)-__o._pcoef.get(power,0) for power in self._pcoef|__o._pcoef},self._unkn,t)
                __o=__o.toMulty()
            return self.toMulty()-__o
        
        self._check__is_Number(__o,"{} cannot subtract a SinglePolinomial")

        t=self._pcoef.copy()
        if 0 in t:
            t[0]-=__o
        else:
            t[0] = -__o

        return self.__class__(t,self._unkn, {power:coef.copy() for power,coef in self._icoef.items()})

    def __rsub__(self, __o: Number | Self) -> Self|MultyPolinomial:
        "subtract this SinglePolynomial to a number or another MultyPolinomial"
        
        if isinstance(__o,MultyPolinomial):
            if isinstance(__o,SinglePolynomial):
                if __o._unkn==self._unkn:
                    t ={}
                    i=0
                    for power in self._icoef|__o._icoef:
                        coef=self._icoef.get(power,["",0])[1]
                        t[power] = [f"C{i}",__o._icoef.get(power,["",0])[1]-coef]
                        i+=1
                    return self.__class__({power:__o._pcoef.get(power,0)-self._pcoef.get(power,0) for power in self._pcoef|__o._pcoef},self._unkn,t)
                __o=__o.toMulty()
            return __o-self.toMulty()
        
        self._check__is_Number(__o,"{} cannot be subtracted be a SinglePolinomial")

        t=self._pcoef.copy()
        if 0 in t:
            t[0]-=__o
        else:
            t[0] = -__o

        return self.__class__(t,self._unkn, {power:coef.copy() for power,coef in self._icoef.items()})

    def __isub__(self, __o: Number | Self) -> Self|MultyPolinomial:
        "Subtract a number or another MultyPolinomial to this SinglePolynomial"
        
        if isinstance(__o,MultyPolinomial):
            if isinstance(__o,SinglePolynomial):
                if __o._unkn==self._unkn:

                    for power, coef in __o._pcoef.items():
                        if power in self._pcoef:
                            self._pcoef[power]-=coef
                            continue
                        self._pcoef[power]=-coef

                    for power, coef in __o._icoef.items():
                        if power in self._icoef:
                            self._icoef[power][1]-=coef
                            continue
                        self._icoef[power][1]=-coef

                    return self

                __o=__o.toMulty()
            return self.toMulty()-__o
        
        self._check__is_Number(__o,"{} cannot subtract a SinglePolinomial")

        self._pcoef
        if 0 in self._pcoef:
            self._pcoef[0]-=__o
        else:
            self._pcoef[0] = -__o

        return self

    def __mul__(self, __o: Number | Self) -> Self|MultyPolinomial:
        "Multiplicate a number or another MultyPolinomial to this SinglePolynomial"
        
        if isinstance(__o,MultyPolinomial):
            if isinstance(__o,SinglePolynomial):
                if __o._unkn==self._unkn:
                    t ={}
                    tt = {}
                    i=0

                    for power,coef in self._pcoef.items():

                        for p,c in __o._pcoef.items():
                            k = p+power
                            if k in t:
                                t[k]+=coef*c
                                continue
                            t[k]=coef*c
                        
                        for p,c in __o._icoef.items():
                            k = p+power
                            if k in tt:
                                tt[k][1]+=coef*c[1]
                                continue
                            tt[k]=[f"C{i}",coef*c]
                            i+=1

                    for power,coef in self._icoef.items():

                        for p,c in __o._pcoef.items():
                            k = p+power
                            if k in tt:
                                tt[k][1]+=coef[1]*c
                                continue
                            tt[k]=[f"C{i}",coef[1]*c]
                            i+=1
                        
                        for p,c in __o._icoef.items():
                            k = p+power
                            if k in tt:
                                tt[k][1]+=coef[1]*c[1]
                                continue
                            tt[k]=[f"C{i}",coef[1]*c]
                            i+=1

                    return self.__class__(t,self._unkn,tt)

                __o=__o.toMulty()
            return self.toMulty()*__o
        
        self._check__is_Number(__o,"{} cannot multiply a SinglePolinomial")

        return self.__class__({power:coef*__o for power,coef in self._pcoef.items()},self._unkn, {power:[coef[0],coef[1]*__o] for power,coef in self._icoef.items()})

    def __imul__(self, __o: Number | Self) -> Self|MultyPolinomial:
        "Multiplicate a number or another MultyPolinomial to this SinglePolynomial"
        
        if isinstance(__o,MultyPolinomial):
            if isinstance(__o,SinglePolynomial):
                if __o._unkn==self._unkn:
                    t =self._pcoef.copy()
                    tt = self._icoef.copy()
                    i=0
                    self._pcoef.clear()
                    self._icoef.clear()

                    for power,coef in t.items():

                        for p,c in __o._pcoef.items():
                            k = p+power
                            if k in self._pcoef:
                                self._pcoef[k]+=coef*c
                                continue
                            self._pcoef[k]=coef*c
                        
                        for p,c in __o._icoef.items():
                            k = p+power
                            if k in self._icoef:
                                self._icoef[k][1]+=coef*c[1]
                                continue
                            self._icoef[k]=[f"C{i}",coef*c[1]]
                            i+=1

                    for power,coef in tt.items():

                        for p,c in __o._pcoef.items():
                            k = p+power
                            if k in self._icoef:
                                self._icoef[k][1]+=coef[1]*c
                                continue
                            self._icoef[k]=[f"C{i}",coef[1]*c]
                            i+=1
                        
                        for p,c in __o._icoef.items():
                            k = p+power
                            if k in self._icoef:
                                self._icoef[k][1]+=coef[1]*c[1]
                                continue
                            self._icoef[k]=[f"C{i}",coef[1]*c[1]]
                            i+=1

                    return self

                __o=__o.toMulty()
            return self.toMulty()*__o
        
        self._check__is_Number(__o,"{} cannot multiply a SinglePolinomial")

        for power in self._pcoef:
            self._pcoef[power]*=__o
        for power in self._icoef:
            self._icoef[power]*=__o

        return self

    def __divmod__(self, __o:Number|Self|MultyPolinomial) -> tuple[Self|MultyPolinomial,Self|MultyPolinomial]:
        """
        Euclidean division, or division with remainder between this MultyPolinomial and teh given number or MultyPolinomial
        This method returns the quotient and the rest
        """

        if not __o:
            raise ZeroDivisionError("Cannot divide by 0")

        if isinstance(__o, MultyPolinomial):
            if isinstance(__o, SinglePolynomial):
                if self._unkn == __o._unkn:

                    #this will operate as a result of the difvision
                    _self = self.copy()
                
                    #this will operate as the quotient
                    p=self.zero(self._unkn)

                    #this is used as operator
                    t = self.zero(self._unkn)

                    while _self and (i:=_self.deg())>=(j:=__o.deg()):
                        
                        #that's the monom for this operation
                        t._pcoef.clear()
                        t._pcoef[i-j] = _self._pcoef[i]/__o._pcoef[j]
                        
                        #it updates quotient and rest
                        _self -= __o*t
                        p+=t

                    return p,_self
                
                __o = __o.toMulty()
            return self.toMulty().divmod(__o)
        
        self._check__is_Number(__o,"{} cannot floor-divide nor module a MultyPolinomial")

        return self.__class__({power:coef//__o for power,coef in self._pcoef.items()},self._unkn, {power:[coef[0],coef[1]//__o] for power,coef in self._icoef.items()}),self.__class__({power:coef%__o for power,coef in self._pcoef.items()},self._unkn, {power:[coef[0],coef[1]%__o] for power,coef in self._icoef.items()})

    def __floordiv__(self, __o:Number|Self) -> Self:
        """
        Euclidean division, or division with remainder between this MultyPolinomial and teh given number or MultyPolinomial
        This method returns the quotient
        """

        if not __o:
            raise ZeroDivisionError("Cannot divide by 0")

        if isinstance(__o, MultyPolinomial):
            if isinstance(__o, SinglePolynomial):
                if self._unkn == __o._unkn:

                    #this will operate as a result of the difvision
                    _self = self.copy()
                
                    #this will operate as the quotient
                    p=self.zero(self._unkn)

                    #this is used as operator
                    t = self.zero(self._unkn)

                    while _self and (i:=_self.deg())>=(j:=__o.deg()):
                        
                        #that's the monom for this operation
                        t._pcoef.clear()
                        t._pcoef[i-j] = _self._pcoef[i]/__o._pcoef[j]
                        
                        #it updates quotient and rest
                        _self -= __o*t
                        p+=t

                    return p
                
                __o = __o.toMulty()
            return self.toMulty().__floordiv__(__o)

        self._check__is_Number(__o,"{} cannot floor-divide a MultyPolinomial")

        return self.__class__({power:coef//__o for power,coef in self._pcoef.items()},self._unkn, {power:[coef[0],coef[1]//__o] for power,coef in self._icoef.items()})

    def __ifloordiv__(self, __o:Number|Self) -> Self:
        """
        Euclidean division, or division with remainder between this MultyPolinomial and teh given number or MultyPolinomial
        This method returns the quotient
        """

        if not __o:
            raise ZeroDivisionError("Cannot divide by 0")

        if isinstance(__o, MultyPolinomial):
            if isinstance(__o, SinglePolynomial):
                if self._unkn == __o._unkn:

                    #this will operate as a result of the difvision
                    _self = self.copy()
                    
                    #it will become the quotient itself
                    self.clear()

                    #this is used as operator
                    t = self.zero(self._unkn)

                    while _self and (i:=_self.deg())>=(j:=__o.deg()):
                        
                        #that's the monom for this operation
                        t._pcoef.clear()
                        t._pcoef[i-j] = _self._pcoef[i]/__o._pcoef[j]
                        
                        #it updates quotient and rest
                        _self -= __o*t
                        self+=t

                    return self
                
                __o = __o.toMulty()
            return self.toMulty().__ifloordiv__(__o)

        self._check__is_Number(__o,"{} cannot floor-divide a MultyPolinomial")

        for power in self._pcoef:
            self._pcoef[power]//=__o
        for power in self._icoef:
            self._icoef[power][1]//=__o

        return self

    def __mod__(self, __o:Number|Self) -> Self:
        """
        Euclidean division, or division with remainder between this MultyPolinomial and teh given number or MultyPolinomial
        This method returns the rest
        """

        if not __o:
            raise ZeroDivisionError("Cannot divide by 0")

        if isinstance(__o, MultyPolinomial):
            if isinstance(__o, SinglePolynomial):
                if self._unkn == __o._unkn:

                    #this will operate as a result of the difvision
                    _self = self.copy()

                    #this is used as operator
                    t = self.zero(self._unkn)

                    while _self and (i:=_self.deg())>=(j:=__o.deg()):
                        
                        #that's the monom for this operation
                        t._pcoef.clear()
                        t._pcoef[i-j] = _self._pcoef[i]/__o._pcoef[j]
                        
                        #it updates quotient and rest
                        _self -= __o*t

                    return _self
                
                __o = __o.toMulty()
            return self.toMulty().__mod__(__o)

        self._check__is_Number(__o,"{} cannot module a MultyPolinomial")
        
        return self.__class__({power:coef%__o for power,coef in self._pcoef.items()},self._unkn, {power:[coef[0],coef[1]%__o] for power,coef in self._icoef.items()})
        
    def __imod__(self, __o:Number|Self) -> Self:
        """
        Euclidean division, or division with remainder between this MultyPolinomial and the given number or MultyPolinomial
        This method returns the rest
        """

        if not __o:
            raise ZeroDivisionError("Cannot divide by 0")

        if isinstance(__o, MultyPolinomial):
            if isinstance(__o, SinglePolynomial):
                if self._unkn == __o._unkn:

                    #this is used as operator
                    t = self.zero(self._unkn)

                    while self and (i:=self.deg())>=(j:=__o.deg()):
                        
                        #that's the monom for this operation
                        t._pcoef.clear()
                        t._pcoef[i-j] = self._pcoef[i]/__o._pcoef[j]
                        
                        #it updates quotient and rest
                        self -= __o*t

                    return self
                
                __o = __o.toMulty()
            return self.toMulty().__imod__(__o)

        self._check__is_Number(__o,"{} cannot module a MultyPolinomial")

        for power in self._pcoef:
            self._pcoef[power]%=__o
        for coef in self._icoef.values():
            coef[1]%=__o

        return self

if __name__ == '__main__':
    y = SinglePolynomial.fromText("3*x+x-1")
    y.unknown="y"
    print(SinglePolynomial.fromSingle(y).__repr__())
    print(y.translate(5,y=2))
    x = MultyPolinomial.fromText("x*y+y+1")
    z = y+x
    print(z,type(z))

