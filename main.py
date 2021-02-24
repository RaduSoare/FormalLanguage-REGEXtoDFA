import sys
from pda import PDA
from constants import *
from nfa import NFA
from nfa2dfa import *


def insert (source_str, insert_str, pos):
    return source_str[:pos]+insert_str+source_str[pos:]

# insereaza "+" in regex pentru a recunoaste operatia de concatenare
def precompute_regex(regex):
    # adauga "." pentru a stii cand s-a terminat sirul
    regex += "."
    i = 0
    while regex[i] != ".":
        if regex[i] in LETTERS and regex[i+1] in LETTERS or \
                regex[i] == PAR_CLOSE and regex[i+1] == PAR_OPEN or\
                regex[i] in LETTERS and regex[i+1] == PAR_OPEN or \
                regex[i] == PAR_CLOSE and regex[i+1] in LETTERS or \
                regex[i] == KLEEN_STAR and regex[i + 1] == PAR_OPEN or \
                regex[i] == KLEEN_STAR and regex[i+1] in LETTERS:
            regex = insert(regex, CONCAT, i+1)
        i += 1

    return regex[:-1]

# citire expresie regulata din fisier
def read_input(input_path):
    input_file = open(input_path, "r")
    regex = input_file.readline()
    input_file.close()
    return regex


if __name__ == '__main__':
    input_path = sys.argv[1]
    output_path_nfa = sys.argv[2]
    output_path_dfa = sys.argv[3]

    # add concatenation symbol into the regex
    regex = precompute_regex(read_input(input_path))

    pda = PDA()
    nfa = NFA()

    # Construieste arborele de parsare
    parse_tree = pda.parseExpression(regex)

    # Adauga root-ul arboerlui de parsare in NFA
    nfa.transitions[0, parse_tree] = 1
    # Creeaza NFA
    nfa.create_NFA(0)

    # Scrie in fisier NFA-ul
    nfa.write_output(output_path_nfa)

    # Foloseste codul din tema2 pentru a transforma NFA-ul obtinut din regex in DFA
    #convert_to_dfa(output_path_nfa, output_path_dfa)
