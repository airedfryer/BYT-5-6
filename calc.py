import tkinter as tk


class Handler:
    def __init__(self, successor=None):
        self.successor = successor

    def handle_request(self, operation, num1, num2):
        if self.successor is not None:
            self.successor.handle_request(operation, num1, num2)


class AddHandler(Handler):
    def handle_request(self, operation, num1, num2):
        if operation == "+":
            result = num1 + num2
            print(f"{num1} + {num2} = {result}")
        else:
            super().handle_request(operation, num1, num2)


class SubtractHandler(Handler):
    def handle_request(self, operation, num1, num2):
        if operation == "-":
            result = num1 - num2
            print(f"{num1} - {num2} = {result}")
        else:
            super().handle_request(operation, num1, num2)


class MultiplyHandler(Handler):
    def handle_request(self, operation, num1, num2):
        if operation == "*":
            result = num1 * num2
            print(f"{num1} * {num2} = {result}")
        else:
            super().handle_request(operation, num1, num2)


class DivideHandler(Handler):
    def handle_request(self, operation, num1, num2):
        if operation == "/":
            if num2 != 0:
                result = num1 / num2
                print(f"{num1} / {num2} = {result}")
            else:
                print("Cannot divide by zero.")
        else:
            super().handle_request(operation, num1, num2)


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")

        self.num1_entry = tk.Entry(root)
        self.num2_entry = tk.Entry(root)

        self.num1_entry.grid(row=0, column=0, padx=10, pady=10)
        self.num2_entry.grid(row=0, column=1, padx=10, pady=10)

        self.add_button = tk.Button(root, text="+", command=lambda: self.calculate("+"))
        self.subtract_button = tk.Button(root, text="-", command=lambda: self.calculate("-"))
        self.multiply_button = tk.Button(root, text="*", command=lambda: self.calculate("*"))
        self.divide_button = tk.Button(root, text="/", command=lambda: self.calculate("/"))

        self.add_button.grid(row=2, column=0, pady=10)
        self.subtract_button.grid(row=2, column=1, pady=10)
        self.multiply_button.grid(row=3, column=0, pady=10)
        self.divide_button.grid(row=3, column=1, pady=10)

        self.handler_chain = AddHandler(
            SubtractHandler(
                MultiplyHandler(
                    DivideHandler()
                )
            )
        )

    def calculate(self, operation):
        try:
            num1 = float(self.num1_entry.get())
            num2 = float(self.num2_entry.get())
            self.handler_chain.handle_request(operation, num1, num2)
        except ValueError:
            print("Invalid input. Please enter valid numbers.")


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
