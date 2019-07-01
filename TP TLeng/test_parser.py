import lexer_rules
import parser_rules

from ply.lex import lex
from ply.yacc import yacc

lexer = lex(module=lexer_rules)
parser = yacc(module=parser_rules)

text = "type persona []struct{nombre string nacionalidad pais edad int} type pais struct{nombre string codigo struct{ prefijo string sufijo string }}"
ast = parser.parse(text, lexer)
print(ast)