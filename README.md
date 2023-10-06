# Core-Interpreter-Project
Submitted Files:
- main.py: file that will run the tokenizer
- scanner.py: file that contains the tokenizer and its asscoiated functions

# How the tokenizer works:
First the tokenizer opens a file and then calls the function __tokenizeLine(self, file) to tokenize the first non empty line. The __tokenizeLine(self, file) function
reads a line from the input file and converts the sequence of characters in that line into a sequence of Core tokens and saves them in a list and sets the cursor to 
point to the first token in the list. Then getToken() and skipToken() are repeatedly called until, after some number of iterations, getToken() returns 33 to indicate 
end-of-file or 34 to indicate invalid token. getToken() specifically returns the current token or the token that the cursor is pointing at. skipToken() increments the
cursor unless there are no more tokens in the current line so then it calls __tokenizeLine(self, file).

# How to run
To run type in the terminal "python main.py textfile" where textfile is the specific file you want to read from