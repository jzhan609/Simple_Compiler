class Symbol:
    def __init__(self):
        self.type = ""
        self.name = ""
        self.value = ""


class SymbolTable:
    def __init__(self):
        self.symbols = [Symbol() for _ in range(MAX_SYMBOLS)]


class Node:
    def __init__(self):
        self.symbolTable = SymbolTable()
        self.count = 0
        self.next = None

    def push_scope(self):
        new_node = Node()
        new_node.next = self
        return new_node

    def pop_scope(self):
        if self is not None:
            self = self.next
            return self
        else:
            print("Cannot pop from an empty symbol table")
            return self

    def print_current_scope(self):
        if self is not None:
            print("Current Scope Symbols:")
            for i in range(self.count):
                print(f"{self.symbolTable.symbols[i].name}\t {self.symbolTable.symbols[i].value}")
            print("\n")
        else:
            print("Symbol table is empty")

    def print_all_scopes(self):
        current = self
        while current is not None:
            print("Scope Symbols:")
            for i in range(current.count):
                print(f"{current.symbolTable.symbols[i].name}\t {current.symbolTable.symbols[i].value}")
            print("\n")
            current = current.next

    def insert_symbol(self, symbol_type, symbol_name, symbol_value):
        if self.count < MAX_SYMBOLS:
            symbol = self.symbolTable.symbols[self.count]
            symbol.name = symbol_name
            symbol.value = symbol_value
            symbol.type = symbol_type
            self.count += 1
        else:
            print("Symbol table is full")

    def symbol_exists(self, name):
        current = self
        while current is not None:
            for i in range(current.count):
                if current.symbolTable.symbols[i].name == name:
                    return current.symbolTable.symbols[i]
            current = current.next
        return None
    
    def symbol_existsInCurrent(self, name):
        for i in range(self.count):
            if self.symbolTable.symbols[i].name == name:
                return self.symbolTable.symbols[i]

        return None


def free_environment(head):
    while head is not None:
        temp = head
        head = head.next
        del temp

MAX_SYMBOLS = 100

