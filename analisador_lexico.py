# Variáveis globais
output = []
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
reserved = ['defun', 'write-line']

def pre_process(line):
    line = line.replace('(', ' ( ')
    line = line.replace(')', ' ) ')
    line = line.replace('\n', '')
    line = line.strip()
    line = line.split(' ')
    return line

def run():
    f = open("entrada.lisp", "r")
    for line in f:
        data = {}
        line = pre_process(line)
        for string in line:
            if string in reserved:
                data[string] = 'keyword'
            try:
                int(string)
                data[string] = 'number'
            except:
                pass
        output.append(data)
    print(output)

run()