#lang racket

;; Escribe aquí tus soluciones

(define countdown
  (lambda (n)
    (if (= n 0)
        '(0)
        (cons n (countdown (- n 1))))))


(define insertL
  (lambda (sym1 sym2 lst)
    (cond
      [(null? lst) '()]
      [(eqv? (car lst) sym1) (cons sym2 (cons sym1 (insertL sym1 sym2 (cdr lst))))]
      [else (cons (car lst) (insertL sym1 sym2 (cdr lst)))])))

(provide (all-defined-out))
