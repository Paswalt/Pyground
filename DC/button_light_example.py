from dcInterpreter import *
from math import prod

""" Note:
Observables are described by a name and a function called domain.
The domain function fully describes the observables behaviour
that should be analyzed. That is, at any t ∈ R^+_0 it should return
the value of the variables domain it takes on. If the domain has
a real world meaning, e.g. gree/yellow/red light, these can still be encoded into
numbers. See for example: light (below)
"""
button = Obs("Button",
              lambda t: 1 if ((1.0 <= t and t <= 1.5)
                          or (2.0 <= t and t <= 3.0))
                          else 0)

# green = 0, yellow = 1, red = 2
light = Obs("Light",
            lambda t: 1 if 1.25 <= t and t <= 3.25
                        else (2 if 3.25 <= t else 0))


if __name__ == "__main__":
    sa = SEq(light, 0)
    print("Check if light is green at t=0.1")
    print(interpAssertion(sa, 0.1))
    print("Check if light is green at t=3.25")
    print(interpAssertion(sa, 3.25))
    myTerm = Fun([GVar("x"), Integral(SConj(SNeg(SEq(button, 1)), SEq(light, 0)))], prod, "*")
    print("Term to be evaluated")
    print(myTerm)
    print("Evaluation of term under gvar valuation {x -> 5.0} and interval [0,8]")
    print(interpTerm({"x": 5.0}, Interval(0,8), myTerm))
    plotObs([button, light], 0,8)
    
