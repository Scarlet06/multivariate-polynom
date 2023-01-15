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

from Polynomial import MultyPolinomial

# that's just to know which unknowns does they have when imported
class Multy_X(MultyPolinomial): "This class is used only for suggest which unknown the MultyPolinomial should have"
class Multy_Y(MultyPolinomial): "This class is used only for suggest which unknown the MultyPolinomial should have"
class Multy_XY(MultyPolinomial): "This class is used only for suggest which unknown the MultyPolinomial should have"
class Multy_XYZ(MultyPolinomial): "This class is used only for suggest which unknown the MultyPolinomial should have"

#   -> 0
m0:Multy_X = MultyPolinomial.zeroMulty("x")
#   -> 1
m1:Multy_XY = MultyPolinomial.oneMulty("x","y")

#   -> 4*y^3 - 0.3333*x^5*y^2
m_dict:Multy_XY = MultyPolinomial({'0-3':4,'5-2':-1/3}, ('x','y'))
#   -> 2*x + 2*C0
m_dict_integrals:Multy_X = MultyPolinomial({'1':2},('x',),{'0':['C0',2]})

#   -> 3*x^2 + y + 1
m_text:Multy_XY = MultyPolinomial.fromText("3*x^2+1+y")
#   -> x^5*y^7
m_text_unkn:Multy_XYZ = MultyPolinomial.fromText("x^3*y^7*x^2",('z',))
#   -> 3*x*y - 7 + C*x
m_text_integ:Multy_XYZ = MultyPolinomial.fromText("-7+3*x*y",('y','x','z'),{'0-1-0':['C',1]})

#   -> eg: x^2 - 2x, max deg is 2
m_random:Multy_X = MultyPolinomial.random(2)
#   -> eg: -3*x^3 + 4*y*x - 2, max deg is 3
m_random_unkn:Multy_XY = MultyPolinomial.random(3,"y","x")
#   -> eg: -x^2*y + 4*y*x, max deg is 4 but y can have max power 1
m_random_dict:Multy_XY = MultyPolinomial.random(4,"x",y=1)
