# Implementar un analizador léxico para el lenguaje LETREC
# El analizador lexico debe tomar una entrada de un flujo
# lineal de caracteres y regresar un flujo lineal de tokens,
# estos son estructuras que permiten identificar los simbolos
# terminales de la sintaxis concreta, así como las categorias
# sintacticas Number y Identifier.

# Sintaxis concreta:
# Expression ::= Number
# Expression ::= -(Expression, Expression)
# Expression ::= zero?(Expression)
# Expression ::= if Expression then Expression else Expression
# Expression ::= Identifier
# Expression ::= let Identifier = Expression in Expression
# Expression ::= proc(Identifier) Expression
# Expression ::= (Expression Expression)
# Expression ::= letrec Identifier (Identifier) Expression in Expression

import ply.lex as lex

# Lista de palabras reservadas
reserved = {
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'let' : 'LET',
    'in' : 'IN',
    'proc' : 'PROC',
    'letrec' : 'LETREC',
    'zero?' : 'ZERO',
    'call' : 'CALL'
}

# Lista de tokens
tokens = [
    'LPAREN',
    'RPAREN',
    'DIFF',
    'CONST',
    'VAR',
    'EQUAL',
    'COMMA'
] + list(reserved.values())

# Expresiones regulares para tokens simples
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_DIFF = r'-'
t_EQUAL = r'='
t_COMMA = r','
t_VAR = r'[a-zA-Z_][a-zA-Z0-9_]*'

# Expresiones regulares para tokens complejos
def t_CONST(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignorar espacios en blanco
t_ignore = ' \t'


# Manejar errores
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Construir el analizador léxico
lexer = lex.lex()

# Prueba del analizador léxico
def test_lexer ( data ):
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

# Prueba de entrada
data = '''
letrec double(x) =
   if zero?(x)
   then 0
   else -((double -(x, 1)), -2)
in (double 6)
'''

# Prueba
test_lexer(data)

