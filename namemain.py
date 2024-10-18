# namemain.py

def some_function():
    print(__name__, type(__name__))


if __name__=="__main__":
    some_function()