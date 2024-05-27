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
    domain: Callable[float, T]
    def __str__(self):
        return self.name

myObsBool = Obs("X",
                lambda t: 1 if 2 <= t and t <= 5 else 0)
myObsBool2 = Obs("Y",
                 lambda t: 1 if 3.5 <= t and t <= 5 else 0)

def interpObs[T](obs: Obs[T], t: float) -> T:
    return obs.domain(t)

# State assertions
type Assertion = None # Placeholder for early definition for SNeg/SConj

@dataclass
class STrue:
    def __str__(self):
        return "True"

@dataclass
class SFalse:
    def __str__(self):
        return "False"

@dataclass
class SEq[T]:
    obs: Obs[T]
    d: T
    def __str__(self):
        return str(self.obs) + " = " + str(self.d)

@dataclass
class SNeg:
    sa: Assertion
    def __str__(self):
        return "¬" + "(" + str(self.sa) + ")"

@dataclass
class SConj:
    left: Assertion
    right: Assertion
    def __str__(self):
        return "(" + str(self.left) + " ∧ " + str(self.right) + ")"

type Assertion = STrue | SFalse | SEq | SNeg | SConj

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
    def __str__(self):
        return "l"

@dataclass
class GVar:
    name: str
    def __str__(self):
        return self.name

@dataclass
class Integral:
    sa: Assertion
    def __str__(self):
        return "∫" + str(self.sa)

@dataclass
class Fun:
    terms: list[Term]
    f: Callable[list[float], float]
    name: str = ""
    def __str__(self):
        if len(self.terms) == 0:
            return self.name
        return ("f_lam" if self.name == "" else self.name) + "(" + ", ".join([str(term) for term in self.terms]) + ")"

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
        case Fun(terms, f, name):
            return f(list(map(lambda t: interpTerm(v, intv, t), terms)))


# Auxiliary functions
def decomposeTerm(term: Term) -> list[Assertion]:
    match term:
        case Length():
            return []
        case GVar(name):
            return []
        case Integral(sa):
            return [sa]
        case Fun(terms, f):
            res = []
            for t in terms:
                res += decomposeTerm(t)
            return res
        
def decomposeAssertion(sa: Assertion) -> list[Obs]:
    match sa:
        case STrue():
            return lst
        case SFalse():
            return lst
        case SEq(obs, d):
            return [obs]
        case SNeg(sa):
            return decomposeAssertion(sa)
        case SConj(left, right):
            lst_right = decomposeAssertion(right)
            return lst_right + list(filter(lambda o: o.name not in [ob.name for ob in lst_right], decomposeAssertion(left)))
    
"""
Plots time diagrams for a term. Finite domains that are not integers can still
be mapped to them, (e.g. kinda as if using enums).
    Args:
        obs       : List of Observables
        start     : Start of the interval to be plotted
        end       : End of the interval to be plotted
        precision : How many points to consider between end and start
"""
def plotTerm(term: Term, start: float, end: float, precision=1000):
    x_values = np.linspace(start, end, precision)
    colors = ['black', 'blue', 'green', 'red', 'orange']
    assertions = decomposeTerm(term)
    observables = []
    for sa in assertions:
        observables += decomposeAssertion(sa)
    num_plots = len(observables) + len(assertions)
    # Create plot for each observable
    fig, axs = plt.subplots(num_plots, 1, sharex=True, figsize=(10,10))
    if (num_plots == 1):
        axs = [axs]
    for i, ob in enumerate(observables):
        y_values = [interpObs(ob, t) for t in x_values]
        axs[i].step(x_values, y_values, label=ob.name, color=colors[i%5])
        axs[i].set_ylabel(ob.name)
        axs[i].grid(True)
    # Create plot for each state assertion
    for i, sa in enumerate(assertions, len(observables)):
        y_values = [interpAssertion(sa, t) for t in x_values]
        axs[i].step(x_values, y_values, label=str(sa), color=colors[i%5])
        axs[i].grid(True)
    # Plot configuration
    axs[-1].set_xlabel('t')
    plt.xticks(np.arange(min(x_values), max(x_values)+1,1))
    plt.tight_layout()
    plt.legend()
    plt.show()

# Formulas
type Formula = None # Placeholder for early definition for FNeg/FConj[...]

@dataclass
class FAtom:
    terms: list[Term]
    p: Callable[list[float], bool]
    name: str = ""
    def __str__(self):
        return (" " + self.name + " ").join([str(term) for term in self.terms])

@dataclass
class FNeg:
    form: Formula
    def __str__(self):
        return "¬" + "(" + str(self.sa) + ")"

@dataclass
class FConj:
    left : Formula
    right: Formula
    def __str__(self):
        return "(" + str(self.left) + " ∧ " + str(self.right) + ")"

""" Due to the nature of quantification over the reals,
    the following are not easily representable using their
    standard semantics:
    
@dataclass
class FForall:
    bind: GVar
    form: Formula

@dataclass
class FChop:
    left : Formula
    right: Formula

Here, smarter semantics or approximations would need to be applied
"""
     
type Formula = FAtom | FNeg | FConj

def interpFormula(v: Valuation, intv: Interval, form: Formula) -> bool:
    match form:
        case FAtom(terms, p, name):
            return p(list(map(lambda term: interpTerm(v, intv, term), terms)))
        case FNeg(f):
            return not interpFormula(v, intv, f)
        case FConj(left, right):
            return interpFormula(v, intv, left) and interpFormula(v, intv, right)
