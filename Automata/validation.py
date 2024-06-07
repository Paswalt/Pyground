"""
Wellformedness conditions:
    1. There has to be exactly a SINGLE start state
    2. Source and destination of transitions need to be part of the states
    3. Each symbol in a transition must be part of the alphabet
    4. Determinism check then checking Transitions
"""

def validateStates(statedefs) -> bool:
    if len(statedefs) == 0:
        print("STATES INVALID: THERE MUST BE AT LEAST A SINGLE STATE ⨉")
        return False
    if len(list(filter(lambda t: t[1], statedefs))) != 1:
        print("STATES INVALID: THERE MUST BE EXACTLY ONE STARTING STATE ⨉")
        return False
    print("STATES VALIDATED ✓")
    return True
    

def validateAlphabet(alphabet) -> bool:
    if len(alphabet) == 0:
        print("ALPHABET INVALID: ALPHABET MUST HAVE AT LEAST ONE SYMBOL ⨉")
        return False
    print("ALPHABET VALIDATED ✓")
    return True

def validateTransitions(statedefs, alphabet, transitions) -> bool:
    states = [t[0] for t in statedefs]
    for transition in transitions:
        source, c, destination = transition
        if (source not in states):
            print("TRANSITIONS INVALID: STATE " + source + " NOT PART OF STATES ⨉")
            print("IN TRANSITION: " + str(transition))
            return False
        if (destination not in states):
            print("TRANSITIONS INVALID: STATE " + destination + " NOT PART OF STATES ⨉")
            print("IN TRANSITION: " + str(transition))
            return False
        if c not in alphabet:
            print("TRANSITIONS INVALID: SYMBOL " + c + " NOT PART OF THE ALPHABET ⨉")
            return False
    print("TRANSITIONS VALIDATED ✓")
    return True

def isDeterministic(transitions) -> bool:
    d = dict()
    for tup in transitions:
        source = tup[0]
        c = tup[1]
        if (source, c) not in d:
            d[(source, c)] = 1
        else:
            return False
    return True
