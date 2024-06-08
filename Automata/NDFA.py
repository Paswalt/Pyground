from typing import Callable, Iterable
from dataclasses import dataclass

@dataclass
class NDFA[Q]:
    E     : set[str]
    delta : Callable[[Q, str], set[Q]]
    q0    : Q
    F     : set[Q]

    def accept(self, inp: Iterable[str]) -> (bool, str):
        current = {self.q0}
        trace = str(current)
        for c in inp:
            nxt = set()
            for state in current:
                nxt = nxt.union(self.delta(state, c))
            trace += " -> " + str(nxt)
            current = nxt
        return (current.intersection(self.F) != set(), trace)
