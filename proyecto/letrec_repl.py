# letrec repl, para salir escribir exit, para ayuda escribir help

from letrec_env import Env
from letrec_parser import parse
from letrec_semantix import run_program

def repl():
    print("Para salir escribir exit, para ayuda escribir help")
    env = Env()
    while True:
        try:
            string = input("letrec> ")
            if string == "exit":
                break
            elif string == "help":
                print("Interfaz textual para el lenguaje LETREC.\n"
                      "Introduzca una expresión LETREC, presione enter y "
                      "se mostrará el resultado de la evaluación.\n"
                      "Para salir escriba: exit y presione enter.")
            else:
                exp = parse(string)
                res = run_program(exp)
                print(res)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    repl()




