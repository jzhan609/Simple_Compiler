class Stack:
    def __init__(self, capacity):
        self.top = -1
        self.capacity = capacity
        self.array = [0.0] * capacity

    def is_empty(self):
        return self.top == -1

    def push(self, item):
        if self.top == self.capacity - 1:
            print("Stack overflow")
            return
        self.top += 1
        self.array[self.top] = item

    def pop(self):
        if self.is_empty():
            print("Stack underflow")
            return
        item = self.array[self.top]
        self.top -= 1
        return item

    def peek(self):
        if self.is_empty():
            print("Stack underflow")
            return
        return self.array[self.top]


def precedence(op):
    if op in ('+', '-'):
        return 1
    elif op in ('*', '/'):
        return 2
    else:
        return -1  # Invalid operator


def evaluate_expression(expression_stack: Stack):
    operand_stack = Stack(200)
    operator_stack = Stack(200)

    while not expression_stack.is_empty():
        token = expression_stack.pop()
        if token == '(':
            operator_stack.push(token)
        elif token == ')':
            while not operator_stack.is_empty() and operator_stack.peek() != '(':
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()
                op = operator_stack.pop()

                # Perform the operation and push the result onto the operand stack
                if op == '+':
                    operand_stack.push(operand1 + operand2)
                elif op == '-':
                    operand_stack.push(operand1 - operand2)
                elif op == '*':
                    operand_stack.push(operand1 * operand2)
                elif op == '/':
                    operand_stack.push(operand1 / operand2)

            # Pop the opening parenthesis from the operator stack
            operator_stack.pop()
        elif token in ('+', '-', '*', '/'):
            while not operator_stack.is_empty() and precedence(operator_stack.peek()) >= precedence(token):
                operand2 = float(operand_stack.pop())
                operand1 = float(operand_stack.pop())
                
                op = operator_stack.pop()

                # Perform the operation and push the result onto the operand stack
                if op == '+':
                    operand_stack.push(operand1 + operand2)
                elif op == '-':
                    operand_stack.push(operand1 - operand2)
                elif op == '*':
                    operand_stack.push(operand1 * operand2)
                elif op == '/':
                    operand_stack.push(operand1 / operand2)

            # Push the current operator onto the operator stack
                print(op)
            operator_stack.push(token)
        else:
            operand = token
            operand_stack.push(operand)

    # Evaluate any remaining operators
    while not operator_stack.is_empty():
        operand2 = float(operand_stack.pop())
        operand1 = float(operand_stack.pop())
        op = operator_stack.pop()

        # Perform the operation and push the result onto the operand stack
        if op == '+':
            operand_stack.push(operand1 + operand2)
        elif op == '-':
            operand_stack.push(operand1 - operand2)
        elif op == '*':
            operand_stack.push(operand1 * operand2)
        elif op == '/':
            operand_stack.push(operand1 / operand2)

    # The final result is on the top of the operand stack
    result = operand_stack.pop()

    return result

