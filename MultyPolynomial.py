from __future__ import annotations
from collections.abc import Iterable, Generator
from typing import Self, Any, Never, overload
from math import floor, ceil, prod
from random import randint

Number = int|float
Powers = dict[str,Number]
Unknowns = tuple[str,...]
Integrals = dict[str,list[str|Number]]
class LenghtError(Exception):
    "The length of a given object doesn't match with the given one"

class MultyPolinomial:
    "This object is used to create and match the needs for a multivariative polinomial"

    #the only variables used by the object
    __slots__ = ('_unkn','_pcoef','_icoef')


    ## SOME INITIALIZATION && CLASSMETHODS ##
    def __new__(cls:type[Self], powers_coefficients:Powers, unknown:Unknowns, integrals_coefficients:Integrals={}) -> Self:
        """
        Before creating the object, it checks that every argument is given in the right format
        """

        if type(unknown) is not Unknowns.__origin__ :
            raise TypeError("'unknown' has to be a tuple which contains only strings")

        if type(powers_coefficients) is not Powers.__origin__ :
            raise TypeError("'powers_coefficients' has to be a dict")

        if type(integrals_coefficients) is not Integrals.__origin__ :
            raise TypeError("'integrals_coefficients' has to be a dict")

        p = len(unknown)
        if any(not q or len(q.split("-"))!=p for q in powers_coefficients|integrals_coefficients):
            raise LenghtError("All the key string used in both 'powers_coefficients' and 'integrals_coefficients' have to be len(unknown)*2-1")

        for coef in powers_coefficients.values():
            cls._check__is_Number(coef,"Every coef has to be a Number")
        for coef in integrals_coefficients.values():
            cls._check__is_Number(coef[1],"Every coef has to be a Number")
        return super().__new__(cls)

    @overload
    def __init__(self, powers_coefficients:Powers, unknown:Unknowns) -> None:
        """
        It creates the Polinoms giving to it a dictionary for the coefficient for each needed combination on power to each unknown:
        - powers = {'0-0':1,'1-0':-1,'2-2':3} -> 1*x^0*x^0-1*x^1*x^1*y^0+3*x^2*y^2
        
        a tuple for the unknowns:
        - unknown = (x,y)
        """
    
    @overload
    def __init__(self, powers_coefficients:Powers, unknown:Unknowns, integrals_coefficients:Integrals={}) -> None:
        """
        It creates the Polinoms giving to it a dictionary for the coefficient for each needed combination on power to each unknown:
        - powers = {'0-0':1,'1-0':-1,'2-2':3} -> 1*x^0*x^0-1*x^1*x^1*y^0+3*x^2*y^2
        
        a tuple for the unknowns:
        - unknown = (x,y)

        and eventually a dictonary for the "integral coefficient" dictionary:
        - integrals_coefficients = {1-0:[C0,3]} -> 3*C0*x
        """
    
    def __init__(self, powers_coefficients:Powers, unknown:Unknowns, integrals_coefficients:Integrals={}) -> None:
        
        self._unkn:Unknowns = tuple(sorted(unknown))
        lam = lambda power, unkn_er:"-".join(power[unkn_er.index(unk)] for unk in self._unkn)
        self._pcoef:Powers = {lam(power.split("-"),unknown):coef for power,coef in powers_coefficients.items()}
        self._icoef:Integrals = {lam(power.split("-"),unknown):coef for power,coef in integrals_coefficients.items()}

    @classmethod
    def fromMulty(cls: type[Self], m:MultyPolinomial) -> MultyPolinomial:
        """
        Given another MultyPolinomial it creates a new MultyPolinomial with the same informations
        """
        
        return cls(m._pcoef.copy(),m._unkn,{p:c.copy() for p,c in m._icoef.items()})

    @overload
    @classmethod
    def fromText(cls: type[Self], text:str) -> MultyPolinomial:
        """
        Given a string of text it tries to create the polinom.
        the string has to be formatted, writing every multiplication *, even between coef and unknown. The exponential has to be written with ^. It doesn't understand parenthesis
        More complex form have to be created by applaying math operation between multiple MultyPolinomial
        """

    @overload
    @classmethod
    def fromText(cls: type[Self], text:str, unknown:Unknowns=()) -> Self:
        """
        Given a string of text it tries to create the polinom.
        the string has to be formatted, writing every multiplication *, even between coef and unknown. The exponential has to be written with ^. It doesn't understand parenthesis
        More complex form have to be created by applaying math operation between multiple MultyPolinomial

        If a unknown str tuple is given, it will add these if are not present in the given text
        """

    @overload
    @classmethod
    def fromText(cls: type[Self], text:str, unknown:Unknowns=(), integrals_coefficients:Integrals={}) -> Self:
        """
        Given a string of text it tries to create the polinom.
        the string has to be formatted, writing every multiplication *, even between coef and unknown. The exponential has to be written with ^. It doesn't understand parenthesis
        More complex form have to be created by applaying math operation between multiple MultyPolinomial

        If a unknown str tuple is given, it will add these if are not present in the given text

        integrals_coefficients have to with each key by the right lenght and in the right format. It is better to not give anything
        If it is really needed, if unknown = ('x', 'y', 'q'), each item has to be: '0-2-1': ['C0',5] -> 5*C0*y^2*q
        """

    @classmethod
    def fromText(cls: type[Self], text:str, unknown:Unknowns=(), integrals_coefficients:Integrals={}) -> Self:

        unknown = list(unknown)
        t = {}
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

    @overload
    @classmethod
    def oneMulty(cls: type[Self]) -> Self:
        """
        This classmethod creates a MultyPolinomial with only the coef 1
        """

    @overload
    @classmethod
    def oneMulty(cls: type[Self], *unknowns:str) -> Self:
        """
        This classmethod creates a MultyPolinomial with only the coef 1
        If unknowns are given, it initializes it with these, else it won't have any
        """

    @classmethod
    def oneMulty(cls: type[Self], *unknowns:str) -> Self:

        return cls({cls._get_key_0(len(unknowns)):1},unknowns,{})

    @overload
    @classmethod
    def zeroMulty(cls: type[Self]) -> Self:
        """
        This classmethod creates a MultyPolinomial with only the coef 0
        """

    @overload
    @classmethod
    def zeroMulty(cls: type[Self], *unknowns:str) -> Self:
        """
        This classmethod creates a MultyPolinomial with only the coef 0
        If unknowns are given, it initializes it with these, else it won't have any
        """

    @classmethod
    def zeroMulty(cls: type[Self], *unknowns:str) -> Self:
        
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
        if not isinstance(unknowns, Unknowns.__origin__) or len(unknowns)!=len(self._unkn):
            raise LenghtError("The lenght of the given Unknowns has to be the same as the previous one")
        self._unkn = unknowns

    @property
    def powers(self) -> Powers:
        "dictionary of the coefficients"
        return self._pcoef

    @powers.setter
    def powers(self, powers_coefficients:Powers) -> None:
        "dictionary of the coefficients"
        if not isinstance(powers_coefficients, Powers.__origin__) or any(len(p.split("-"))!=len(self._unkn) for p in powers_coefficients):
            raise LenghtError("The lenght of all the keys inthe given Powers has to be the same as unknown")
        self._pcoef = powers_coefficients

    @property
    def integrals(self) -> Integrals:
        "dictionary of the integrals costants"
        return self._icoef

    @integrals.setter
    def integrals(self, integrals_coefficients:Integrals) -> None:
        "dictionary of the coefficients"
        if not isinstance(integrals_coefficients, Integrals.__origin__) or any(len(p.split("-"))!=len(self._unkn) for p in integrals_coefficients):
            raise LenghtError("The lenght of all the keys inthe given Integrals has to be the same as unknown")
        self._icoef = integrals_coefficients

    @property
    def all(self) -> tuple[Powers, Unknowns, Integrals]:
        "itis a tuple with powers, unknown, integrals"
        return self._pcoef,self._unkn,self._icoef


    ## SOME INTERESTING METHODS ##
    def has_integrals_const(self) -> bool:
        """
        This function check if any integral's coef is present
        """
        return any(i[1] for i in self._icoef.values())

    def is_a_number(self) -> bool:
        """
        Retruns True if and only if there is not integration's constants and all the coef qwhich degree is greater than 0 are 0
        """

        t=self._get_key_0(len(self._unkn))
        return not (any(coef for power,coef in self._icoef.items() if power!=t) or any(coef[1] for coef in self._icoef.values()))

    def is_a_int_number(self) -> bool:
        """
        Retruns True if and only if there is not integration's constants and all the coef which degree is greater than 0 are 0 and the other is float
        """

        return self.is_a_number() and isinstance(self._pcoef.get(self._get_key_0(len(self._unkn)),0),int)

    def is_a_float_number(self) -> bool:
        """
        Retruns True if and only if there is not integration's constants and all the coef which degree is greater than 0 are 0 and the other is float
        """

        return self.is_a_number() and isinstance(self._pcoef.get(self._get_key_0(len(self._unkn)),0),float)

    def __int__(self) -> int:
        "returns the 0 degree coef as int"

        return int(self._pcoef.get(self._get_key_0(len(self._unkn)),0))

    def __float__(self) -> float:
        "returns the 0 degree coef as float"

        return float(self._pcoef.get(self._get_key_0(len(self._unkn)),0.0))

    def __len__(self) -> int:
        """
        return the number of unknowns 
        """
        return len(self._unkn)

    @overload
    def monoms(self) -> Generator[MultyPolinomial]:
        """
        It returns all the monoms of this polynomial
        """

    @overload
    def monoms(self, __ignore=False) -> Generator[MultyPolinomial]:
        """
        It returns all the monoms of this polynomial except the Integrals constants if __ignore is True
        """

    def monoms(self, __ignore=False) -> Generator[MultyPolinomial]:
        h=True
        for power,coef in self._pcoef.items():
            if not coef:
                continue
            yield self.__class__({power:coef}, self._unkn)
            h=False

        if  __ignore:
            if h:
                yield self.zeroMulty(*self._unkn)
            return

        k = {self._get_key_0(len(self._unkn)):0}
        for power,coef in self._icoef.items():
            if not coef[1]:
                continue
            yield self.__class__(k.copy(), self._unkn, {power:coef})
            h=False
        
        if h:
            yield self.zeroMulty(*self._unkn)

    @overload
    def deg(self) -> int:
        """
        it returns the maximum degree of the polynomial
        """

    @overload
    def deg(self, unknown:str) -> int:
        """
        it returns the maximum degree regarding the given unknown of the polynomial
        """

    def deg(self, unknown:str|None=None) -> int:
        if not unknown:
            return max(0,0,*tuple(eval(power.replace("-","+")) for power,coef in self._pcoef.items() if coef),*tuple(eval(power.replace("-","+")) for power,coef in self._icoef.items() if coef))
        
        if unknown not in self._unkn:
            return 0
            
        index = self._unkn.index(unknown)
        
        return max(0,0,*tuple(int(power.split("-")[index]) for power in self._pcoef),*tuple(int(power.split("-")[index]) for power in self._icoef))

    def degs(self) -> Generator[int]:
        """
        for each Unknown it returns its degree
        """

        return (self.deg(u) for u in self._unkn)
        

    ## STRING METHODS ##
    def __repr__(self) -> str:
        """
        rapresentation of the MultyPolinomial
        """
        
        return f"{self.__class__.__name__}{self.all}"

    def __str__(self) -> str:
        """
        string of the MultyPolinomial

        if this MultyPolinomial has any Integrals, it will raise an error if used for fromText()
        Before to do so, is best practice to check if Integrals are present with has_integrals_const() or by passing 'i' at __format__()
        """
        
        s = ""
        h = ("+","-")

        _ = sorted(self._pcoef.keys(),reverse=True)

        for power in sorted(self._pcoef.keys(),reverse=True):
            coef = self._pcoef[power]

            if not coef:
                continue

            if coef == floor(coef):
                coef = floor(coef)

            t = tuple(map(int,power.split("-")))

            if any(t) and abs(coef)==1:
                if coef> 0:
                    s+="+"
                else:
                    s+="-"
            else:
                s+=f"{coef:+}"

            if not any(t):
                continue

            for p,i in zip(self._unkn,t):
                
                if not i:
                    continue

                if not s[-1] in h:
                    s+=f"*{p}"
                else:
                    s+=f"{p}"

                if i>=2:
                    s+=f"^{i}"
                
        for power in sorted(self._icoef.keys(),reverse=True):
            coef = self._icoef[power]

            if not coef[1]:
                continue
            
            if coef[1] == floor(coef[1]):
                coef[1] = floor(coef[1])

            t = tuple(map(int,power.split("-")))

            if abs(coef[1])==1:
                if coef[1]> 0:
                    s+="+"
                else:
                    s+="-"
            else:
                s+=f"{coef[1]:+}*"
            s+=coef[0]

            if not any(t):
                continue

            for p,i in zip(self._unkn,t):
                
                if not i:
                    continue

                if not s[-1] in h:
                    s+=f"*{p}"
                else:
                    s+=f"{p}"

                if i>=2:
                    s+=f"^{i}"

        if not s:
            s = "0"

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

            ks = f"{coef[1]:{numbers}}*{coef[0]}"

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

        if not s:
            return f"""{f"{f'{0:{numbers}}':{monomials}} ":{polynomial}}""".strip("+")
        return f"{s:{polynomial}}".strip("+")

    @staticmethod
    def _get_key_0(__len:int = 0) -> str:
        """
        it returns a string used as key for _pcoef or _icoef.
        it is a 0 sequence of lenght as __mod is 0-0-0-...-0
        """
        
        if __len:
            return ("0-"*__len)[:-1]
        return ("0-"*__len)


    ## EQUALITY AND NON-EQUALITY METHODS ##
    def __eq__(self, __o:Any) -> bool:
        """
        It checks if two MultyPolinomial are identical between eachother or if MultyPolinomial is identical to the given number
        Returns False otherways
        """
        
        if isinstance(__o,MultyPolinomial|Number):
            return self.__str__()==__o.__str__()

        return False

    def __ne__(self, __o:Any) -> bool:
        """
        It checks if two MultyPolinomial are different between eachother or if MultyPolinomial is not to the given number
        Returns True otherways
        """
        
        if isinstance(__o,MultyPolinomial|Number):
            return self.__str__()!=__o.__str__()

        return True

    @overload
    def round_equal(self, __o:Any) -> bool:
        """
        It checks if two MultyPolinomial are almost equal by rounding
        each coef at the 14th decimal
        """
        
    @overload
    def round_equal(self, __o:Any, precision:int=14) -> bool:
        """
        It checks if two MultyPolinomial are almost equal by rounding
        each coef at the given position decimal
        """

    def round_equal(self, __o:Any, precision:int=14) -> bool:
        if isinstance(__o,MultyPolinomial|Number):
            return round(self,precision) == round(__o, precision)

        return False

    @overload
    def non_round_equal(self, __o:Any) -> bool:
        """
        It checks if two MultyPolinomial are NOT almost equal by rounding
        each coef at the 14th decimal
        """
        
    @overload
    def non_round_equal(self, __o:Any, precision:int=14) -> bool:
        """
        It checks if two MultyPolinomial are NOT almost equal by rounding
        each coef at the given position decimal
        """

    def non_round_equal(self, __o:Any, precision:int=14) -> bool:
        if isinstance(__o,MultyPolinomial|Number):
            return round(self,precision) != round(__o, precision)
            
        return False

    def almost_equal(self,__o:Any) -> bool:
        """
        It checks if two MultyPolinomial are different between eachother or if MultyPolinomial is not to the given number
        But ignores the Integrals' coefficients
        Returns True otherways
        """
        
        if isinstance(__o,MultyPolinomial):
            return self.__format__('i')==__o.__format__('i')
        if isinstance(self, Number):
            return self.__format__('i')==__o.__str__()

        return False

    def non_almost_equal(self,__o:Any) -> bool:
        """
        It checks if two MultyPolinomial are different between eachother or if MultyPolinomial is not to the given number
        But ignores the Integrals' coefficients
        Returns True otherways
        """
        
        if isinstance(__o,MultyPolinomial):
            return self.__format__('i')!=__o.__format__('i')
        if isinstance(self, Number):
            return self.__format__('i')!=__o.__str__()

        return True

    def __bool__(self) -> bool:
        """
        It returns False if and only if this is 0
        """
        return any(self._pcoef.values()) or any(i[1] for i in self._icoef.values())


    ## OPERATION OVER MULTIVARIATIVE POLYNOMIALS ##
    @overload
    def __call__(self, values:Number) -> tuple[Number,str]:
        """
        values can be a number if and only if Unknowns has only one element, and evaluate this polynomial in the given value
        To make only a partial evaluation, use evaluate or evaluate_ip methods

        It returns the number of the evaluation and the string representing the Integrals consts
        """

    @overload
    def __call__(self, values:Iterable[Number]) -> tuple[Number,str]:
        """
        by giving the exact number of Numbers as the number of elements in Unknowns, it evaluates the polynomial by replacing each value following the order of Unknowns
        To make only a partial evaluation, use evaluate or evaluate_ip methods

        It returns the number of the evaluation and the string representing the Integrals consts
        """

    @overload
    def __call__(self, values:dict[str, Number]) -> tuple[Number,str]:
        """
        To deal more easily be associating the correct value to the right unknown, is possible to pass values as a dict
        To make only a partial evaluation, use evaluate or evaluate_ip methods

        It returns the number of the evaluation and the string representing the Integrals consts
        """

    @overload
    def __call__(self, values:Number|Iterable[Number]|dict[str, Number], __ignore:bool=False) -> Number | tuple[Number,str]:
        """
        values can be either:
        - a number if and only if Unknowns has only one element, and evaluate this polynomial in the given value
        - an iterable with the exact number of Numbers as the number of elements in Unknowns, it evaluates the polynomial by replacing each value following the order of Unknowns
        - a dict by associating the correct value to the right unknown for each one

        It returns the number of the evaluation and the string representing the Integrals consts

        if __ignore is give True, only the evaluation will be returned

        To make only a partial evaluation, use evaluate or evaluate_ip methods
        """

    def __call__(self, values:Number|Iterable[Number]|dict[str, Number], __ignore:bool=False) -> Number | tuple[Number,str]:

        if isinstance(values, Number):
            if len(self._unkn) != 1:
                raise LenghtError("The number of the given 'values' has to be the same as for the 'unknowns'\nUse .evaluate() for partial evaluation")

            if __ignore:
                return eval(t.replace(self._unkn[0],str(values)).replace("^","**"))

            t=t.replace(self._unkn[0],str(values))
            k=k.replace(self._unkn[0],str(values))
                
            return eval(t.replace("^","**")), k

        if not isinstance(values, Iterable):
            raise TypeError("'values' can be either a Number, a tuple of Numbers or a dict of Numbers")

        if len(values) != len(self._unkn):
            raise LenghtError("The number of the given 'values' has to be the same as for the 'unknowns'\nUse .evaluate() for partial evaluation")

        t = self.__str__().split("+")
        if self._icoef:
            k = "+".join(t[-len(self._icoef):])
            t = "+".join(t[:-len(self._icoef)])
        else:
            k=""
            t= "+".join(t)

        if isinstance(values,dict):
            if any(unk not in values for unk in self._unkn):
                raise KeyError(f"keys value in values of type dict, have to by the same as {self._unkn}")

            if __ignore:
                for unk,val in values.items():
                    t=t.replace(unk,str(val))
        
                return eval(t.replace("^","**"))

            for unk,val in values.items():
                t=t.replace(unk,str(val))
                k=k.replace(unk,str(val))
            return eval(t.replace("^","**")),k

            
        if __ignore:
            for unk,val in zip(self._unkn,values):
                t=t.replace(unk,str(val))
            return eval(t.replace("^","**"))

        for unk,val in zip(self._unkn,values):
            t=t.replace(unk,str(val))
            k=k.replace(unk,str(val))
            
        return eval(t.replace("^","**")), k

    @overload
    def evaluate(self, values:Number) -> Self:
        """
        It returns a copy but making a partial evaluatation of this polynomial in the given value replacing the first element in Unknowns
        """

    @overload
    def evaluate(self, values:Iterable[Number]) -> Self:
        """
        It returns a copy but making a partial evaluatation of this polynomial in the given values replacing the value following the order of Unknowns
        """

    @overload
    def evaluate(self, values:dict[str, Number]) -> Self:
        """
        It returns a copy but making a partial evaluatation of this polynomial replacing each given unknown by its given value
        """

    def evaluate(self, values:Number|Iterable[Number]|dict[str, Number]) -> Self:

        icoef=self._icoef.copy()
        it={}
        pcoef=self._pcoef.copy()
        pt = {}
        if isinstance(values, Number):

            for power,coef in pcoef.items():
                power = list(map(int,power.split("-")))

                coef*=values**power[0]
                power[0] = 0

                power = "-".join(map(str,power))
                if power in pt:
                    pt[power]+=coef
                else:
                    pt[power]=coef

            pcoef.clear()
            pcoef.update(pt)
            pt.clear()
            
            for power,coef in icoef.items():
                power = list(map(int,power.split("-")))

                coef[1]*=values**power[0]
                power[0]=0

                power = "-".join(map(str,power))
                if power in it:
                    it[power][0]+="*"+coef[0]
                    it[power][1]+=coef[1]
                else:
                    it[power]=coef

            icoef.clear()
            icoef.update(it)
            it.clear()

            return self.__class__(pcoef,self._unkn,icoef)

        if not isinstance(values, Iterable):
            raise TypeError("'values' can be either a Number, a tuple of Numbers or a dict of Numbers")

        if isinstance(values,dict):
            for unk,val in values.items():
                if not unk in self._unkn:
                    continue

                index = self._unkn.index(unk)

                for power,coef in pcoef.items():
                    power = list(map(int,power.split("-")))

                    coef*=val**power[index]
                    power[index]=0

                    power = "-".join(map(str,power))
                    if power in pt:
                        pt[power]+=coef
                    else:
                        pt[power]=coef

                pcoef.clear()
                pcoef.update(pt)
                pt.clear()
                
                for power,coef in icoef.items():
                    power = list(map(int,power.split("-")))

                    coef[1]*=val**power[index]
                    power[index]=0

                    power = "-".join(map(str,power))
                    if power in it:
                        it[power][0]+="*"+coef[0]
                        it[power][1]+=coef[1]
                    else:
                        it[power]=coef

                icoef.clear()
                icoef.update(it)
                it.clear()

            return self.__class__(pcoef,self._unkn,icoef)
                
        for unk,val in zip(self._unkn,values):

            index = self._unkn.index(unk)

            for power,coef in pcoef.items():
                power = list(map(int,power.split("-")))

                coef*=val**power[index]
                power[index]=0

                power = "-".join(map(str,power))
                if power in pt:
                    pt[power]+=coef
                else:
                    pt[power]=coef

            pcoef.clear()
            pcoef.update(pt)
            pt.clear()
            
            for power,coef in icoef.items():
                power = list(map(int,power.split("-")))

                coef[1]*=val**power[index]
                power[index] = 0

                power = "-".join(map(str,power))
                if power in it:
                    it[power][0]+="*"+coef[0]
                    it[power][1]+=coef[1]
                else:
                    it[power]=coef

            icoef.clear()
            icoef.update(it)
            it.clear()

        return self.__class__(pcoef,self._unkn,icoef)

    @overload
    def evaluate_ip(self, values:Number) -> None:
        """
        It updates it by making a partial evaluatation of this polynomial in the given value replacing the first element in Unknowns
        """

    @overload
    def evaluate_ip(self, values:Iterable[Number]) -> None:
        """
        It updates it by making  a partial evaluatation of this polynomial in the given values replacing the value following the order of Unknowns
        """

    @overload
    def evaluate_ip(self, values:dict[str, Number]) -> None:
        """
        It updates it by making  a partial evaluatation of this polynomial replacing each given unknown by its given value
        """

    def evaluate_ip(self, values:Number|Iterable[Number]|dict[str, Number]) -> None:

        it={}
        pt = {}
        if isinstance(values, Number):

            for power,coef in self._pcoef.items():
                power = list(map(int,power.split("-")))

                coef*=values**power[0]
                power[0]=0

                power = "-".join(map(str,power))
                if power in pt:
                    pt[power]+=coef
                else:
                    pt[power]=coef

            self._pcoef.clear()
            self._pcoef.update(pt)
            
            for power,coef in self._icoef.items():
                power = list(map(int,power.split("-")))

                coef[1]*=values**power[0]
                power[0]=0

                power = "-".join(map(str,power))
                if power in it:
                    it[power][0]+="*"+coef[0]
                    it[power][1]+=coef[1]
                else:
                    it[power]=coef

            self._icoef.clear()
            self._icoef.update(it)

            return 

        if not isinstance(values, Iterable):
            raise TypeError("'values' can be either a Number, a tuple of Numbers or a dict of Numbers")

        if isinstance(values,dict):
            for unk,val in values.items():

                index = self._unkn.index(unk)

                for power,coef in self._pcoef.items():
                    power = list(map(int,power.split("-")))

                    coef*=val**power[index]
                    power[index]=0

                    power = "-".join(map(str,power))
                    if power in pt:
                        pt[power]+=coef
                    else:
                        pt[power]=coef

                self._pcoef.clear()
                self._pcoef.update(pt)
                pt.clear()
                
                for power,coef in self._icoef.items():
                    power = list(map(int,power.split("-")))

                    coef[1]*=val**power[index]
                    power[index]=0

                    power = "-".join(map(str,power))
                    if power in it:
                        it[power][0]+="*"+coef[0]
                        it[power][1]+=coef[1]
                    else:
                        it[power]=coef

                self._icoef.clear()
                self._icoef.update(it)
                it.clear()

            return
                
        for unk,val in zip(self._unkn,values):

            index = self._unkn.index(unk)

            for power,coef in self._pcoef.items():
                power = list(map(int,power.split("-")))

                coef*=val**power[index]
                power[index]=0

                power = "-".join(map(str,power))
                if power in pt:
                    pt[power]+=coef
                else:
                    pt[power]=coef

            self._pcoef.clear()
            self._pcoef.update(pt)
            pt.clear()
            
            for power,coef in self._icoef.items():
                power = list(map(int,power.split("-")))

                coef[1]*=val**power[index]
                power[index] =0

                power = "-".join(map(str,power))
                if power in it:
                    it[power][0]+="*"+coef[0]
                    it[power][1]+=coef[1]
                else:
                    it[power]=coef

            self._icoef.clear()
            self._icoef.update(it)
            it.clear()

    def partial(self, unknown:str) -> Self:
        """
        It makes a partial derivation in the given unknown
        """

        if not self.deg(unknown):
            if unknown not in self._unkn:
                return self.__class__({self._get_key_0(len(self._unkn)+1):0},self._unkn+(unknown,))
            return self.__class__({self._get_key_0(len(self._unkn)+1):0},self._unkn)

        index = self._unkn.index(unknown)
        t={}
        for power,coef in self._pcoef.items():
            power = list(map(int,power.split("-")))
            if not power[index]:
                continue
            coef*=power[index]
            power[index]-=1
            t["-".join(map(str,power))] = coef

        tt={}
        for power,coef in self._icoef.items():
            power = list(map(int,power.split("-")))
            if not power[index]:
                continue
            coef[1]*=power[index]
            power[index]-=1
            tt["-".join(map(str,power))] = coef
        
        return self.__class__(t,self._unkn, tt)

    def partial_ip(self, unknown:str) -> None:
        """
        It makes a partial derivation in the given unknown
        """
        
        if not self.deg(unknown):
            self._icoef.clear()
            self._pcoef.clear()
            self._pcoef[self._get_key_0(len(self._unkn)+1)] = 0
            if unknown not in self._unkn:
                self._unkn+=(unknown,)
            return

        index = self._unkn.index(unknown)
        t={}
        for power,coef in self._pcoef.items():
            power = list(map(int,power.split("-")))
            if not power[index]:
                continue
            coef*=power[index]
            power[index]-=1
            t["-".join(map(str,power))] = coef

        self._pcoef.clear()
        self._pcoef.update(t)

        t.clear()
        for power,coef in self._icoef.items():
            power = list(map(int,power.split("-")))
            if not power[index]:
                continue
            coef[1]*=power[index]
            power[index]-=1
            t["-".join(map(str,power))] = coef

        self._icoef.clear()
        self._icoef.update(t)

    @overload
    def n_partial(self, *unknown:str) -> Self:
        """
        it makes sequentially all the partial derivations in the given unknown
        """

    @overload
    def n_partial(self, **kwargs:int) -> Self:
        """
        it makes sequentially all the partial derivations in the given unknown by the given number
        """

    @overload
    def n_partial(self, *unknown:str, **kwargs:int) -> Self:
        """
        it makes sequentially all the partial derivations in the given unknown and by given unknown by the given number
        """

    def n_partial(self, *unknown:str, **kwargs:int) -> Self:
        s = self.copy()
        for unk in unknown:
            s.partial_ip(unk)

        for unk, tiems in kwargs.items():
            for _ in range(tiems):
                s.partial_ip(unk)

        return s

    @overload
    def n_partial_ip(self, *unknown:str) -> None:
        """
        it makes sequentially all the partial derivations in the given unknown
        """

    @overload
    def n_partial_ip(self, **kwargs:int) -> None:
        """
        it makes sequentially all the partial derivations in the given unknown by the given number
        """

    @overload
    def n_partial_ip(self, *unknown:str, **kwargs:int) -> None:
        """
        it makes sequentially all the partial derivations in the given unknown and by given unknown by the given number
        """

    def n_partial_ip(self, *unknown:str, **kwargs:int) -> None:
        for unk in unknown:
            self.partial_ip(unk)

        for unk, tiems in kwargs.items():
            for _ in range(tiems):
                self.partial_ip(unk)

    def integral(self, unknown:str) -> Self:
        """
        It integrates the MultyPolinomial in the given unknown
        """

        if unknown not in self._unkn:
            return self.__class__({coef+"-1":power for coef,power in self._pcoef.items()},self._unkn+(unknown,),{coef+"-1":power.copy() for coef,power in self._icoef.items()}|{self._get_key_0(len(self._unkn)+1):[f"C{len(self._icoef)}",1]})

        index = self._unkn.index(unknown)

        t={}
        for power,coef in self._pcoef.items():
            power = list(map(int,power.split("-")))
            
            power[index]+=1
            coef/=power[index]
            t["-".join(map(str,power))] = coef

        tt={}
        for power,coef in self._icoef.items():
            power = list(map(int,power.split("-")))

            power[index]+=1
            coef[1]/=power[index]
            tt["-".join(map(str,power))] = coef

        return self.__class__(t, self._unkn, tt|{self._get_key_0(len(self._unkn)):[f"C{len(self._icoef)}",1]})

    def integral_ip(self, unknown:str) -> None:
        """
        It integrates the MultyPolinomial in the given unknown
        """

        icoef = self._icoef.copy()
        pcoef=self._pcoef.copy()
        self._pcoef.clear()
        self._icoef.clear()

        if unknown not in self._unkn:
            self._unkn+=(unknown,)
            self._pcoef.update({coef+"-1":power for coef,power in pcoef})
            self._icoef.update({coef+"-1":power for coef,power in icoef.items()}|{self._get_key_0(len(self._unkn)):[f"C{len(icoef)}",1]})

            return

        index = self._unkn.index(unknown)

        for power,coef in pcoef.items():
            power = list(map(int,power.split("-")))
            
            power[index]+=1
            coef/=power[index]
            self._pcoef["-".join(map(str,power))] = coef

        for power,coef in icoef.items():
            power = list(map(int,power.split("-")))

            power[index]+=1
            coef[1]/=power[index]
            self._icoef["-".join(map(str,power))] = coef

        self._icoef[self._get_key_0(len(self._unkn))] = [f"C{len(icoef)}",1]
        return 

    @overload
    def n_integral(self, *unknown:str) -> Self:
        """
        it makes sequentially all the integrations in the given unknown
        """

    @overload
    def n_integral(self, **kwargs:int) -> Self:
        """
        it makes sequentially all the integrations in the given unknown by the given number
        """

    @overload
    def n_integral(self, *unknown:str, **kwargs:int) -> Self:
        """
        it makes sequentially all the integrations in the given unknown and by given unknown by the given number
        """

    def n_integral(self, *unknown:str, **kwargs:int) -> Self:
        s = self.copy()
        for unk in unknown:
            s.integral_ip(unk)

        for unk, times in kwargs.items():
            for _ in range(times):
                s.integral_ip(unk)

        return s

    @overload
    def n_integral_ip(self, *unknown:str) -> None:
        """
        it makes sequentially all the integrations in the given unknown
        """

    @overload
    def n_integral_ip(self, **kwargs:int) -> None:
        """
        it makes sequentially all the integrations in the given unknown by the given number
        """

    @overload
    def n_integral_ip(self, *unknown:str, **kwargs:int) -> None:
        """
        it makes sequentially all the integrations in the given unknown and by given unknown by the given number
        """

    def n_integral_ip(self, *unknown:str, **kwargs:int) -> None:
        for unk in unknown:
            self.integral_ip(unk)

        for unk, times in kwargs.items():
            for _ in range(times):
                self.integral_ip(unk)

    def integralAB(self, unknown:str, a:Number, b:Number) -> Self:
        """
        It integrates the MultyPolinomial in the given unknown in the [a,b] interval
        """

        if a>b:
            raise ValueError(f"'b':({b}) has to be greater than 'a':({a})")

        t = self.integral(unknown)

        return t.evaluate({unknown:b})-t.evaluate({unknown:a})

    def integralAB_ip(self, unknown:str, a:Number, b:Number) -> None:
        """
        It integrates the MultyPolinomial in the given unknown in the [a,b] interval
        """

        if a>b:
            raise ValueError(f"'b':({b}) has to be greater than 'a':({a})")

        self.integral_ip(unknown)
        t= self.copy()

        self.evaluate_ip({unknown:b})
        self-=t.evaluate({unknown:a})

    def n_integralAB(self, **kwargs:tuple[int,int]) -> Self:
        """
        it makes sequentially all the integrations in the given unknown in its respective interval
        """

        t = self.copy()

        for unk, interval in kwargs.items():
            t.integralAB_ip(unk, *interval)

        return t

    def n_integralAB_ip(self, **kwargs:tuple[int,int]) -> None:
        """
        it makes sequentially all the integrations in the given unknown in its respective interval
        """

        for unk, interval in kwargs.items():
            self.integralAB_ip(unk, *interval)
        

    ## TRASNFORMATIONS ##
    def __neg__(self) -> Self:
        """
        It returns a new MultyPolinomial with every coef negated
        """
        
        return self.__class__({power:-coef for power,coef in self._pcoef.items() if coef}, self._unkn, {power:[coef[0],-coef[1]] for power,coef in self._icoef.items() if coef[1]})

    def __pos__(self) -> Self:
        """
        It returns a new MultyPolinomial
        """
        
        return self.__class__({power:coef for power,coef in self._pcoef.items() if coef}, self._unkn, {power:coef[:] for power,coef in self._icoef.items() if coef[1]})

    def __abs__(self) -> Self:
        """
        It returns a new MultyPolinomial with every coef positive. It doesn't change the unknown sign
        """
        
        return self.__class__({power:abs(coef) for power,coef in self._pcoef.items() if coef}, self._unkn, {power:[coef[0],abs(coef[1])] for power,coef in self._icoef.items() if coef})

    @overload
    def __round__(self) -> Self:
        """
        It returns a new MultyPolinomial with each coef rounded to the closer integer
        """
    
    @overload
    def __round__(self, __n:int|None = None) -> Self:
        """
        It returns a new MultyPolinomial with each coef in the given position
        """
    
    def __round__(self, __n:int|None = None) -> Self:

        return self.__class__({power:round(coef,__n) for power,coef in self._pcoef.items()}, self._unkn, {power:[coef[0],round(coef[1],__n)] for power,coef in self._icoef.items()})

    def __floor__(self) -> Self:
        "It returns the MultyPolinomial with all the coefs floored"

        return self.__class__({power:floor(coef) for power,coef in self._pcoef.items()}, self._unkn, {power:[coef[0],floor(coef[1])] for power,coef in self._icoef.items()})

    def __ceil__(self) -> Self:
        "It returns the MultyPolinomial with all the coefs ceiled"

        return self.__class__({power:ceil(coef) for power,coef in self._pcoef.items()}, self._unkn, {power:[coef[0],ceil(coef[1])] for power,coef in self._icoef.items()})

    def clear(self) -> None:
        """
        It transform itself to zeroMulty
        """
        
        self._pcoef.clear()
        self._pcoef[self._get_key_0(len(self._unkn))]=0
        self._icoef.clear()

    def clean(self) -> Self:
        """
        It returns a new MultyPolinomial removing any unkown wich isn't used. It skips any zero coef
        """

        t = [False]*len(self._unkn)
        _pcoef = self._pcoef.copy()
        for power,coef in self._pcoef.items():
            if not coef:
                del _pcoef[power]
                continue

            if all(t):
                continue
                
            for i,p in enumerate(power.split("-")):
                if p>"0":
                    t[i] = True

        _icoef = self._icoef.copy()
        for power,coef in self._icoef.items():
            if not coef[1]:
                del _icoef[power]
                continue

            if all(t):
                continue

            for i,p in enumerate(power.split("-")):
                if p>"0":
                    t[i] = True
        
        if all(t):
            return self.__class__(_pcoef,self._unkn,self._icoef)
        
        unkn = tuple(unknown for i,unknown in enumerate(self._unkn) if t[i])
        if unkn:
            pcoef = {"-".join(p for i,p in enumerate(power.split("-")) if t[i]):coef for power,coef in _pcoef.items()}
            icoef = {"-".join(p for i,p in enumerate(power.split("-")) if t[i]):coef for power,coef in _icoef.items()}
        else:
            unkn = (self._unkn[0],)
            pcoef = {"0":coef for power,coef in _pcoef.items()}
            icoef = {"0":coef.copy() for power,coef in _icoef.items()}

        return self.__class__(pcoef,unkn,icoef)

    def clean_ip(self) -> None:
        """
        It updates this MultyPolinomial by removing any unkown wich isn't used. It removes any zero coef
        """

        t = [False]*len(self._unkn)
        pcoef = self._pcoef.copy()
        for power,coef in pcoef.items():
            if not coef:
                del self._pcoef[power]
                continue

            if all(t):
                continue
                
            for i,p in enumerate(power.split("-")):
                if p>"0":
                    t[i] = True
            
        if not self._pcoef:
            self._pcoef[self._get_key_0(len(self._unkn))] = 0

        icoef = self._icoef.copy()
        for power,coef in icoef.items():
            if not coef[1]:
                del self._icoef[power]
                continue

            if all(t):
                continue

            for i,p in enumerate(power.split("-")):
                if p>"0":
                    t[i] = True
        
        if all(t):
            return
        
        self._pcoef.clear()
        self._icoef.clear()
        if all([not i for i in t]):
            self._unkn = ()
            return

        unkn = self._unkn[0]
        self._unkn = tuple(unknown for i,unknown in zip(t,self._unkn) if i)
        if not self._unkn:
            self._unkn = unkn
        self._pcoef.update({"-".join(p for i,p in zip(t,power.split("-")) if i):coef for power,coef in pcoef.items()})
        self._icoef.update({"-".join(p for i,p in zip(t,power.split("-")) if i):coef for power,coef in icoef.items()})

    def update(self, __o:Self) -> None:
        """
        given a MultyPolinomial,. it updates this MultyPolinomial with the same information of the given one
        """

        self._icoef.clear()
        self._icoef.update(__o._icoef.copy())
        self._pcoef.clear()
        self._pcoef.update(__o._pcoef.copy())
        self._unkn = __o._unkn

    @overload
    def copy(self) -> Self:
        """
        It creates a copy of the current MultyPolinomial
        """

    @overload
    def copy(self, __ignore:bool=False) -> Self:
        """
        It creates a copy of the current MultyPolinomial
        if __ignore is True, the Integrals part will be ignored
        """

    def copy(self, __ignore:bool = False) -> Self:
        if __ignore:
            return self.__class__(self._pcoef.copy(),self._unkn)

        return self.__class__(self._pcoef.copy(),self._unkn,self._icoef.copy())

    @overload
    def translate(self, *args:Number) -> Self:
        "by giving a number, one and only one, is possible to translate 'vertically' the polymoial"

    @overload
    def translate(self, **kwargs:Number) -> Self:
        """
        for each given unknown, it translates the polynomial by the corrispective value.
        """

    @overload
    def translate(self, *args:Number, **kwargs:Number) -> Self:
        """
        By giving a number, in args one and only one, is possible to translate 'vertically' the polymoial.
        For each given unknown in kwargs, it translates the polynomial by its corrispective value.
        """

    def translate(self, *args:Number, **kwargs:Number) -> Self:
        
        if args:
            p = self.__class__({self._get_key_0(len(self._unkn)):args[0]},self._unkn)
        else:
            p = self.__class__.zeroMulty(*self._unkn,)
        p._icoef = {power:coef.copy() for power,coef in self._icoef.items()}
        
        if kwargs:
            s = tuple(self.__class__({'1':1,'0':-kwargs.get(unk,0)},(unk,)) for unk in p._unkn)
            exp = lambda y,x:x**int(y)
            trans = lambda power: prod(map(exp,power.split('-'),s))

            for power,coef in self._pcoef.items():
                p+=trans(power)*coef
                
            for pol in s:
                pol.clear()
                pol._icoef.update({'1':['c',1],'0':['c',-kwargs.get(*pol._unkn,0)]})

            for power in self._icoef:
                p+=trans(power)
            for i,coef in enumerate(p._icoef.values()):
                coef[:] = f'C{i}',1

        return p
    
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

        if kwargs:
            p = self.copy()
            self.clear()

            s = tuple(self.__class__({'1':1,'0':-kwargs.get(unk,0)},(unk,)) for unk in self._unkn)
            exp = lambda y,x:x**int(y)
            trans = lambda power: prod(map(exp,power.split('-'),s))

            for power,coef in p._pcoef.items():
                self+=trans(power)*coef
            for i,coef in enumerate(p._icoef.values()):
                coef[:] = f'C{i}',1
            self._icoef.update(p._icoef)
        
        elif args:
            self+=args[0]


    ## OPERATION WITH MULTIVARIATIVE POLYNOMIALS ##
    @staticmethod
    def _check__is_Number(__o:Any, error:str="{}"):
        "This function raises a TypeError if the given __o is not a Number"
        if not isinstance(__o, Number):
            raise TypeError(error.format(type(__o)))

    def __add__(self, __o:Number | Self) -> Self:
        "Add a number or another MultyPolinomial to this MultyPolinomial"
        if isinstance(__o, MultyPolinomial):
            unkn = tuple(sorted(tuple(set(self._unkn)|set(__o._unkn))))
            lam = lambda power, unkn_er:"-".join(power[unkn_er.index(unk)] if unk in unkn_er else '0' for unk in unkn)
            t = {lam(power.split("-"),self._unkn):coef for power,coef in self._pcoef.items()}
            tt = {lam(power.split("-"),self._unkn):coef for power,coef in self._icoef.items()}

            for power, coef in __o._pcoef.items():
                power = lam(power.split("-"),__o._unkn)

                if power in t:
                    t[power] += coef
                else:
                    t[power] = coef

            for power, coef in __o._icoef.items():
                power = lam(power.split("-"),__o._unkn)

                if power in tt:
                    tt[power][1] += coef[1]
                else:
                    tt[power] = coef[:]

            return self.__class__(t,unkn,tt)

        self._check__is_Number(__o,"{} cannot added to a MultyPolinomial")

        t = self._pcoef.copy()
        power = self._get_key_0(len(self._unkn))
        if power in t:
            t[power]+=__o
            return self.__class__(t,self._unkn,{power:coef[:] for power,coef in self._icoef.items()})
        
        t[power] =__o
        
        return self.__class__(t, self._unkn, {power:coef[:] for power,coef in self._icoef.items()})
    
    def __radd__(self, __o:Number | Self) -> Self:
        "Add a number or another MultyPolinomial to this MultyPolinomial"

        if isinstance(__o, MultyPolinomial):
            unkn = tuple(sorted(tuple(set(self._unkn)|set(__o._unkn))))
            lam = lambda power, unkn_er:"-".join(power[unkn_er.index(unk)] if unk in unkn_er else '0' for unk in unkn)
            t = {lam(power.split("-"),self._unkn):coef for power,coef in self._pcoef.items()}
            tt = {lam(power.split("-"),self._unkn):coef for power,coef in self._icoef.items()}

            for power, coef in __o._pcoef.items():
                power = lam(power.split("-"),__o._unkn)

                if power in t:
                    t[power] += coef
                else:
                    t[power] = coef

            for power, coef in __o._icoef.items():
                power = lam(power.split("-"),__o._unkn)

                if power in tt:
                    tt[power][1] += coef[1]
                else:
                    tt[power] = coef[:]

            return self.__class__(t,unkn,tt)

        self._check__is_Number(__o,"{} cannot added to a MultyPolinomial")
        
        t = self._pcoef.copy()
        power = self._get_key_0(len(self._unkn))
        if power in t:
            t[power]+=__o
            return self.__class__(t,self._unkn,{power:coef[:] for power,coef in self._icoef.items()})
        
        t[power] =__o
        
        return self.__class__(t, self._unkn, {power:coef[:] for power,coef in self._icoef.items()})
    
    def __iadd__(self, __o:Number | Self) -> Self:
        "Add a number or another MultyPolinomial to this MultyPolinomial"

        if isinstance(__o, MultyPolinomial):
            unkn = tuple(sorted(tuple(set(self._unkn)|set(__o._unkn))))
            lam = lambda power, unkn_er:"-".join(power[unkn_er.index(unk)] if unk in unkn_er else '0' for unk in unkn)
            t = {lam(power.split("-"),self._unkn):coef for power,coef in self._pcoef.items()}
            tt = {lam(power.split("-"),self._unkn):coef for power,coef in self._icoef.items()}

            for power, coef in __o._pcoef.items():
                power = lam(power.split("-"),__o._unkn)

                if power in t:
                    t[power] += coef
                else:
                    t[power] = coef

            for power, coef in __o._icoef.items():
                power = lam(power.split("-"),__o._unkn)

                if power in tt:
                    tt[power][1] += coef[1]
                else:
                    tt[power] = coef[:]

            self._pcoef.clear()
            self._pcoef.update(t)
            self._icoef.clear()
            self._icoef.update(tt)
            self._unkn = unkn

            return self

        self._check__is_Number(__o,"{} cannot added to a MultyPolinomial")

        power = self._get_key_0(len(self._unkn))
        if power in self._pcoef:
            self._pcoef[power]+=__o
        else:
            self._pcoef[power] =__o
        
        return self

    def __sub__(self, __o:Number | Self) -> Self:
        "subtract a number or another MultyPolinomial to this MultyPolinomial"

        if isinstance(__o, MultyPolinomial):
            unkn = tuple(sorted(tuple(set(self._unkn)|set(__o._unkn))))
            lam = lambda power, unkn_er:"-".join(power[unkn_er.index(unk)] if unk in unkn_er else '0' for unk in unkn)
            t = {lam(power.split("-"),self._unkn):coef for power,coef in self._pcoef.items()}
            tt = {lam(power.split("-"),self._unkn):coef for power,coef in self._icoef.items()}

            for power, coef in __o._pcoef.items():
                power = lam(power.split("-"),__o._unkn)

                if power in t:
                    t[power] -= coef
                else:
                    t[power] = -coef

            for power, coef in __o._icoef.items():
                power = lam(power.split("-"),__o._unkn)

                if power in tt:
                    tt[power][1] -= coef[1]
                else:
                    tt[power] = [coef[0],-coef[1]]

            return self.__class__(t,unkn,tt)
        
        self._check__is_Number(__o,"{} cannot subtract a MultyPolinomial")

        t = self._pcoef.copy()
        power = self._get_key_0(len(self._unkn))
        if power in t:
            t[power]-=__o
            return self.__class__(t,self._unkn,{power:coef[:] for power,coef in self._icoef.items()})
        
        t[power] =-__o
        
        return self.__class__(t, self._unkn, {power:coef[:] for power,coef in self._icoef.items()})
    
    def __rsub__(self, __o:Number | Self) -> Self:
        "Add this MultyPolinomial to a number or another MultyPolinomial"

        if isinstance(__o, MultyPolinomial):
            unkn = tuple(sorted(tuple(set(self._unkn)|set(__o._unkn))))
            lam = lambda power, unkn_er:"-".join(power[unkn_er.index(unk)] if unk in unkn_er else '0' for unk in unkn)
            t = {lam(power.split("-"),self._unkn):-coef for power,coef in self._pcoef.items()}
            tt = {lam(power.split("-"),self._unkn):-coef for power,coef in self._icoef.items()}

            for power, coef in __o._pcoef.items():
                power = lam(power.split("-"),__o._unkn)

                if power in t:
                    t[power] += coef
                else:
                    t[power] = coef

            for power, coef in __o._icoef.items():
                power = lam(power.split("-"),__o._unkn)

                if power in tt:
                    tt[power][1] -= coef[1]
                else:
                    tt[power] = [coef[0],-coef[1]]

            return self.__class__(t,unkn,tt)

        self._check__is_Number(__o,"{} cannot be subtract by a MultyPolinomial")

        t = self._pcoef.copy()
        power = self._get_key_0(len(self._unkn))
        if power in t:
            t[power]+=__o
            return self.__class__(t,self._unkn,{power:coef[:] for power,coef in self._icoef.items()})
        
        t[power] =__o
        
        return self.__class__(t, self._unkn, {power:coef[:] for power,coef in self._icoef.items()})
    
    def __isub__(self, __o:Number | Self) -> Self:
        "subtract a number or another MultyPolinomial to this MultyPolinomial"

        if isinstance(__o, MultyPolinomial):
            unkn = tuple(sorted(tuple(set(self._unkn)|set(__o._unkn))))
            lam = lambda power, unkn_er:"-".join(power[unkn_er.index(unk)] if unk in unkn_er else '0' for unk in unkn)
            t = {lam(power.split("-"),self._unkn):coef for power,coef in self._pcoef.items()}
            tt = {lam(power.split("-"),self._unkn):coef for power,coef in self._icoef.items()}

            for power, coef in __o._pcoef.items():
                power = lam(power.split("-"),__o._unkn)

                if power in t:
                    t[power] -= coef
                else:
                    t[power] = -coef

            for power, coef in __o._icoef.items():
                power = lam(power.split("-"),__o._unkn)

                if power in tt:
                    tt[power][1] -= coef[1]
                else:
                    tt[power] = [coef[0],-coef[1]]

            self._pcoef.clear()
            self._pcoef.update(t)
            self._icoef.clear()
            self._icoef.update(tt)
            self._unkn = unkn

            return self

        self._check__is_Number(__o,"{} cannot subtract a MultyPolinomial")

        power = self._get_key_0(len(self._unkn))
        if power in self._pcoef:
            self._pcoef[power]-=__o
        else:
            self._pcoef[power] =-__o
        
        return self

    def __mul__(self, __o:Number | Self) -> Self:
        "Multiplicate a number or another MultyPolinomial to this MultyPolinomial"
        
        if isinstance(__o, MultyPolinomial):
            unkn = tuple(sorted(tuple(set(self._unkn)|set(__o._unkn))))
            lam = lambda power, unkn_er:"-".join(power[unkn_er.index(unk)] if unk in unkn_er else '0' for unk in unkn)
            join = lambda x,y:str(eval(f'{x}+{y}'))
            ts = {lam(power.split("-"),self._unkn):coef for power,coef in self._pcoef.items()}
            tts = {lam(power.split("-"),self._unkn):coef for power,coef in self._icoef.items()}
            to = {lam(power.split("-"),__o._unkn):coef for power,coef in __o._pcoef.items()}
            tto = {lam(power.split("-"),__o._unkn):coef for power,coef in __o._icoef.items()}
            t = {}
            tt={}

            for power,coef in ts.items():
                power=power.split("-")
                for po,co in to.items():
                    k = "-".join(map(join,power,po.split("-")))
                    if k in t:
                        t[k] += coef * co
                        continue
                    t[k] = coef * co
                for po,co in tto.items():
                    k = "-".join(map(join,power,po.split("-")))
                    if k in tt:
                        tt[k][1] += coef * co[1]
                        continue
                    tt[k] =["", coef * co[1]]

            for power,coef in tts.items():
                power=power.split("-")
                for po,co in to.items():
                    k = "-".join(map(join,power,po.split("-")))
                    if k in tt:
                        tt[k][1] += coef[1] * co
                        continue
                    tt[k] =["", coef[1] * co]
                for po,co in tto.items():
                    k = "-".join(map(join,power,po.split("-")))
                    if k in tt:
                        tt[k][1] += coef[1] * co[1]
                        continue
                    tt[k] =["", coef[1] * co[1]]
            i=0
            for power,coef in tt.copy().items():
                if not coef[1]:
                    del tt[power]
                    continue
                tt[power][0] = f"C{i}"
                i+=1
            tt
            return self.__class__(t,unkn,tt)
        
        self._check__is_Number(__o,"{} cannot multiply a MultyPolinomial")

        return self.__class__( {power:coef*__o for power,coef in self._pcoef.items()},self._unkn,{power:[coef[0],coef[1]*__o] for power,coef in self._icoef.items()})

    def __rmul__(self, __o:Number | Self) -> Self:
        "Multiplicate a number or another MultyPolinomial to this MultyPolinomial"

        if isinstance(__o, MultyPolinomial):
            unkn = tuple(sorted(tuple(set(self._unkn)|set(__o._unkn))))
            lam = lambda power, unkn_er:"-".join(power[unkn_er.index(unk)] if unk in unkn_er else '0' for unk in unkn)
            join = lambda x,y:str(eval(f'{x}+{y}'))
            ts = {lam(power.split("-"),self._unkn):coef for power,coef in self._pcoef.items()}
            tts = {lam(power.split("-"),self._unkn):coef for power,coef in self._icoef.items()}
            to = {lam(power.split("-"),__o._unkn):coef for power,coef in __o._pcoef.items()}
            tto = {lam(power.split("-"),__o._unkn):coef for power,coef in __o._icoef.items()}
            t = {}
            tt={}

            for power,coef in ts.items():
                power=power.split("-")
                for po,co in to.items():
                    k = "-".join(map(join,power,po.split("-")))
                    if k in t:
                        t[k] += coef * co
                        continue
                    t[k] = coef * co
                for po,co in tto.items():
                    k = "-".join(map(join,power,po.split("-")))
                    if k in tt:
                        tt[k][1] += coef * co[1]
                        continue
                    tt[k] =["", coef * co[1]]

            for power,coef in tts.items():
                power=power.split("-")
                for po,co in to.items():
                    k = "-".join(map(join,power,po.split("-")))
                    if k in tt:
                        tt[k][1] += coef[1] * co
                        continue
                    tt[k] =["", coef[1] * co]
                for po,co in tto.items():
                    k = "-".join(map(join,power,po.split("-")))
                    if k in tt:
                        tt[k][1] += coef[1] * co[1]
                        continue
                    tt[k] =["", coef[1] * co[1]]
            i=0
            for power,coef in tt.copy().items():
                if not coef[1]:
                    del tt[power]
                    continue
                tt[power][0] = f"C{i}"
                i+=1

            return self.__class__(t,unkn,tt)
        
        self._check__is_Number(__o,"{} cannot multiply a MultyPolinomial")

        return self.__class__( {power:coef*__o for power,coef in self._pcoef.items()},self._unkn,{power:[coef[0],coef[1]*__o] for power,coef in self._icoef.items()})

    def __imul__(self, __o:Number | Self) -> Self:
        "Multiplicate a number or another MultyPolinomial to this MultyPolinomial"

        if isinstance(__o, MultyPolinomial):
            unkn = tuple(sorted(tuple(set(self._unkn)|set(__o._unkn))))
            lam = lambda power, unkn_er:"-".join(power[unkn_er.index(unk)] if unk in unkn_er else '0' for unk in unkn)
            join = lambda x,y:str(eval(f'{x}+{y}'))
            ts = {lam(power.split("-"),self._unkn):coef for power,coef in self._pcoef.items()}
            tts = {lam(power.split("-"),self._unkn):coef for power,coef in self._icoef.items()}
            to = {lam(power.split("-"),__o._unkn):coef for power,coef in __o._pcoef.items()}
            tto = {lam(power.split("-"),__o._unkn):coef for power,coef in __o._icoef.items()}
            
            self._pcoef.clear()
            self._icoef.clear()
            self._unkn = unkn

            for power,coef in ts.items():
                power=power.split("-")
                for po,co in to.items():
                    k = "-".join(map(join,power,po.split("-")))
                    if k in self._pcoef:
                        self._pcoef[k] += coef * co
                        continue
                    self._pcoef[k] = coef * co
                for po,co in tto.items():
                    k = "-".join(map(join,power,po.split("-")))
                    if k in self._icoef:
                        self._icoef[k][1] += coef * co[1]
                        continue
                    self._icoef[k] =["", coef * co[1]]

            for power,coef in tts.items():
                power=power.split("-")
                for po,co in to.items():
                    k = "-".join(map(join,power,po.split("-")))
                    if k in self._icoef:
                        self._icoef[k][1] += coef[1] * co
                        continue
                    self._icoef[k] =["", coef[1] * co]
                for po,co in tto.items():
                    k = "-".join(map(join,power,po.split("-")))
                    if k in self._icoef:
                        self._icoef[k][1] += coef[1] * co[1]
                        continue
                    self._icoef[k] =["", coef[1] * co[1]]

            i=0
            for power,coef in self._icoef.copy().items():
                if not coef[1]:
                    del self._icoef[power]
                    continue
                self._icoef[power][0] = f"C{i}"
                i+=1

            return self

        self._check__is_Number(__o,"{} cannot multiply a MultyPolinomial")

        for power in self._pcoef:
            self._pcoef[power]*=__o

        for coef in self._icoef.values():
            coef[1]*=__o
        
        return self

    def __pow__(self,__o:int) -> Self:
        "elevate this MultyPolinomial to the given positive integer power"

        if not isinstance(__o,int) or __o<0:
            raise TypeError("MultyPolinomial can only have positive integers powers")

        if not __o:
            return self.__class__({self._get_key_0(len(self._unkn)):1},self._unkn)

        t = self.copy()
        for _ in range(1,__o):
            t*=self
        return t

    def __rpow__(self,__o:Never) -> Self:
        "elevation of anything by this MultyPolinomimal"
        
        raise TypeError(f"{type(__o)} cannot be elevate to the power of a MultyPolinomial")

    def __ipow__(self,__o:int) -> Self:
        "elevate this MultyPolinomial to the given positive integer power"
        
        if not isinstance(__o,int) or __o<0:
            raise TypeError("MultyPolinomial can only have positive integers powers")

        if not __o:
            self._pcoef.clear()
            self._icoef.clear()
            self._pcoef[self._get_key_0(len(self._unkn))] = 1
            return self

        t = self.copy()
        for _ in range(1,__o):
            self*=t
        return self

    def __truediv__(self, __o:Number) -> Self:
        "Divide this MultyPolinomial bythe given number"
        
        self._check__is_Number(__o,"{} cannot divide a MultyPolinomial")
            
        return self.__class__({power:coef/__o for power,coef in self._pcoef.items()},self._unkn, {power:[coef[0],coef[1]/__o] for power,coef in self._icoef.items()})

    def __rtruediv__(self, __o:Never) -> Self:
        "division of anything by this MultyPolynomial"

        raise TypeError(f"{type(__o)} cannot be divided by MultyPolinomial")

    def __itruediv__(self, __o:Number) -> Self:
        "Divide this MultyPolinomial bythe given number"
        
        self._check__is_Number(__o,"{} cannot divide a MultyPolinomial")
            
        for power in self._pcoef:
            self._pcoef[power]/=__o
        for power in self._icoef:
            self._icoef[power][1]/=__o

        return self

    def divmod(self, __o:Number|Self) -> tuple[Self,Self]:
        """
        Euclidean division, or division with remainder between this MultyPolinomial and teh given number or MultyPolinomial
        This method returns the quotient and the rest
        """

        if not __o:
            raise ZeroDivisionError("Cannot divide by 0")

        if isinstance(__o, MultyPolinomial):
            if any(_ou not in self._unkn for _ou in __o._unkn):
                return self.zeroMulty(*__o._unkn),self.copy()

            #this function let reorder the powers
            lam = lambda power, unkn_er:"-".join(power[unkn_er.index(unk)] if unk in unkn_er else '0' for unk in self._unkn)

            #this MultyPolinomial is the same as __o, but with every power in the right order
            _otemp = self.__class__({lam(power.split("-"),__o._unkn):coef for power,coef in __o._pcoef.items() if coef},self._unkn,  {lam(power.split("-"),__o._unkn):coef.copy() for power,coef in __o._icoef.items() if coef[1]})
            del lam

            #this contains all the monoms of __o tupled with its degs
            _om = tuple((m,tuple(m.degs())) for m in _otemp.monoms(True))

            #this chooses the highest monom of __o, the order has to follow higher deg with higher per incognita
            m = sorted(_om,key=lambda x:sum(x[1])*10+max(x[1]))[-1]
            del _om

            #this will operate as a result of the difvision
            _self = self.copy()
            
            #this will operate as the quotient
            p=self.zeroMulty(*self._unkn)

            #that's to evaluate the fraction 
            values = [1]*len(self._unkn)

            while str(_self)!="0":
                #this contains all the monoms of _self tupled with its degs, None is added to stop the iteranion when none of the monom can be devided by m
                _sn = tuple((n,tuple(n.degs())) for n in _self.monoms(True))+((None,(1,)),)

                #this chooses the highest monom of _self, the order has to follow higher deg (+1) that can be devided by m or 0, 1 if is None
                n = sorted(_sn, key= lambda x: sum(x[1],start=1)*all(_x>=_m for _x,_m in zip(x[1],m[1]))+(not x[0]))[-1]

                #it stops if n[0] is None or the actual monom is zero. The last one should never be the case, but it works
                if not n[0]:
                    break
                
                #this calculates the diffenece of the exponents
                power = "-".join(tuple(str(j-k) for j,k in zip(n[1],m[1])))
                
                #that's used to calculate the coeff
                coef = n[0](values,True)/m[0](values,True)
                
                #that's the monom for this operation
                s =self.__class__({power:coef}, self._unkn)

                #it updates quotient and rest
                _self -= _otemp*s
                p+=s

            return p,_self
        
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
            if any(_ou not in self._unkn for _ou in __o._unkn):
                return self.zeroMulty(*__o._unkn)

            lam = lambda power, unkn_er:"-".join(power[unkn_er.index(unk)] if unk in unkn_er else '0' for unk in self._unkn)
            
            #this MultyPolinomial is the same as __o, but with every power in the right order
            _otemp = self.__class__({lam(power.split("-"),__o._unkn):coef for power,coef in __o._pcoef.items() if coef},self._unkn,  {lam(power.split("-"),__o._unkn):coef for power,coef in __o._icoef.items() if coef[1]})
            del lam
            
            #this contains all the monoms of __o tupled with its degs
            _om = tuple((m,tuple(m.degs())) for m in _otemp.monoms(True))

            #this chooses the highest monom of __o, the order has to follow higher deg with higher per incognita
            m = sorted(_om,key=lambda x:sum(x[1])*10+max(x[1]))[-1]
            del _om
            
            #this will operate as a result of the difvision
            _self = self.copy()
            
            #this will operate as the quotient
            p=self.zeroMulty(*self._unkn)

            #that's to evaluate the fraction 
            values = [1]*len(self._unkn)

            while str(_self)!="0":
                #this contains all the monoms of _self tupled with its degs, None is added to stop the iteranion when none of the monom can be devided by m
                _sn = tuple((n,tuple(n.degs())) for n in _self.monoms(True))+((None,(1,)),)

                #this chooses the highest monom of _self, the order has to follow higher deg (+1) that can be devided by m or 0, 1 if is None
                n = sorted(_sn, key= lambda x: sum(x[1],start=1)*all(_x>=_m for _x,_m in zip(x[1],m[1]))+(not x[0]))[-1]

                #it stops if n[0] is None or the actual monom is zero. The last one should never be the case, but it works
                if not n[0]:
                    break
                
                #this calculates the diffenece of the exponents
                power = "-".join(tuple(str(j-k) for j,k in zip(n[1],m[1])))
                
                #that's used to calculate the coeff
                coef = n[0](values,True)/m[0](values,True)
                
                #that's the monom for this operation
                s =self.__class__({power:coef}, self._unkn)
                
                #it updates quotient and rest
                _self -= _otemp*s
                p+=s

            return p

        self._check__is_Number(__o,"{} cannot floor-divide a MultyPolinomial")

        return self.__class__({power:coef//__o for power,coef in self._pcoef.items()},self._unkn, {power:[coef[0],coef[1]//__o] for power,coef in self._icoef.items()})

    def __rfloordiv__(self,__o:Never) -> None:
        "the quotient of an Euclidean division"

        raise TypeError(f"{type(__o)} cannot be floor-divided by MultyPolinomial")

    def __ifloordiv__(self, __o:Number|Self) -> Self:
        """
        Euclidean division, or division with remainder between this MultyPolinomial and teh given number or MultyPolinomial
        This method returns the quotient
        """

        if not __o:
            raise ZeroDivisionError("Cannot divide by 0")

        if isinstance(__o, MultyPolinomial):
            if any(_ou not in self._unkn for _ou in __o._unkn):
                self.clear()
                return self

            #this function let reorder the powers
            lam = lambda power, unkn_er:"-".join(power[unkn_er.index(unk)] if unk in unkn_er else '0' for unk in self._unkn)
            
            #this MultyPolinomial is the same as __o, but with every power in the right order
            _otemp = self.__class__({lam(power.split("-"),__o._unkn):coef for power,coef in __o._pcoef.items() if coef},self._unkn,  {lam(power.split("-"),__o._unkn):coef.copy() for power,coef in __o._icoef.items() if coef[1]})
            del lam

            #this contains all the monoms of __o tupled with its degs
            _om = tuple((m,tuple(m.degs())) for m in _otemp.monoms(True))

            #this chooses the highest monom of __o, the order has to follow higher deg with higher per incognita
            m = sorted(_om,key=lambda x:sum(x[1])*10+max(x[1]))[-1]
            del _om

            #this will operate as a result of the difvision
            _self = self.copy()
            
            #it will become the quotient itself
            self.update(self.zeroMulty(*self._unkn))

            #that's to evaluate the fraction 
            values = [1]*len(self._unkn)

            while str(_self)!="0":
                #this contains all the monoms of _self tupled with its degs, None is added to stop the iteranion when none of the monom can be devided by m
                _sn = tuple((n,tuple(n.degs())) for n in _self.monoms(True))+((None,(1,)),)

                #this chooses the highest monom of _self, the order has to follow higher deg (+1) that can be devided by m or 0, 1 if is None
                n = sorted(_sn, key= lambda x: sum(x[1],start=1)*all(_x>=_m for _x,_m in zip(x[1],m[1]))+(not x[0]))[-1]

                #it stops if n[0] is None or the actual monom is zero. The last one should never be the case, but it works
                if not n[0]:
                    break
                
                #this calculates the diffenece of the exponents
                power = "-".join(tuple(str(j-k) for j,k in zip(n[1],m[1])))
                
                #that's used to calculate the coeff
                coef = n[0](values,True)/m[0](values,True)
                
                #that's the monom for this operation
                s =self.__class__({power:coef}, self._unkn)

                #it updates quotient and rest
                _self -= _otemp*s
                self+=s

            return self

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
            if any(_ou not in self._unkn for _ou in __o._unkn):
                return self.copy()

            #this function let reorder the powers
            lam = lambda power, unkn_er:"-".join(power[unkn_er.index(unk)] if unk in unkn_er else '0' for unk in self._unkn)

            #this MultyPolinomial is the same as __o, but with every power in the right order
            _otemp = self.__class__({lam(power.split("-"),__o._unkn):coef for power,coef in __o._pcoef.items() if coef},self._unkn,  {lam(power.split("-"),__o._unkn):coef.copy() for power,coef in __o._icoef.items() if coef[1]})
            del lam

            #this contains all the monoms of __o tupled with its degs
            _om = tuple((m,tuple(m.degs())) for m in _otemp.monoms(True))

            #this chooses the highest monom of __o, the order has to follow higher deg with higher per incognita
            m = sorted(_om,key=lambda x:sum(x[1])*10+max(x[1]))[-1]
            del _om

            #this will operate as a result of the difvision
            _self = self.copy()

            #that's to evaluate the fraction 
            values = [1]*len(self._unkn)

            while str(_self)!="0":
                #this contains all the monoms of _self tupled with its degs, None is added to stop the iteranion when none of the monom can be devided by m
                _sn = tuple((n,tuple(n.degs())) for n in _self.monoms(True))+((None,(1,)),)

                #this chooses the highest monom of _self, the order has to follow higher deg (+1) that can be devided by m or 0, 1 if is None
                n = sorted(_sn, key= lambda x: sum(x[1],start=1)*all(_x>=_m for _x,_m in zip(x[1],m[1]))+(not x[0]))[-1]

                #it stops if n[0] is None or the actual monom is zero. The last one should never be the case, but it works
                if not n[0]:
                    break
                
                #this calculates the diffenece of the exponents
                power = "-".join(tuple(str(j-k) for j,k in zip(n[1],m[1])))
                
                #that's used to calculate the coeff
                coef = n[0](values,True)/m[0](values,True)

                #it updates rest
                _self -= _otemp*self.__class__({power:coef}, self._unkn)

            return _self

        self._check__is_Number(__o,"{} cannot module a MultyPolinomial")
        
        return self.__class__({power:coef%__o for power,coef in self._pcoef.items()},self._unkn, {power:[coef[0],coef[1]%__o] for power,coef in self._icoef.items()})
        
    def __rmod__(self,__o:Never) -> None:
        "the rest of an Euclidean division"
        
        raise TypeError(f"{type(__o)} cannot be moduled by MultyPolinomial")

    def __imod__(self, __o:Number|Self) -> Self:
        """
        Euclidean division, or division with remainder between this MultyPolinomial and the given number or MultyPolinomial
        This method returns the rest
        """

        if not __o:
            raise ZeroDivisionError("Cannot divide by 0")

        if isinstance(__o, MultyPolinomial):
            if any(_ou not in self._unkn for _ou in __o._unkn):
                return self

            #this function let reorder the powers
            lam = lambda power, unkn_er:"-".join(power[unkn_er.index(unk)] if unk in unkn_er else '0' for unk in self._unkn)

            #this MultyPolinomial is the same as __o, but with every power in the right order
            _otemp = self.__class__({lam(power.split("-"),__o._unkn):coef for power,coef in __o._pcoef.items() if coef},self._unkn,  {lam(power.split("-"),__o._unkn):coef.copy() for power,coef in __o._icoef.items() if coef[1]})
            del lam

            #this contains all the monoms of __o tupled with its degs
            _om = tuple((m,tuple(m.degs())) for m in _otemp.monoms(True))

            #this chooses the highest monom of __o, the order has to follow higher deg with higher per incognita
            m = sorted(_om,key=lambda x:sum(x[1])*10+max(x[1]))[-1]
            del _om

            #that's to evaluate the fraction 
            values = [1]*len(self._unkn)

            while self.__str__()!="0":
                #this contains all the monoms of _self tupled with its degs, None is added to stop the iteranion when none of the monom can be devided by m
                _sn = tuple((n,tuple(n.degs())) for n in self.monoms(True))+((None,(1,)),)

                #this chooses the highest monom of _self, the order has to follow higher deg (+1) that can be devided by m or 0, 1 if is None
                n = sorted(_sn, key= lambda x: sum(x[1],start=1)*all(_x>=_m for _x,_m in zip(x[1],m[1]))+(not x[0]))[-1]

                #it stops if n[0] is None or the actual monom is zero. The last one should never be the case, but it works
                if not n[0]:
                    break
                
                #this calculates the diffenece of the exponents
                power = "-".join(tuple(str(j-k) for j,k in zip(n[1],m[1])))
                
                #that's used to calculate the coeff
                coef = n[0](values,True)/m[0](values,True)
                
                #it updates rest
                self -= _otemp*self.__class__({power:coef}, self._unkn)

            return self

        self._check__is_Number(__o,"{} cannot module a MultyPolinomial")

        for power in self._pcoef:
            self._pcoef[power]%=__o
        for coef in self._icoef.values():
            coef[1]%=__o

        return self



if __name__ == '__main__':
    print(MultyPolinomial.fromText("-x-x*y^2","y")*2)
