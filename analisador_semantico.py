def analyse_id(token, var_type, origin, identifiers, symbol_table, semantic_errors):

    if origin == "declaration" and token.value not in identifiers:
        identifiers.append(token.value)
        symbol_table.append(
            [token.value, var_type, 0, "Global"]
        )
    
    elif origin == "declaration" and token.value in identifiers:
        semantic_errors.append(f"Redeclaração de {token.value} detectada!")
    
    if origin == "param":
        identifiers.append(token.value)
        symbol_table.append(
            [token.value, var_type, 0, "Local"]
        )
    if origin == "param" and token.value in identifiers:
        semantic_errors.append(f"Já existe um parâmetro com esse nome! {token.value}")

    if origin == "use" and token.value not in identifiers:
        semantic_errors.append(f"A variável {token.value} não foi declarada")

    if origin == "for" and token.value not in identifiers:
        identifiers.append(token.value)
        symbol_table.append(
            [token.value, var_type, 0, "Local"]
        )

    return identifiers, symbol_table, semantic_errors