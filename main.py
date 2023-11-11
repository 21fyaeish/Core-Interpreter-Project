import scanner
import interperter
import sys

# get files and setup indent
fileCore = sys.argv[1]
dataFile = open(sys.argv[2], 'r')
indent = "\t"

# setup tokenizer and interperter
tokenizer = scanner.Scanner(fileCore)
coreProgram = interperter.Program(dataFile)

# interpert the program
coreProgram.parseProgram(tokenizer)
coreProgram.printProgram(indent)
coreProgram.executeProgram()

        


