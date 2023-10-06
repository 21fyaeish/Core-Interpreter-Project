import scanner
import sys

file = sys.argv[1]
tokenizer = scanner.Scanner(file)


while True:
    token = tokenizer.getToken()
    print(token)

    if token == 33:
        print("reached EOF")
        break
    if token == 34:
        print("error invalid token entered")
        break
            
    tokenizer.skipToken()
        


