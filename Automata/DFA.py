from typing import Callable, Iterable
from dataclasses import dataclass

@dataclass
class DFA[Q]:
    E     : frozenset[str]
    delta : Callable[[Q, str], Q]
    q0    : Q
    F     : frozenset[Q]

    def accept(self, inp: Iterable[str]) -> (bool, str):
        current = self.q0
        trace = str(self.q0)
        for c in inp:
            current = self.delta(current, c)
            trace += " -> " + str(current)
        return (current in self.F, trace)
