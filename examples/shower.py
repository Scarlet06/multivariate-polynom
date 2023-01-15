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

from Polynomial import MultyPolinomial,Self,overload

class shower:

    __slots__ = ("m",)
    def __new__(cls: type[Self], m:MultyPolinomial, print_all:bool=True) -> Self:
        if not isinstance(m,MultyPolinomial):
            raise TypeError("this method has to be used only with MultyPolinomial")

        return super().__new__(cls)
        
    @overload
    def __init__(self, m:MultyPolinomial) -> None:
        "Given a MultyPolinomial, it prints it, formats it, and shows its repr.\nIt prints everything right away"
        
    @overload
    def __init__(self, m:MultyPolinomial, print_all:bool=True) -> None:
        "Given a MultyPolinomial, it prints it, formats it, and shows its repr.\nIf print_all is True, it prints everithing rn"
        
    def __init__(self, m:MultyPolinomial, print_all:bool=True) -> None:
        
        self.m = m

        if print_all:
            self.print()
            self.format()
            self.repr()
            self.infos()
            print("\n")

    def print(self) -> None:
        "it prints the MultyPolinomial"

        print(self.m)

    def format(self) -> None:
        "it prints the MultyPolinomial formatted"

        print(f"{self.m:+i<15}")

    def repr(self) -> None:
        "it prints the repr of the MultyPolinomial"

        print(self.m.__repr__())

    def infos(self) -> None:
        "it prints all the values separately"

        print("",*self.m.all,sep="\n\t")
