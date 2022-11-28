# Entorno de evaluación de expresiones con letrec

import letrec_ast as ast

class Env:
    def __init__(self, parent=None):
        self.parent = parent
        self.bindings = {}

    def __getitem__(self, var):
        if var in self.bindings:
            return self.bindings[var]
        elif self.parent:
            return self.parent[var]
        else:
            raise Exception("Variable %s no definida" % var)

    def __setitem__(self, var, val):
        self.bindings[var] = val

    def __str__(self):
        return str(self.bindings)

    def __repr__(self):
        return str(self)

    def extend(self, var, val):
        new_env = Env(self)
        new_env[var] = val
        return new_env

    def extend_rec(self, p_name, b_var, p_body):
        new_env = Env(self)
        new_env.bindings[p_name] = ast.ProcVal(b_var, p_body, new_env)
        return new_env

    def apply_env(self, var):
        if var in self.bindings:
            return self.bindings[var]
        elif self.parent:
            return self.parent.apply_env(var)
        else:
            raise Exception("Variable %s no definida" % var)

    def extend_env(self, var, val):
        new_env = Env(self)
        new_env[var] = val
        return new_env

    def extend_env_rec(self, p_name, b_var, p_body):
        new_env = Env(self)
        new_env.bindings[p_name] = ast.ProcVal(b_var, p_body, new_env)
        return new_env

    def empty_env():
        return Env()






