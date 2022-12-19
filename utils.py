from io import StringIO
import csv
import pandas as pd

def print_red(msg): 
    print(f"\033[91m{msg}\033[00m")

def print_green(msg): 
    print(f"\033[92m{msg}\033[00m")

def sintatic_error(expected, got, line):
    return f"Linha {line}: Programa esperava {expected} mas recebeu {got}"

def convert_to_df(matrix):
    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer, delimiter=';')

    csv_writer.writerow(['Lexema', 'Tipo', 'Valor', 'Escopo', 'Indice'])

    for line in matrix:
        csv_writer.writerow([line[0], line[1], line[2], line[3], line[4]])

    csv_buffer.seek(0)
    df = pd.read_csv(csv_buffer, sep=';')
    return df

def print_table(table):
    print("\033[93m")
    print(convert_to_df(table))
    print("\n")
    print("\033[00m")