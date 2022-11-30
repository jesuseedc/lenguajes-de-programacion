from abc import ABC


class ExpVal(ABC):
    pass


class NumVal(ExpVal):
    def __init__(self, num):
        self.num = num

    def __repr__(self):
        return f"{self.num}"


class BoolVal(ExpVal):
    def __init__(self, bool):
        self.bool = bool

    def __repr__(self):
        return f"{self.bool}"


class ProcVal(ExpVal):
    def __init__(self, proc):
        self.proc = proc

    def __repr__(self):
        return f"[{self.proc}]"


class Proc:
    def __init__(self, var, body, env):
        self.var = var
        self.body = body
        self.env = env

    def __repr__(self):
        return f"λ{self.var}.{self.body} in {self.env}"

class ErrorVal(ExpVal):
    def __init__(self, error):
        self.error = error

    def __repr__(self):
        return f"{self.error}"
