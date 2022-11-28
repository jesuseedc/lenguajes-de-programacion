from abc import ABC
from letrec_ast import LetrecExp, ConstExp, DiffExp, ZeroPExp, IfExp, VarExp, LetExp, ProcExp, CallExp, LetrecExp
from letrec_env import Env

class ExpVal(ABC):
    pass

class NumVal(ExpVal):
    def __init__(self, num):
        self.num = num

    def __repr__(self):
        return f"<NumVal {self.num}>"

class BoolVal(ExpVal):
    def __init__(self, bool):
        self.bool = bool

    def __repr__(self):
        return f"<BoolVal {self.bool}>"

class ProcVal(ExpVal):
    def __init__(self, proc):
        self.proc = proc

    def __repr__(self):
        return f"<ProcVal {self.proc}>"

class Procedure:
    def __init__(self, var, body, env):
        self.var = var
        self.body = body
        self.env = env

    def __repr__(self):
        return f"<Procedure {self.var} {self.body} {self.env}>"

def expval_to_num(expval):
    if isinstance(expval, NumVal):
        return expval.num
    else:
        raise TypeError(f"Expected NumVal, got {expval}")

def expval_to_bool(expval):
    if isinstance(expval, BoolVal):
        return expval.bool
    else:
        raise TypeError(f"Expected BoolVal, got {expval}")

def expval_to_proc(expval):
    if isinstance(expval, ProcVal):
        return expval.proc
    else:
        raise TypeError(f"Expected ProcVal, got {expval}")

def value_of(exp, env):
    if isinstance(exp, ConstExp):
        return NumVal(exp.num)
    elif isinstance(exp, VarExp):
        return Env.apply_env(env, exp.var)
    elif isinstance(exp, DiffExp):
        val1 = value_of(exp.left, env)
        val2 = value_of(exp.right, env)
        return NumVal(expval_to_num(val1) - expval_to_num(val2))
    elif isinstance(exp, ZeroPExp):
        val1 = value_of(exp.exp1, env)
        return BoolVal(expval_to_num(val1) == 0)
    elif isinstance(exp, IfExp):
        val1 = value_of(exp.exp1, env)
        if expval_to_bool(val1):
            return value_of(exp.exp2, env)
        else:
            return value_of(exp.exp3, env)
    elif isinstance(exp, LetExp):
        val1 = value_of(exp.exp1, env)
        return value_of(exp.body, Env.extend_env(env, exp.var, val1))
    elif isinstance(exp, ProcExp):
        return ProcVal(Procedure(exp.var, exp.body, env))
    elif isinstance(exp, CallExp):
        proc = expval_to_proc(value_of(exp.op_exp, env))
        arg = value_of(exp.arg_exp, env)
        return apply_procedure(proc, arg)
    elif isinstance(exp, LetrecExp):
        return value_of(exp.letrec_body, Env.extend_env_rec(env, exp.p_name, exp.b_var, exp.p_body))
    else:
        raise TypeError(f"Unknown expression type {exp}")

def apply_procedure(proc, arg):
    return value_of(proc.body, Env.extend_env(proc.env, proc.var, arg))

def test():
    env = Env.empty_env()
    env = Env.extend_env(env, "x", NumVal(3))
    env = Env.extend_env(env, "y", NumVal(4))
    env = Env.extend_env(env, "z", NumVal(5))
    env = Env.extend_env(env, "f", ProcVal(Procedure("x", DiffExp(VarExp("x"), ConstExp(1)), env)))
    env = Env.extend_env(env, "g", ProcVal(Procedure("x", DiffExp(VarExp("x"), ConstExp(2)), env)))
    env = Env.extend_env(env, "h", ProcVal(Procedure("x", DiffExp(VarExp("x"), ConstExp(3)), env)))
    env = Env.extend_env(env, "k", ProcVal(Procedure("x", DiffExp(VarExp("x"), ConstExp(4)), env)))
    env = Env.extend_env(env, "p", ProcVal(Procedure("x", DiffExp(VarExp("x"), ConstExp(5)), env)))
    env = Env.extend_env(env, "q", ProcVal(Procedure("x", DiffExp(VarExp("x"), ConstExp(6)), env)))
    env = Env.extend_env(env, "r", ProcVal(Procedure("x", DiffExp(VarExp("x"), ConstExp(7)), env)))
    env = Env.extend_env(env, "s", ProcVal(Procedure("x", DiffExp(VarExp("x"), ConstExp(8)), env)))
    env = Env.extend_env(env, "t", ProcVal(Procedure("x", DiffExp(VarExp("x"), ConstExp(9)), env)))
    env = Env.extend_env(env, "u", ProcVal(Procedure("x", DiffExp(VarExp("x"), ConstExp(10)), env)))
    env = Env.extend_env(env, "v", ProcVal(Procedure("x", DiffExp(VarExp("x"), ConstExp(11)), env)))
    env = Env.extend_env(env, "w", ProcVal(Procedure("x", DiffExp(VarExp("x"), ConstExp(12)), env)))
    env = Env.extend_env(env, "a", ProcVal(Procedure("x", DiffExp(VarExp("x"), ConstExp(13)), env)))
    print(env)
    
test()