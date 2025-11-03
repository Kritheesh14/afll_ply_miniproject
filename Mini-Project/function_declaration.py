# Example Lua code:
code = ''' function add(a, b) c = a + b end '''

import ply.lex as lex
import ply.yacc as yacc

# Lexer - Tokenize all the code

tokens = (
    'FUNCTION',
    'END',
    'ID',
    'LPAREN',
    'RPAREN',
    'COMMA',
    'ASSIGN',
    'PLUS'
)

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_ASSIGN = r'='
t_PLUS = r'\+'
t_ID = r'[a-zA-Z_]\w*'

t_ignore = ' \t\n'

def t_FUNCTION(t):
    r'function'
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
    '''statement : function_def
                 | assignment'''
    p[0] = p[1]

def p_function_def(p):
    'function_def : FUNCTION ID LPAREN params RPAREN statements END'
    p[0] = ('function', p[2], p[4], p[6])

def p_params_multi(p):
    'params : params COMMA ID'
    p[0] = p[1] + [p[3]]

def p_params_single(p):
    'params : ID'
    p[0] = [p[1]]

def p_params_empty(p):
    'params :'
    p[0] = []

def p_statements(p):
    '''statements : statements statement
                  | statement'''
    p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]

def p_assignment(p):
    'assignment : ID ASSIGN expr'
    p[0] = ('assign', p[1], p[3])

def p_expr(p):
    '''expr : ID
            | expr PLUS expr'''
    p[0] = ('+', p[1], p[3]) if len(p) == 4 else p[1]

def p_error(p):
    pass

parser = yacc.yacc()
print("\n\nParser Part:")
print(parser.parse(code))