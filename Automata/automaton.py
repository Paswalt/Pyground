# This file is auto generated
from DFA import *
from enum import auto, Enum

class State(Enum):
    Q0 = "q0"
    Q1 = "q1"
    Q2 = "q2"
    QERR = "qerr"

def delta(state, i):
    match state:
        case State.Q0:
            match i:
                case 'a':
                    return State.Q1
                case 'b':
                    return State.Q0
                case 'c':
                    return State.Q0
                case _:
                    return State.QERR
        case State.Q1:
            match i:
                case 'a':
                    return State.Q2
                case 'b':
                    return State.Q1
                case 'c':
                    return State.Q1
                case _:
                    return State.QERR
        case State.Q2:
            match i:
                case 'b':
                    return State.Q1
                case _:
                    return State.QERR
        case State.QERR:
            return State.QERR

aut = DFA(frozenset({'b', 'c', 'a'}), delta, State.Q0, frozenset({State.Q0, State.Q1}))
