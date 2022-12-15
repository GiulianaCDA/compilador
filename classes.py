class Token:
    def __init__(self, value, token_type):
        self.value = value
        self.token = token_type

    def __str__(self):
        return f"{self.value} ({self.token})"

    def __repr__(self):
        return self.__str__()