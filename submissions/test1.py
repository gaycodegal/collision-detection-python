

def fib(n):
    """gets the nth term of the fibonacci sequence inefficiently"""
    
    if n  <= 1:
        return n
    
    return fib(n - 1) + fib(n - 2)

def likelynoconflict():
    print("bacon") + 0
