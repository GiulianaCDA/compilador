from classes import Node, TokenList
from utils import print_red, print_table
from analisador_lexico import pre_process

def run(sintatic_tree, symbol_table, tokens):
    if float_incompatibility(sintatic_tree, symbol_table):
        return False
    assignments(sintatic_tree.root, symbol_table)
    loops(sintatic_tree, symbol_table)
    recursion(sintatic_tree, symbol_table, tokens)
    return True


def get_term(node: Node, symbol_table):
    if len(node.children) == 1:
        fator = node.children[0]
        if fator.children[0].type == "id":
            s = fator.children[0].children[0].value
            for symbol in symbol_table:
                if s == symbol[0]:
                    return symbol[2]
        return fator.children[0].children[0].value
    else:
        t1 = float(node.children[0].children[0].children[0].value)
        t2 = float(node.children[2].children[0].children[0].value)
        op = node.children[1].children[0].value
        return make_operation(t1, op, t2)

def make_operation(t1, op, t2):
    if op == '+':
        return t1 + t2
    elif op == '-':
        return t1 - t2
    elif op == '*':
        return t1 * t2
    elif op == '/':
        return t1 / t2

def evaluate_condition(a, op, b):
    if op == "<":
        return a < b
    if op == ">":
        return a > b
    if op == "<=":
        return a <= b
    if op == ">=":
        return a >= b
    if op == "==":
        return a == b

def calculate_expression(node: Node, symbol_table):
    if len(node.children) == 1:
        return get_term(node.children[0], symbol_table)
    elif len(node.children) == 3:
        t1 = float(get_term(node.children[0], symbol_table))
        t2 = float(get_term(node.children[2], symbol_table))
        op = node.children[1].children[0].value
        return make_operation(t1, op, t2)


def select_type(tokens):
    type_token = tokens.peekToken(2)
    if type_token.type == "INT":
        return "inteira"
    else:
        return "flutuante"

def analyse_id(token, var_type, origin, tokens, identifiers, symbol_table, semantic_errors):

    if origin == "declaration" and token.value not in identifiers:
        identifiers.append(token.value)
        if var_type == "numero":
            var_type = "Variável " + select_type(tokens)
        symbol_table.append(
            [token.value, var_type, 0, "Global", 0]
        )
    
    elif origin == "declaration" and token.value in identifiers:
        semantic_errors.append(f"Redeclaração de {token.value} detectada!")
    
    elif origin == "param":
        identifiers.append(token.value)
        var_type = "Parâmetro " + select_type(tokens)
        symbol_table.append(
            [token.value, var_type, 0, "Local", 0]
        )
    elif origin == "param" and token.value in identifiers:
        semantic_errors.append(f"Já existe um parâmetro com esse nome! {token.value}")

    elif origin == "use" and token.value not in identifiers:
        semantic_errors.append(f"A variável {token.value} não foi declarada")

    elif origin == "for" and token.value not in identifiers:
        identifiers.append(token.value)
        symbol_table.append(
            [token.value, var_type, 0, "Local", 0]
        )

    return identifiers, symbol_table, semantic_errors

def float_incompatibility(tree, symbol_table):
    
    def function(node: Node):
        id_var = node.children[0].children[0].value
        for symbol in symbol_table:
            if id_var == symbol[0]:
                if 'flutuante' in symbol[1]:
                    return False
        
        exp = node.children[2]
        for n in exp.children:
            if n.type == "termo":
                fator = n.children[0]
                if fator.type == "id":
                    for symbol in symbol_table:
                        if fator.type == symbol[0]:
                            if '.' in fator.value:
                                print_red(f"Erro: Incompatibilidade float na variável {id_var}")
                                print_red("\n----FIM DA COMPILAÇÃO DEVIDO A ERRO SEMÂNTICO!----")
                                exit()
                if fator.children[0].children[0].type == "numero flutuante":
                    print_red(f"Erro: Incompatibilidade float na variável {id_var}")
                    print_red("\n----FIM DA COMPILAÇÃO DEVIDO A ERRO SEMÂNTICO!----")
                    exit()
    
    dfs(tree.root, [], "let", function)

def assignments(node, symbol_table):
    def function(node: Node):
        id_var = node.children[0].children[0].value
        
        exp = node.children[2]
        value = calculate_expression(exp, symbol_table)
        
        for symbol in symbol_table:
            if id_var == symbol[0]:
                if 'inteira' in symbol[1]:
                    symbol[2] = int(value)
                else:
                    symbol[2] = value
                print_table(symbol_table)
    
    dfs(node, [], "let", function)

def loops(tree, symbol_table):
    def function(node: Node):
        id_var = node.children[0].children[0].value
        initial_value = int(calculate_expression(node.children[2], symbol_table))
        final_value = int(calculate_expression(node.children[4], symbol_table)) 
        

        for i in range(initial_value, final_value+1):
            for symbol in symbol_table:
                if id_var == symbol[0]:
                    symbol[2] = i
                    print_table(symbol_table)
            
    dfs(tree.root, [], "for", function)
    
def recursion(tree, symbol_table, tokens):
    def function(node: Node):
        id_var = node.children[0].children[0].value
        args = node.children[1]
        exp = args.children[1].children[0]
        value = calculate_expression(exp, symbol_table)
        
        for i in range(len(symbol_table)):
            if symbol_table[i][0] == id_var:
                symbol_table[i+1][2] = value
                print_table(symbol_table)
                execute_function(value, get_line(id_var, tokens), 0, id_var, symbol_table)
    dfs(tree.root, [], "chamada", function)

def execute_function(n, line, indice, id_var, symbol_table):
    f = open("entrada.vb", "r")
    backup_line = line
    lines = []
    for l in f.readlines():
        if l != '\n':
            lines.append(l)
    
    comando = pre_process(lines[line])

    while comando[0] + " " + comando[1] != "END FUNCTION":
        comando = pre_process(lines[line])
        if comando[0] == "IF":
            a = 0
            for i in range(len(symbol_table)):
                    if symbol_table[i][0] == comando[1] and symbol_table[i][4] == indice:
                        a = int(symbol_table[i][2])
            b = int(comando[3])
            if evaluate_condition(a, comando[2], b):
                value = pre_process(lines[line+1])[3]
                for i in range(len(symbol_table)):
                    if symbol_table[i][0] == id_var and symbol_table[i][4] == indice:
                        symbol_table[i][2] = value
                        print_table(symbol_table)
                        return
        
        if comando[0] == "CALL":
            p_name = comando[3]
            t1 = 0
            for i in range(len(symbol_table)):
                if symbol_table[i][0] == p_name and symbol_table[i][4] == indice:
                    t1 = int(symbol_table[i][2])
            op = comando[4]
            t2 = int(comando[5])
            n = make_operation(t1, op, t2)
            symbol_table.append([id_var, "Função", 0, "Local", indice+1])
            symbol_table.append([p_name, "Parâmetro inteira", n, "Local", indice+1])
            print_table(symbol_table)
            execute_function(n, backup_line, indice+1, id_var, symbol_table)
        line += 1
    
    symbol_table.pop()
    value = symbol_table.pop()[2]
    for i in range(len(symbol_table)):
        if symbol_table[i][0] == id_var and symbol_table[i][4] == indice-1:
            symbol_table[i][2] = value
    print_table(symbol_table)
    

def dfs(node: Node, visited: list, value, function):
    if node.id not in visited:
        visited.append(node.id)
        if node.type == value:
            function(node)
        for n in node.children:
            if node.value != "funcao":
                dfs(n, visited, value, function)

def get_line(string, tokens: TokenList):
    tokens.line = 0
    tokens.index = 0

    token = tokens.nextToken()
    while token != None:
        if token.type == "FUNCTION":
            peek = tokens.peekToken()
            if peek.value == string:
                return tokens.line+1
        token = tokens.nextToken()