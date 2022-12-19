import analisador_lexico
import analisador_sintatico
import analisador_semantico
from classes import TokenList
from utils import convert_to_df, print_green, print_red

print("Compilando seu código...\n")

tokens = TokenList(analisador_lexico.run())
print_green("\nAnálise Léxica concluída!\n")
symbol_table, errors, sintatic_tree = analisador_sintatico.run(tokens)
print(convert_to_df(symbol_table))
print_green("\nAnálise Sintática concluída!\n")

if errors:
    for err in errors:
        print_red(err)
    print_red("\n----FIM DA COMPILAÇÃO DEVIDO A ERRO SEMÂNTICO!----")
else:
    if analisador_semantico.run(sintatic_tree, symbol_table, tokens):
        print_green("\nAnálise Semântica concluída!\n")
    else:
        print_red("\n----FIM DA COMPILAÇÃO DEVIDO A ERRO SEMÂNTICO!----")
