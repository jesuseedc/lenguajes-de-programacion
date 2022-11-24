# Semantica de expresiones con letrec

# (value-of (const-exp n) env) = (num-val n)
#
# (value-of (var-exp var) env) = env(var)
#
# (value-of (diff-exp exp1 exp2) env)
#   = (num-val (- (expval->num (value-of exp1 env))
#                 (expval->num (value-of exp2 env))))
#
# (value-of (zero?-exp exp1) env)
#   = (let ([val1 (value-of exp1 env)])
#     (bool-val (= 0 (expval->num val1))))
#
# (value-of (if-exp exp1 exp2 exp3) env)
#   = (if (expval->bool (value-of exp1 env)) (value-of exp2 env) (value-of exp3 env))
#
# (value-of (let-exp var exp1 body) env)
#   = (let ([val1 (value-of exp1 env)])
#       (value-of body [var = val1]env))
#
# (value-of (proc-exp var body) env) = (proc-val (procedure var body env))
#
# (value-of (call-exp op-exp arg-exp) env)
#   = (let ([proc (expval->proc (value-of op-exp env))]
#           [arg (value-of arg-exp env)])
#         (apply-procedure proc arg))
# donde:
# (apply-procedure (procedure var body env) val)
#   = (value-of body [var = val]env)
#
# (value-of (letrec-exp p-name b-var p-body letrec-body) env)
#   = (value-of letrec-body [p-name = b-var |-> p-body]env)
# donde:
# Si env_1 = [p-name = b-var |-> p-body]env, entonces
# (apply-env env_1 var) =
#  (proc-val (procedure b-var p-body env_1))
# si var = p-name, y 
#  (apply-env env_1 var) = (apply-env env var)
# si var != p-name.




