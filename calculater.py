import tkinter as tk

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.resizable(False, False)

        self.expr = ""  # what the user is building
        self.display_var = tk.StringVar(value="0")

        self._build_ui()

    def _build_ui(self):
        display = tk.Entry(
            self,
            textvariable=self.display_var,
            font=("Arial", 20),
            bd=10,
            relief="ridge",
            justify="right"
        )
        display.grid(row=0, column=0, columnspan=4, sticky="nsew")

        # Button layout
        buttons = [
            ("C", 1, 0), ("⌫", 1, 1), ("%", 1, 2), ("÷", 1, 3),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("×", 2, 3),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("−", 3, 3),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3),
            ("0", 5, 0), (".", 5, 1), ("(", 5, 2), (")", 5, 3),
            ("=", 6, 0),  # "=" spans columns 1-3
        ]

        # Make grid columns expand evenly
        for col in range(4):
            self.grid_columnconfigure(col, weight=1)
        for row in range(7):
            self.grid_rowconfigure(row, weight=1)

        # Create buttons
        for (text, r, c) in buttons:
            if text == "=":
                btn = tk.Button(
                    self, text=text, font=("Arial", 18),
                    command=self.calculate, bg="#2d7ff9", fg="white"
                )
                btn.grid(row=r, column=c, columnspan=4, sticky="nsew", padx=2, pady=2)
                continue

            cmd = lambda t=text: self.on_button(t)
            btn = tk.Button(self, text=text, font=("Arial", 18), command=cmd)

            # Styling: operators slightly different
            if text in {"+", "−", "×", "÷"}:
                btn.configure(bg="#e9ecef")
            elif text in {"C", "⌫"}:
                btn.configure(bg="#ffdddd")

            btn.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)

    def on_button(self, char: str):
        if char == "C":
            self.expr = ""
            self.display_var.set("0")
            return

        if char == "⌫":
            self.expr = self.expr[:-1]
            self.display_var.set(self.expr if self.expr else "0")
            return

        # Map display symbols to actual operators
        mapping = {
            "÷": "/",
            "×": "*",
            "−": "-",
        }
        if char in mapping:
            char = mapping[char]

        self.expr += char
        self.display_var.set(self.expr)

    def calculate(self):
        if not self.expr.strip():
            return

        try:
            # Evaluate expression safely enough for a tutorial
            # (In production, you'd want a safer parser.)
            result = eval(self.expr, {"__builtins__": {}}, {})
            self.display_var.set(str(result))
            self.expr = str(result)
        except Exception:
            self.display_var.set("Error")
            self.expr = ""

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()