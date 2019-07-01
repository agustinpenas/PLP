from lexer_rules import tokens

# A -> type T S'
def p_primary_var_declaration(subexpressions):
    'primary_var_declaration : TYPEDEF field_declaration var_next_declaration'

# S -> type T S'
def p_var_declaration(subexpressions):
    'var_declaration : TYPEDEF field_declaration var_next_declaration'

# S' -> lambda
def p_var_next_declaration_empty(subexpressions):
    'var_next_declaration :'
    pass

# S' -> S
def p_var_next_declaration(subexpressions):
    'var_next_declaration : var_declaration'

# T -> id T' E
def p_field_declaration(subexpressions):
    'field_declaration : ID field_array type_declaration'

# T' -> lambda
def p_field_array_empty(subexpressions):
    'field_array :'
    pass

# T' -> []
def p_field_array(subexpressions):
    'field_array : BRACKETS'

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