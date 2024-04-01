#https://gdevanla.github.io/posts/write-a-parser-combinator-in-python.html
#https://www.youtube.com/watch?v=1axJDmK_pnE


import operator 
import typing as tp

ParserP = tp.Callable[[str], tp.Tuple[tp.Any, str]]
#A simple parser
example_parser = lambda s: (s[0], s[1:])

class ParserError(Exception):
    def __init__(self, msg, content):
        super().__init__(f"{msg}: {content}")
#parse function here, can be used to run the parsers/parser combinators that will build below

def parse(p: ParserP, s: str) -> tp.Tuple[tp.Any, str]:
    (a, s) = p(s)
    return(a,s)

def anyChar() -> ParserP:
    def func(s):
        return(s[0], s[1:])
    return func

def oneChar(c) -> ParserP:
    def func(s):
        if s[0]==c:
            return(s[0],  s[1:])
        raise ParserError(f"Unexpected {s[0]}, expecting {c}", s)
    return func

def anyDigit() -> ParserP:
    def func(s):
        if s[0].isdigit():
            return(s[0], s[1:])
        raise ParserError(f"Expected digit, got {s[0]}", s)
    return func
out=parse(anyChar(), 'hello world!')
out=parse(oneChar('h'), 'hello world!')
print(out)
out=parse(anyDigit(), '234')
print(out)

def satisfy(pred_function: tp.Callable[["char"], bool]) -> ParserP:
    def func(s):
        if not s:
            raise ParserError("Empty string", "")
        if pred_function(s[0]):
            return(s[0], s[1:])
        raise ParserError(f"Unexpected condition", s)
    return func

def oneCharP(c) -> ParserP:
    return(satisfy(lambda c1: c==c1))

def anyDigitP() -> ParserP:
    return(satisfy(lambda c1: c1.isdigit()))

def compose(p1: ParserP, p2: ParserP) -> ParserP:
    def func(s):
        a1, s1 = parse(p1, s)
        a2, s2 = parse(p2, s1)
        return ((a1,a2), s2) #parser not necessarily returns a tuple (a1,a2); depends on the parser used.
    return func

hp = oneChar('h')
ep = oneChar('e')
parse(compose(hp, ep), "hello world")

def choiceP(p1: ParserP, p2: ParserP) -> ParserP:
    def func(s):
        try:
            return p1(s)
        except ParserError:
            return p2(s)
    return func

hp = oneChar('h')
ep = oneChar('H')
print(parse(choiceP(hp, ep), "hello world"))
print(parse(choiceP(hp, ep), "Hello world"))

def mathOp(op):
    return satisfy(lambda c: c == op )

#def mathOp(op):
#    def is_op(c):
#        if c==op:
#            if op == "+":
#                print("c=",c)
#                c=operator.add
#                print("c=",c)
#            return(True)
#        return(False)
#
#    return satisfy(lambda c: is_op(c))
def mathOpP() -> ParserP:
    plus = mathOp("+")  
    minus = mathOp("-")  
    mult = mathOp("*")  
    div = mathOp("/")  
    return choiceP(plus, choiceP(minus, choiceP(mult, minus)))

def expr_does_not_work():
    def func(s):
        (digit1, s1) = parse(anyDigitP(), s)
        (op, s2) = parse(mathOpP(), s1)
        (digit2, s3) = parse(anyDigitP(), s2) #this does not work

        return((int(digit1), op, int(digit2)), s3)
    return func

print(parse(expr_does_not_work(), "1+2"))

ParserF = tp.Callable[[tp.Any], ParserP]

def bind(p1: ParserP, pf: ParserF) -> ParserP:
    def func(s):
        (a,s1)=parse(p1,s)
        p2=pf(a)
        (b,s2)=parse(p2,s1)
        return(b,s2)

    return func



def mathOpP() -> ParserP:
    def f(op):
        if op == "+":
            return operator.add
        elif op == "-":
            return operator.sub
        elif op == "*":
            return operator.mul
        elif op == "/":
            return operator.floordiv

    plus = bind(mathOp("+"), lambda a: lambda s: (f(a), s)) #si "+" le parser est une fonction qui à s associe add.operator
    minus = bind(mathOp("-"), lambda a: lambda s: (f(a), s)) 
    mult = bind(mathOp("*"), lambda a: lambda s: (f(a), s)) 
    div = bind(mathOp("/"), lambda a: lambda s: (f(a), s)) 

    return choiceP(plus, choiceP(minus, choiceP(mult, minus)))

def expr_or_digit():
    return(choiceP(expr(), anyDigitP()))

def expr():
    def func(s):
        (digit1,s1) = parse(anyDigitP(), s)
        (op, s2) = parse(mathOpP(), s1)
        (digit2, s3) = parse(expr_or_digit(), s2)
        return (op(int(digit1), int(digit2)), s3)
    return func

print(parse(expr_or_digit(), "1+2+5*8"))


def strP(es: str) -> ParserP:
    def f2(c):
        def f(x):
            f1 = lambda xs: lambda s: (x+xs, s)
            return bind(oneCharP(c),  f1)
        return f

    def func(s):
        p = oneCharP(es[0])
        for c in es[1:]:
            p = bind(p, f2(c))
        return p(s)

    return func

print(parse(strP("toto!"), "toto!"))
