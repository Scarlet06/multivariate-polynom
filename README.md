# multivariate-polynomial

This Project let you work with multivariate polinomials and has every operation needed to work well with them.
RN it doesn't supports numpy and probably never will, for efficiency I suggest you to check [jannikmi's work](https://github.com/jannikmi/multivar_horner) it looks very good, but it asks you to have a C compiler too.

RN I'm working about finializing my examples and the Test file. Probably in the future I'll add a single variable polynomial sub-class that supports operations with multivariate polynomials.
It doesn't work with complex numbers, but I may update it in the future

To understand better how to use this package I suggest you to check some of the [examples](https://github.com/Scarlet06/multivariate-polynomial/blob/main/examples):
 - creator.py is used to create some multivariate polynomial with the many aviable ways
 - shower.py is used to print out some of these in a fancy way
 - operator.py is used to apply every standard operator and check that it works well with its _ip counterpart, printing the results in a boring way
 - applicator.py is used to applay every special operation (eg: integrals or partial) and checks the resoults with its _ip counterpart, printing the results in an interesting way

The test file is used to check everything is working as expected