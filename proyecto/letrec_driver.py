# Controlador de la aplicación Letrec

import sys
import letrec_parser
import letrec_env as env
import letrec_semantix as sem

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 letrec_driver.py <archivo>")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        exp = letrec_parser.parse(f.read())
        print("Expresión leída:")
        print(exp)
        print("Valor de la expresión:")
        print(sem.value_of(exp, env.Env.empty_env()))

if __name__ == "__main__":
    main()

# Path: letrec_parser.py