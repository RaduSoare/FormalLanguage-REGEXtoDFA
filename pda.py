'''
 Automatul Push-Down cu ajutorul caruia o sa fie parsat regexul
'''
from typing import List, Dict, Tuple
from stack import Stack
from expression import *
from constants import *

class PDA:
    def __init__(self):
        self.states : List[State] = [0, 1, 2]
        self.initialState = 0
        self.finalStates: List[State] = [1, 2]

        # Tranzitiile automatului ce accepta o expresie regulata
        self.transitions: Dict[Tuple[State, Transition], State] = {}
        self.transitions[0, (PAR_OPEN, EPS, PAR_OPEN)] = 0
        for letter in LETTERS:
            self.transitions[0, (letter, EPS, letter)] = 1
        self.transitions[1, (CONCAT, EPS, CONCAT)] = 0
        self.transitions[1, (UNION, EPS, UNION)] = 0
        self.transitions[1, (KLEEN_STAR, EPS, KLEEN_STAR)] = 2
        self.transitions[1, (PAR_CLOSE, EPS, PAR_CLOSE)] = 1
        self.transitions[2, (KLEEN_STAR, EPS, KLEEN_STAR)] = 2
        self.transitions[2, (PAR_CLOSE, EPS, PAR_CLOSE)] = 1
        self.transitions[2, (CONCAT, EPS, CONCAT)] = 0
        self.transitions[2, (UNION, EPS, UNION)] = 0
        self.transitions[2, (PAR_OPEN, EPS, PAR_OPEN)] = 0

        # Stiva automatului
        self.stack : Stack = Stack()

    # Adauga caracterul curent in stiva si returneaza starea urmatoare
    def nextState(self, current_state, word):
        current_transition = (word[0], EPS, word[0])
        if (current_state, current_transition) in self.transitions:
            self.stack.push(word[0])
            return self.transitions[(current_state, current_transition)]

        return None


    def computeCharacter(self):
        # extract the character
        char = self.stack.pop()
        self.stack.push(Character(char))

    def computeUnion(self):
        # extract expression 1
        exp2 = self.stack.pop()
        # eliminate "|"
        self.stack.pop()
        # extract expression 2
        exp1 = self.stack.pop()

        self.stack.push(Union(exp1, exp2))


    def computeConcat(self):
        # extract expression 1
        exp2 = self.stack.pop()
        # eliminate "+"
        self.stack.pop()
        # extract expression 2
        exp1 = self.stack.pop()

        # Asigur faptul ca o Concatenare se intampla mereu inaintea unei reuniuni
        if isinstance(exp2, Union):
            self.stack.push(Union(Concat(exp1, exp2.left), exp2.right))
        elif isinstance(exp2, Concat):
            self.stack.push(Concat(Concat(exp1, exp2.left), exp2.right))
        else:
            self.stack.push(Concat(exp1, exp2))


    def computeKleenStar(self):
        # eliminate star
        self.stack.pop()
        # extract last expression
        last_exp = self.stack.pop()

        # reduc cazurile de Kleen Star dublat la un singur Kleen Star
        if isinstance(last_exp, KleenStar):
            self.stack.push(last_exp)
        else:
            self.stack.push(KleenStar(last_exp))


    def computeParanthesis(self):
        # eliminate close par
        self.stack.pop()
        # extract expression
        exp = self.stack.pop()
        # eliminate open par
        self.stack.pop()
        self.stack.push(Paranthesis(exp))

    def computeAlphabet(self):
        if self.stack.peek(0) in LETTERS:
            self.computeCharacter()
            return True

        return False

    def expandExpression(self, index):
        # verific daca in varful stivei am un kleen_star urmat de o expresie
        if self.stack.peek(0) == KLEEN_STAR and isinstance(self.stack.peek(1), Expression):
            self.computeKleenStar()
            return True
        # verific daca in varful stivei am o expresie intre paranteze
        if self.stack.peek(index) == PAR_CLOSE and isinstance(self.stack.peek(index + 1), Expression) and self.stack.peek(index+2) == PAR_OPEN:
            self.computeParanthesis()
            return True
        # verific daca in varful stive am 2 expresii in jurul unei concatenari
        if isinstance(self.stack.peek(index), Expression) and self.stack.peek(index + 1) == CONCAT and isinstance(self.stack.peek(index + 2), Expression):
            self.computeConcat()
            return True
        # verific daca in varful stive am 2 expresii in jurul unei reuniuni
        if isinstance(self.stack.peek(index), Expression) and self.stack.peek(index + 1) == UNION and isinstance(self.stack.peek(index + 2), Expression):
            self.computeUnion()
            return True

        return False


    def expand(self):
        index = 0
        # creez o stiva temporara
        to_be_added: Stack = Stack()
        # cat timp in lista exista mai mult de o expresie (ROOT)
        while self.stack.size() != 1:
            # daca elementul curent nu a fost expandat, este adaugat la stiva temporara
            if self.expandExpression(index) == False:
                to_be_added.push(self.stack.pop())
            else:
                # daca elementul a fost expandat, i se adauga la final elementele peste care s-a trecut fara expandare
                # stiva_temporara -> lista -> stiva principala - pentru a pastra ordinea
                temp_stack = []
                while not to_be_added.isEmpty():
                    temp_stack.append(to_be_added.pop())
                while len(temp_stack) != 0:
                    self.stack.push(temp_stack.pop(0))



    def parseExpression(self, regex: str):
        currentState = self.initialState
        while regex != EPS:
            currentState = self.nextState(currentState, regex)
            if currentState is None:
                break
            regex = regex[1:]

            # Odata cu iterarea prin regex, se transforma literele din alfabet in obiecte Character
            self.computeAlphabet()

        # Expandeaza elementele din stiva pana cand se ajunge la root
        self.expand()

        ## Daca regexul nu s-a consumat sau in stiva nu a ramas decat root-ul arborelui
        # inseamna ca nu am putut parsa expresia
        if regex != EPS or self.stack.size() != 1:
            return None

        # Returneaza root-ul arborelui de parsare
        return self.stack.pop()