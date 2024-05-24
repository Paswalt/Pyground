from dcInterpreter import *
from math import prod

button = Obs("Button",
                        lambda i: 1 if ((1.0 <= i.start and i.end <= 1.5)
                                     or (2.0 <= i.start and i.end <= 3.0))
                                     else 0)

# green = 0, yellow = 1, red = 2
light = Obs("Light",
                lambda i: 1 if 1.25 <= i.start and i.end <= 3.25 else (2 if 3.25 <= i.start else 0))





if __name__ == "__main__":
    sa = SEq(light, 0)
    print(interpAssertion(sa, 0.1))
    print(interpAssertion(sa, 3.25))
    print(interpTerm({"x": 5.0}, Interval(0,8), Fun([GVar("x"), Integral(SConj(SNeg(SEq(button, 1)), SEq(light, 0)))], prod)))
    plotObs([button, light], 0,8)
    
