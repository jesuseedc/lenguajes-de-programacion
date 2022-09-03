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
  (if (< x 0)
      (- x)
      x))

;; 7.
(define (inclis1 ls)
  (map (lambda (x) (+ x 1)) ls))


;; 8.
(define (even? x)
  (map (lambda (x) (if (= (modulo x 2) 0) #t #f)) x))

;; 9.
(define another-add
  (lambda (n m)
    (cond ((= n 0) m)
          ((= m 0) n)
          (else (+ n m)))))

(provide (all-defined-out))
