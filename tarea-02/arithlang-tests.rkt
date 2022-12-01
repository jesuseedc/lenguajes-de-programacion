#lang plait

(require "arithlang.rkt")

(test (eval `(+ 1 2)) 3)
(test (eval `(* (+ 1 2) 3)) 9)
(test (eval `(+ (* 5 6) 6)) 36)
(test (eval `(- 10 5)) 5)
(test (eval `(+ 1 6)) 7)
(test (eval `(- (* (+ 1 2) 3) 4)) 5)




