import lexer_rules

from ply.lex import lex

text = "type persona []struct{nombre string nacionalidad pais edad int} type pais struct{nombre string codigo struct{ prefijo string sufijo string }}"
lexer = lex(module=lexer_rules)
lexer.input(text)

token = lexer.token()

while token is not None:
    print(token.value + " " + token.type)
    token = lexer.token()