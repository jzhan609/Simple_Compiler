import sys
from lexical_analyzer import PRINT, TYPE_INT, TYPE_FLOAT, TYPE_STRING, EOF, IDENT
from lexical_analyzer import SEMICOLON, LEFT_BRACE, RIGHT_BRACE,ADD_OP, SUB_OP, MULT_OP, DIV_OP, ASSIGN_OP
from lexical_analyzer import LEFT_PAREN, RIGHT_PAREN, getNextToken, initLexicalAnalyzer
from referencing_environment import Symbol, SymbolTable, Node
from expression_evaluator import Stack, evaluate_expression



def isType(code):
    return code in (TYPE_FLOAT, TYPE_INT, TYPE_STRING)


def isOp(code):
    return code in (code == ADD_OP, SUB_OP, MULT_OP, DIV_OP, LEFT_PAREN, RIGHT_PAREN)


def analyze_syntax():
    statement_stack = Stack(300)
    symbol_table_list = Node()
    identifier = Symbol()

    while True:
        token = getNextToken()  # Get the next token from the lexical analyzer

        if token['code'] == EOF:
            break  # Exit the loop when the end of the input is reached
        else:
            if token['code'] == LEFT_BRACE:
                symbol_table_list = symbol_table_list.push_scope()
            elif token['code'] == RIGHT_BRACE:
                symbol_table_list = symbol_table_list.pop_scope()
            elif isType(token['code']):
                variable = getNextToken()
                found_symbol = symbol_table_list.symbol_existsInCurrent(variable['lexeme'])
                if found_symbol is not None:
                    print(f"Variable {variable['lexeme']} already defined")
                    return
                symbol_table_list.insert_symbol(token['lexeme'], variable['lexeme'], 0)
                # Skip semicolon
                getNextToken()
            elif token['code'] == PRINT:
                # Skip opening parenthesis
                getNextToken()
                variable = getNextToken()
                # Skip closing parenthesis
                getNextToken()
                # Skip semicolon
                getNextToken()
                found_symbol = symbol_table_list.symbol_exists(variable['lexeme'])
                if found_symbol is None:
                    print(f"Variable {variable['lexeme']} undefined")
                    return
                print(f"Variable {found_symbol.name} : {found_symbol.value}")
                
            elif token['code'] == IDENT:
                found_symbol = symbol_table_list.symbol_exists(token['lexeme'])
                if found_symbol is None:
                    print(f"Variable {token['lexeme']} undefined")
                    return
                else:
                    next_token = getNextToken()
                    if next_token['code'] != ASSIGN_OP:
                        statement_stack.push(found_symbol.value)
                        if next_token['code'] != SEMICOLON:
                            statement_stack.push(next_token['lexeme'][0])
                        else:
                            identifier_value = evaluate_expression(statement_stack)
                            identifier.value = str(identifier_value)
                    else:
                        identifier = found_symbol
                        
            elif token['code'] != SEMICOLON:
                if isOp(token['code']):
                    statement_stack.push(token['lexeme'][0])
                else:
                    statement_stack.push(token['lexeme'])
            else:
                identifier_value = evaluate_expression(statement_stack)
                identifier.value = str(identifier_value)
            
    return

if __name__ == "__main__":
    initLexicalAnalyzer()
    analyze_syntax()
        
