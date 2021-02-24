'''
Clasa generica Expression mostenita de fiecare tip de expresie ce poate sa apara in regex
'''
class Expression:
    pass

class Concat(Expression):
    def __init__(self, left: Expression , right: Expression):
        self.left: Expression = left
        self.right: Expression = right

class Union(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left: Expression = left
        self.right: Expression = right

class KleenStar(Expression):
    def __init__(self, exp: Expression):
        self.exp: Expression = exp

class Paranthesis(Expression):
    def __init__(self, exp: Expression):
        self.exp: Expression = exp


class Character(Expression):
    def __init__(self, char: str):
        self.char = char
