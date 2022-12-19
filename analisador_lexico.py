from classes import Token
from constants import *
from utils import print_red


def check_identifier(string):
    if len(string) == 0: return False
    if len(string) == 1 and string.isalpha():
        return True
    elif string[0].isalpha() and string[1:].isalnum():
        return True
    return False

def pre_process(line):
    line = line.replace('(', ' ( ')
    line = line.replace(')', ' )')
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
        if line != ['']:
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
                        try:
                            float(string)
                            data.append(Token(string, "numero flutuante"))
                        except:
                            errors.append(string)

            output.append(data)
    for i, line in enumerate(output):
        print(f"Linha {i+1}: {line}")

    for err in errors:
        print_red(f"Erro: Símbolo {err} não reconhecido")
    
    return output

if __name__ == '__main__':
    run()