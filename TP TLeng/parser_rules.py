from lexer_rules import tokens
from expressions import *

# A -> type T S'
def p_primary_var_declaration(subexpressions):
    'primary_var_declaration : TYPEDEF field_declaration var_next_declaration'
    subexpressions[0] = PrimaryVarDeclaration(subexpressions[2], subexpressions[3])

# S -> type T S'
def p_var_declaration(subexpressions):
    'var_declaration : TYPEDEF field_declaration var_next_declaration'
    subexpression[0] = VarDeclaration(subexpressions[2], subexpressions[3])

# S' -> lambda
def p_var_next_declaration_empty(subexpressions):
    'var_next_declaration :'
    subexpressions[0] = VarNextDeclaration(None, True)

# S' -> S
def p_var_next_declaration(subexpressions):
    'var_next_declaration : var_declaration'
    subexpressions[0] = VarNextDeclaration(subexpressions[1], False)

# T -> id T' E
def p_field_declaration(subexpressions):
    'field_declaration : ID field_array type_declaration'


# T' -> lambda
def p_field_array_empty(subexpressions):
    'field_array :'
    subexpressions[0] = { "esArray" : False}

# T' -> []
def p_field_array(subexpressions):
    'field_array : BRACKETS'
    subexpressions[0] = { "esArray" : True}

# E -> string | int | float64 | bool
def p_basic_type_declaration(subexpressions):
    'type_declaration : TYPE'

# E -> id
def p_type_ref_declaration(subexpressions):
    'type_declaration : ID'

# E -> struct{E'}
def p_type_struct_declaration(subexpressions):
    'type_declaration : STRUCT LBRACE type_next_declaration RBRACE'

# E' -> lambda
def p_type_next_declaration_empty(subexpressions):
    'type_next_declaration :'
    pass

# E' -> T E'
def p_type_next_declaration(subexpressions):
    'type_next_declaration : field_declaration type_next_declaration'

def p_error(token):
    message = "[Syntax error]"
    if token is not None:
        message += "\ntype:" + token.type
        message += "\nvalue:" + str(token.value)
        message += "\nline:" + str(token.lineno)
        message += "\nposition:" + str(token.lexpos)
    raise Exception(message)