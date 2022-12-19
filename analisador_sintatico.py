global tokens, errors
from utils import print_red, sintatic_error
from analisador_semantico import analyse_id
from classes import Tree, Node, Token
import constants

def check_reserved_keyword(token, keyword):
    if token.type != keyword:
        errors.append(sintatic_error(keyword, token.value, tokens.line+1))

def check_delimiter(token, keyword):
    if token.value != keyword:
        errors.append(sintatic_error(keyword, token.value, tokens.line+1))

def run(token_list):
    global tokens, errors, symbol_table, identifiers, semantic_errors, s_tree
    tokens = token_list
    errors = []
    symbol_table = []
    identifiers = []
    semantic_errors = []
    s_tree = Tree()
    programa()
    for err in errors:
        print_red(err)
    return symbol_table, semantic_errors, s_tree

def programa():
    s_tree.root = Node(None, Token("root","root"))
    declara(s_tree.root)
    rotina(s_tree.root)
    sentencas(s_tree.root)
    token = tokens.nextToken()
    check_reserved_keyword(token, "END")
    s_tree.root.add(token)

def declara(parent: Node):
    if tokens.peekToken().value == None: return
    node = parent.add(Token("declara", "declara"))
    token = tokens.peekToken()
    if token.value == "DIM":
        dvar(node)
        declara(node)


def dvar(parent: Node):
    if tokens.peekToken().value == None: return
    node = parent.add(Token("dvar", "dvar"))
    token = tokens.nextToken()
    check_reserved_keyword(token, "DIM")
    node.add(token)
    variaveis(node)
    token = tokens.nextToken()
    check_reserved_keyword(token, "AS")
    node.add(token)
    tipo(node)


def tipo(parent: Node):
    if tokens.peekToken().value == None: return
    node = parent.add(Token("tipo", "tipo"))
    token = tokens.nextToken()
    if token.type != "INT" and token.type != "FLOAT":
        errors.append(sintatic_error("INT ou FLOAT", token.value, tokens.line+1))
    node.add(token)

def variaveis(parent: Node):
    if tokens.peekToken().value == None: return
    node = parent.add(Token("variaveis", "variaveis"))
    id(node, "numero", "declaration")
    mais_var(node)

def mais_var(node: Node):
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    if token.value == ",":
        token = tokens.nextToken()
        if token.value != ",":
            errors.append(f"Linha {tokens.line+1}: Esperava uma vírgula, mas encontrei {token.value}")
        variaveis(node)

def rotina(parent: Node):
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    node = parent.add(Token("rotina", "rotina"))
    if token.value == "SUB" or token.value == "FUNCTION":
        if token.type == "SUB":
            procedimento(node)
        elif token.type == "FUNCTION":
            funcao(node)

def procedimento(parent: Node):
    if tokens.peekToken().value == None: return
    node = parent.add(Token("procedimento", "procedimento"))
    token = tokens.nextToken()
    check_reserved_keyword(token, "SUB")
    node.add(token)
    id(node, "Procedimento", "declaration")
    parametros(node)
    sentencas(node)
    token = tokens.nextToken()
    check_reserved_keyword(token, "END")
    node.add(token)
    token = tokens.nextToken()
    check_reserved_keyword(token, "SUB")
    node.add(token)
    rotina(node)

def funcao(parent: Node):
    if tokens.peekToken().value == None: return
    node = parent.add(Token("funcao", "funcao"))
    token = tokens.nextToken()
    check_reserved_keyword(token, "FUNCTION")
    node.add(token)
    id(node, "Função", "declaration")
    parametros(node)
    token = tokens.nextToken()
    check_reserved_keyword(token, "AS")
    node.add(token)
    tipo(node)
    sentencas(node)
    token = tokens.nextToken()
    check_reserved_keyword(token, "END")
    node.add(token)
    token = tokens.nextToken()
    check_reserved_keyword(token, "FUNCTION")
    node.add(token)

def parametros(parent: Node):
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    node = parent.add(Token("parametros", "parametros"))
    if token.value == "(":
        token = tokens.nextToken()
        check_delimiter(token, "(")
        node.add(token)
        lista_parametros(node)
        token = tokens.nextToken()
        check_delimiter(token, ")")
        node.add(token)

def lista_parametros(parent: Node):
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    node = parent.add(Token("lista_parametros", "lista_parametros"))
    if token.type == "identificador":
        id(node, "Parâmetro", "param")
        token = tokens.nextToken()
        check_reserved_keyword(token, "AS")
        node.add(token)
        tipo(node)
        cont_lista_par(node)

def cont_lista_par(node: Node):
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    if token.value == ",":
        token = tokens.nextToken()
        if token.value != ",":
            errors.append(f"Linha {tokens.line+1}: Esperava uma vírgula, mas encontrei {token.value}")
        node.add(token)
        id(node, "Parâmetro", "param")
        token = tokens.nextToken()
        check_reserved_keyword(token, "AS")     
        node.add(token)
        tipo(node)
        cont_lista_par(node)

def sentencas(parent: Node):
    if tokens.peekToken().value == None: return
    if tokens.peekToken().value == "END": return
    node = parent.add(Token("sentencas", "sentencas"))
    comando(node)
    mais_sentencas(node)

def mais_sentencas(node: Node):
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    if token.value != None and token.value != "END" and token.value != "NEXT":
        sentencas(node)

def var_read(parent: Node):
    if tokens.peekToken().value == None: return
    node = parent.add(Token("var_read", "var_read"))
    id(node, "Variável inteira", "use")
    mais_var_read(node)

def mais_var_read(node: Node):
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    if token.value == ",":
        token = tokens.nextToken()
        if token.value != ",":
            errors.append(f"Linha {tokens.line+1}: Esperava uma vírgula, mas encontrei {token.value}")
        var_read(node)

def var_write(parent: Node):
    if tokens.peekToken().value == None: return
    node = parent.add(Token("var_write", "var_write"))
    id(node, "Variável inteira", "use")
    mais_var_write(node)

def mais_var_write(node: Node):
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    if token.value == ",":
        token = tokens.nextToken()
        if token.value != ",":
            errors.append(f"Linha {tokens.line+1}: Esperava uma vírgula, mas encontrei {token.value}")
        var_write(node)

def comando(parent: Node):
    if tokens.peekToken().value == None: return
    token = tokens.nextToken()
    if token.type == "INPUT":
        node = parent.add(Token("input", "input"))
        var_read(node)
    elif token.type == "PRINT":
        node = parent.add(Token("print", "print"))
        var_write(node)
    elif token.type == "FOR":
        node = parent.add(Token("for", "for"))
        id(node, "Variável inteira", "for")
        token = tokens.nextToken()
        if token.type != "atribuição":
            errors.append(f"Linha {tokens.line+1}: Esperava um operador de atribuição, recebi {token.value}")
        node.add(token)
        expressao(node)
        token = tokens.nextToken()
        check_reserved_keyword(token, "TO")
        node.add(token)
        expressao(node)
        sentencas(node)
        token = tokens.nextToken()
        check_reserved_keyword(token, "NEXT")
        node.add(token)

    elif token.type == "DO":
        node = parent.add(Token("do", "loop"))
        token = token.nextToken()
        check_reserved_keyword(token, "LOOP")
        node.add(token)
        sentencas(node)
        token = token.nextToken()
        check_reserved_keyword(token, "WHILE")
        node.add(token)
        condicao(node)
        
    elif token.type == "IF":
        node = parent.add(Token("if", "then"))
        condicao(node)
        token = tokens.nextToken()
        check_reserved_keyword(token, "THEN")
        node.add(token)
        sentencas(node)
        pfalsa(node)
        token = tokens.nextToken()
        check_reserved_keyword(token, "END")
        node.add(token)
        token = tokens.nextToken()
        check_reserved_keyword(token, "IF")
        node.add(token)

    elif token.type == "LET":
        node = parent.add(Token("let", "let"))
        id(node, "Variável inteira", "use")
        token = tokens.nextToken()
        if token.type != "atribuição":
            errors.append(f"Linha {tokens.line+1}: Esperava um operador de atribuição, recebi {token.value}")
        node.add(token)
        expressao(node)
    else:
        node = parent.add(Token("chamada", "chamada"))
        chamada_funcao(node)

def chamada_funcao(node: Node):
    if tokens.peekToken().value == None: return
    id(node, "call", "call")
    argumentos(node)

def argumentos(parent: Node):
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    node = parent.add(Token("argumentos", "argumentos"))
    if token.value == "(":
        token = tokens.nextToken()
        check_delimiter(token, "(")
        node.add(token)
        lista_arg(node)
        token = tokens.nextToken()
        check_delimiter(token, ")")
        node.add(token)

def lista_arg(parent: Node):
    if tokens.peekToken().value == None: return
    node = parent.add(Token("lista_arg", "lista_arg"))
    expressao(node)
    cont_lista_arg(node)

def cont_lista_arg(node: Node):
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    if token.value == ",":
        token = tokens.nextToken()
        if token.value != ",":
            errors.append(f"Linha {tokens.line+1}: Esperava uma vírgula, mas encontrei {token.value}")
        lista_arg(node)

def pfalsa(parent: Node):
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    node = parent.add(Token("pfalsa", "pfalsa"))
    if token.type == "ELSE":
        token = tokens.nextToken()
        check_reserved_keyword(token, "ELSE")
        node.add(token)
        sentencas(node)

def condicao(parent: Node):
    if tokens.peekToken().value == None: return
    node = parent.add(Token("condicao", "condicao"))
    expressao(node)
    relacao(node)
    expressao(node)

def relacao(parent: Node):
    if tokens.peekToken().value == None: return
    node = parent.add(Token("relacao", "procedimento"))
    token = tokens.nextToken()
    if token.value not in constants.RELATION_OPERATORS:
        errors.append(f"Esperava um operador relacional, recebi {token.value}")
    node.add(token)

def expressao(parent: Node):
    if tokens.peekToken().value == None: return
    node = parent.add(Token("expressao", "expressao"))
    termo(node)
    outros_termos(node)

def outros_termos(node: Node):
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    if token.value in constants.MATH_OPERATORS:
        op_ad(node)
        termo(node)
        outros_termos(node)

def op_ad(parent: Node):
    if tokens.peekToken().value == None: return
    node = parent.add(Token("op_ad", "op_ad"))
    token = tokens.nextToken()
    if token.value not in constants.MATH_OPERATORS:
        errors.append(f"Esperava um operador matemático, recebi {token.value}")
    node.add(token)

def termo(parent: Node):
    if tokens.peekToken().value == None: return
    node = parent.add(Token("termo", "termo"))
    fator(node)
    mais_fatores(node)

def mais_fatores(node: Node):
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    if token.value == '*' or token.value == '/':
        op_mul(node)
        fator(node)
        mais_fatores(node)

def op_mul(parent: Node):
    if tokens.peekToken().value == None: return
    node = parent.add(Token("op_mul", "op_mul"))
    token = tokens.nextToken()
    if token.value != '*' and token.value != '/':
        errors.append(f"Linha {tokens.line+1}: Esperava um * ou /, recebi {token.value}")
    node.add(token)

def fator(parent: Node):
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    node = parent.add(Token("fator", "fator"))
    if token.type == "identificador":
        id(node, "Variável inteira", "use")
    elif token.type == "numero" or token.type == "numero flutuante":
        intnum(node)
    elif token.value == "(":
        expressao(node)
        token = tokens.nextToken()
        check_reserved_keyword(token, ")")
        node.add(token)

def id(parent: Node, var_type, origin):
    global tokens, errors, symbol_table, identifiers, semantic_errors
    if tokens.peekToken().value == None: return
    node = parent.add(Token("id", "id"))
    token = tokens.nextToken()
    if token.type != "identificador":
        errors.append(f"Linha {tokens.line+1}: Esperava um identificador, mas recebi {token.type}")
    else:
        identifiers, symbol_table, semantic_errors = analyse_id(token, var_type, origin, tokens, identifiers, symbol_table, semantic_errors)
    node.add(token)

def intnum(parent: Node):
    if tokens.peekToken().value == None: return
    node = parent.add(Token("num", "num"))
    token = tokens.nextToken()
    if token.type != "numero" and token.type != "numero flutuante":
        errors.append(f"Linha {tokens.line+1}: Esperava um número, mas recebi {token.value}")
    node.add(token)