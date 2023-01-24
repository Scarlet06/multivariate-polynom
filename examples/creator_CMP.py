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

from ComplexMultyPolynomial import ComplexMultyPolynomial

# that's just to know which unknowns does they have when imported
class CMulty_X(ComplexMultyPolynomial): "This class is used only for suggest which unknown the ComplexMultyPolynomial should have"
class CMulty_Y(ComplexMultyPolynomial): "This class is used only for suggest which unknown the ComplexMultyPolynomial should have"
class CMulty_XY(ComplexMultyPolynomial): "This class is used only for suggest which unknown the ComplexMultyPolynomial should have"
class CMulty_XYZ(ComplexMultyPolynomial): "This class is used only for suggest which unknown the ComplexMultyPolynomial should have"

#   -> 0
cm0 = CMulty_X.zero("x")
#   -> 1
cm1 = CMulty_XY.one("x","y")

#   -> (1+2j)*y^3 - 0.3333*x^5*y^2
cm_dict = CMulty_XY({'0-3':1+2j,'5-2':-1/3}, ('x','y'))
#   -> (2j)*x + 2*C0
cm_dict_integrals = CMulty_X({'1':2j},('x',),{'0':['C0',2]})

#   -> (-6-14.1j)*x^2 + y + 1
cm_text = CMulty_XY.fromText("(3j-4-7.7j+2)*3*x^2+1+y")
#   -> x^5*y^7 - (2j)
cm_text_unkn = CMulty_XYZ.fromText("x^3*y^7*x^2+(-2j)",('z',))
#   -> 3*x*y + z^2 - 7 + C*x
cm_text_integ = CMulty_XYZ.fromText("-7+3*x*y+(1)*z^2",('y','x','z'),{'0-1-0':['C',1]})

#   -> eg: x^2 - 2x, max deg is 2
cm_random = CMulty_X.random(2)
#   -> eg: -3*x^3 + 4*y*x - 2, max deg is 3
cm_random_unkn = CMulty_XY.random(3,"y","x")
#   -> eg: -x^2*y + 4*y*x, max deg is 4 but y can have max power 1
cm_random_dict = CMulty_XY.random(4,"x",y=1)


if __name__ == '__main__':
    print(cm_random_dict)