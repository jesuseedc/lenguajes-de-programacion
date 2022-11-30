from abc import ABC

from letrec_ast import (
    CallExp,
    ConstExp,
    DiffExp,
    IfExp,
    LetExp,
    LetrecExp,
    ProcExp,
    VarExp,
    ZeroPExp,
)
from letrec_env import Env
from letrec_vals import NumVal, BoolVal, ProcVal, Proc, ErrorVal


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


def apply_procedure(proc, arg):
    return value_of(proc.body, Env.extend_env(proc.env, proc.var, arg))

debug = False

def value_of(exp, env):
    if(debug):
        print(f"value of {exp} in environment {env}")
    if isinstance(exp, ConstExp):
        return NumVal(exp.num)
    elif isinstance(exp, DiffExp):
        return NumVal(
            expval_to_num(value_of(exp.left, env))
            - expval_to_num(value_of(exp.right, env))
        )
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
        return ProcVal(Proc(exp.var, exp.body, env))
    elif isinstance(exp, CallExp):
        return apply_procedure(
            expval_to_proc(value_of(exp.op, env)), value_of(exp.arg, env)
        )
    elif isinstance(exp, LetrecExp):
        return value_of(
            exp.letrec_body,
            env.extend_env_rec(exp.p_name, exp.b_var, exp.p_body),
        )
    else:
        raise TypeError(f"Unknown expression type {exp}")
        
def run_program(exp):
    try:
        return value_of(exp, Env.empty_env())
    except TypeError as e:
        print(f"Ocurrió un error!: {e}")
        return ErrorVal(e)
        """
    except Exception as e:
        print(f"Ocurrió un error!: {e}")
        return None
        """

def test():
    env = Env.empty_env()
    print(
        value_of(
            LetrecExp(
                "fact",
                "n",
                IfExp(
                    ZeroPExp(VarExp("n")),
                    ConstExp(1),
                    DiffExp(VarExp("n"), ConstExp(1)),
                ),
                CallExp(VarExp("fact"), ConstExp(0)),
            ),
            env,
        )
    )

# if __name__ == "__main__":
#     test()
