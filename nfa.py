'''
Clasa NFA ce modeleaza propritatile unui astfel de automat
'''
from typing import List, Dict, Tuple
from expression import *
from constants import *

class NFA:
    def __init__(self):
        self.states: List[State] = [0, 1]
        self.initialState = 0
        self.finalStates: List[State] = [1]
        self.transitions: Dict[Tuple[State, Symbol], List[State]] = {}
        self.nextStateCode = 2

    # scrie intr-un fisier datele NFA-ului
    def write_output(self, output_path):
        output_file = open(output_path, "w+", newline='\n')
        output_file.write(str(len(self.states)) + "\n")
        output_file.write(str(self.finalStates[0]) + "\n")

        # aseaza intr-un mod mai compact scrierea NFA-ului
        final_nfa = {}
        for key, value in self.transitions.items():
            if isinstance(key[1], Character):
                symbol = "eps"
            else:
                symbol = key[1]
            if (key[0], symbol) in final_nfa:
                final_nfa[(key[0], symbol)].append(value)
            else:
                final_nfa[(key[0], symbol)] = [value]

        # scrie in fisier varianta finala de NFA
        for key, value in final_nfa.items():
            output_file.write(str(key[0]) + " " + key[1] )
            for state in value:
                output_file.write(" " + str(state))
            output_file.write("\n")

        output_file.close()

    '''
     Itereaza intr-un loop tranzitiile NFA-ului si le expandeaza in functie de tipul de expresie
     Initial primeste o singura tranzitie ce reprezinta root-ul arborelui de parsare
     Iteratia se opreste cand nu mai exista tranzitii diferite de EPS
    '''
    def create_NFA(self, current_state : State):

        while True:
            flag = False
            for key, value in self.transitions.copy().items():
                if isinstance(key[1], Paranthesis):
                    # sterge tranzitia veche
                    del self.transitions[key]
                    # adauga tranzitia updatata
                    self.transitions[key[0], key[1].exp] = value
                    flag = True
                if isinstance(key[1], Concat):
                    del self.transitions[key]
                    self.transitions[key[0], key[1].left] = self.nextStateCode
                    self.transitions[self.nextStateCode, key[1].right] = value
                    self.states.append(self.nextStateCode)
                    self.nextStateCode += 1
                    flag = True
                if isinstance(key[1], Union):
                    del self.transitions[key]
                    self.transitions[key[0], Character(EPS)] = self.nextStateCode
                    self.transitions[self.nextStateCode, key[1].left] = self.nextStateCode + 1
                    self.transitions[self.nextStateCode + 1, Character(EPS)] = value

                    self.transitions[key[0], Character(EPS)] = self.nextStateCode + 2
                    self.transitions[self.nextStateCode + 2, key[1].right] = self.nextStateCode + 3
                    self.transitions[self.nextStateCode + 3, Character(EPS)] = value

                    for i in range(self.nextStateCode, self.nextStateCode + 4):
                        self.states.append(i)
                    self.nextStateCode += 4
                    flag = True
                if isinstance(key[1], KleenStar):
                    del self.transitions[key]
                    self.transitions[key[0], Character(EPS)] = self.nextStateCode
                    self.transitions[self.nextStateCode, key[1].exp] = self.nextStateCode + 1
                    self.transitions[self.nextStateCode + 1, Character(EPS)] = self.nextStateCode
                    self.transitions[self.nextStateCode + 1, Character(EPS)] = value

                    self.transitions[key[0], Character(EPS)] = value
                    for i in range(self.nextStateCode, self.nextStateCode + 2):
                        self.states.append(i)
                    self.nextStateCode += 2
                    flag = True
                if isinstance(key[1], Character):
                    if key[1].char != EPS:
                        self.transitions[key[0], key[1].char] = value
                        del self.transitions[key]
                        flag = True
            # daca intr-o iteratie nu s-a gasit nicio tranzitie diferita de EPS, se iese din loop
            if flag is False:
                break