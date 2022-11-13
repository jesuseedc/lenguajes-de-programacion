# Implementar un analizador léxico para el lenguaje LETREC
# El analizador léxico debe tomar de entrada un flujo lineal
# de caracteres y regresar un flujo lineal de tokens, estos
# son estructuras que permiten identificar los simbolos 
# terminales de la sintaxis concreta, asi como las categorias
# sintacticas Number y Identifier.


import sys
import ply.lex as lex

# Lista de palabras reservadas
reserved = {
    'let' : 'LET',
    'in' : 'IN',
    'rec' : 'REC',
    'end' : 'END',
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'and' : 'AND',
    'or' : 'OR',
    'not' : 'NOT',
    'print' : 'PRINT',
    'read' : 'READ',
    'write' : 'WRITE',
    'newline' : 'NEWLINE',
    'iszero' : 'ISZERO',
    'succ' : 'SUCC',
    'pred' : 'PRED',
    'isnum' : 'ISNUM',
    'isbool' : 'ISBOOL',
    'isunit' : 'ISUNIT',
    'ispair' : 'ISPAIR',
    'fst' : 'FST',
    'snd' : 'SND',
    'cons' : 'CONS',
    'hd' : 'HD',
    'tl' : 'TL',
    'islist' : 'ISLIST',
    'nil' : 'NIL',
    'isnil' : 'ISNIL',
    'raise' : 'RAISE',
    'handle' : 'HANDLE',
    'with' : 'WITH',
    'try' : 'TRY',
    'catch' : 'CATCH'
}

# Lista de tokens
tokens = [
    'NUMBER',
    'IDENTIFIER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'EQUALS',
    'LESS',
    'GREATER',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'COMMA',
    'SEMICOLON',
    'COLON',
    'DOT',
    'ASSIGN',
    'QUOTE',
    'BACKQUOTE'
] + list(reserved.values())

# Expresiones regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LESS = r'<'
t_GREATER = r'>'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_SEMICOLON = r';'
t_COLON = r':'
t_DOT = r'\.'
t_ASSIGN = r':='
t_QUOTE = r'\''
t_BACKQUOTE = r'`'

# Expresiones regulares para tokens compuestos
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'IDENTIFIER')    # Checar palabras reservadas
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# Expresiones regulares para saltos de linea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Expresiones regulares para comentarios
def t_comment(t):
    r'\#.*'
    pass

# Expresiones regulares para espacios en blanco
t_ignore  = ' \t'

# Manejo de errores
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Construir el analizador léxico
lexer = lex.lex()

# Prueba del analizador léxico
data = '''
let x = 1 in
let y = 2 in
let z = 3 in
let f = fun x -> fun y -> fun z -> x + y + z in
f x y z
end
'''

# Pasar la entrada al analizador léxico
lexer.input(data)

# Tokenizar
while True:
    tok = lexer.token()
    if not tok: 
        break      # No hay más tokens
    print(tok)
