from letrec_semantix import run_program
from letrec_parser import parse


def test(string):
    exp = parse(string)
    res = run_program(exp)
    print()
    print("El programa:", string)
    print("tiene valor:", res)


def run_tests():
    # test("1")
    # test("x") # debe señalar error
    # test("-(1, 2)")
    # test("zero?(0)")
    # test("zero?(1)")
    # test("if zero?(0) then 1 else 2")
    # test("if zero?(1) then 1 else 2")
    # test("let x = 1 in x")
    # test("let x = 1 in -(x,2)")
    # test("let x = 1 in zero?(x)")
    # test("let x = 1 in if zero?(x) then 1 else 2")
    # test("let x = 1 in if zero?(-(x,1)) then 1 else 2")
    # test("(proc (x) x 1)")
    # test("(proc (x) -(x, 1) 1)")
    # test("(proc (x) zero?(x) 1)")
    # test("(proc (x) if zero?(x) then 1 else 2 1)")
    # test("(proc (x) if zero?(-(x, 1)) then 1 else 2 1)")
    test("letrec p(x) = if zero?(x) then 0 else -((p -(x,1)),-(0,x)) in (p 0)")
    test("letrec p(x) = if zero?(x) then 0 else -((p -(x,1)),-(0,x)) in (p 1)")
    test("letrec p(x) = if zero?(x) then 0 else -((p -(x,1)),-(0,x)) in (p 2)")
    test("letrec p(x) = if zero?(x) then 0 else -((p -(x,1)),-(0,x)) in (p 3)")
    test("letrec p(x) = if zero?(x) then 0 else -((p -(x,1)),-(0,x)) in (p 4)")
    test("letrec p(x) = if zero?(x) then 0 else -((p -(x,1)),-(0,x)) in (p 5)")
    test("letrec p(x) = if zero?(x) then 0 else -((p -(x,1)),-(0,x)) in (p 6)")
