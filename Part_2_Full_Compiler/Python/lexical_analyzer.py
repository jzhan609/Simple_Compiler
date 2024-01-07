import os

# Global declarations
# Variables
charClass = 0
lexeme = ''
error = ''
nextChar = ''
token = 0
nextToken = 0
in_fp = None
current_line_number = 1


# Function declarations
def addChar():
    global lexeme
    if len(lexeme) <= 98:
        lexeme += nextChar
    else:
        print("Error - lexeme is too long")


def getChar():
    global nextChar, charClass, in_fp, current_line_number
    try:
        nextChar = in_fp.read(1)
    except Exception as e:
        nextChar = ''
    if nextChar:
        if(nextChar == '\n'):
            current_line_number += 1
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
    while nextChar.isspace():
        getChar()


def getNextToken():
    global lexeme, nextToken, charClass, error, current_line_number
    lexeme = ''
    getNonBlank()
    if charClass == LETTER or charClass == UNDERSCORE:
        addChar()
        getChar()
        while charClass == LETTER or charClass == DIGIT or charClass == UNDERSCORE:
            addChar()
            getChar()

        if lexeme == "int":
            nextToken = TYPE_INT
        elif lexeme == "float":
            nextToken = TYPE_FLOAT
        elif lexeme == "string":
            nextToken = TYPE_STRING
        elif lexeme == "print":
            nextToken = PRINT
        elif charClass == UNKNOWN and not nextChar.isspace() and nextChar not in "(+-*/<>)":
            addChar()
            error = "Error - illegal identifier"
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
            error = "Error - illegal identifier"
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
            error = "Error - unclosed string literal"
            nextToken = EOF

    elif charClass == UNKNOWN:
        lookup(nextChar)
        getChar()

    elif charClass == EOF:
        nextToken = EOF
        lexeme = 'EOF'

    #print(f"Next token is: {nextToken}, Next lexeme is {lexeme} line {current_line_number}")
    #print(f"\t{error}")
    return {
        "code": nextToken,
        "lexeme": lexeme,
        "line": current_line_number
    }


def lookup(ch):
    global nextToken, lexeme, error, current_line_number
    if ch == '(':
        addChar()
        nextToken = LEFT_PAREN
    elif ch == ')':
        addChar()
        nextToken = RIGHT_PAREN
    elif ch == '{':
        addChar()
        nextToken = LEFT_BRACE
    elif ch == '}':
        addChar()
        nextToken = RIGHT_BRACE
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
        elif nextChar == '*':
            addChar()
            getChar()
            while not (nextChar == '*' and in_fp.read(1) == '/'):
                if nextChar == '':
                    error = "Error - unclosed block comment"
                    nextToken = EOF
                    break
                getChar()
            getChar()  # Consume the '/'
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
TYPE_INT = 43
TYPE_FLOAT = 44
TYPE_STRING = 45
PRINT = 46

file = "A3_3120/IO/input1.txt"
def initLexicalAnalyzer():
    global in_fp
    if os.path.exists(file):
        in_fp = open(file, "r")
        getChar()
    else:
        print("ERROR - cannot open file")
