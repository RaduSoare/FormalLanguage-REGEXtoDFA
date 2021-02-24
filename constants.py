# TOKENS
from expression import Expression

EPS = ""
CONCAT = "+"
UNION = "|"
KLEEN_STAR = "*"
PAR_OPEN = "("
PAR_CLOSE = ")"
LETTERS = [chr(letter) for letter in range(ord('a'), ord('z') + 1)]

# define tipuri de date pentru mai multa claritate
State = int
Transition = (str, str, str)
Symbol = Expression