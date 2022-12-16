import analisador_lexico
import analisador_sintatico
from classes import TokenList
from utils import convert_to_df, print_green

print("Compilando seu código...\n")

tokens = TokenList(analisador_lexico.run())
print_green("\nAnálise Léxica concluída!\n")
symbol_table = analisador_sintatico.run(tokens)
print(convert_to_df(symbol_table))
print_green("\nAnálise Sintática concluída!\n")