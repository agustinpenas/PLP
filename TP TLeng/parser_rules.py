from lexer_rules import tokens
from expressions import *
from sys import stderr, exit

# A -> type T S'
def p_primary_type_definition(subexpressions):
    'primary_type_definition : TYPEDEF type_declaration new_type_definition'
    subexpressions[0] = PrimaryTypeDefinition(subexpressions[2], subexpressions[3])

# S -> type T S'
def p_type_definition(subexpressions):
    'type_definition : TYPEDEF type_declaration new_type_definition'
    subexpressions[0] = TypeDefinition(subexpressions[2], subexpressions[3])

# S' -> lambda
def p_new_type_definition_empty(subexpressions):
    'new_type_definition :'
    subexpressions[0] = NewTypeDefinition(None, True)

# S' -> S
def p_new_type_definition(subexpressions):
    'new_type_definition : type_definition'
    subexpressions[0] = NewTypeDefinition(subexpressions[1], False)

# T -> id T' E
def p_type_declaration(subexpressions):
    'type_declaration : ID is_array type'
    id = subexpressions[1]
    is_array = subexpressions[2]
    _type = subexpressions[3]
    if id in _type.referencias:
        stderr.write('Hay una referencia circular sobre el tipo "' + id + '"')
        exit()
    subexpressions[0] = TypeDeclaration(_type.referencias, id, is_array, _type)

# T' -> lambda
def p_is_array_empty(subexpressions):
    'is_array :'
    subexpressions[0] = { "cantArrays" : 0}

# T' -> [] T'
def p_is_array(subexpressions):
    'is_array : BRACKETS is_array'
    subexpressions[0] = { "cantArrays" : 1 + subexpressions[2]["cantArrays"] }

# E -> string | int | float64 | bool
def p_basic_type(subexpressions):
    'type : TYPE'
    subexpressions[0] = BasicType(subexpressions[1])

# E -> id
def p_type_ref(subexpressions):
    'type : ID'
    subexpressions[0] = TypeRef(subexpressions[1])

# E -> struct{E'}
def p_type_struct(subexpressions):
    'type : STRUCT LBRACE struct_field RBRACE'
    subexpressions[0] = TypeStruct(subexpressions[3])

# E' -> lambda
def p_struct_field_empty(subexpressions):
    'struct_field :'
    subexpressions[0] = StructField(True, list(), None, None)

# E' -> T E'
def p_struct_field(subexpressions):
    'struct_field : type_declaration struct_field'
    type_declaration = subexpressions[1]
    struct_field = subexpressions[2]
    referencias = type_declaration.referencias + struct_field.referencias
    subexpressions[0] = StructField(False, referencias, type_declaration, struct_field)

def p_error(token):
    message = "[Syntax error]"
    if token is not None:
        message += "\ntype:" + token.type
        message += "\nvalue:" + str(token.value)
        message += "\nline:" + str(token.lineno)
        message += "\nposition:" + str(token.lexpos)
    raise Exception(message)
