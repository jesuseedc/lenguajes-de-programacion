#lang eopl 

;;;;;;;;;;;;;;; Grammar ;;;;;;;;;;;;;;;

(define the-lexical-spec
  '((whitespace (whitespace) skip)
    (comment ("%" (arbno (not #\newline))) skip)
    (identifier
     (letter (arbno (or letter digit "_" "-" "?")))
     symbol)
    (number (digit (arbno digit)) number)
    (number ("-" digit (arbno digit)) number)
    ))

(define the-grammar
  '((program (expression) a-program)

    (expression (number) const-exp)
    (expression
     ("-" "(" expression "," expression ")")
     diff-exp)
    (expression
     ("zero?" "(" expression ")")
     zero?-exp)
    (expression
     ("if" expression "then" expression "else" expression)
     if-exp)
    (expression (identifier) var-exp)
    (expression
     ("let" identifier "=" expression "in" expression)
     let-exp)
    (expression
     ("proc" "(" identifier ")" expression)
     proc-exp)
    (expression
     ("(" expression expression ")")
     call-exp)
    (expression
     ("letrec"
      (arbno identifier "(" identifier ")" "=" expression)
      "in" expression)
     letrec-exp)
    (expression
     ("begin" expression (arbno ";" expression) "end")
     begin-exp)
    (expression
     ("newref" "(" expression ")")
     newref-exp)
    (expression
     ("deref" "(" expression ")")
     deref-exp)
    (expression
     ("setref" "(" expression "," expression ")")
     setref-exp)
    ;;new stuff
    (expression ("emptylist") emptylist-exp)
    (expression ("list" "(" (separated-list expression ",") ")" ) list-exp)))

(sllgen:make-define-datatypes the-lexical-spec the-grammar)

(define show-the-datatypes
  (lambda () (sllgen:list-define-datatypes the-lexical-spec the-grammar)))

(define scan&parse
  (sllgen:make-string-parser the-lexical-spec the-grammar))


;;;;;;;;;;;;;; Data structures ;;;;;;;;;;;;;;

(define (reference? v)
    (and (integer? v)
         (not (negative? v))))

(define-datatype expval expval?
  (num-val
   (value number?))
  (bool-val
   (boolean boolean?))
  (proc-val
   (proc proc?))
  (ref-val
   (ref reference?))
  (pair-val
   (car expval?)
   (cdr expval?))
  (emptylist-val)
  )

(define expval->num
  (lambda (v)
    (cases expval v
           (num-val (num) num)
           (else (expval-extractor-error 'num v)))))

(define expval->bool
  (lambda (v)
    (cases expval v
           (bool-val (bool) bool)
           (else (expval-extractor-error 'bool v)))))

(define expval->proc
  (lambda (v)
    (cases expval v
           (proc-val (proc) proc)
           (else (expval-extractor-error 'proc v)))))

(define expval->ref
  (lambda (v)
    (cases expval v
           (ref-val (ref) ref)
           (else (expval-extractor-error 'reference v)))))

(define expval-extractor-error
  (lambda (variant value)
    (eopl:error 'expval-extractors "Looking for a ~s, found ~s"
           variant value)))

(define-datatype proc proc?
  (procedure
   (bvar symbol?)
   (body expression?)
   (env environment?)))

;;;;;;;;;;;;;; Environments ;;;;;;;;;;;;;;

(define-datatype environment environment?
  (empty-env)
  (extend-env
   (bvar symbol?)
   (bval expval?)
   (saved-env environment?))
  (extend-env-rec*
   (proc-names (list-of symbol?))
   (b-vars (list-of symbol?))
   (proc-bodies (list-of expression?))
   (saved-env environment?)))

(define init-env
  (lambda ()
    (empty-env)))

(define apply-env
  (lambda (env search-sym)
    (cases environment env
           (empty-env ()
                      (eopl:error 'apply-env "No binding for ~s" search-sym))
           (extend-env (bvar bval saved-env)
                       (if (eqv? search-sym bvar)
                           bval
                           (apply-env saved-env search-sym)))
           (extend-env-rec* (p-names b-vars p-bodies saved-env)
                            (cond
                             ((location search-sym p-names)
                              => (lambda (n)
                                   (proc-val
                                    (procedure
                                     (list-ref b-vars n)
                                     (list-ref p-bodies n)
                                     env))))
                             (else (apply-env saved-env search-sym)))))))

(define location
  (lambda (sym syms)
    (cond
     ((null? syms) #f)
     ((eqv? sym (car syms)) 0)
     ((location sym (cdr syms))
      => (lambda (n)
           (+ n 1)))
     (else #f))))


(define env->list
  (lambda (env)
    (cases environment env
           (empty-env () '())
           (extend-env (sym val saved-env)
                       (cons
                        (list sym (expval->printable val))
                        (env->list saved-env)))
           (extend-env-rec* (p-names b-vars p-bodies saved-env)
                            (cons
                             (list 'letrec p-names '...)
                             (env->list saved-env))))))

(define expval->printable
  (lambda (val)
    (cases expval val
           (proc-val (p)
                     (cases proc p
                            (procedure (var body saved-env)
                                       (list 'procedure var '... (env->list saved-env)))))
           (else val))))



(define instrument-let (make-parameter #f))

(define value-of-program
  (lambda (pgm)
    (initialize-store!)              
    (cases program pgm
           (a-program (exp1)
                      (value-of exp1 (init-env))))))

(define list-val
  (lambda (args)
    (if (null? args)
        (emptylist-val)
        (pair-val (car args)
                  (list-val (cdr args))))))

(define apply-elm
  (lambda (env)
    (lambda (elem)
      (value-of elem env))))

(define value-of
  (lambda (exp env)
    (cases expression exp
           (const-exp (num) (num-val num))
           (var-exp (var) (apply-env env var))

           (diff-exp (exp1 exp2)
                     (let ((val1 (value-of exp1 env))
                           (val2 (value-of exp2 env)))
                       (let ((num1 (expval->num val1))
                             (num2 (expval->num val2)))
                         (num-val
                          (- num1 num2)))))

           (zero?-exp (exp1)
                      (let ((val1 (value-of exp1 env)))
                        (let ((num1 (expval->num val1)))
                          (if (zero? num1)
                              (bool-val #t)
                              (bool-val #f)))))

           (if-exp (exp1 exp2 exp3)
                   (let ((val1 (value-of exp1 env)))
                     (if (expval->bool val1)
                         (value-of exp2 env)
                         (value-of exp3 env))))

           (let-exp (var exp1 body)
                    (let ((val1 (value-of exp1 env)))
                      (value-of body
                                (extend-env var val1 env))))

           (proc-exp (var body)
                     (proc-val (procedure var body env)))

           (call-exp (rator rand)
                     (let ((proc (expval->proc (value-of rator env)))
                           (arg (value-of rand env)))
                       (apply-procedure proc arg)))

           (letrec-exp (p-names b-vars p-bodies letrec-body)
                       (value-of letrec-body
                                 (extend-env-rec* p-names b-vars p-bodies env)))

           (begin-exp (exp1 exps)
                      (letrec
                          ((value-of-begins
                            (lambda (e1 es)
                              (let ((v1 (value-of e1 env)))
                                (if (null? es)
                                    v1
                                    (value-of-begins (car es) (cdr es)))))))
                        (value-of-begins exp1 exps)))

           (newref-exp (exp1)
                       (let ((v1 (value-of exp1 env)))
                         (ref-val (newref v1))))

           (deref-exp (exp1)
                      (let ((v1 (value-of exp1 env)))
                        (let ((ref1 (expval->ref v1)))
                          (deref ref1))))

           (setref-exp (exp1 exp2)
                       (let ((ref (expval->ref (value-of exp1 env))))
                         (let ((v2 (value-of exp2 env)))
                           (begin
                             (setref! ref v2)
                             (num-val 1)))))
	   (emptylist-exp ()
			  (emptylist-val))
	   (list-exp (vars)
		     (list-val (map (apply-elm env) vars)))
           )))

(define (apply-procedure proc1 args store)
  (cases proc proc1
    [procedure (bvars body saved-env) 
                (let ([body-env (let loop ([bvars bvars]
                                           [args args]
                                           [env saved-env])
                                          (if (null? bvars)
                                                env
                                                (loop (cdr bvars)
                                                      (cdr args)
                                                      (extend-env (car bvars)
                                                                  (car args)
                                                                  env))))])
                                        (value-of body
                                                  body-env
                                                  store))]))

(define store->readable
  (lambda (l)
    (map
     (lambda (p)
       (cons
        (car p)
        (expval->printable (cadr p))))
     l)))


(define run
  (lambda (string)
    (value-of-program (scan&parse string))))


;;;;;;;;;; Store ;;;;;;;;;;;;

(define store? (list-of expval?))

(define (make-store)
  (vector))

(define the-store 'uninitialized)

(define (get-store)
  (if (eq? the-store 'uninitialized)
      (begin (set! the-store (make-store))
             the-store)
      the-store))

(define (initialize-store!)
  (set! the-store (make-store)))

(define (extend-store store val)
    (let* ([store-size (vector-length store)]
           [new-store (make-vector (+ store-size 1))])
    (let loop ([i 0])
        (if (< i store-size)
            (let ([val (vector-ref store i)])
                (vector-set! new-store i val)
                (loop (+ i 1)))
            (vector-set! new-store i val)))
        (cons new-store store-size)))

(define (newref val)
    (let* ([new-store-info (extend-store (get-store) val)]
           [new-store (car new-store-info)]
           [new-ref (cdr new-store-info)])
        (set! the-store new-store)
        new-ref))

(define (deref ref)
    (vector-ref the-store ref))

(define (invalid-reference ref store)
    (eopl:error 'setref
                "invalid reference"
                ref
                store))

(define (setref! ref val)
    (if (and (reference? ref)
             (< ref (vector-length the-store)))
        (vector-set! the-store ref val)
        (invalid-reference ref the-store)))

