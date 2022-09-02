#lang racket

;; 1.
(define pi 3.14)

;; 2.
(define (area-circle r)
  (* pi (* r r)))

;; 3.
(define (circle-properties r)
  (list (* 2 (* pi r)) ()))

;; 4.
(define (rectangle-properties rec)
  (list (* (list-ref rec 0) (list-ref rec 1))
        (+ (* 2 (list-ref rec 0)) (* 2 (list-ref rec 1)))))

;; 5.
(define (find-needle ls)
  ...)

;; 6.
(define (abs x)
  ...)

;; 7.
(define (inclis1 ls)
  ...)

;; 8.
(define (even? x)
  ...)

;; 9.
(define another-add
  (lambda (n m)
    ...))

(provide (all-defined-out))
