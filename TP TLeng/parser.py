import lexer_rules
import parser_rules
import fileinput

from ply.lex import lex
from ply.yacc import yacc


if __name__ == "__main__":
    text = ''
    for line in fileinput.input():
        text += line

    lexer = lex(module=lexer_rules)
    parser = yacc(module=parser_rules)

    expression = parser.parse(text, lexer)

    result = expression.evaluate()
    print (result)