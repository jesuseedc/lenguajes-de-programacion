# Implementar un analizador sintáctico para el lenguaje LETREC
# El analizador sintáctico debe tomar de entrada un flujo lineal
# de tokens y regresar una expresión del lenguaje de acuerdo a
# su sintaxis concreta. Esta expresión debe ser una estructura
# de acuerdo a la sintaxis abstracta.


# Reconocer la sintaxis concreta
# Expression ::= Number
# Expression ::= -(Expression, Expression)
# Expression ::= zero?(Expression)
# Expression ::= if Expression then Expression else Expression
# Expression ::= Identifier
# Expression ::= let Identifier = Expression in Expression
# Expression ::= proc(Identifier) Expression
# Expression ::= (Expression Expression)
# Expression ::= letrec Identifier (Identifier) Expression in Expression

import ply.yacc as yacc

from letrec_lexer import tokens
import letrec_ast as ast


def p_expression_const(p):
    "expression : NUM"
    p[0] = ast.ConstExp(int(p[1]))


def p_expression_diff(p):
    "expression : DIFF LPAREN expression COMMA expression RPAREN"
    p[0] = ast.DiffExp(p[3], p[5])


def p_expression_zero(p):
    "expression : ZERO LPAREN expression RPAREN"
    p[0] = ast.ZeroPExp(p[3])


def p_expression_if(p):
    "expression : IF expression THEN expression ELSE expression"
    p[0] = ast.IfExp(p[2], p[4], p[6])


def p_expression_var(p):
    "expression : ID"
    p[0] = ast.VarExp(p[1])


def p_expression_let(p):
    "expression : LET ID EQUAL expression IN expression"
    p[0] = ast.LetExp(p[2], p[4], p[6])


def p_expression_proc(p):
    "expression : PROC LPAREN ID RPAREN expression"
    p[0] = ast.ProcExp(p[3], p[5])


def p_expression_call(p):
    "expression : LPAREN expression expression RPAREN"
    p[0] = ast.CallExp(p[2], p[3])


def p_expression_letrec(p):
    "expression : LETREC ID LPAREN ID RPAREN EQUAL expression IN expression"
    p[0] = ast.LetrecExp(p[2], p[4], p[7], p[9])


def p_error(p):
    print("Syntax error in input!")


parser = yacc.yacc()

def parse(s):
    return parser.parse(s)

"""
def tests():
    while True:
        try:
            s = input("letrec > ")
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(result)

"""
#if __name__ == "__main__":
 #   tests()
