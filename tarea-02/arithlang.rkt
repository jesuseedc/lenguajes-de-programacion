#lang plait

(define (eval [input : S-Exp]) : Number
    (interp (desugar (parse input))))

(define (parse [s : S-Exp]) : ArithC 
    (cond [(s-exp-number? s) (numC (s-exp->number s))]
          [(s-exp list? s)
            (let ([ls (s-exp->list s)
                (case (s-exp->symbol (first ls))
                    [(+) (plusC (parse (second ls)) (parse (third ls)))]
                    [(*) (multC (parse (second ls)) (parse (third ls)))]
                    [else (error 'parse "operacion aritmetica mal formada")])]
                [else (error 'parse "expresion aritmetica mal formada")]))
                