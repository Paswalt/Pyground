"""
Quick and dirty parser for a made up automaton file format.
The grammar is not 100% well-thouhgt out and formal and should just give an idea.
For a better and easier reference check out the example file. There is absolutely no
error handling, error messages or testing in here :=) if things break too often I will
revamp this file but for now it should serve as a good start for my purposes. No need to
put more time into it.
"""

from dataclasses import dataclass
from typing import Callable

type char = str

@dataclass
class Just[T]:
    match: T

type Maybe[T] = None | Just[T]

# Parser generators
def charParser(c: char):
    def parser(s):
        if s == "":
            return None
        if s[0] == c:
            return Just((c, s[1:]))
        return None
    return parser

def stringParser(word: str):
    parserList = [charParser(c) for c in word]
    def parser(s):
        acc = ("", s)
        for parser in parserList:
            res = parser(acc[1])
            match res:
                case Just((c, r)):
                    acc = (acc[0] + c, r)
                case None:
                    return None
        return Just(acc)
    return parser

"""
*args = sequence of parsers that should all be either-or'd in the order they were given as arguments
"""
def alternativesParser(*args):
    def parser(s):
        res = None
        for parser in args:
            res = parser(s)
            if res is not None:
                break
        return res
    return parser

"""
Repeats a parser AT LEAST ONE time. If there's not a single match, none is returned. If parser p recognizes
language L, repeatParser(p, join) recognizes language L^+ and collects each word into a list.
join = callable that transforms a list of results. If list is wanted, use identity function lambda x: x
"""
def repeatParser(p, join):
    def parser(s):
        acc = p(s)
        if acc is None:
            return None
        res = ([], "")
        while (acc is not None):
            acc = acc.match
            res = (res[0] + [acc[0]], acc[1])
            acc = p(acc[1])
        res = (join(res[0]), res[1])
        return Just(res)
    return parser

"""
Chains all parsers and only returns if all were successful
"""
def chainParser(join, *args):
    def parser(s):
        res = ([], "")
        stream = s
        for parser in args:
            acc = parser(stream)
            if acc is None:
                return None
            acc = acc.match
            res = (res[0] + [acc[0]], acc[1])
            stream = acc[1]
        res = (join(res[0]), res[1])
        return Just(res)
    return parser

def predicateParser(pred):
    def parser(s):
        if s == "":
            return None
        if pred(s[0]):
            return Just((s[0], s[1:]))
        return None
    return parser

# Auxiliary parsers
def emptyParser(s):
    return Just(("", s))

"""
Recognizes ZERO OR MORE whitespaces
"""
def whitespaceParser(s):
    return alternativesParser(repeatParser(charParser(' '), "".join), emptyParser)(s)

"""
Recognizes ONE OR MORE whitespaces
"""
def whitespaceParserPlus(s):
    return repeatParser(charParser(' '), "".join)(s)

# Parse grammar:
#   Automata   ::= [statedef] alphabet [transition]
#   statedef   ::= prefix "state" name endl
#   prefix     ::= ("start"||"") ("final"||"")
#   alphabet   ::= { charseq } endl
#   charseq    ::= char , charseq | char
#   transition ::= name "x" char "->" name endl
#   name       ::= str
#   endl       ::= "\n"     

# 1. Statedef
# 1.1 Prefix (Discontinued)
def prefixParser(s):
    return alternativesParser(stringParser("start"), stringParser("final"), emptyParser)(s)

# 1.2
def nameParser(s):
    return repeatParser(predicateParser(lambda x: str.isalnum(x)), "".join)(s)

# 1.3
def endlParser(s):
    return charParser('\n')(s)

def endlsParser(s):
    return alternativesParser(repeatParser(charParser('\n'), lambda x: x), emptyParser)(s)

def lle(p, m):
    if m is None:
        return None
    m = m.match
    return p(m[1])

def statedefParser(s):
    res = whitespaceParser(s)
    res = lle(alternativesParser(stringParser("start"), emptyParser), res)
    pref_s = bool(res.match[0])
    if pref_s:
        res = lle(whitespaceParserPlus, res)
    res = lle(alternativesParser(stringParser("final"), emptyParser), res)
    pref_f = bool(res.match[0])
    if pref_f:
        res = lle(whitespaceParserPlus, res)
    res = lle(stringParser("state"), res)
    res = lle(whitespaceParserPlus, res)
    res = lle(nameParser, res)
    if res is None:
        return None
    name = res.match[0]
    res = lle(whitespaceParser, res)
    res = lle(alternativesParser(endlParser, emptyParser), res)
    return Just(((name, pref_s, pref_f), res.match[1]))
        
def statedefListParser(s):
    return repeatParser(statedefParser, lambda x: x)(s)

# 2. Alphabet
def charseqParser(s):
    return alternativesParser(charseqRecParser, predicateParser(lambda x: str.isalnum(x)))(s)

def charseqRecParser(s):
    res = predicateParser(lambda x: str.isalnum(x))(s)
    if res is None:
        return None
    c = res.match[0]
    res = lle(whitespaceParser, res)
    res = lle(charParser(','), res)
    if res is None:
        return None
    res = lle(whitespaceParser, res)
    res = lle(charseqParser, res)
    if res is None:
        return None
    return Just((c + res.match[0], res.match[1]))

def alphabetParser(s):
    res = whitespaceParser(s)
    res = lle(charParser('{'), res)
    res = lle(whitespaceParser, res)
    res = lle(charseqParser, res)
    if res is None:
        return None
    seq = res.match[0]
    res = lle(whitespaceParser, res)
    res = lle(charParser('}'), res)
    res = lle(whitespaceParser, res)
    res = lle(alternativesParser(endlParser, emptyParser), res)
    return Just((frozenset(c for c in seq), res.match[1]))

# 3. Transitions
def transitionParser(s):
    res = whitespaceParser(s)
    res = lle(nameParser, res)
    if res is None:
        return None
    source = res.match[0]
    res = lle(whitespaceParserPlus, res)
    res = lle(charParser('x'), res)
    res = lle(whitespaceParserPlus, res)
    res = lle(predicateParser(lambda x: str.isalnum(x)), res)
    if res is None:
        return None
    c = res.match[0]
    res = lle(whitespaceParserPlus, res)
    res = lle(stringParser("->"), res)
    res = lle(whitespaceParserPlus, res)
    res = lle(nameParser, res)
    if res is None:
        return res
    destination = res.match[0]
    res = lle(whitespaceParser, res)
    res = lle(alternativesParser(endlParser, emptyParser), res)
    return Just(((source, c, destination), res.match[1]))

def transitionListParser(s):
    return repeatParser(transitionParser, lambda x: x)(s)

# ---------------------------------Parse a file-------------------------------------
def sanitizeStates(statedefs):
    d = dict()
    res = []
    for sdef in statedefs:
        if sdef[0] not in d:
            d[sdef[0]] = (sdef[1], sdef[2])
        else:
            d[sdef[0]] = (d[sdef[0]][0] or sdef[1], d[sdef[0]][1] or sdef[2])
    for key in d:
        res.append((key,) + d[key])
    return res

def sanitizeTransitions(transitions):
    d = dict()
    res = []
    for trans in transitions:
        if trans not in d:
            d[trans] = True
    for key in d:
        res.append(key)
    return res
        

def parseFile(filename):
    with open(filename, 'r') as file:
        inp = file.read()
        res = endlsParser(inp)
        res = lle(statedefListParser, res)
        if res is None:
            return None
        statedefs = sanitizeStates(res.match[0])
        res = lle(endlsParser, res)
        res = lle(alphabetParser, res)
        if res is None:
            return None
        alphabet = res.match[0]
        res = lle(endlsParser, res)
        res = lle(transitionListParser, res)
        if res is None:
            transitions = []
        else:
            transitions = sanitizeTransitions(res.match[0])
        return (statedefs, alphabet, transitions)
        
    
