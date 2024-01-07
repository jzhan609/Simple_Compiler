import os

# Global declarations
# Variables
charClass = 0
lexeme = ''
error = ''
nextChar = ''
token = 0
nextToken = 0
lineNum = 1
stack = []
isIdent = False

# Function declarations
def addChar():
    global lexeme
    if len(lexeme) <= 98:
        lexeme += nextChar
    else:
        print("Error - lexeme is too long")


def getChar():
    global nextChar, charClass
    
    try:
        nextChar = in_fp.read(1)
    except Exception as e:
        nextChar = ''
    if nextChar:
        if nextChar.isalpha():
            charClass = LETTER
        elif nextChar == '_':
            charClass = UNDERSCORE
        elif nextChar.isdigit():
            charClass = DIGIT
        else:
            charClass = UNKNOWN
    else:
        charClass = EOF


def getNonBlank():
    global nextChar, lineNum
    while nextChar in (" ", "\t", "\n"):
        if(nextChar == "\n"):
            lineNum += 1
        getChar()

def rules():
    global token, nextToken, isIdent, error, lexeme
    if token == TYPE:
        if nextToken != IDENT:
            error = 'Invalid Identity'
            nextToken = EOF
        else:
            lex()
            if(nextToken != IN):
                error = 'Invalid statement'
                nextToken = EOF
            else:
                lex()

    if token == IDENT:
        if nextToken not in [GREATER_THAN,LESS_THAN,ASSIGN_OP,EQUALS,RIGHT_PAREN,LEFT_PAREN]:
            if nextToken == STR_LIT:
                error = 'String assignment error'
                nextToken = EOF
            elif nextToken == INT_LIT:
                error = 'Integer assignment error'
                nextToken = EOF
            elif nextToken == FLOAT_LIT:
                error = 'Float assignment error'
                nextToken = EOF
            else:
                error = 'Missing ='
                nextToken = EOF

    if nextToken in [GREATER_THAN,LESS_THAN,ASSIGN_OP,EQUALS]:
        if token != IDENT:
            error = 'Invalid assignment'
            nextToken = EOF
        else:
            isIdent = True

    if token == ASSIGN_OP:
        if nextToken not in [INT_LIT, STR_LIT, FLOAT_LIT]:
            error = "Invalid operand"
            nextToken = EOF

    if nextToken in [ADD_OP,SUB_OP,MULT_OP,DIV_OP]:
        if token not in [INT_LIT,FLOAT_LIT,STR_LIT]:
            error = "Missing operand before operator"
            nextToken = EOF

    if token in [ADD_OP,SUB_OP,MULT_OP,DIV_OP]:
        if nextToken not in [INT_LIT,FLOAT_LIT]:
            if nextToken == STR_LIT:
                error = "String assignment error"
                nextToken = EOF
            else:
                error = "Missing operand after operator"
                nextToken = EOF

    if token in [INT_LIT, STR_LIT, FLOAT_LIT]:
        if(isIdent):
            if nextToken not in [ADD_OP,SUB_OP,MULT_OP,DIV_OP,SEMICOLON,RIGHT_PAREN]:
                error = 'Missing semi colon'
                nextToken = EOF
            else:
                isIdent = False
        else:
            if nextToken != SEMICOLON:
                error = 'Missing semi colon'
                nextToken = EOF

    if token in [IF, FOR, WHILE]:
        if nextToken != LEFT_PAREN:
            error = 'Missing ('
            nextToken = EOF
    
    if token == ELSE:
        if nextToken not in [IF,LEFT_BRACE]:
            error = 'Missing {'
            nextToken = EOF

def lex():
    global lexeme, nextToken, charClass, error, token, isIdent
    lexeme = ''
    getNonBlank()
    token = nextToken
    if charClass == LETTER or charClass == UNDERSCORE:
        addChar()
        getChar()
        while charClass == LETTER or charClass == DIGIT or charClass == UNDERSCORE:
            addChar()
            getChar()

        if lexeme == "if":
            nextToken = IF
        elif lexeme == "else":
            nextToken = ELSE
        elif lexeme == "for":
            nextToken = FOR
        elif lexeme == "while":
            nextToken = WHILE
        elif lexeme in ['String','Int','Float']:
            nextToken = TYPE
        elif lexeme == 'in':
            nextToken = IN
        elif charClass == UNKNOWN and not nextChar.isspace() and nextChar not in "(+-*/<>)":
            addChar()
            error = "Illegal identifier"
            nextToken = EOF
        else:
            nextToken = IDENT

    elif charClass == DIGIT:
        addChar()
        getChar()
        while charClass == DIGIT:
            addChar()
            getChar()
        if nextChar == ".":
            addChar()  # Include the decimal point
            getChar()
            while charClass == DIGIT:
                addChar()
                getChar()
            nextToken = FLOAT_LIT
        elif charClass == LETTER or nextChar == "_":
            while charClass == LETTER or charClass == DIGIT or nextChar == "_":
                addChar()
                getChar()
            error = "Illegal identifier"
            nextToken = EOF
        else:
            nextToken = INT_LIT
    elif nextChar == "\"":
        addChar()
        getChar()
        while nextChar != "\"" and nextChar != "":
            addChar()
            getChar()
        if nextChar == "\"":
            addChar()  # Include the closing double quote
            getChar()
            
            nextToken = STR_LIT
        else:
            error = "Unclosed string literal"
            nextToken = EOF
            return
    
    elif charClass == UNKNOWN:
        lookup(nextChar)
        getChar()

    elif charClass == EOF:
        nextToken = EOF
        lexeme = 'EOF'

    print(f"Next token is: {nextToken}, Next lexeme is {lexeme}")
    print("lineNum: ", lineNum)
    print(stack)

def lookup(ch):
    global nextToken, lexeme, error, lineNum, stack, token
    if ch == '(':
        addChar()
        stack += '('
        nextToken = LEFT_PAREN
    elif ch == ')':
        addChar()
        if(len(stack) == 0):
            error = "Unmatched closing )"
            nextToken = EOF
        
        elif (stack[len(stack)-1] == '('):
            stack.pop()
            nextToken = RIGHT_PAREN
        else:
            error = "Unmatched closing )"
            nextToken = EOF
        
    elif ch == '{':
        addChar()
        stack += '{'
        nextToken = LEFT_BRACE
    elif ch == '}':
        addChar()
        if(len(stack) == 0):
            error = "Unmatched closing }"
            nextToken = EOF
        elif (stack[len(stack)-1] == '{'):
            stack.pop()
            nextToken = RIGHT_BRACE
        else:
            error = "Unmatched closing }"
            nextToken = EOF
            
    elif ch == '+':
        addChar()
        nextToken = ADD_OP
    elif ch == '-':
        addChar()
        nextToken = SUB_OP
    elif ch == '*':
        addChar()
        nextToken = MULT_OP
    elif ch == '/':
        addChar()
        getChar()
        if nextChar == '/':
            while nextChar != '\n' and nextChar != '':
                getChar()
            nextToken = COMMENT
            lexeme = "a single line comment"
            if nextChar == '\n':
                lineNum += 1
        elif nextChar == '*':
            addChar()
            getChar()
            while not (nextChar == '*' and in_fp.read(1) == '/'):
                if nextChar == '\n':
                    lineNum += 1
                if nextChar == '':
                    error = "Unclosed block comment"
                    nextToken = EOF
                    break
                getChar()
            getChar() # Consume the '/'
            if(nextChar == '\n'):
                lineNum += 1
            nextToken = COMMENT
            lexeme = "a block comment"
        else:
            nextToken = DIV_OP
    elif ch == '=':
        addChar()
        getChar()
        if nextChar == '=':
            addChar()
            nextToken = EQUALS
        else:
            nextToken = ASSIGN_OP
    elif ch == ';':
        addChar()
        nextToken = SEMICOLON
    elif ch == '<':
        addChar()
        getChar()
        if nextChar == '=':
            addChar()
            nextToken = LESS_THAN
        else:
            nextToken = LESS_THAN
    elif ch == '>':
        addChar()
        getChar()
        if nextChar == '=':
            addChar()
            nextToken = GREATER_THAN
        else:
            nextToken = GREATER_THAN
    elif ch == '!':
        addChar()
        getChar()
        if nextChar == '=':
            addChar()
            nextToken = NOT_EQUALS
        else:
            nextToken = UNKNOWN
    elif ch == '&':
        addChar()
        getChar()
        if nextChar == '&':
            addChar()
            nextToken = AND_OP
        else:
            nextToken = UNKNOWN
    elif ch == '|':
        addChar()
        getChar()
        if nextChar == '|':
            addChar()
            nextToken = OR_OP
        else:
            nextToken = UNKNOWN
    elif ch == '?':
        addChar()
        nextToken = QUESTION_MARK
    elif ch == ':':
        addChar()
        nextToken = COLON
    else:
        addChar()
        nextToken = EOF

# Character classes
EOF = -1
LETTER = 0
DIGIT = 1
UNDERSCORE = 2
UNKNOWN = 99

# Token codes
INT_LIT = 10
FLOAT_LIT = 12
IDENT = 11
STR_LIT = 13
ASSIGN_OP = 20
ADD_OP = 21
SUB_OP = 22
MULT_OP = 23
DIV_OP = 24
LEFT_PAREN = 25
RIGHT_PAREN = 26
LEFT_BRACE = 27
RIGHT_BRACE = 28
SEMICOLON = 29
LESS_THAN = 30
GREATER_THAN = 31
EQUALS = 32
NOT_EQUALS = 33
AND_OP = 34
OR_OP = 35
IF = 36
ELSE = 37
FOR = 38
WHILE = 39
COMMENT = 40
QUESTION_MARK = 41
COLON = 42
NEWLINE = 43
LEFT_SQUARE_BRACKET = 44
RIGHT_SQUARE_BRACKET = 44
TYPE = 45
IN = 46


# Main driver
file = "A2_3120/TestCases/input20.txt"
if os.path.exists(file):
    in_fp = open(file, "r")

    getChar()
    while nextToken != EOF:
        lex()
        if(nextToken != EOF):
            rules()

    if len(stack) > 0 and len(error) == 0:
        error = "Unmatched opening " + stack[len(stack)-1]

    if len(error) > 0:
        if(nextChar == '\n'):
            lineNum += 1
        print('Syntax analysis failed.\nsyntax_analyzer_error -', error, 'at line', lineNum)
    else:
        print('Syntax analysis suceeded.')
    
else:
    print("ERROR - cannot open input.txt")
