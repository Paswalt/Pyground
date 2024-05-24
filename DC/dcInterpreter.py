from dataclasses import dataclass
from typing import Callable
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

# Intervals
class Interval:
    def __init__(self, start: float, end: float):
        assert start <= end
        self.start = start
        self.end = end

    def __repr__(self):
        return "[" + str(self.start) + ", " + str(self.end) + "]"
        
    def length(self) -> float:
        return self.end - self.start

# Observables
@dataclass
class Obs[T]:
    name: str
    domain: Callable[Interval, T]

myObsBool = Obs("X",
                lambda i: 1 if 2 <= i.start and i.end <= 5 else 0)
myObsBool2 = Obs("Y",
                 lambda i: 1 if 3.5 <= i.start and i.end <= 5 else 0)

def interpObs[T](obs: Obs[T], t: float) -> T:
    return obs.domain(Interval(t,t))

# State assertions
type Assertion = None # Placeholder for early definition for SNeg/SConj

@dataclass
class STrue:
    pass

@dataclass
class SFalse:
    pass

@dataclass
class SEq[T]:
    obs: Obs[T]
    d: T

@dataclass
class SNeg:
    sa: Assertion

@dataclass
class SConj:
    left: Assertion
    right: Assertion

type Assertion = STrue | SFalse | Seq | SNeg | SConj

def interpAssertion(sa: Assertion, t: float) -> bool:
    match sa:
        case STrue():
            return True
        case SFalse():
            return False
        case SEq(obs, d):
            return interpObs(obs, t) == d
        case SNeg(sa1):
            return not interpAssertion(sa1, t)
        case SConj(sa1, sa2):
            return interpAssertion(sa1, t) and interpAssertion(sa2, t)

# Terms
type Term = None

@dataclass
class Length:
    pass

@dataclass
class GVar:
    name: str

@dataclass
class Integral:
    sa: Assertion

@dataclass
class Fun:
    terms: list[Term]
    f: Callable[list[float], float]

type Term = Length | GVar | Integral | Fun
type Valuation = dict[str, float]

def interpTerm(v: Valuation, intv: Interval, term: Term) -> float:
    match term:
        case Length():
            return intv.length()
        case GVar(name):
            return v[name]
        case Integral(sa):
            return round(integrate.quad(lambda x: interpAssertion(sa, x), intv.start, intv.end)[0], 2)
        case Fun(terms, f):
            return f(list(map(lambda t: interpTerm(v, intv, t), terms)))


# Auxiliary functions
colors = ['black', 'blue', 'green', 'red', 'orange']
def plotObs(obs: list[Obs], start: float, end: float, precision=1000: int):
    fig, axs = plt.subplots(len(obs), 1, sharex=True, figsize=(10,10))
    if (len(obs) == 1):
        axs = [axs]
    x_values = np.linspace(start, end, precision)
    for i, ob in enumerate(obs):
        y_values = [interpObs(ob, i) for i in x_values]
        axs[i].step(x_values, y_values, label=ob.name, color=colors[i%5])
        axs[i].set_ylabel(ob.name)
        axs[i].grid(True)
    axs[-1].set_xlabel('t')
    for ax in axs:
        ax.xaxis.set_minor_locator(ticker.FixedLocator(np.arange(0.5, max(x_values), 1)))
        ax.tick_params(which='minor', length=4)
    plt.xticks(np.arange(min(x_values), max(x_values)+1,1))
    plt.tight_layout()
    plt.show()


# Main
if __name__ == "__main__":
    pass
    #print(interpTerm({}, Interval(0,10) ,Integral(SConj(SEq(myObsBool, 1), SEq(myObsBool2, 1)))))
    #plotObs([myObsBool], 0, 10)
