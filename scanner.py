import sys

class Scanner:

    reserved_words = ['program', 'begin', 'end', 'int', 'if', 'then', 'else', 'while', 'loop', 'read', 'write']
    special_symbols = [';', ',', '=', '!', '[', ']', '&&', '||', '(', ')', '+', '-', '*', '!=', '==', '<', '>', '<=', '>=']
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    uppercase_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    tokens = []
    cursor = 0

    def __init__(self, inputFile):
        self.file = open(inputFile, 'r')
        self.__tokenizeLine(self.file)
       


    def __tokenizeLine(self, file):

        line = file.readline()          
        
        while line == '\n':
            line = file.readline()

        convertedToken = 0
        if line == '':
            convertedToken = 33
            self.tokens.append((convertedToken, ''))
            
        index = 0
        while index < len(line):
            if index + 1 < len(line) and line[index:index + 2] in self.special_symbols:
                line = line[:index] + ' ' + line[index:index + 2] + ' ' + line[index + 2:]
                index += 3  
            elif line[index] in self.special_symbols:
                line = line[:index] + ' ' + line[index] + ' ' + line[index + 1:]
                index += 2
            else:
                index += 1
        

        i = 0
        strings = line.split()
        while i < len(strings):  

            if strings[i] in self.reserved_words:
                convertedToken = self.reserved_words.index(strings[i]) + 1
            elif strings[i] in self.special_symbols:
                convertedToken = self.special_symbols.index(strings[i]) + 12
            elif strings[i].isdigit():
                convertedToken = 31
            elif self.isid(strings[i]):
                convertedToken = 32
            elif strings[0] == '':
                convertedToken = 33
            else:
                convertedToken = 34
                print("error invalid token:" + strings[i])

            self.tokens.append((convertedToken, strings[i]))
            i += 1

        self.cursor = 0
        
    def getToken(self):
        if self.cursor < len(self.tokens):
            return self.tokens[self.cursor][0]
       
    def skipToken(self):
        if self.cursor < len(self.tokens) - 1 and self.tokens[self.cursor][0] != 33:
            self.cursor += 1
        else:
            self.tokens = []
            self.__tokenizeLine(self.file)

    def intVal(self):
        if self.getToken(self) == 31:
            return int(self.tokens[self.cursor][1])
        else:
            print("error this is not a integer")
            sys.exit(1)

    def idName(self):
        if self.getToken(self) == 32:
            return self.tokens[self.cursor][1]
        else:
            print("error this is not a identifier")
            sys.exit(1)

    def isid(self, token):
        if token[0] not in self.uppercase_letters:
            return False
        i = 1
        while i < len(token):
            if token[i] not in self.uppercase_letters and token[i] not in self.digits:
                return False
            i += 1      
            
        return True