# This file is auto generated
from NDFA import *
from enum import auto, Enum

class State(Enum):
    Q0 = "q0"
    Q1 = "q1"
    QERR = "qerr"

def delta(state, i):
    match state:
        case State.Q0:
            match i:
                case 'a':
                    return {State.Q0, State.Q1}
                case _:
                    return {State.QERR}
        case State.Q1:
            match i:
                case 'b':
                    return {State.Q0}
                case _:
                    return {State.QERR}
        case State.QERR:
            return {State.QERR}


aut = NDFA({'b', 'a'}, delta, State.Q0, {State.Q1})