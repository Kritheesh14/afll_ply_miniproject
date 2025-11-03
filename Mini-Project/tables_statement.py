# Example Lua code:
code = ''' mytable = {a = 1, b = {x = 2, y = 3}, [5] = 10} '''

import ply.lex as lex
import ply.yacc as yacc

# Lexer

tokens = (
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET',
    'ID',
    'NUMBER',
    'EQUAL',
    'COMMA'
)

t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_EQUAL = r'='
t_COMMA = r','
t_ID = r'[a-zA-Z_]\w*'
t_NUMBER = r'\d+'

t_ignore = ' \t\n'

def t_error(t):
    t.lexer.skip(1)

lexer = lex.lex()
lexer.input(code)

print("Tokenization Part:")
while True:
    token = lexer.token()
    if not token:
        break
    print(token)

# Parser

def p_statement(p):
    'statement : assignment'
    p[0] = p[1]

def p_assignment(p):
    'assignment : ID EQUAL table'
    p[0] = ('assign', p[1], p[3])

def p_table(p):
    '''table : LBRACE fields RBRACE
             | LBRACE RBRACE'''
    p[0] = ('table', p[2] if len(p) == 4 else [])

def p_fields_multi(p):
    'fields : fields COMMA field'
    p[0] = p[1] + [p[3]]

def p_fields_single(p):
    'fields : field'
    p[0] = [p[1]]

def p_field(p):
    '''field : ID EQUAL value
             | LBRACKET value RBRACKET EQUAL value'''
    if len(p) == 4:
        p[0] = (p[1], p[3])
    else:
        p[0] = (p[2], p[5])

def p_value(p):
    '''value : NUMBER
             | ID
             | table'''
    p[0] = p[1]

def p_error(p):
    pass

parser = yacc.yacc()
print("\n\nParser Part:")
print(parser.parse(code))