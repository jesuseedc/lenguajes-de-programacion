import ply.lex as lex

tokens = (
    'ID',
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'EQUALS',
    'LET',
    'IN',
    'REC',
    'SEMICOLON',
    'COMMA',
    'DOT',
    'IF',
    'THEN',
    'ELSE',
    'TRUE',
    'FALSE',
    'LESS',
    'GREATER',
    'LESS_EQUAL',
    'GREATER_EQUAL',
    'EQUAL',
    'NOT_EQUAL',
    'AND',
    'OR',
    'NOT',
    'FUN',
    'ARROW',
    'NIL',
    'CONS',
    'HEAD',
    'TAIL',
    'ISNIL',
    'INT',
    'BOOL',
    'LIST',
    'COLON',
    'TYPE'
)

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_EQUALS  = r'='
t_LET     = r'let'
t_IN      = r'in'
t_REC     = r'rec'
t_SEMICOLON = r';'
t_COMMA   = r','
t_DOT     = r'\.'
t_IF      = r'if'
t_THEN    = r'then'
t_ELSE    = r'else'
t_TRUE    = r'true'
t_FALSE   = r'false'
t_LESS    = r'<'
t_GREATER = r'>'
t_LESS_EQUAL = r'<='
t_GREATER_EQUAL = r'>='
t_EQUAL   = r'=='
t_NOT_EQUAL = r'!='
t_AND     = r'&&'
t_OR      = r'\|\|'
t_NOT     = r'!'
t_FUN     = r'fun'
t_ARROW   = r'->'
t_NIL     = r'nil'
t_CONS    = r'::'
t_HEAD    = r'head'
t_TAIL    = r'tail'
t_ISNIL   = r'isnil'
t_INT     = r'int'
t_BOOL    = r'bool'
t_LIST    = r'list'
t_COLON   = r':'
t_TYPE    = r'type'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test
data = '''
(define (module-get mod name)

'''

lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      
    print(tok)









    

    





