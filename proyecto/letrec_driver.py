import letrec_parser as parser
from letrec_env import Env
import letrec_semantix as semantix

def main():
    while True:
        try:
            text = input("letrec> ")
        except EOFError:
            break
        if text:
            exp = parser.parse(text)
            val = semantix.value_of(exp, Env.empty_env)
            print(val)

if __name__ == "__main__":
    main()
