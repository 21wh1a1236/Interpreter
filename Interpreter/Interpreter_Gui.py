from tkinter import *
from functools import partial

class InterpreterGUI:
    @staticmethod
    def menu_window():
        # Create a window
        box = Tk()
        box.title("Help Menu")
        # Add a label with instructions
        instructions = Label(box, text="These are the instruction for the interpreter:\n"+
                             "\n1. Alphabets only from A to E are accepted\n2. Operators accepted are  +,  -,  *\n"+
                             "3. A number should not have more than two digits\n4. First we should give operand in expression\n"+
                             "5. Only one operator allowed in an input statement\n6. Spaces are not allowed in the input\n"+
                             "7. Negative numbers are not defined\n"+
                             "8. A valid expression is: \n   'Alphabet = Number' \n                or\n   'Alphabet = Alphabet' \n                or\n   'Alphabet = (Alphabet/Number) (Operator) (Alphabet/Number)'\n"+
                             "9. Press 'RUN' button to stop taking input and to get output\n10. Press 'Clear' to give new input")
        instructions.config(font=('Times New Roman',18), justify=LEFT)
        instructions.pack(fill="both", expand=True)
        btn = Button(box,text = "Back",fg="white",bg="RoyalBlue4",width=10,command=lambda: [box.destroy(),InterpreterGUI.start_window()])
        btn.pack(side=BOTTOM)
        # Run the window
        box.mainloop()

    @staticmethod
    def Interpreter_window():
        box = Tk()
        box.title("Interpreter")
        def on_keyboard_button_click(button_text):
            if button_text == "Clear":
                input_text.delete(1.0, END)
            elif button_text == "<-":
                input_text.delete("end-2c", END)
            elif button_text == "Space":
                input_text.insert(END, " ")
            elif button_text == "Enter":
                input_text.insert(END, "\n")
            elif button_text == "Main":
                box.destroy(),InterpreterGUI.start_window()
            elif button_text == "Exit":
                box.destroy()    
            else:
                input_text.insert(END, button_text)
        box.configure(bg='gainsboro')
        input_frame = Frame(box)
        input_frame.pack(side=TOP, fill=BOTH, expand=True)
        input_frame.configure(bg='gainsboro')
        input_label = Label(input_frame, text="Input:")
        input_label.pack(side=TOP, padx=5, pady=5)
        input_text = Text(input_frame, height=10, width=60)
        input_text.pack(side=TOP, padx=5, pady=5)
        button_frame = Frame(box)
        button_frame.pack(side=TOP, fill=X, padx=5, pady=5)
        button_frame.configure(bg='gainsboro')
        run_button = Button(button_frame, text="RUN", command=lambda:InterpreterRunner.statement_evaluator(input_text, output_text))
        run_button.pack(side=TOP, padx=5, pady=5)
        output_frame = Frame(box)
        output_frame.pack(side=TOP, fill=BOTH, expand=True)
        output_frame.configure(bg='gainsboro')
        output_label = Label(output_frame, text="Output:")
        output_label.pack(side=TOP, padx=5, pady=5)
        output_text = Text(output_frame, height=10, width=60)
        output_text.pack(side=TOP, padx=5, pady=5)
        # Virtual keyboard
        keyboard_frame = Frame(box)
        keyboard_frame.pack(side=BOTTOM, expand=True)
        button_width = 6
        button_height = 2
        buttons={}
        buttons_text = [
            "1", "2", "3", "4", "5", "6", "7", "8", "9", "0","<-","Enter", 
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
            "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W",
            "X", "Y", "Z", "-", "=","+", "*", "/","%","Space","Clear","Main","Exit"]

        for i in range(len(buttons_text)):
            button = Button(keyboard_frame, text=buttons_text[i],
            width=button_width, height=button_height,
            command=partial(on_keyboard_button_click, buttons_text[i]))
            button.grid(row=i//12+1, column=i%12, padx=6, pady=6)
            buttons[buttons_text[i]] = button
        box.mainloop()
    
    @staticmethod
    def start_window():
        box = Tk()
        box.title("Interpreter Interface")
        box.geometry("650x450")
        # Add a background image
        bg_image = PhotoImage(file = "C:\\Users\\deeks\\OneDrive\\Desktop\\Projects\\Interpreter\\paint.png")
        bg_label = Label(box, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        def close():
            box.destroy()
        btn1 = Button(box,text = "Interpreter",fg="black",bg="SteelBlue1",width=20,font=(8),command=lambda: [close(),InterpreterGUI.Interpreter_window()])
        btn1.place(relx=0.5, rely=0.25, anchor=CENTER)
        btn2 = Button(box,text = "Exit",fg="black",bg="SteelBlue1",width=20,font=(8),command=close)
        btn2.place(relx=0.5, rely=0.75, anchor=CENTER)
        btn3 = Button(box,text = "Help Menu",fg="black",bg="SteelBlue1",width=20,font=(8),command=lambda: [close(),InterpreterGUI.menu_window()])
        btn3.place(relx=0.5, rely=0.5, anchor=CENTER)
        box.mainloop()

class InterpreterRunner():
    @staticmethod
    def constituent_evaluator(statement, constituent, variables, output_text):
        value = None
        if constituent.isdigit():
            if InterpreterRules.interpreter_number(int(constituent)):
                value = int(constituent)
            else:
                output_text.insert(END,f"{statement} (number must not have more than two digits)\n")
        elif constituent.isalpha():
            if InterpreterRules.interpreter_var(constituent):
                value = variables[constituent]
            else:
                output_text.insert(END,f"{statement} ({constituent} is not a valid variable)\n")
        else:
            output_text.insert(END,f"{statement} ({constituent} is not allowed in expression)\n")
        return value

    @staticmethod
    def expression_evaluator(statement, expression, variables, output_text):
        value = None
        if 1 <= len(expression):
            if (sum(not oper.isalnum() for oper in expression) == 0
                    or len(expression) == 1 or len(expression) == 2):
                value = InterpreterRunner.constituent_evaluator(statement,
                                                                expression, variables, output_text)
            elif sum(not oper.isalnum() for oper in expression) > 1:
                output_text.insert(END,f"{statement} (only one operator is allowed)\n")
            else:
                oper = None
                for oper in expression:
                    if not oper.isalnum():
                        break
                if expression.startswith(oper):
                    output_text.insert(END,f"{statement} ({oper} is not allowed at start of expression)\n")
                elif expression.endswith(oper):
                    output_text.insert(END,f"{statement} ({oper} is not allowed at end of expression)\n")
                else:
                    constituents = expression.split(oper)                  
                    constituent1 = constituents[0]
                    constituent2 = constituents[1]
                    value1 = InterpreterRunner.constituent_evaluator(statement,
                                                                     constituent1, variables, output_text)
                    value2 = InterpreterRunner.constituent_evaluator(statement,
                                                                     constituent2, variables, output_text)
                    if value1 is not None and value2 is not None:
                        if InterpreterRules.interpreter_oper(oper):
                            if oper == '+':
                                value = value1 + value2
                            elif oper == '-':
                                value = value1 - value2
                            elif oper == '*':
                                value = value1 * value2
                        else:
                            output_text.insert(END,"{statement} (operator is not valid)\n")
        else:
            if len(expression) == 0:
                output_text.insert(END,f"{statement} (no expression in statement)\n")
        return value

    @staticmethod
    def statement_evaluator(input_text, output_text):
        variables = {'A': None, 'B': None, 'C': None, 'D': None, 'E': None}
        output_text.delete("1.0", END)
        statements = input_text.get("1.0", END).splitlines()
        for statement in statements:
            if statement.find(' ') != -1:
                output_text.insert(END,f"{statement} (no spaces allowed)\n")
            else:
                if statement.find('=') != -1:
                    parts = statement.split('=')
                    var = parts[0]                            
                    expression = parts[1]
                    value = None
                    if var == '':
                        output_text.insert(END,"please give a variable before = operator\n")
                    elif InterpreterRules.interpreter_var(var):
                        value = InterpreterRunner.expression_evaluator(statement, expression, variables, output_text)
                    else:
                        output_text.insert(END,f"{statement} ({var} is not a valid variable)\n")
                    variables[var] = value
                else:
                    output_text.insert(END,statement, " (Not a valid Statement without = operator)\n")
        for var, value in variables.items():
            if value is not None:
                output_text.insert(END,f"{var}=   {value}\n")


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


InterpreterGUI.start_window()