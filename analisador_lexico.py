from classes import Token
from constants import *

def print_red(msg): 
    print(f"\033[91m{msg}\033[00m")

def check_identifier(string):
    if len(string) == 1 and string.isalpha():
        return True
    elif string[0].isalpha() and string[1:].isalnum():
        return True
    return False

def pre_process(line):
    line = line.replace('(', ' ( ')
    line = line.replace(')', ' ) ')
    line = line.replace('\n', '')
    line = line.strip()
    line = line.split(' ')
    return line

def run():
    f = open("entrada.vb", "r")
    output = []
    errors = []
    for line in f:
        data = []
        line = pre_process(line)
        for string in line:
            # Lógica do reconhecimento de tokens
            if string == "=":
                data.append(Token(string, "atribuição"))
            elif string in OPERATORS:
                data.append(Token(string, "operador"))
            elif string in DELIMITERS:
                data.append(Token(string, "delimitador"))
            elif string in KEYWORDS:
                data.append(Token(string, string))
            elif check_identifier(string):
                data.append(Token(string, "identificador"))
            else:
                try:
                    int(string)
                    data.append(Token(string, "numero"))
                except:
                    errors.append(string)

        output.append(data)
    for i, line in enumerate(output):
        print(f"Linha {i}: {line}")

    for err in errors:
        print_red(f"Erro: Símbolo {err} não reconhecido")
run()