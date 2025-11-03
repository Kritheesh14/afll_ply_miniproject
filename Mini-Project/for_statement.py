# Example Lua code:
code = ''' for i = 1, 10, 2 do x = x + i end '''

import ply.lex as lex
import ply.yacc as yacc

# Lexer - Tokenize all the code

tokens = (
    'FOR',
    'DO',
    'END',
    'ID',
    'NUMBER',
    'ASSIGN',
    'COMMA',
    'PLUS'
)

t_ID = r'[a-zA-Z_]\w*'
t_ASSIGN = r'='
t_COMMA = r','
t_PLUS = r'\+'
t_NUMBER = r'\d+'

t_ignore = ' \t\n'

def t_FOR(t):
    r'for'
    return t

def t_DO(t):
    r'do'
    return t

def t_END(t):
    r'end'
    return t

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

# Yacc - Parse the code

def p_statement(p):
    '''statement : for_loop
                 | assignment'''
    p[0] = p[1]

def p_for_loop_three(p):
    'for_loop : FOR ID ASSIGN expr COMMA expr DO statements END'
    p[0] = ('for', p[2], p[4], p[6], None, p[8])

def p_for_loop_four(p):
    'for_loop : FOR ID ASSIGN expr COMMA expr COMMA expr DO statements END'
    p[0] = ('for', p[2], p[4], p[6], p[8], p[10])

def p_statements(p):
    '''statements : statements statement
                  | statement'''
    p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]

def p_assignment(p):
    'assignment : ID ASSIGN expr'
    p[0] = ('assign', p[1], p[3])

def p_expr(p):
    '''expr : NUMBER
            | ID
            | expr PLUS expr'''
    p[0] = ('+', p[1], p[3]) if len(p) == 4 else p[1]

def p_error(p):
    print("Syntax error at", p)

parser = yacc.yacc()
print("\n\nParser Part:")
print(parser.parse(code))