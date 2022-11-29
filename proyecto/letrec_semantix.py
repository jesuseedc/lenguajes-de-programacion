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
    try: 
        if isinstance(exp, ConstExp):
            return NumVal(exp.num)
        elif isinstance(exp, DiffExp):
            return NumVal(expval_to_num(value_of(exp.left, env)) - expval_to_num(value_of(exp.right, env)))
        elif isinstance(exp, ZeroPExp):
            return BoolVal(expval_to_num(value_of(exp.exp, env)) == 0)
        elif isinstance(exp, IfExp):
            if expval_to_bool(value_of(exp.cond, env)):
                return value_of(exp.thenb, env)
            else:
                return value_of(exp.elseb, env)
        elif isinstance(exp, VarExp):
            return Env.lookup_env(env, exp.var)
        elif isinstance(exp, LetExp):
            return value_of(exp.body, Env.extend_env(env, exp.var, value_of(exp.exp, env)))
        elif isinstance(exp, ProcExp):
            return ProcVal(Procedure(exp.var, exp.body, env))
        elif isinstance(exp, CallExp):
            return apply_procedure(expval_to_proc(value_of(exp.op, env)), value_of(exp.arg, env))
        elif isinstance(exp, LetrecExp):
            return value_of(exp.letrec_body, Env.extend_env(env, exp.p_name, ProcVal(Procedure(exp.b_var, exp.p_body, env))))
        else:
            raise TypeError(f"Unknown expression type {exp}")
    except TypeError as e:
        print(f"Error: {e}")
        return None
        

def apply_procedure(proc, arg):
    return value_of(proc.body, Env.extend_env(proc.env, proc.var, arg))

def test():
    env = Env.empty_env()
    print(value_of(LetrecExp("fact", "n", IfExp(ZeroPExp(VarExp("n")), ConstExp(1), DiffExp(VarExp("n"), ConstExp(1))), CallExp(VarExp("fact"), ConstExp(5))), env))

if __name__ == "__main__":
    test()

