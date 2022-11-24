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

    def __repr__(self):
        return f"<Const {self.num}>"


class DiffExp(LetrecExp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"<Diff {self.left} - {self.right}>"


class ZeroPExp(LetrecExp):
    def __init__(self, exp):
        self.exp = exp

    def __repr__(self):
        return f"<ZeroP {self.exp}>"


class IfExp(LetrecExp):
    def __init__(self, cond, thenb, elseb):
        self.cond = cond
        self.thenb = thenb
        self.elseb = elseb

    def __repr__(self):
        return f"<If {self.cond} Then {self.thenb} Else {self.elseb}>"


class VarExp(LetrecExp):
    def __init__(self, var):
        self.var = var

    def __repr__(self):
        return f"<Var {self.var}>"


class LetExp(LetrecExp):
    def __init__(self, var, exp, body):
        self.var = var
        self.exp = exp
        self.body = body

    def __repr__(self):
        return f"<Let {self.var} = {self.exp} in {self.body}>"


class ProcExp(LetrecExp):
    def __init__(self, var, body):
        self.var = var
        self.body = body

    def __repr__(self):
        return f"<Proc {self.var} => {self.body}>"


class CallExp(LetrecExp):
    def __init__(self, op, arg):
        self.op = op
        self.arg = arg

    def __repr__(self):
        return f"<Call {self.op} with {self.arg}>"


class LetrecExp(LetrecExp):
    def __init__(self, p_name, b_var, p_body, letrec_body):
        self.p_name = p_name
        self.b_var = b_var
        self.p_body = p_body
        self.letrec_body = letrec_body

    def __repr__(self):
        return f"<Letrec {self.p_name}({self.b_var}) = {self.p_body} in {self.letrec_body}>"
