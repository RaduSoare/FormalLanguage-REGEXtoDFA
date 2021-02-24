'''
Clasa Stack folosita de automatul Push-Down folosit la parsarea regex-ului
'''
class Stack:
    def __init__(self):
        self.stack = []

    def push(self, elem):
        self.stack.append(elem)

    def peek(self, pos):
        if pos < len(self.stack):
            return self.stack[-(pos + 1)]
        return None

    def pop(self):
        return self.stack.pop()

    def isEmpty(self):
        return self.stack == []

    def size(self):
        return len(self.stack)