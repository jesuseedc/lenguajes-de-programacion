#lang racket

;; Escribe aquí tus soluciones

(define countdown
  (lambda (n)
    (if (= n 0)
        '(0)
        (cons n (countdown (- n 1))))))


(define insertL
  (lambda (c1 c2 lst)
    (cond
      [(null? lst) '()]
      [(eqv? (car lst) c1) (cons c2 (cons c1 (insertL c1 c2 (cdr lst))))]
      [else (cons (car lst) (insertL c1 c2 (cdr lst)))])))


(define remv-1st
  (lambda (sym lst)
    (cond
      [(null? lst) '()]
      [(eqv? (car lst) sym) (cdr lst)]
      [else (cons (car lst) (remv-1st sym (cdr lst)))])))


(define map
  (lambda (p ls)
    (cond
      [(null? ls) '()]
      [else (cons (p (car ls)) (map p (cdr ls)))])))


(define filter
  (lambda (p ls)
    (cond
      [(null? ls) '()]
      [(p (car ls)) (cons (car ls) (filter p (cdr ls)))]
      [else (filter p (cdr ls))])))


(define zip
  (lambda (ls1 ls2)
    (cond
      [(and (null? ls1) (null? ls2)) '()]
      [(and (null? ls1) (not (null? ls2))) '()]
      [(and (not (null? ls1)) (null? ls2)) '()]
      [else (cons (cons (car ls1) (car ls2)) (zip (cdr ls1) (cdr ls2)))])))


(define list-index-ofv
  (lambda (elem lst)
    (define aux
      (lambda (elem lst index)
        (cond
          [(null? lst) -1]
          [(eqv? (car lst) elem) index]
          [else (aux elem (cdr lst) (+ index 1))])))
    (aux elem lst 0)))


(define append
  (lambda (ls1 ls2)
    (cond
      [(null? ls1) ls2]
      [else (cons (car ls1) (append (cdr ls1) ls2))])))


(define reverse
  (lambda (lst)
    (cond
      [(null? lst) '()]
      [else (append (reverse (cdr lst)) (cons (car lst) '()))])))


(define repeat
  (lambda (lst n)
    (cond
      [(= n 0) '()]
      [else (append lst (repeat lst (- n 1)))])))


(define same-lists*
  (lambda (lst1 lst2)
    (cond
      [(and (null? lst1) (null? lst2)) #t]
      [(and (null? lst1) (not (null? lst2))) #f]
      [(and (not (null? lst1)) (null? lst2)) #f]
      [(and (not (null? lst1)) (not (null? lst2)))
       (and (same-lists* (car lst1) (car lst2)) (same-lists* (cdr lst1) (cdr lst2)))]
      [else #f])))


(define binary->natural
  (lambda (lst)
    (define aux
      (lambda (lst index)
        (cond
          [(null? lst) 0]
          [(eqv? (car lst) 1) (+ (expt 2 index) (aux (cdr lst) (+ index 1)))]
          [else (aux (cdr lst) (+ index 1))])))
    (aux lst 0)))


(define div
  (lambda (n m)
    (cond
      [(< n m) 0]
      [else (+ 1 (div (- n m) m))])))


(define append-map
  (lambda (p ls)
    (cond
      [(null? ls) '()]
      [else (append (p (car ls)) (append-map p (cdr ls)))])))


(define set-difference
  (lambda (s1 s2)
    (cond
      [(null? s1) '()]
      [(member (car s1) s2) (set-difference (cdr s1) s2)]
      [else (cons (car s1) (set-difference (cdr s1) s2))])))


(define foldr
  (lambda (op init lst)
    (cond
      [(null? lst) init]
      [else (op (car lst) (foldr op init (cdr lst)))])))


(define powerset
  (lambda (lst)
    (cond
      [(null? lst) (list '())]
      [else (let ([rest (powerset (cdr lst))])
              (append rest (map (lambda (x) (cons (car lst) x)) rest)))])))


(define cartesian-product
  (lambda (lst)
    (cond
      [(null? lst) (list '())]
      [else (let ([rest (cartesian-product (cdr lst))])
              (append-map (lambda (x) (map (lambda (y) (cons x y)) rest)) (car lst)))])))


(define snowball
  (lambda (n)
    (if (= n 1)
        1
        (snowball (if (= (remainder n 2) 0)
                      (/ n 2)
                      (+ (* 3 n) 1))))))

(provide (all-defined-out))
