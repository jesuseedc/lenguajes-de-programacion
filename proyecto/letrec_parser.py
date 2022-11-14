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

import ply.yacc as yacc
from letrec_lexer import tokens

def p_program(p):
    '''program : exp'''
    p[0] = p[1]

def p_exp_const(p):
    '''exp : CONST'''
    p[0] = ('const-exp', p[1])

def p_exp_diff(p):
    '''exp : LPAREN DIFF exp exp RPAREN'''
    p[0] = ('diff-exp', p[3], p[4])

"""def p_exp_zero(p):
    '''exp : LPAREN ZERO? exp RPAREN'''
    p[0] = ('zero?-exp', p[3])"""

def p_exp_if(p):
    '''exp : LPAREN IF exp exp exp RPAREN'''
    p[0] = ('if-exp', p[3], p[4], p[5])

def p_exp_var(p):
    '''exp : VAR'''
    p[0] = ('var-exp', p[1])

def p_exp_let(p):
    '''exp : LPAREN LET VAR exp exp RPAREN'''
    p[0] = ('let-exp', p[3], p[4], p[5])

def p_exp_proc(p):
    '''exp : LPAREN PROC VAR exp RPAREN'''
    p[0] = ('proc-exp', p[3], p[4])

def p_exp_call(p):
    '''exp : LPAREN CALL exp exp RPAREN'''
    p[0] = ('call-exp', p[3], p[4])

def p_exp_letrec(p):
    '''exp : LPAREN LETREC VAR VAR exp exp RPAREN'''
    p[0] = ('letrec-exp', p[3], p[4], p[5], p[6])

def p_error(p):
    print("Syntax error in input!")

parser = yacc.yacc()

if __name__ == '__main__':
    import sys
    prog = open(sys.argv[1]).read()
    result = parser.parse(prog)
    print(result)

# Path: proyecto\letrec-lexer.py
