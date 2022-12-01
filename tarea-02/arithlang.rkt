#lang plait


(define-type ArithC
  [numC (n : Number)]
  [plusC (e1 : ArithC) (e2 : ArithC)]
  [minusC (e1 : ArithC) (e2 : ArithC)]
  [multC (e1 : ArithC) (e2 : ArithC)])


(define-type ArithS
  [numS (n : Number)]
  [plusS (e1 : ArithS) (e2 : ArithS)]
  [minusS (e1 : ArithS) (e2 : ArithS)]
  [multS (e1 : ArithS) (e2 : ArithS)])

(define (parse [s : S-Exp]) : ArithS
    (cond [(s-exp-number? s) (numS (s-exp->number s))]
            [(s-exp-list? s)
            (let ([ls (s-exp->list s)])
                (case (s-exp->symbol (first ls))
                [(+) (plusS (parse (second ls)) (parse (third ls)))]
                [(-) (minusS (parse (second ls)) (parse (third ls)))]
                [(*) (multS (parse (second ls)) (parse (third ls)))]
                [else (error 'parse "operación aritmetica malformada")]))]
            [else (error 'parse "expresión aritmetica malformada")]))

(define (desugar [e : ArithS]) : ArithC
    (cond [(numS? e) (numC (numS-n e))]
            [(plusS? e) (plusC (desugar (plusS-e1 e)) (desugar (plusS-e2 e)))]
            [(minusS? e) (minusC (desugar (minusS-e1 e)) (desugar (minusS-e2 e)))]
            [(multS? e) (multC (desugar (multS-e1 e)) (desugar (multS-e2 e)))]))

(define (interp [e : ArithC]) : Number
    (cond [(numC? e) (numC-n e)]
            [(plusC? e) (+ (interp (plusC-e1 e)) (interp (plusC-e2 e)))]
            [(minusC? e) (- (interp (minusC-e1 e)) (interp (minusC-e2 e)))]
            [(multC? e) (* (interp (multC-e1 e)) (interp (multC-e2 e)))]))

(define (eval [input : S-Exp]) : Number
    (interp (desugar (parse input))))

