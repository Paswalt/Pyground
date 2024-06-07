from parser import parseFile
from validation import * 

def generateAutomata(filename):
    statedefs, alphabet, transitions = parseFile(filename)
    if not (validateStates(statedefs)
            and validateAlphabet(alphabet)
            and validateTransitions(statedefs, alphabet, transitions)):
        print("ABORT")
        return
    is_det = isDeterministic(transitions)
    with open("automaton.py", 'w') as file:
        # Header
        file.write("# This file is auto generated\n")
        # Imports
        file.write("from DFA import *\n")
        file.write("from enum import auto, Enum\n")
        file.write("\n")
        # Generate states
        file.write("class State(Enum):\n")
        i = 0
        start_state = None
        final_states = []
        enum_mapping = dict()
        for sdef in statedefs:
            file.write("    Q" + str(i) + " = " + "\"" + sdef[0] + "\"" +"\n")
            enum_mapping[sdef[0]] = "Q" + str(i)
            if sdef[1]:
                start_state = "Q" + str(i)
            if sdef[2]:
                final_states.append("State.Q" + str(i))
            i += 1
        file.write(4 * " " + "QERR = \"qerr\"")
        file.write("\n")
        file.write("\n")
        # Create DFA or NDFA depending on whether the automaton is deterministic or not
        if is_det:
            # Create the transition function
            file.write("def delta(state, i):\n")
            file.write(4 * " " + "match state:\n")
            file.write(generateDelta(transitions, enum_mapping))
            file.write("\n")
            file.write("\n")
            # Create automata instance
            file.write("aut = DFA(" + str(alphabet) + ", delta, State." + str(start_state) + ", frozenset({")
            if len(final_states) > 0:
                for state in final_states[:len(final_states)-1]:
                    file.write(state + ", ")
                file.write(final_states[-1] + "}))")
            else:
                file.write("}))")
        else:
            print("NON DETERMINISM NOT YET IMPLEMENTED. ABORT")
            
        file.close()

def generateDelta(transitions, enum_mapping):
    cases = ""
    d = dict()
    for trans in transitions:
        source, c, destination = trans
        state = enum_mapping[source]
        if state not in d:
            d[state] = [(c, enum_mapping[destination])]
        else:
            d[state].append((c, enum_mapping[destination]))
    for key in d:
        trans_dests = d[key]
        cases += (8 * " " + "case State." + key + ":\n")
        cases += (12 * " " + "match i:\n")
        for dest in trans_dests:
            cases += (16 * " " + "case " + "'" + dest[0] + "'" + ":\n")
            cases += (20 * " " + "return State." + str(dest[1]) + "\n")
        cases += 16 * " " + "case _:\n"
        cases += 20 * " " + "return State.QERR\n"
    cases += (8 * " " + "case State.QERR:\n")
    cases += (12 * " " + "return State.QERR\n")
    return cases
        
        
    
    
