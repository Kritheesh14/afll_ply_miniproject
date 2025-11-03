# Example Lua code:
code = ''' if x < 5 then y = 2 else y = y + 1 end '''

import ply.lex as lex
import ply.yacc as yacc

# Lexer - Tokenize all the code

tokens = (
    'IF',
    'THEN',
    'ELSE',
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

def t_IF(t):
    r'if'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_THEN(t):
    r'then'
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
    '''statement : if_statement
                 | assignment'''
    p[0] = p[1]

def p_if_statement(p):
    '''if_statement : IF condition THEN statements END
                    | IF condition THEN statements ELSE statements END'''
    p[0] = ('if', p[2], p[4]) if len(p) == 6 else ('if-else', p[2], p[4], p[6])

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