from uuid import uuid4
class Token:
    def __init__(self, value, token_type):
        self.value = value
        self.type = token_type

    def __str__(self):
        return f"{self.value} ({self.type})"

    def __repr__(self):
        return self.__str__()

class TokenList:
    def __init__(self, tokens):
        self.line = 0
        self.index = 0
        self.matrix = tokens
        
    def nextToken(self):
        if self.line >= len(self.matrix):
            return Token(None, None)
        
        if self.index == len(self.matrix[self.line]):
            self.index = 0
            self.line += 1
        
        if self.line >= len(self.matrix):
            return Token(None, None)

        self.index += 1
        return self.matrix[self.line][self.index-1]

    def copy(self):
        copied = TokenList(self.matrix)
        copied.line = self.line
        copied.index = self.index
        return copied

    def peekToken(self, n=1):
        token_list_copy = self.copy()
        for i in range(n):
            token = token_list_copy.nextToken()
        return token

class Tree:
    def __init__(self):
        self.root = None

class Node:
    def __init__(self, parent, token):
        self.id = str(uuid4())
        self.parent = parent
        self.value = token.value
        self.type = token.type
        self.children = []
    
    def add(self, token):
        self.children.append(Node(self, token))
        return self.children[-1]
    
    def __str__(self):
        string = f"{self.value} ({self.type})\nFilhos: "
        for n in self.children:
            string += f"{n.value} "
        return string
        
    def __repr__(self):
        return self.__str__()
