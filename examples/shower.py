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
            self.beautiful_print()
            # self.repr()
            # self.print()
            # self.format()
            # self.infos()
            # print("\n")

    def string(self) -> None:
        "it prints the MultyPolinomial"

        return self.m.__str__()

    def format(self) -> None:
        "it prints the MultyPolinomial formatted"

        return self.m.__format__("<15i+")

    def repr(self) -> None:
        "it prints the repr of the MultyPolinomial"

        return self.m.__repr__()

    def infos(self) -> None:
        "it prints all the values separately"

        return map(str, self.m.all)

    def beautiful_print(self) -> None:
        s = self.string()
        f = self.format()
        r = self.repr()
        i,j,k = self.infos()
        l = len(max(s,f,r,i,j,k, key=lambda x: len(x)))+6
        self._print_rect(l,s,r,f,i,j,k)

    @staticmethod
    def _open_rect(length:int, title:str) -> str:
        t=f'{title:^{len(title)+2}}'
        t=f'{t:=^{length-2}}'
        return f'{t:#^{length}}'

    @staticmethod
    def _border_rect(length:int, what:str='') -> str:
        t=f'{what:^{length-2}}'
        return f'{t:#^{length}}'

    @staticmethod
    def _close_rect(length:int) -> str:
        return f'{"":#^{length}}'

    def _print_rect(self,length:int, title:str, *what:str) -> None:
        print(self._open_rect(length,title))
        print(self._border_rect(length))
        for arg in what:
            print(self._border_rect(length))
            print(self._border_rect(length,arg))
            
        print(self._border_rect(length))
        print(self._close_rect(length))
        print("\n")
