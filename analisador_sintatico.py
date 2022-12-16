global tokens, errors
from utils import print_red, sintatic_error
import constants

def check_reserved_keyword(token, keyword):
    if token.type != keyword:
        errors.append(sintatic_error(keyword, token.value, tokens.line+1))

def run(token_list):
    global tokens, errors, symbol_table, identifiers
    tokens = token_list
    errors = []
    symbol_table = []
    identifiers = []
    programa()
    for err in errors:
        print_red(err)
    return symbol_table

def programa():
    if tokens.peekToken().value == None: return
    declara()
    rotina()
    sentencas()
    token = tokens.nextToken()
    check_reserved_keyword(token, "END")

def declara():
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    if token.value == "DIM":
        dvar()
        declara()


def dvar():
    if tokens.peekToken().value == None: return
    token = tokens.nextToken()
    check_reserved_keyword(token, "DIM")
    variaveis()
    token = tokens.nextToken()
    check_reserved_keyword(token, "AS")
    tipo()


def tipo():
    if tokens.peekToken().value == None: return
    token = tokens.nextToken()
    check_reserved_keyword(token, "INT")

def variaveis():
    if tokens.peekToken().value == None: return
    id("Variável inteira")
    mais_var()

def mais_var():
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    if token.value == ",":
        token = tokens.nextToken()
        if token.value != ",":
            errors.append(f"Linha {tokens.line+1}: Esperava uma vírgula, mas encontrei {token.value}")
        variaveis()

def rotina():
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    if token.value == "SUB" or token.value == "FUNCTION":
        if token.type == "SUB":
            procedimento()
        elif token.type == "FUNCTION":
            funcao()

def procedimento():
    if tokens.peekToken().value == None: return
    token = tokens.nextToken()
    check_reserved_keyword(token, "SUB")
    id("Procedimento")
    parametros()
    sentencas()
    token = tokens.nextToken()
    check_reserved_keyword(token, "END")
    token = tokens.nextToken()
    check_reserved_keyword(token, "SUB")
    rotina()

def funcao():
    if tokens.peekToken().value == None: return
    token = tokens.nextToken()
    check_reserved_keyword(token, "FUNCTION")
    id("Função")
    parametros()
    token = tokens.nextToken()
    check_reserved_keyword(token, "AS")
    tipo()
    sentencas()
    token = tokens.nextToken()
    check_reserved_keyword(token, "END")
    token = tokens.nextToken()
    check_reserved_keyword(token, "FUNCTION")

def parametros():
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    if token.value == "(":
        token = tokens.nextToken()
        check_reserved_keyword(token, "(")
        lista_parametros()
        token = tokens.nextToken()
        check_reserved_keyword(token, ")")

def lista_parametros():
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    if token.type == "identificador":
        id("Parâmetro")
        token = tokens.nextToken()
        check_reserved_keyword(token, "AS")
        tipo()
        cont_lista_par()

def cont_lista_par():
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    if token.value == ",":
        token = tokens.nextToken()
        if token.value != ",":
            errors.append(f"Linha {tokens.line+1}: Esperava uma vírgula, mas encontrei {token.value}")
        id("Parâmetro")
        token = tokens.nextToken()
        check_reserved_keyword(token, "AS")     
        tipo()
        cont_lista_par()

def sentencas():
    if tokens.peekToken().value == None: return
    if tokens.peekToken().value == "END": return
    comando()
    mais_sentencas()

def mais_sentencas():
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    if token.value != None and token.value != "END" and token.value != "NEXT":
        sentencas()

def var_read():
    if tokens.peekToken().value == None: return
    id("Variável inteira")
    mais_var_read()

def mais_var_read():
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    if token.value == ",":
        token = tokens.nextToken()
        if token.value != ",":
            errors.append(f"Linha {tokens.line+1}: Esperava uma vírgula, mas encontrei {token.value}")
        var_read()

def var_write():
    if tokens.peekToken().value == None: return
    id("Variável inteira")
    mais_var_write()

def mais_var_write():
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    if token.value == ",":
        token = tokens.nextToken()
        if token.value != ",":
            errors.append(f"Linha {tokens.line+1}: Esperava uma vírgula, mas encontrei {token.value}")
        var_write()

def comando():
    if tokens.peekToken().value == None: return
    token = tokens.nextToken()
    
    if token.type == "INPUT":
        var_read()
    elif token.type == "PRINT":
        var_write()
    elif token.type == "FOR":
        id("Variável inteira")
        token = tokens.nextToken()
        if token.type != "atribuição":
            errors.append(f"Linha {tokens.line+1}: Esperava um operador de atribuição, recebi {token.value}")
        expressao()
        token = tokens.nextToken()
        check_reserved_keyword(token, "TO")
        expressao()
        sentencas()
        token = tokens.nextToken()
        check_reserved_keyword(token, "NEXT")     

    elif token.type == "DO":
        token = token.nextToken()
        check_reserved_keyword(token, "LOOP")
        sentencas()
        token = token.nextToken()
        check_reserved_keyword(token, "WHILE")
        condicao()
        
    elif token.type == "IF":
        condicao()
        token = tokens.nextToken()
        check_reserved_keyword(token, "THEN")    
        sentencas()
        pfalsa()
        token = tokens.nextToken()
        check_reserved_keyword(token, "END")   
        token = tokens.nextToken()
        check_reserved_keyword(token, "IF")   
    
    elif token.type == "LET":
        id("Variável inteira")
        token = tokens.nextToken()
        if token.type != "atribuição":
            errors.append(f"Linha {tokens.line+1}: Esperava um operador de atribuição, recebi {token.value}")
        expressao()
    else:
        funcao()

def argumentos():
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    if token.value == "(":
        token = tokens.nextToken()
        check_reserved_keyword(token, "(")
        lista_arg()
        token = tokens.nextToken()
        check_reserved_keyword(token, ")")

def lista_arg():
    if tokens.peekToken().value == None: return
    expressao()
    cont_lista_arg()

def cont_lista_arg():
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    if token.value == ",":
        token = tokens.nextToken()
        if token.value != ",":
            errors.append(f"Linha {tokens.line+1}: Esperava uma vírgula, mas encontrei {token.value}")
        lista_arg()

def pfalsa():
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    if token.type == "ELSE":
        token = tokens.nextToken()
        check_reserved_keyword(token, "ELSE")
        sentencas()

def condicao():
    if tokens.peekToken().value == None: return
    expressao()
    relacao()
    expressao()

def relacao():
    if tokens.peekToken().value == None: return
    token = tokens.nextToken()
    if token.value not in constants.RELATION_OPERATORS:
        errors.append(f"Esperava um operador relacional, recebi {token.value}")
        
def expressao():
    if tokens.peekToken().value == None: return
    termo()
    outros_termos()

def outros_termos():
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    if token.value == '+' or token.value == '-':
        op_ad()
        termo()
        outros_termos()

def op_ad():
    if tokens.peekToken().value == None: return
    token = tokens.nextToken()
    if token.value != '+' and token.value != '-':
        errors.append(f"Esperava um + ou -, recebi {token.value}")

def termo():
    if tokens.peekToken().value == None: return
    fator()
    mais_fatores()

def mais_fatores():
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    if token.value == '*' or token.value == '/':
        op_mul()
        fator()
        mais_fatores()

def op_mul():
    if tokens.peekToken().value == None: return
    token = tokens.nextToken()
    if token.value != '*' and token.value != '/':
        errors.append(f"Linha {tokens.line+1}: Esperava um * ou /, recebi {token.value}")

def fator():
    if tokens.peekToken().value == None: return
    token = tokens.peekToken()
    if token.type == "identificador":
        id("Variável inteira")
    elif token.type == "numero":
        intnum()
    elif token.value == "(":
        expressao()
        token = tokens.nextToken()
        check_reserved_keyword(token, ")")

def id(origin):
    if tokens.peekToken().value == None: return
    token = tokens.nextToken()
    if token.type != "identificador":
        errors.append(f"Linha {tokens.line+1}: Esperava um identificador, mas recebi {token.type}")
    else:
        if token.value not in identifiers:
            identifiers.append(token.value)
            symbol_table.append(
                [token.value, origin, 0]
            )
def intnum():
    if tokens.peekToken().value == None: return
    token = tokens.nextToken()
    if token.type != "numero":
        errors.append(f"Linha {tokens.line+1}: Esperava um número, mas recebi {token.value}")