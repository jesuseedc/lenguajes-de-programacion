# Implementar un analizador sintáctico para el lenguaje LETREC
# El analizador sintáctico debe tomar de entrada un flujo lineal
# de tokens y regresar una expresión del lenguaje de acuerdo a
# su sintaxis concreta. Esta expresión debe ser una estructura
# de acuerdo a la sintaxis abstracta.

# Sintaxis abstracta:
# (const-exp num)
# (diff-exp exp1 exp2)
# (zero?-exp exp1)
# (if-exp exp1 exp2 exp3)
# (var-exp var)
# (let-exp var exp1 body)
# (proc-exp var body)
# (call-exp op-exp arg-exp)
# (letrec-exp p-name b-var p-body letrec-body)

from abc import ABC 

class LetrecExp(ABC):
    pass

class ConstExp(LetrecExp):
    def __init__(self, num):
        self.num = num

class DiffExp(LetrecExp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class ZeroPExp(LetrecExp):
    def __init__(self, exp):
        self.exp = exp

class IfExp(LetrecExp):
    def __init__(self, cond, thenb, elseb):
        self.cond = cond
        self.thenb = thenb
        self.elseb = elseb

class VarExp(LetrecExp):
    def __init__(self, var):
        self.var = var

class LetExp(LetrecExp):
    def __init__(self, var, exp, body):
        self.var = var
        self.exp = exp
        self.body = body

class ProcExp(LetrecExp):
    def __init__(self, var, body):
        self.var = var
        self.body = body

class CallExp(LetrecExp):
    def __init__(self, op, arg):
        self.op = op
        self.arg = arg

class LetrecExp(LetrecExp):
    def __init__(self, p_name, b_var, p_body, letrec_body):
        self.p_name = p_name
        self.b_var = b_var
        self.p_body = p_body
        self.letrec_body = letrec_body

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

def p_expression_const(p):
    'expression : CONST'
    p[0] = ConstExp(int(p[1]))

def p_expression_diff(p):
    'expression : DIFF LPAREN expression COMMA expression RPAREN'
    p[0] = DiffExp(p[3], p[5])

def p_expression_zero(p):
    'expression : ZERO LPAREN expression RPAREN'
    p[0] = ZeroPExp(p[3])

def p_expression_if(p):
    'expression : IF expression THEN expression ELSE expression'
    p[0] = IfExp(p[2], p[4], p[6])

def p_expression_var(p):
    'expression : VAR'
    p[0] = VarExp(p[1])

def p_expression_let(p):
    'expression : LET VAR EQUAL expression IN expression'
    p[0] = LetExp(p[2], p[4], p[6])

def p_expression_proc(p):
    'expression : PROC LPAREN VAR RPAREN expression'
    p[0] = ProcExp(p[3], p[5])

def p_expression_call(p):
    'expression : LPAREN expression expression RPAREN'
    p[0] = CallExp(p[2], p[3])

def p_expression_letrec(p):
    'expression : LETREC VAR LPAREN VAR RPAREN expression IN expression'
    p[0] = LetrecExp(p[2], p[4], p[6], p[8])

def p_error(p):
    print("Syntax error in input!")

parser = yacc.yacc()

# Pruebas
# (letrec f (x) (if (zero? x) 1 (- x 1)) in (f 5))

def tests():
    while True:
        try:
            s = input('letrec > ')
        except EOFError:
            break
        if not s: continue
        result = parser.parse(s)
        print(result)

if __name__ == '__main__':
    tests()




