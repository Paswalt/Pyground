import argparse
from generator import Generator


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="The name of the file to process")
    parser.add_argument("-g", "--grammar", action="store_true", help="generate grammar from file", default=False)
    parser.add_argument("-a", "--automata", action="store_true", help="generate automata from file", default=True)
    parser.add_argument("-i", "--interactive", action="store_true", help="Run the generated automata in interactive mode", default=False)
    parser.add_argument("-v", "--verbose", action="store_true", help="Prints the trace of acceptance/non-acceptance", default=False)
    args = parser.parse_args()
    generator = Generator(args.filename)
    
    if args.automata:    
        generator.generateAutomata()
        if args.grammar:
            generator.generateGrammar()
        
    if args.interactive:
        from automaton import *
        while(True):
            print("Running " + ("DFA" if generator.isDeterministic else "NDFA")+ " with input alphabet: " + str(aut.E))
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
