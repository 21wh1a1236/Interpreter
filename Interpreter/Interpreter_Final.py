class InterpreterRunner:
    @staticmethod
    def interpreter_input():
        statements = []
        while True:
            statement = input()
            if statement == 'STOP':
                return statements
                break
            else:
                statements.append(statement)

    @staticmethod
    def constituent_evaluator(statement, constituent, variables):
        value = None
        if constituent.isdigit():
            if InterpreterRules.interpreter_number(int(constituent)):
                value = int(constituent)
            else:
                print(f"{statement} (number must not have more than two digits)")
        elif constituent.isalpha():
            if InterpreterRules.interpreter_var(constituent):
                value = variables[constituent]
            else:
                print(f"{statement} ({constituent} is not a valid variable)")
        else:
            print(f"{statement} ({constituent} is not allowed in expression)")
        return value

    @staticmethod
    def expression_evaluator(statement, expression, variables):
        value = None
        if 1 <= len(expression):
            if (sum(not oper.isalnum() for oper in expression) == 0
                    or len(expression) == 1 or len(expression) == 2):
                value = InterpreterRunner.constituent_evaluator(statement,
                                                                expression, variables)
            elif sum(not oper.isalnum() for oper in expression) > 1:
                print(f"{statement} (only one operator is allowed)")
            else:
                oper = None
                for oper in expression:
                    if not oper.isalnum():
                        break
                if expression.startswith(oper):
                    print(f"{statement} ({oper} is not allowed at start of expression)")
                elif expression.endswith(oper):
                    print(f"{statement} ({oper} is not allowed at end of expression)")
                else:
                    constituents = expression.split(oper)                  
                    constituent1 = constituents[0]
                    constituent2 = constituents[1]
                    value1 = InterpreterRunner.constituent_evaluator(statement,
                                                                     constituent1, variables)
                    value2 = InterpreterRunner.constituent_evaluator(statement,
                                                                     constituent2, variables)
                    if value1 is not None and value2 is not None:
                        if InterpreterRules.interpreter_oper(oper):
                            if oper == '+':
                                value = value1 + value2
                            elif oper == '-':
                                value = value1 - value2
                            elif oper == '*':
                                value = value1 * value2
                        else:
                            print(f"{statement} (operator is not valid)")
        else:
            if len(expression) == 0:
                print(f"{statement} (no expression in statement)")
        return value

    @staticmethod
    def statement_evaluator():
        variables = {'A': None, 'B': None, 'C': None, 'D': None, 'E': None}
        statements = InterpreterRunner.interpreter_input()
        for statement in statements:
            if statement.find(' ') != -1:
                print(f"{statement} (no spaces allowed)")
            else:
                if statement.find('=') != -1:
                    parts = statement.split('=')
                    var = parts[0]                            
                    expression = parts[1]
                    value = None
                    if var == '':
                        print("please give a variable before = operator")
                    elif InterpreterRules.interpreter_var(var):
                        value = InterpreterRunner.expression_evaluator(statement, expression, variables)
                    else:
                        print(f"{statement} ({var} is not a valid variable)")
                    variables[var] = value
                else:
                    print(statement, " (Not a valid Statement without = operator)")
        for var, value in variables.items():
            if value is not None:
                print(f"{var}=   {value}")


class InterpreterRules:
    @staticmethod
    def interpreter_number(user_number):
        if 0 <= user_number <= 99:
            return True
        else:
            return False

    @staticmethod
    def interpreter_var(user_var):
        list_of_var = ['A', 'B', 'C', 'D', 'E']
        if user_var in list_of_var:
            return True
        else:
            return False

    @staticmethod
    def interpreter_oper(user_oper):
        list_of_oper = ['*', '+', '-']
        if user_oper in list_of_oper:
            return True
        else:
            return False


InterpreterRunner.statement_evaluator()