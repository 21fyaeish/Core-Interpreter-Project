file = open('test.txt', 'r')    

while True:
    line = file.readline()
    print(line)
    if line == '':
        break 
    