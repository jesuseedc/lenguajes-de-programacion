#lang plait

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; EXPRESIONES DEL LENGUAJE EXTENDIDO ;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define-type Value
  (numV [n : Number])
  (strV [s : String])
  (boolV [b : Boolean])
  (funV [name : Symbol]
        [rg : Symbol]
        [body : ExprC]))

(define-type ExprS
  (numS [n : Number])
  (strS [s : String])
  (boolS [b : Boolean])
  (idS [name : Symbol])
  (ifS [a : ExprS] [b : ExprS] [c : ExprS])
  (andS [left : ExprS] [right : ExprS])
  (orS [left : ExprS] [right : ExprS])
  (letS [name : Symbol] [value : ExprS] [body : ExprS])
  (appS [func : ExprS] [arg : ExprS])
  (plusS [left : ExprS] [right : ExprS])
  (numeqS [left : ExprS] [right : ExprS])
  (streqS [left : ExprS] [right : ExprS])
  (notS [expr : ExprS])
  (bminusS [left : ExprS] [right : ExprS])
  (uminusS [expr : ExprS])
  (multS [left : ExprS] [right : ExprS])
  (zeropS [expr : ExprS]))

(define-type ExprC
  (numC [n : Number])
  (strC [s : String])
  (boolC [b : Boolean])
  (plusC [left : ExprC] [right : ExprC])
  (appC [left : ExprC] [right : ExprC])
  (numeqC [left : ExprC] [right : ExprC])
  (streqC [left : ExprC] [right : ExprC])
  (multC [left : ExprC] [right : ExprC])
  (idC [name : Symbol])
  (ifC [a : ExprC] [b : ExprC] [c : ExprC])
  (orC [left : ExprC] [right : ExprC])
  (andC [left : ExprC] [right : ExprC])
  (zeroC [expr : ExprC])
  (letC [name : Symbol] [value : ExprC] [body : ExprC]))


(define (bad-arg-to-op-error [op : Symbol] [v : Value])
  (error 'interp "argumento incorrecto"))

(define (bad-conditional-error [v : Value])
  (error 'interp "no es un valor booleano"))

(define (unbound-id-error [id : Symbol])
  (error 'interp "identificador no esta enlazado"))

(define-type Binding
  (binding [name : Symbol] [value : Value]))

(define-type-alias Environment (Listof Binding))

(define empty-env empty)

(define (lookup-env name env)
  (if (empty? env)
      (unbound-id-error name)
      (if (eq? name (binding-name (first env)))
          (binding-value (first env))
          (lookup-env name (rest env)))))

(define (extend-env name value env)
  (cons (binding name value) env))



;;;;;;;;;;;;;;;
;; EVALUADOR ;;
;;;;;;;;;;;;;;;

(define (eval [in : S-Exp]) : Value
  (interp (desugar (parse in)) empty-env))


;;;;;;;;;;;;;
;; DESUGAR ;;
;;;;;;;;;;;;;

(define (desugar [e : ExprS]) : ExprC
  (type-case ExprS e
    [(numS n) (numC n)]
    [(strS s) (strC s)]
    [(boolS b) (boolC b)]
    [(idS name) (idC name)]
    [(ifS a b c) (ifC (desugar a) (desugar b) (desugar c))]
    [(andS left right) (andC (desugar left) (desugar right))]
    [(orS left right) (orC (desugar left) (desugar right))]
    [(letS name value body) (letC name (desugar value) (desugar body))]
    [(plusS left right) (plusC (desugar left) (desugar right))]
    [(appS left right) (appC (desugar left) (desugar right))]
    [(numeqS left right) (numeqC (desugar left) (desugar right))]
    [(streqS left right) (streqC (desugar left) (desugar right))]
    [(notS expr) (ifC (desugar expr) (boolC #f) (boolC #t))]
    [(bminusS left right) (plusC (desugar left) (multC (desugar right) (numC -1)))]
    [(uminusS expr) (multC (desugar expr) (numC -1))]
    [(multS left right) (multC (desugar left) (desugar right))]
    [(zeropS expr) (zeroC (desugar expr))]))


;;;;;;;;;;;;
;; INTERP ;;
;;;;;;;;;;;;


(define (interp [e : ExprC] [env : Environment]) : Value
  (type-case ExprC e
    [(numC n) (numV n)]
    [(strC s) (strV s)]
    [(boolC b) (boolV b)]
    [(idC name) (lookup-env name env)]
    [(letC name value body)
      (interp body (extend-env name (interp value env) env))]
    [(ifC a b c)
      (let ([v1 (interp a env)])
        (cond [(not (boolV? v1))
               (bad-conditional-error v1)]
              [(boolV-b v1) 
                (interp b env)]
              [else 
                (interp c env)]))]
    [(appC left right) 
      (let ([v1 (interp left env)]
            [v2 (interp right env)])
        (cond [(not (strV? v1))
               (bad-arg-to-op-error 'append v1)]
              [(not (strV? v2))
               (bad-arg-to-op-error 'append v2)]
              [else
               (strV (string-append (strV-s v1) (strV-s v2)))]))]
    [(plusC left right)
      (let ([v1 (interp left env)]
            [v2 (interp right env)])
        (cond [(not (numV? v1))
               (bad-arg-to-op-error '+ v1)]
              [(not (numV? v2))
               (bad-arg-to-op-error '+ v2)]
              [else
               (numV (+ (numV-n v1) (numV-n v2)))]))]
    [(numeqC left right)
      (cond [(not (numV? (interp left env)))
             (bad-arg-to-op-error 'numeq? (interp left env))]
            [(not (numV? (interp right env)))
             (bad-arg-to-op-error 'numeq? (interp right env))]
            [else
             (boolV (equal? (numV-n (interp left env)) (numV-n (interp right env))))])]
    [(streqC left right)
      (cond [(not (strV? (interp left env)))
             (bad-arg-to-op-error 'streq? (interp left env))]
            [(not (strV? (interp right env)))
             (bad-arg-to-op-error 'streq? (interp right env))]
            [else
             (boolV (equal? (strV-s (interp left env)) (strV-s (interp right env))))])]
    [(multC left right)
      (let ([v1 (interp left env)]
            [v2 (interp right env)])
        (cond [(not (numV? v1))
               (bad-arg-to-op-error '* v1)]
              [(not (numV? v2))
               (bad-arg-to-op-error '* v2)]
              [else
               (numV (* (numV-n v1) (numV-n v2)))]))]
    [(andC left right)
      (let ([v1 (interp left env)]
            [v2 (interp right env)])
        (cond [(not (boolV? v1))
               (bad-conditional-error v1)]
              [(not (boolV? v2))
               (bad-conditional-error v2)]
              [else
               (boolV (and (boolV-b v1) (boolV-b v2)))]))]
    [(orC left right)
      (let ([v1 (interp left env)]
            [v2 (interp right env)])
        (cond [(not (boolV? v1))
               (bad-conditional-error v1)]
              [(not (boolV? v2))
               (bad-conditional-error v2)]
              [else
               (boolV (or (boolV-b v1) (boolV-b v2)))]))]
    [(zeroC expr)
      (let ([v (interp expr env)])
        (cond [(not (numV? v))
               (bad-arg-to-op-error 'zero? v)]
              [else
               (boolV (= (numV-n v) 0))]))]))

;;;;;;;;;;;;
;; PARSER ;;
;;;;;;;;;;;;

(define (parse-error e)
  (error 'parse "no es una funcion"))

(define (parse [in : S-Exp]) : ExprS
  (cond
    [(s-exp-number? in)                            (parse-number in)]
    [(s-exp-string? in)                            (parse-string in)]
    [(s-exp-match? `true in)                       (boolS #t)]
    [(s-exp-match? `false in)                      (boolS #f)]
    [(s-exp-list? in)
     (let ([ls (s-exp->list in)])
       (cond [(empty? ls)
              (parse-error ls)]
             [else
              (let ([tag (first ls)])
                (cond [(s-exp-symbol? tag)
                       (case (s-exp->symbol tag)

                         [(+)
                          (if (= (length ls) 3)
                              (plusS (parse (second ls))
                                     (parse (third ls)))
                              (parse-error ls))]
                         [(++)
                          (if (= (length ls) 3)
                              (appS (parse (second ls))
                                    (parse (third ls)))
                              (parse-error ls))]
                         [(num=)
                          (if (= (length ls) 3)
                              (numeqS (parse (second ls))
                                    (parse (third ls)))
                              (parse-error ls))]
                         [(str=)
                          (if (= (length ls) 3)
                              (streqS (parse (second ls))
                                    (parse (third ls)))
                              (parse-error ls))]
  
                         [(*)
                          (if (= (length ls) 3)
                              (multS (parse (second ls))
                                     (parse (third ls)))
                              (parse-error ls))]
                         [(-)
                          (let ([len (length ls)])
                            (cond [(= len 2)
                                   (uminusS (parse (second ls)))]
                                  [(= len 3)
                                   (bminusS (parse (second ls))
                                            (parse (third ls)))]
                                  [else
                                   (parse-error ls)]))]
                         [(or)
                          (let ([len (length ls)])
                            (if (= len 3)
                                (orS (parse (second ls))
                                     (parse (third ls)))
                                (parse-error ls)))]
                         [(and)
                          (let ([len (length ls)])
                            (if (= len 3)
                                (andS (parse (second ls))
                                      (parse (third ls)))
                                (parse-error ls)))]
                         [(not)
                          (let ([len (length ls)])
                            (if (= len 2)
                                (notS (parse (second ls)))
                                (parse-error ls)))]
                         [(if)
                          (let ([len (length ls)])
                            (if (= len 4)
                                (ifS (parse (second ls))
                                     (parse (third ls))
                                     (parse (fourth ls)))
                                (parse-error ls)))]
                         [(zero?)
                          (let ([len (length ls)])
                            (if (= len 2)
                                (zeropS (parse (second ls)))
                                (parse-error ls)))]
                         [(let)
                          (let ([len (length ls)])
                            (if (= len 3)
                                (let ([binding (second ls)]
                                      [body (third ls)])
                                  (if (s-exp-list? binding)
                                      (let ([binding (s-exp->list binding)])
                                        (if (= (length binding) 2)
                                            (let ([name (first binding)]
                                                  [value (second binding)])
                                              (if (s-exp-symbol? name)
                                                  (letS (s-exp->symbol name)
                                                        (parse value)
                                                        (parse body))
                                                  (parse-error ls)))
                                            (parse-error ls)))
                                      (parse-error ls)))
                                (parse-error ls)))])]
                      [else
                       (parse-error tag)]))]))]
    [(s-exp-symbol? in)
     (idS (s-exp->symbol in))]
    [else (parse-error in)]))
            

(define (parse-number in)
  (numS (s-exp->number in)))

(define (parse-string in)
  (strS (s-exp->string in)))


