class Parser:
    def __init__(self,to_parse):
        self.to_parse=to_parse
        self.idx=0
        self.size=len(self.to_parse)
        self.stack=[]

    def charAt(self):
       return(self.to_parse[self.idx])

    def parseNumberParity(self, parity):
        is_num=False
        num=""
        if self.idx>=self.size: return(False)
        while (self.idx<self.size and self.charAt().isnumeric() and int(self.charAt())%2==parity): #last element idx=size-1
            num+=self.charAt()
            is_num=True
            self.idx+=1
        if is_num: 
            self.stack.append([num])
            return(True)

    def parseEvenNumber(self):
        return(self.parseNumberParity(0))

    def parseOddNumber(self):
        return(self.parseNumberParity(1))

    def parse(self) -> bool:
        raise NotImplementedError("Method 'parse' must be implemented by subclasses.")

#class Combinators():
#Module*

class parseEvenNumber(Parser):
    def parse(self) -> bool:
        return(self.parseEvenNumber())
class parseOddNumber(Parser):
    def parse(self) -> bool:
        return(self.parseOddNumber())

class Choice(Parser):
    def __init__(self, *children: Parser):
        self.children = children

    def parse(self) -> bool:
        for child in self.children:
            if child.parse():
                return True
        return False

#class ImplGrammar():
#Module*
    
class parseNumber(Parser):
    def parse(self) -> bool:
        return(Choice(parseEvenNumber(), parseOddNumber()).parse())

x=parseNumber("000")
y=x.parse()
print(x)
print(y)


