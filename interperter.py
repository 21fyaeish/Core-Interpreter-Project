import sys
import scanner

class Program:  
    def __init__(self, dataFile):
        self.ds = None
        self.ss = None
        self.data = dataFile

    def parseProgram(self, tokenizer):
        #check for program
        if(tokenizer.getToken() != 1):
            print("error: program token missing")
            sys.exit(1)
        
        #skip "program" keyword
        tokenizer.skipToken()

        #parse decl seq
        Id.phase = 1
        self.ds = DeclSeq()
        self.ds.parseDeclSeq(tokenizer)

        #check for begin
        if(tokenizer.getToken() != 2):
            print("error: begin token missing")
            sys.exit(1)
        
        #skip "begin" keyword
        tokenizer.skipToken()
        
        #parse stmt seq
        Id.phase = 2
        self.ss = StmtSeq()
        self.ss.parseStmtSeq(tokenizer)

        #check for end
        if(tokenizer.getToken() != 3):
            print("error: end token missing in program")
            sys.exit(1)
        
        #skip "end" keyword
        tokenizer.skipToken()

    def printProgram(self, indent):
        print("program")
        self.ds.printDeclSeq(indent)
        print("begin")
        self.ss.printStmtSeq(indent)
        print("end")
        
    def executeProgram(self):
        #execute stmt seq
        self.ss.executeStmtSeq(self.data)
        
class DeclSeq:
    def __init__(self):
        self.d = None
        self.ds = None

    def parseDeclSeq(self, tokenizer):
        #parse decl and move to next token
        self.d = Decl()
        self.d.parseDecl(tokenizer)


        if(tokenizer.getToken() == 4):
            #parse decl seq and move to next token
            self.ds = DeclSeq()
            self.ds.parseDeclSeq(tokenizer)
        
    
    def printDeclSeq(self, indent):
        #print decl
        print(indent, end="")
        self.d.printDecl(indent)

        #print decl seq if it exists
        if(self.ds != None):
            self.ds.printDeclSeq(indent)

class StmtSeq:
    def __init__(self):
        self.s = None
        self.ss = None

    def parseStmtSeq(self, tokenizer):
        #parse stmt and move to next token
        self.s = Stmt()
        self.s.parseStmt(tokenizer)

        if(tokenizer.getToken() in [32, 5, 8, 10, 11]):
            #parse stmt seq and move to next token
            self.ss = StmtSeq()
            self.ss.parseStmtSeq(tokenizer)
    
    def printStmtSeq(self, indent):
        #print stmt
        print(indent, end="")
        self.s.printStmt(indent)

        #print stmt seq if it exists
        if(self.ss != None):
            self.ss.printStmtSeq(indent)
    
    def executeStmtSeq(self, data):
        #execute stmt
        self.s.executeStmt(data)

        #execute stmt seq if it exists
        if(self.ss != None):
            self.ss.executeStmtSeq(data)

class Decl:
    def __init__(self):
        self.idList = None
    
    def parseDecl(self, tokenizer):
        #check for int
        if(tokenizer.getToken() != 4):
            print("error: int token missing")
            sys.exit(1)
        
        #skip "int" keyword
        tokenizer.skipToken()

        #parse id list and move to next token
        self.idList = IdList()
        self.idList.parseIdList(tokenizer)

        #check for ;
        if(tokenizer.getToken() != 12):
            print("error: ; token missing in decl")
            sys.exit(1)

        #skip ";" special symbol
        tokenizer.skipToken()

    
    def printDecl(self, indent):
        print("int ", end="")
        self.idList.printIdList(indent)
        print(";")
    
    

class IdList:
    def __init__(self):
        self.id = None
        self.idlist = None

    def parseIdList(self, tokenizer):

        #parse id and move to next token
        self.id = Id.parseId(tokenizer)

        if(tokenizer.getToken() == 13):
            #skip "," special symbol
            tokenizer.skipToken()

            if(tokenizer.getToken() != 32):
                print("error: id token missing in id list")
                sys.exit(1)
            
            #parse idList and move to next token
            self.idlist = IdList()
            self.idlist.parseIdList(tokenizer)

    
    def printIdList(self, indent):
        #print id
        self.id.printId(indent)
        

        #print id list if it exists
        if(self.idlist != None):
            print(", ", end="")
            self.idlist.printIdList(indent)
    
    def executeInIdList(self, data):
        line = data.readline()
        value = int(line.strip())
        self.id.setIdVal(value)

    def executeOutIdList(self):
        print(str(self.id.getIdName()) + " = " + str(self.id.getIdVal()) + "\n")
    
class Stmt:
    def __init__(self):
        self.altNum = 0
        self.assign = None
        self.IF = None
        self.LOOP = None
        self.IN = None
        self.OUT = None

    def parseStmt(self, tokenizer):

        tokenNum = tokenizer.getToken()

        if(tokenNum == 32):
            self.altNum = 1
            self.assign = Assign()
            self.assign.parseAssign(tokenizer)
        elif(tokenNum == 5): 
            self.altNum = 2
            self.IF = If()
            self.IF.parseIf(tokenizer)
        elif(tokenNum == 8):
            self.altNum = 3
            self.LOOP = Loop()
            self.LOOP.parseLoop(tokenizer)
        elif(tokenNum == 10):
            self.altNum = 4
            self.IN = In()
            self.IN.parseIn(tokenizer)
        elif(tokenNum == 11):
            self.altNum = 5
            self.OUT = Out()
            self.OUT.parseOut(tokenizer)
        else:
            print("error: incorrect stmt")
            sys.exit(1)
        
    
    def printStmt(self, indent):
        if(self.altNum == 1):
            self.assign.printAssign(indent)
        elif(self.altNum == 2):
            self.IF.printIf(indent)
        elif(self.altNum == 3):
            self.LOOP.printLoop(indent)
        elif(self.altNum == 4):
            self.IN.printIn(indent)
        elif(self.altNum == 5):
            self.OUT.printOut(indent)
        

    def executeStmt(self, data):
        if(self.altNum == 1):
            self.assign.executeAssign()
        elif(self.altNum == 2):
            self.IF.executeIf(data)
        elif(self.altNum == 3):
            self.LOOP.executeLoop(data)
        elif(self.altNum == 4):
            self.IN.executeIn(data)
        elif(self.altNum == 5):
            self.OUT.executeOut()
            

class Assign:
    def __init__(self):
        self.id = None
        self.exp = None

    def parseAssign(self, tokenizer):
        #parse id and move to next token
        self.id = Id.parseId(tokenizer)

        #check for =
        if(tokenizer.getToken() != 14):
            print("error: = token missing")
            sys.exit(1)
        
        #skip "=" special symbol
        tokenizer.skipToken()

        #parse exp and move to next token
        self.exp = Exp()
        self.exp.parseExp(tokenizer)

        #check for ;
        if(tokenizer.getToken() != 12):
            print("error: ; token missing in assign")
            sys.exit(1)
        
        #skip ";" special symbol
        tokenizer.skipToken()
    
    def printAssign(self, indent):
        self.id.printId(indent)
        print(" = ", end="")
        self.exp.printExp(indent)
        print(";")

    def executeAssign(self):
        self.id.setIdVal(self.exp.evalExp())


class If:
    def __init__(self):
        self.c = None
        self.ss1 = None
        self.ss2 = None

    def parseIf(self, tokenizer):
        #check for if
        if(tokenizer.getToken() != 5):
            print("error: if token missing")
            sys.exit(1)
        
        #skip "if" reserved word
        tokenizer.skipToken()

        #parse condition and move to next token
        self.c = Cond()
        self.c.parseCond(tokenizer)

        #check for then
        if(tokenizer.getToken() != 6):
            print("error: then token missing")
            sys.exit(1)
        
        #skip "then" reserved word
        tokenizer.skipToken()

        #parse stmtseq1 and move to next token
        self.ss1 = StmtSeq()
        self.ss1.parseStmtSeq(tokenizer)

        #check if current token is "end" keyword
        if(tokenizer.getToken() == 3):
            tokenizer.skipToken()
            tokenizer.skipToken()
            return
        
        #check for else
        if(tokenizer.getToken() != 7):
            print("Error: else token missing")
            sys.exit(1)
        
        #skip "else" reserved word
        tokenizer.skipToken()

        #parse stmtseq2 and move to next token
        self.ss2 = StmtSeq()
        self.ss2.parseStmtSeq(tokenizer)

        #check for end
        if(tokenizer.getToken() != 3):
            print("Error: end token missing")
            sys.exit(1)

        #skip "end" reserved word
        tokenizer.skipToken()

        #check for ;
        if(tokenizer.getToken() != 12):
            print("Error: ; token missing")
            sys.exit(1)

        #skip ";" special symbol
        tokenizer.skipToken()
   
    def printIf(self, indent):
        #print if, cond, then
        print("if ", end="")
        self.c.printCond(indent)
        print(" then ")

        #print ss1
        indent += '\t'
        self.ss1.printStmtSeq(indent)

        #check if ss2 exists and if so print ss2, else
        if(self.ss2 != None):
            print(indent.replace("\t", "", 1) + "else")
            self.ss2.printStmtSeq(indent)

        #print end;
        print(indent.replace("\t", "", 1) + "end;")

    
    def executeIf(self, data):
        #execute ss1 if cond true
        if(self.c.evalCond()):
            self.ss1.executeStmtSeq(data)
        else:
            #execute ss2 if it exists
            if(self.ss2 != None):
                self.ss2.executeStmtSeq(data)    

class Loop:
    def __init__(self):
        self.c = None
        self.ss = None
    
    def parseLoop(self, tokenizer):
         #check for while
        if(tokenizer.getToken() != 8):
            print("error: while token missing")
            sys.exit(1)
        
        #skip "while" reserved word
        tokenizer.skipToken()

        #parse condition and move to next token
        self.c = Cond()
        self.c.parseCond(tokenizer)

        #check for loop
        if(tokenizer.getToken() != 9):
            print("error: loop token missing")
            sys.exit(1)
        
        #skip "loop" reserved word
        tokenizer.skipToken()

        #parse stmtseq1 and move to next token
        self.ss = StmtSeq()
        self.ss.parseStmtSeq(tokenizer)

        #check for end
        if(tokenizer.getToken() != 3):
            print("Error: end token missing in while")
            sys.exit(1)

        #skip "end" reserved word
        tokenizer.skipToken()

        #check for ;
        if(tokenizer.getToken() != 12):
            print("Error: ; token missing in while")
            sys.exit(1)

        #skip ";" special symbol
        tokenizer.skipToken()

    def printLoop(self, indent):
        #print while, cond, loop
        print("while ", end="")
        self.c.printCond(indent)
        print(" loop")
        indent += '\t'
        #print ss1
        self.ss.printStmtSeq(indent)

        #print end;
        print(indent.replace("\t", "", 1) + "end;")
    
    def executeLoop(self, data):
        while(self.c.evalCond()):
            self.ss.executeStmtSeq(data)


class In:
    def __init__(self):
        self.idList = None
    
    def parseIn(self, tokenizer):
        #check for read
        if(tokenizer.getToken() != 10):
            print("error: read token missing")
            sys.exit(1)
        
        #skip "read" keyword
        tokenizer.skipToken()

        #parse id list and move to next token
        self.idList = IdList()
        self.idList.parseIdList(tokenizer)

        #check for ;
        if(tokenizer.getToken() != 12):
            print("error: ; token missing in read")
            sys.exit(1)
        
        #skip ";" special symbol
        tokenizer.skipToken()
    
    def printIn(self, indent):
        print("read ", end="")
        self.idList.printIdList(indent)
        print(";")

    def executeIn(self, data):
        self.idList.executeInIdList(data)

class Out:
    
    def __init__(self):
        self.idList = None
    
    def parseOut(self, tokenizer):
        #check for write
        if(tokenizer.getToken() != 11):
            print("error: write token missing")
            sys.exit(1)
        
        #skip "write" keyword
        tokenizer.skipToken()

        #parse id list and move to next token
        self.idList = IdList()
        self.idList.parseIdList(tokenizer)

        #check for ;
        if(tokenizer.getToken() != 12):
            print("error: ; token missing")
            sys.exit(1)
        
        #skip ";" special symbol
        tokenizer.skipToken()
    
    def printOut(self, indent):
        print("write ", end="")
        self.idList.printIdList(indent)
        print(";")

    def executeOut(self):
        self.idList.executeOutIdList()

class Cond:
    def __init__(self):
        self.altNum = 0
        self.comp = None
        self.cond1 = None
        self.cond2 = None
    
    def parseCond(self, tokenizer):
        tokenNum = tokenizer.getToken()

        if(tokenNum == 20):
            self.altNum = 1
            self.comp = Comp()
            self.comp.parseComp(tokenizer)
        elif(tokenNum == 15): 
            #skip "!" special symbol
            tokenizer.skipToken()

            #parse cond1
            self.altNum = 2
            self.cond1 = Cond()
            self.cond1.parseCond(tokenizer)
        elif(tokenNum == 16):
            #skip "[" special symbol
            tokenizer.skipToken()

            #parse cond1 and move to next token
            self.cond1 = Cond()
            self.cond1.parseCond(tokenizer)
            tokenizer.skipToken()

            #check for && or ||
            if(tokenizer.getToken() == 18):
                self.altNum = 3
            elif(tokenizer.getToken() == 19):
                self.altNum = 4
            else:
                print("error: && or || token missing")
                sys.exit(1)

            
            #skip "&&" or "||" special symbol
            tokenizer.skipToken()

            #parse cond2 and move to next token
            self.cond2 = Cond()
            self.cond2.parseCond(tokenizer)
            tokenizer.skipToken()

            #check for ]
            if(tokenizer.getToken() != 17):
                print("error: ] token missing")
                sys.exit(1)
            
            tokenizer.skipToken()
        else:
            print("error: incorrect cond")
            sys.exit(1)
        
    
    def printCond(self, indent):
        if(self.altNum == 1):
            self.comp.printComp(indent)
        elif(self.altNum == 2):
            print("!", end="")
            self.cond1.printCond(indent)
        elif(self.altNum == 3):
            print("[", end="")
            self.cond1.printCond(indent)
            print(" && ", end="")
            self.cond2.printCond(indent)
            print("]", end="")
        elif(self.altNum == 4):
            print("[", end="")
            self.cond1.printCond(indent)
            print(" || ", end="")
            self.cond2.printCond(indent)
            print("]", end="")

    def evalCond(self):
        if(self.altNum == 1):
            return self.comp.evalComp()
        elif(self.altNum == 2):
            return not self.cond1.evalCond()
        elif(self.altNum == 3):
            return self.cond1.evalCond() and self.cond2.evalCond()
        elif(self.altNum == 4):
            return self.cond1.evalCond() or self.cond2.evalCond()



class Comp:
    def __init__(self):
        self.op1 = None
        self.compop = None
        self.op2 = None
        self.altNum = 0
        
    def parseComp(self, tokenizer):
        #check for (
        if(tokenizer.getToken() != 20):
            print("error: ( token missing")
            sys.exit(1)
        
        #skip "(" special symbol
        tokenizer.skipToken()

        #parse op1 and move to next token
        self.op1 = Op()
        self.op1.parseOp(tokenizer)

        #set value of compop
        tokenNum = tokenizer.getToken()
        if(tokenNum == 25):
            self.altNum = 1
            self.compop = "!="
        elif(tokenNum == 26):
            self.altNum = 2
            self.compop = "=="
        elif(tokenNum == 27):
            self.altNum = 3
            self.compop = "<"
        elif(tokenNum == 28):
            self.altNum = 4
            self.compop = ">"
        elif(tokenNum == 29):
            self.altNum = 5
            self.compop = "<="
        elif(tokenNum == 30):
            self.altNum = 6
            self.compop = ">="
        else:
            print("error: incorrect compop")
            sys.exit(1)

        #skip compop
        tokenizer.skipToken()

        #parse op2 and move to next token
        self.op2 = Op()
        self.op2.parseOp(tokenizer)

        #check for )
        if(tokenizer.getToken() != 21):
            print("Error: ) token missing")
            sys.exit(1)

        #skip ")" special symbol
        tokenizer.skipToken()
    
    def printComp(self, indent):
        print("(", end="")
        self.op1.printOp(indent)
        if(self.altNum == 1):
            print(" != ", end="")
        elif(self.altNum == 2):
            print(" == ", end="")
        elif(self.altNum == 3):
           print(" < ", end="")
        elif(self.altNum == 4):
            print(" > ", end="")
        elif(self.altNum == 5):
            print(" <= ", end="")
        elif(self.altNum == 6):
            print(" >= ", end="")
        self.op2.printOp(indent)
        print(")", end="")
    
    def evalComp(self):
        if(self.altNum == 1):
            return (self.op1.executeOp() != self.op2.executeOp())
        elif(self.altNum == 2):
            return (self.op1.executeOp() == self.op2.executeOp())
        elif(self.altNum == 3):
           return (self.op1.executeOp() < self.op2.executeOp())
        elif(self.altNum == 4):
            return (self.op1.executeOp() > self.op2.executeOp())
        elif(self.altNum == 5):
            return (self.op1.executeOp() <= self.op2.executeOp())
        elif(self.altNum == 6):
            return (self.op1.executeOp() >= self.op2.executeOp())


class Exp:
    def __init__(self):
        self.fac = None
        self.exp = None
        self.plusOrMinus = 0
        
    def parseExp(self, tokenizer):
        #parse fac and move to next token
        self.fac = Fac()
        self.fac.parseFac(tokenizer)

        #check for "+"
        if(tokenizer.getToken() == 22):
            self.plusOrMinus = 1
            #skip "+" special symbol
            tokenizer.skipToken()
            #parse exp and move to next token
            self.exp = Exp()
            self.exp.parseExp(tokenizer)

        #check for "-"
        if(tokenizer.getToken() == 23):
            self.plusOrMinus = 2
            #skip "-" special symbol
            tokenizer.skipToken()
            #parse exp and move to next token
            self.exp = Exp()
            self.exp.parseExp(tokenizer)

    def printExp(self, indent):
        #print fac
        self.fac.printFac(indent)

        #print + and exp if they are available
        if(self.plusOrMinus == 1):
            print(" + ", end="")
            self.exp.printExp(indent)
        
        #print - and exp if they are available
        if(self.plusOrMinus == 2):
            print(" - ", end="")
            self.exp.printExp(indent)


    def evalExp(self):
        if(self.plusOrMinus == 0):
            return self.fac.evalFac()
        elif(self.plusOrMinus == 1):
            return (self.fac.evalFac() + self.exp.evalExp())     
        elif(self.plusOrMinus == 2):
            return (self.fac.evalFac() - self.exp.evalExp())
    
class Fac:
    def __init__(self):
        self.op = None
        self.fac = None
        self.altNum = 0
    
    def parseFac(self, tokenizer):
        #parse op and move to next token
        self.op = Op()
        self.op.parseOp(tokenizer)

        #check for "*"
        if(tokenizer.getToken() == 24):
            self.altNum = 1
            #skip "*" special symbol
            tokenizer.skipToken()
            #parse fac and move to next token
            self.fac = Fac()
            self.fac.parseFac(tokenizer)


    def printFac(self, indent):
        #print op
        self.op.printOp(indent)

        #print fac if it is available
        if(self.altNum == 1):
            print(" * ", end="")
            self.fac.printFac(indent)


    def evalFac(self):
        if(self.altNum == 0):
            return self.op.executeOp()
        elif(self.altNum == 1):
            return (self.op.executeOp() * self.fac.evalFac())

class Op:
    def __init__(self):
        self.int = None
        self.id = None
        self.exp = None
        self.altNum = 0

    def parseOp(self, tokenizer):
        tokenNum = tokenizer.getToken()
        if(tokenNum == 31):
            self.altNum = 1
            #set int value
            self.int = tokenizer.intVal()
            tokenizer.skipToken()      
        elif(tokenNum == 32):
            self.altNum = 2
            #parse id and move to next token 
            self.id = Id.parseId(tokenizer)
        elif(tokenNum == 20):
            self.altNum = 3
        
            #skip "(" special symbol
            tokenizer.skipToken()
            
            #parse exp and move to next token
            self.exp = Exp()
            self.exp.parseExp(tokenizer)

            #check for )
            if(tokenizer.getToken() != 21):
                print("error: ) token missing")
                sys.exit(1)
        
            #skip ")" special symbol
            tokenizer.skipToken()
        else:
            print("error: op doesn't contain correct tokens")
            sys.exit(1)
        
    def printOp(self, indent):
        if(self.altNum == 1):
            print(self.int, end="")
        elif(self.altNum == 2):
            self.id.printId(indent)
        elif(self.altNum == 3):
            self.exp.printExp()

    def executeOp(self):
        if(self.altNum == 1):
            return self.int
        elif(self.altNum == 2):
            return self.id.getIdVal()
        elif(self.altNum == 3):
            return self.exp.evalExp()

class Id:

    eIds = []
    phase = 0 # 1 for stmt seq and 2 for decl seq
 
    def __init__(self, n):
        self.name = n
        self.val = 0
        self.initialized = False

    def getIdVal(self):
        if(self.initialized):
            return self.val
        else:
            print(self.name + " has not been initialized!")
            sys.exit(1)

    def setIdVal(self, value):
        self.initialized = True
        self.val = value

    def getIdName(self):
        return self.name

    @staticmethod
    def parseId(tokenizer):
        current_name = tokenizer.idName()

        if(Id.phase == 1):
            i = 0
            while(i < len(Id.eIds)):
                if(current_name == Id.eIds[i].name):
                    print("Double declaration!" + current_name + " has already been declared!")
                    sys.exit(1)
                i += 1
            
            newId = Id(current_name)
            newId.declared = True
            Id.eIds.append(newId)
            tokenizer.skipToken()
            return newId
        elif(Id.phase == 2):
            j = 0
            while(j < len(Id.eIds)):
                if(current_name == Id.eIds[j].name):
                    Id.eIds[j].initialized = True
                    tokenizer.skipToken()
                    return Id.eIds[j]
                j += 1
            print("Undeclared variable!" + current_name + " has not been declared!")
            sys.exit(1)
            
    def printId(self, indent):
        print(self.getIdName(), end="")

    
    