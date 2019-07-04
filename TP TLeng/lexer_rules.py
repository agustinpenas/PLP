reserved = { 
    'struct' : 'STRUCT',
    'type'   : 'TYPEDEF'
}

tokens = [
    'ID',
    'BRACKETS',
    'TYPE',
    'LBRACE',
    'RBRACE'
] + list(reserved.values())

types = set(['string', 'int', 'float64', 'bool'])

t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_BRACKETS = r"\[]"

def t_ID(token):
    r"[a-z][_a-zA-Z0-9]*"
    token.type = reserved.get(token.value, 'ID')
    if token.value in types:
        token.type = 'TYPE'
    return token

def t_NEWLINE(token):
    r"\n+"
    token.lexer.lineno += len(token.value)

t_ignore = " \t"

def t_error(token):
    message = "Token desconocido:"
    message += "\ntype:" + token.type
    message += "\nvalue:" + str(token.value)
    message += "\nline:" + str(token.lineno)
    message += "\nposition:" + str(token.lexpos)
    raise Exception(message)