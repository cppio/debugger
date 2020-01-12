def fibi(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a

def fibr(n):
    return n if n < 2 else fibr(n - 1) + fibr(n - 2)

def fib(n):
    i = fibi(10)
    r = fibr(10)
    return i, r

def main():
    f = fib(10)
    i, r = f

    print(i)
    print(r)

if __name__ == "__main__":
    print("fib.py v1")
    main()
