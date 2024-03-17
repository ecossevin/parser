class Parser:
    """
    * One function per symbol (non-terminals & terminals)
    * Input = string 
    * Calling a function = attempting to parse the symbol it denotes at the current input position
    * A parsing function returns : . true if the symbol was matched, updating the input position past the matched input.
                                   . false if they failed to match, the input remains unchanged.
    Grammar : 
    VALUE ::= STRINGLIT / NUMBER / OBJECT / ARRAY
    OBJECT ::= "{" (PAIR ("," PAIR)* )? "}" 
    PAIR ::= STRINGLIT ":" VALUE 
    ARRAY ::= "[" (VALUE ("," VALUE)* )? "]"

    This parser implements PEG semantics for the grammar.
    """
    def __init__(self,to_parse):
        self.to_parse=to_parse
        self.idx=0
        self.size=len(self.to_parse)

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
    def parseString(self):
        #breakpoint()
        if self.idx>=self.size: return(False)
        if self.charAt() != '"': return(False)
        if '"' in self.to_parse[self.idx+1:]:
            last=self.to_parse[self.idx+1:].index('"')
        else:
            return(False)
        self.idx=self.idx+last+2
#        self.skipWhitespace()
        return(True)

    def parseNumber(self):
        #breakpoint()
        num=False
        if self.idx>=self.size: return(False)
        while self.idx<self.size and self.charAt().isnumeric(): #last element idx=size-1
            num=True
            self.idx+=1
        if num: 
#            self.skipWhitespace()
            return(True)
    # VALUE ::= STRINGLIT / NUMBER / OBJECT / ARRAY
    def parseValue(self):
        #breakpoint()
#        self.skipWhitespace()
        if (self.parseString() or self.parseNumber() or self.parseObject() or self.parseArray()):
#            self.skipWhitespace()
            return True
        else: 
            return False
    # OBJECT ::= "{" (PAIR ("," PAIR)* )? "}"
    def parseObject(self):
        #breakpoint()
        idx0=self.idx
        success = self.parseChar('{') and self.parsePairs() and self.parseChar('}')
        if not success :
            self.idx=idx0
        return success
    # (PAIR ("," PAIR)* )?
    def parsePairs(self):
        if (self.parsePair()): self.parsePairTails()
        return True
    # PAIR ::= STRINGLIT ":" VALUE
    def parsePair(self):
        idx0=self.idx        
        success = self.parseString() and self.parseChar(":") and self.parseValue()
        if not success : 
            self.idx=idx0
        return success
    # ("," PAIR)*
    def parsePairTails(self):
        while (True):
            idx0=self.idx
            success = self.parseChar(',') and self.parsePair()
            if not success : 
                self.idx=idx0
                return True # * -> can be no PAIR
    # ARRAY ::= "[" (VALUE ("," VALUE)* )? "]"
    def parseArray(self):
        #breakpoint()
        idx0=self.idx
        success = self.parseChar("[") and self.parseValues() and self.parseChar(']')
        if not success: 
            self.idx=idx0
        return success
    # (VALUE ("," VALUE)* )?
    def parseValues(self):
        if self.parseValue() : self.parseValueTails()
        return True #should be in if ?? 
    # ("," VALUE)*
    def parseValueTails(self):
        while (True):
            idx0=self.idx
            success=self.parseChar(',') and self.parseValue()
            if not success:
                self.idx=idx0
                return(True)
    def parseChar(self, char):
        if self.idx>=self.size:
            return(False)
        if self.charAt()==char:
            self.idx+=1
#            self.skipWhitespace()
            return(True)
        else:
            return(False)
    
         
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

#INPUT2="""
#<?xml version="1.0" encoding="UTF-8" ?>
#<hello>world</hello>
#"""
#INPUT2="""
#
#"""

mp = Parser(EXAMPLE_INPUT)
#mp = Parser(INPUT2)
if mp.parseValue():
    print("OK")
else:
    print("NO OK")
