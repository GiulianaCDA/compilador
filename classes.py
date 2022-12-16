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

    def peekToken(self):
        token_list_copy = self.copy()
        return token_list_copy.nextToken()