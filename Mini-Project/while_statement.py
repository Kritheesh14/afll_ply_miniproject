# Example Lua code:
code = ''' while x < 10 do x = x + 1 end '''

import ply.lex as lex
import ply.yacc as yacc

# Lexer - Tokenize all the code

tokens = (
    'WHILE',
    'DO',
    'END',
    'ID',
    'NUMBER',
    'OP',
    'ASSIGN',
    'PLUS'
)

t_ID = r'[a-zA-Z_]\w*'
t_OP = r'[<>]=?|==|~='
t_ASSIGN = r'='
t_PLUS = r'\+'
t_NUMBER = r'\d+'

t_ignore = ' \t\n'

def t_WHILE(t):
    r'while'
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
    '''statement : while_loop
                 | assignment'''
    p[0] = p[1]

def p_while_loop(p):
    'while_loop : WHILE condition DO statements END'
    p[0] = ('while', p[2], p[4])

def p_condition(p):
    'condition : ID OP expr'
    p[0] = (p[1], p[2], p[3])

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
    pass

parser = yacc.yacc()
print("\n\nParser Part:")
print(parser.parse(code))