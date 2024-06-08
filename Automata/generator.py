from parser import parseFile
from validation import * 

class Generator:
    def __init__(self, filename):
        self.statedefs, self.alphabet, self.transitions = parseFile(filename)
        self.states = [sdef[0] for sdef in self.statedefs]
        self.start_state = None
        self.final_states = []
        self.isDeterministic = None

    def generateAutomata(self):
        if not (validateStates(self.statedefs)
                and validateAlphabet(self.alphabet)
                and validateTransitions(self.statedefs, self.alphabet, self.transitions)):
            print("ABORT")
            return
        self.isDeterministic = isDeterministic(self.transitions)
        if self.isDeterministic:
            self.generateDFA()
        else:
            self.generateNDFA()


    def generateDFA(self):
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
            final_states = []
            # Mapping from state names to enum names
            enum_mapping = dict()
            start_state = None
            for sdef in self.statedefs:
                file.write(4 * " " + "Q" + str(i) + " = " + "\"" + sdef[0] + "\"" +"\n")
                enum_mapping[sdef[0]] = "Q" + str(i)
                if sdef[1]:
                    start_state = "Q" + str(i)
                    self.start_state = sdef[0]
                if sdef[2]:
                    final_states.append("State.Q" + str(i))
                    self.final_states.append(sdef[0])
                i += 1
            file.write(4 * " " + "QERR = \"qerr\"")
            file.write("\n")
            file.write("\n")
            # Create the transition function
            file.write("def delta(state, i):\n")
            file.write(4 * " " + "match state:\n")
            file.write(self.generateDetDelta(enum_mapping))
            file.write("\n")
            file.write("\n")
            # Create automata instance
            file.write("aut = DFA(" + str(self.alphabet) + ", delta, State." + str(start_state) + ", {")
            if len(final_states) > 0:
                for state in final_states[:len(final_states)-1]:
                    file.write(state + ", ")
                file.write(final_states[-1] + "})")
            else:
                file.write("}))")
            file.close()

    def generateDetDelta(self, enum_mapping):
        cases = ""
        d = dict()
        # Capture enum transitions
        for trans in self.transitions:
            source, c, destination = trans
            state = enum_mapping[source]
            if state not in d:
                d[state] = [(c, enum_mapping[destination])]
            else:
                d[state].append((c, enum_mapping[destination]))
        # Key is an enum name
        for key in d:
            trans_dests = d[key] # List of (symbol, enum_destination)
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


    def generateNDFA(self):
        with open("automaton.py", 'w') as file:
            # Header
            file.write("# This file is auto generated\n")
            # Imports
            file.write("from NDFA import *\n")
            file.write("from enum import auto, Enum\n")
            file.write("\n")
            # Generate states
            file.write("class State(Enum):\n")
            i = 0
            final_states = []
            # Mapping from state names to enum names
            enum_mapping = dict()
            start_state = None
            for sdef in self.statedefs:
                file.write(4 * " " + "Q" + str(i) + " = " + "\"" + sdef[0] + "\"" +"\n")
                enum_mapping[sdef[0]] = "Q" + str(i)
                if sdef[1]:
                    start_state = "Q" + str(i)
                    self.start_state = sdef[0]
                if sdef[2]:
                    final_states.append("State.Q" + str(i))
                    self.final_states.append(sdef[0])
                i += 1
            file.write(4 * " " + "QERR = \"qerr\"")
            file.write("\n")
            file.write("\n")
            # Create the transition function
            file.write("def delta(state, i):\n")
            file.write(4 * " " + "match state:\n")
            file.write(self.generateNonDetDelta(enum_mapping))
            file.write("\n")
            file.write("\n")
            # Create automata instance
            file.write("aut = NDFA(" + str(self.alphabet) + ", delta, State." + str(start_state) + ", {")
            if len(final_states) > 0:
                for state in final_states[:len(final_states)-1]:
                    file.write(state + ", ")
                file.write(final_states[-1] + "})")
            else:
                file.write("}))")
            file.close()

    def generateNonDetDelta(self, enum_mapping):
        cases = ""
        d = dict()
        # Capture enum transitions
        for trans in self.transitions:
            source, c, destination = trans
            state = enum_mapping[source]
            if state not in d:
                d[state] = {c: [enum_mapping[destination]]}
            else:
                if c not in d[state]:
                    d[state][c] = [enum_mapping[destination]]
                else:
                    d[state][c].append(enum_mapping[destination])
        # Key is an enum name
        for key in d:
            symDict = d[key]
            cases += (8 * " " + "case State." + key + ":\n")
            cases += (12 * " " + "match i:\n")
            for sym in symDict:
                cases += (16 * " " + "case " + "'" + sym + "'" + ":\n")
                cases += (20 * " " + "return {" + ", ".join(["State." + dest for dest in symDict[sym]]) + "}" + "\n")        
            cases += 16 * " " + "case _:\n"
            cases += 20 * " " + "return {State.QERR}\n"
        cases += (8 * " " + "case State.QERR:\n")
        cases += (12 * " " + "return {State.QERR}\n")
        return cases

    def generateGrammar(self):
        d = dict()
        for trans in self.transitions:
            if trans[0] not in d:
                d[trans[0]] = [(trans[1], trans[2])]
            else:
                d[trans[0]].append((trans[1], trans[2]))
        with open("grammar.txt", 'w') as file:
            file.write("Startsymbol: " + self.start_state + "\n")
            for k in d:
                file.write(k + " -> ")
                productions = []
                for trans in d[k]:
                    productions.append(trans[0] + trans[1])
                    if trans[1] in self.final_states:
                        productions.append(trans[0])
                file.write(" | ".join(productions) + "\n")
            file.write("\n")
            file.close()
                    
            
            
        
    
    
