import argparse
from generator import generateAutomata


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="The name of the file to process")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-g", "--generate", action="store_true", help="generate automata from file", default=True)
    group.add_argument("-a", "--automata", action="store_true", help="choose an already existing automata from file (not yet supported)", default=False)
    parser.add_argument("-i", "--interactive", action="store_true", help="Run the generated automata in interactive mode")
    parser.add_argument("-v", "--verbose", action="store_true", help="Prints the trace of acceptance/non-acceptance", default=False)
    args = parser.parse_args()
    
    if args.generate:    
        generateAutomata(args.filename)
        
    if args.interactive:
        from automaton import *
        while(True):
            print("Running DFA with input alphabet: " + str(aut.E))
            word = input("Enter word: ").lower()
            for c in word:
                if c not in aut.E:
                    print("")
                    print(" ------------------------------------ ")
                    print("|                                    |")
                    print("| Symbol " + c + " not part of the alphabet! |")
                    print("|                                    |")
                    print(" ------------------------------------ ")
                    print("")
                    break
            else:
                isAccepted, trace = aut.accept(word)
                if (isAccepted):
                    print("")
                    print(" ----------------- ")
                    print("|                 |")
                    print("|  Word Accepted  |")
                    print("|                 |")
                    print(" ----------------- ")
                    if (args.verbose):
                        print("Trace: " + trace)
                    print("")

                else:
                    print("")
                    print(" --------------------- ")
                    print("|                     |")
                    print("|  Word Not Accepted  |")
                    print("|                     |")
                    print(" --------------------- ")
                    if (args.verbose):
                        print("Countertrace: " + trace)
                    print("")
