from collections import deque
from typing import Callable, List, Any, Union

class Parser:

    def __init__(self,to_parse):
        self.to_parse=to_parse
        self.idx=0
        self.size=len(self.to_parse)
        self.stack=[]

    def isEnd(self) : 
        return(self.idx>self.size)
    def charAt_(self):
        return(self.to_parse[self.idx])
    def charAt(self):
       self.skipWhitespace()
       return(self.to_parse[self.idx])

    def skipWhitespace(self):
        while (self.idx<self.size and (self.charAt_() == " " or self.charAt_()=="\n")):
            self.idx+=1
    
    def parse_string_lit(self):
        #breakpoint()
        if self.idx>=self.size: return(False)
        if self.charAt() != '"': return(False)
        if '"' in self.to_parse[self.idx+1:]:
            last=self.to_parse[self.idx+1:].index('"')
            self.stack.append([self.to_parse[self.idx+1:self.idx+1+last]])
        else:
            return(False)
        self.idx=self.idx+last+2
#        self.skipWhitespace()
        return(True)

    def parseNumber(self):
        #breakpoint()
        is_num=False
        num=""
        if self.idx>=self.size: return(False)
        while self.idx<self.size and self.charAt().isnumeric(): #last element idx=size-1
            num+=self.charAt()
            is_num=True
            self.idx+=1
        if is_num: 
            self.stack.append([num])
#            self.skipWhitespace()
            return(True)
    def parse(self) -> bool:
        raise NotImplementedError("Method 'parse' must be implemented by subclasses.")

class Combinators(Parser):
    """
    Grammar : 
    VALUE ::= STRINGLIT / NUMBER / OBJECT / ARRAY
    OBJECT ::= "{" (PAIR ("," PAIR)* )? "}" 
    PAIR ::= STRINGLIT ":" VALUE 
    ARRAY ::= "[" (VALUE ("," VALUE)* )? "]"

    This parser implements PEG semantics for the grammar.
    """

    def __init__(self,to_parse):
       Parser.__init__(self, to_parse) 


    class StringLitParser(Parser):
        def parse(self) -> bool:
            return parse_string_lit()
    
    class NumberParser(Parser):
        def parse(self) -> bool:
            return parse_number()
    
    class CharParser(Parser):
        def __init__(self, c: str):
            self.c = c
    
        def parse(self) -> bool:
            return parse_char(self.c)
    
    class Sequence(Parser):
        def __init__(self, *children: Parser):
            self.children = children
    
        def parse(self) -> bool:
            self.idx0 = self.idx
            for child in self.children:
                if not child.parse():
                    self.idx = self.idx0
                    return False
            return True
    
    class ForwardReference(Parser):
        def __init__(self, supplier: Callable[[], Parser]):
            self.supplier = supplier
    
        def parse(self) -> bool:
            return self.supplier().parse()
    
    class Repetition(Parser):
        def __init__(self, child: Parser):
            self.child = child
    
        def parse(self) -> bool:
            while self.child.parse():
                pass
            return True
    
    class Optional(Parser):
        def __init__(self, child: Parser):
            self.child = child
    
        def parse(self) -> bool:
            self.child.parse()
            return True
    
    class Choice(Parser):
        def __init__(self, *children: Parser):
            self.children = children
    
        def parse(self) -> bool:
            for child in self.children:
                if child.parse():
                    return True
            return False
    
    class ComposeObject(Parser):
        def __init__(self, child: Parser):
            self.child = child
    
        def parse(self) -> bool:
            stack0 = len(self.stack)
            success = self.child.parse()
            if not success:
                return False
            obj = {}
            while len(self.stack) > stack0:
                value = self.stack.pop()
                string = self.stack.pop()
                obj[string] = value
            self.stack.append(obj)
            return True
    
    class ComposeArray(Parser):
        def __init__(self, child: Parser):
            self.child = child
    
        def parse(self) -> bool:
            stack0 = len(self.stack)
            success = self.child.parse()
            if not success:
                return False
            array = []
            while len(self.stack) > stack0:
                array.append(self.stack.pop())
            array.reverse()
            self.stack.append(array)
            return True
    
   
###pair, pair_tails
class Json_parser(Combinators):

    def __init__(self,to_parse):
       Combinators.__init__(self, to_parse) 

    # PAIR ::= STRINGLIT ":" VALUE
    pair = Sequence(StringLitParser(), CharParser(':'), ForwardReference(lambda: value))
    
    # ("," PAIR)*
    pair_tails = Repetition(Sequence(CharParser(','), pair))
    
    # (PAIR ("," PAIR)* )?
    pairs = Optional(Sequence(pair, pair_tails))
    
    # OBJECT  ::= "{" (PAIR ("," PAIR)* )? "}"
    object_parser = ComposeObject(Sequence(CharParser('{'), pairs, CharParser('}')))
    
    # ("," VALUE)*
    value_tails = Repetition(Sequence(CharParser(','), ForwardReference(lambda: value)))
    
    # (VALUE ("," VALUE)* )?
    values = Optional(Sequence(ForwardReference(lambda: value), value_tails))
    
    # ARRAY ::= "[" (VALUE ("," VALUE)* )? "]"
    array_parser = ComposeArray(Sequence(CharParser('['), values, CharParser(']')))
    
    # VALUE ::= STRINGLIT / NUMBER / OBJECT / ARRAY
    value = Choice(StringLitParser(), NumberParser(), object_parser, array_parser)


##########################################################        
##########################################################        
   
       

EXAMPLE_INPUT="""
{
    "version": 17,
    "bundles" : [
        { "name" : "org.gci.Bundle" },
        { "name" : "org.gci.commands.Bundle" },
        { "name" : "org.gci.installer.remote.Bundle" }, 
        { "name" : "org.gci.installer.os.Bundle" }
    ]
}
"""

INPUT2="""
{
  "key": "String",
  "Number": 1,
  "array": [1,2,3],
  "nested": {
       "literals": "true"
  }
}
"""

INPUT3="""
{
  "obj1" : { "a" : "A", "b" : "B"}
}
"""

#INPUT2="""
#<?xml version="1.0" encoding="UTF-8" ?>
#<hello>world</hello>
#"""
#INPUT2="""
#
#"""

#mp = Parser(EXAMPLE_INPUT)
#mp = Parser(INPUT2)

input_str = EXAMPLE_INPUT
mc = Combinators(input_str)
#mc = Json_parser(input_str)
mp = mc

if mp.value:
#if mp.parseValue():
    print("OK")
    print("input = ", mp.to_parse)
    print("stack = ", mp.stack)
else:
    print("NO OK")
