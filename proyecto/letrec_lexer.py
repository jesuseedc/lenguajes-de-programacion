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
    'zero?' : 'ZERO'
}

# Lista de tokens
tokens = [
    'LPAREN',
    'RPAREN',
    'DIFF',
    'CONST',
    'VAR'
] + list(reserved.values())

# Expresiones regulares para tokens simples
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_DIFF = r'-'
t_CONST = r'\d+'

# Expresiones regulares con acciones semánticas
def t_VAR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'VAR')    # Checar palabras reservadas
    return t

# Expresiones regulares ignoradas
t_ignore = " \t"

# Manejador de errores
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Construir el analizador léxico
lexer = lex.lex()

# Prueba del analizador léxico
data = '''
(letrec fact (n)
    (if (zero? n)
        1
        (- n (fact (- n 1)))))
'''

# Prueba del analizador léxico
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: break      # No hay más tokens
    print(tok)