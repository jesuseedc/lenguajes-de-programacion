# Implementar un analizador léxico. 
# El analizador lexico debe tomar de entrada un flujo lineal
# de caracteres y regresar un flujo lineal de tokens, estos
# son estructuras que permiten identificar simolos terminales
# de la sintaxis concreta, asi como las categorias sintacticas
# Number y Identifier.


# Importar el modulo de expresiones regulares
import re

# Definir una lista de tokens
tokens = (
    'NUMBER',
    'IDENTIFIER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'EQUALS',
    'SEMICOLON',
    'COMMA',
    'LBRACKET',
    'RBRACKET',
    'LBRACE',
    'RBRACE',
    'IF',
    'ELSE',
    'WHILE',
    'FOR',
    'RETURN',
    'PRINT',
    'READ',
    'INT',
    'FLOAT',
    'STRING',
    'BOOL',
    'TRUE',
    'FALSE',
    'AND',
    'OR',
    'NOT',
    'GREATER',
    'LESS',
    'GREATEREQUAL',
    'LESSEQUAL',
    'EQUAL',
    'NOTEQUAL',
    'COMMENT',
    'NEWLINE',
    'INDENT',
    'DEDENT',
    'ENDMARKER',
)

# Definir una lista de palabras reservadas
reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'for' : 'FOR',
    'return' : 'RETURN',
    'print' : 'PRINT',
    'read' : 'READ',
    'int' : 'INT',
    'float' : 'FLOAT',
    'string' : 'STRING',
    'bool' : 'BOOL',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'and' : 'AND',
    'or' : 'OR',
    'not' : 'NOT',
}

# Definir una lista de tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'='
t_SEMICOLON = r';'
t_COMMA = r','

# Definir una expresion regular para los numeros
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Definir una expresion regular para los identificadores
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

# Definir una expresion regular para los comentarios
def t_COMMENT(t):
    r'\#.*'
    pass

# Definir una expresion regular para los saltos de linea
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Definir una expresion regular para los espacios en blanco
t_ignore = ' \t'

# Definir una expresion regular para los errores
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Construir el analizador lexico
import ply.lex as lex
lexer = lex.lex()

# Pruebas
data = '''
# Comentario
if (a == 10) {
    a = 0; # Comentario
}
'''

lexer.input(data)

# Tokenizar
while True:
    tok = lexer.token()
    if not tok: break
    print(tok)



