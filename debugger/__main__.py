from . import *

if __name__ == "__main__":

    def fibi(n):
        a, b = 0, 1
        for i in range(n):
            a, b = b, a + b
        return a

    def fibr(n):
        return n if n < 2 else fibr(n - 1) + fibr(n - 2)

    def main():
        i = fibi(10)
        j = fibr(10)

    trace(main)
