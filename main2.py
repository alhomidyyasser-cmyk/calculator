

from __future__ import annotations

import ast
import math
import operator
import tkinter as tk


class SafeCalculator:
 
    BINARY = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
    }
    UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}
    CONSTANTS = {"pi": math.pi, "e": math.e}
    FUNCTIONS = {
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log10,
        "ln": math.log,
        "abs": abs,
    }

    @classmethod
    def calculate(cls, expression: str) -> float:
        expression = expression.replace("×", "*").replace("÷", "/").replace("^", "**").strip()
        if not expression:
            raise ValueError("اكتب عملية حسابية أولاً")
        try:
            tree = ast.parse(expression, mode="eval")
        except SyntaxError as error:
            raise ValueError("التعبير غير مكتمل أو غير صحيح") from error
        result = cls._evaluate(tree.body)
        if not math.isfinite(result):
            raise ValueError("النتيجة خارج النطاق المسموح")
        return result

    @classmethod
    def _evaluate(cls, node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return float(node.value)
        if isinstance(node, ast.BinOp) and type(node.op) in cls.BINARY:
            return cls.BINARY[type(node.op)](cls._evaluate(node.left), cls._evaluate(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in cls.UNARY:
            return cls.UNARY[type(node.op)](cls._evaluate(node.operand))
        if isinstance(node, ast.Name) and node.id in cls.CONSTANTS:
            return cls.CONSTANTS[node.id]
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in cls.FUNCTIONS
            and len(node.args) == 1
            and not node.keywords
        ):
            return cls.FUNCTIONS[node.func.id](cls._evaluate(node.args[0]))
        raise ValueError("هذه العملية غير مدعومة")


class CalculatorApp(tk.Tk):
    BG, PANEL, DISPLAY = "#111827", "#1f2937", "#0b1220"
    TEXT, MUTED, ACCENT, OPERATOR, DANGER = "#f9fafb", "#9ca3af", "#2563eb", "#374151", "#b91c1c"

    def __init__(self) -> None:
        super().__init__()
        self.title("الحاسبة الاحترافية")
        self.geometry("760x560")
        self.minsize(680, 500)
        self.configure(bg=self.BG)
        self.expression = tk.StringVar()
        self.status = tk.StringVar(value="جاهز للحساب")
        self.history: list[tuple[str, str]] = []
        self.memory = 0.0
        self._build_ui()
        self._bind_keys()
        self.display.focus_set()

    def _build_ui(self) -> None:
        header = tk.Frame(self, bg=self.BG)
        header.pack(fill="x", padx=22, pady=(18, 8))
        tk.Label(header, text="الحاسبة الاحترافية", bg=self.BG, fg=self.TEXT,
                 font=("Segoe UI", 18, "bold"), anchor="e").pack(side="right")
        tk.Label(header, text="عمليات أساسية ومتقدمة", bg=self.BG, fg=self.MUTED,
                 font=("Segoe UI", 10)).pack(side="right", padx=(0, 14), pady=6)

        content = tk.Frame(self, bg=self.BG)
        content.pack(fill="both", expand=True, padx=22, pady=(0, 18))
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=2)
        content.rowconfigure(0, weight=1)

        calculator = tk.Frame(content, bg=self.PANEL, padx=16, pady=16)
        calculator.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        calculator.columnconfigure(tuple(range(5)), weight=1)
        self.display = tk.Entry(calculator, textvariable=self.expression, justify="right",
                                bg=self.DISPLAY, fg=self.TEXT, insertbackground=self.TEXT,
                                relief="flat", font=("Consolas", 24), bd=0)
        self.display.grid(row=0, column=0, columnspan=5, sticky="ew", ipady=16, pady=(0, 8))
        tk.Label(calculator, textvariable=self.status, bg=self.PANEL, fg=self.MUTED,
                 font=("Segoe UI", 9), anchor="e").grid(row=1, column=0, columnspan=5,
                                                         sticky="ew", pady=(0, 10))

        buttons = [
            ("MC", lambda: self._memory("clear"), self.DANGER), ("MR", lambda: self._memory("recall"), self.OPERATOR),
            ("M+", lambda: self._memory("add"), self.OPERATOR), ("M−", lambda: self._memory("subtract"), self.OPERATOR),
            ("⌫", self._backspace, self.DANGER),
            ("sin", lambda: self._insert("sin("), self.OPERATOR), ("cos", lambda: self._insert("cos("), self.OPERATOR),
            ("tan", lambda: self._insert("tan("), self.OPERATOR), ("√", lambda: self._insert("sqrt("), self.OPERATOR),
            ("C", self._clear, self.DANGER),
            ("log", lambda: self._insert("log("), self.OPERATOR), ("ln", lambda: self._insert("ln("), self.OPERATOR),
            ("π", lambda: self._insert("pi"), self.OPERATOR), ("^", lambda: self._insert("^"), self.OPERATOR),
            ("÷", lambda: self._insert("÷"), self.ACCENT),
            ("7", lambda: self._insert("7"), self.PANEL), ("8", lambda: self._insert("8"), self.PANEL),
            ("9", lambda: self._insert("9"), self.PANEL), ("(", lambda: self._insert("("), self.OPERATOR),
            ("×", lambda: self._insert("×"), self.ACCENT),
            ("4", lambda: self._insert("4"), self.PANEL), ("5", lambda: self._insert("5"), self.PANEL),
            ("6", lambda: self._insert("6"), self.PANEL), (")", lambda: self._insert(")"), self.OPERATOR),
            ("−", lambda: self._insert("-"), self.ACCENT),
            ("1", lambda: self._insert("1"), self.PANEL), ("2", lambda: self._insert("2"), self.PANEL),
            ("3", lambda: self._insert("3"), self.PANEL), ("%", lambda: self._insert("%"), self.OPERATOR),
            ("+", lambda: self._insert("+"), self.ACCENT),
            ("0", lambda: self._insert("0"), self.PANEL), (".", lambda: self._insert("."), self.PANEL),
            ("e", lambda: self._insert("e"), self.OPERATOR), ("abs", lambda: self._insert("abs("), self.OPERATOR),
            ("=", self._calculate, "#16a34a"),
        ]
        for index, (label, command, color) in enumerate(buttons):
            row, column = divmod(index, 5)
            tk.Button(calculator, text=label, command=command, bg=color, fg=self.TEXT,
                      activebackground=self.ACCENT, activeforeground=self.TEXT, relief="flat", bd=0,
                      cursor="hand2", font=("Segoe UI", 12, "bold"), padx=5, pady=11).grid(
                          row=row + 2, column=column, sticky="nsew", padx=3, pady=3)

        history_panel = tk.Frame(content, bg=self.PANEL, padx=14, pady=14)
        history_panel.grid(row=0, column=1, sticky="nsew")
        title_row = tk.Frame(history_panel, bg=self.PANEL)
        title_row.pack(fill="x", pady=(0, 10))
        tk.Label(title_row, text="سجل العمليات", bg=self.PANEL, fg=self.TEXT,
                 font=("Segoe UI", 13, "bold")).pack(side="right")
        tk.Button(title_row, text="مسح", command=self._clear_history, bg=self.OPERATOR,
                  fg=self.TEXT, relief="flat", cursor="hand2").pack(side="left")
        self.history_box = tk.Listbox(history_panel, bg=self.DISPLAY, fg=self.TEXT,
                                      selectbackground=self.ACCENT, selectforeground=self.TEXT,
                                      relief="flat", bd=0, font=("Consolas", 11), activestyle="none")
        self.history_box.pack(fill="both", expand=True)
        self.history_box.bind("<Double-Button-1>", self._reuse_history)
        tk.Label(history_panel, text="انقر مرتين على نتيجة لإعادة استخدامها\nEnter للحساب • Esc للمسح",
                 justify="right", bg=self.PANEL, fg=self.MUTED, font=("Segoe UI", 9)).pack(
                     anchor="e", pady=(10, 0))

    def _bind_keys(self) -> None:
        self.bind("<Return>", lambda _event: self._calculate())
        self.bind("<Escape>", lambda _event: self._clear())
        self.bind("<KeyRelease>", lambda _event: self.status.set("اضغط Enter لعرض النتيجة"))

    def _insert(self, value: str) -> None:
        self.display.insert(self.display.index(tk.INSERT), value)
        self.display.focus_set()

    def _clear(self) -> None:
        self.expression.set("")
        self.status.set("تم مسح العملية")
        self.display.focus_set()

    def _backspace(self) -> None:
        position = self.display.index(tk.INSERT)
        if position:
            self.display.delete(position - 1, position)
        self.display.focus_set()

    def _calculate(self) -> None:
        expression = self.expression.get()
        try:
            result = SafeCalculator.calculate(expression)
        except (ValueError, ZeroDivisionError, OverflowError) as error:
            self.status.set(f"خطأ: {error}")
            self.bell()
            return
        shown_result = self._format_number(result)
        self.expression.set(shown_result)
        self.status.set("تم الحساب بنجاح")
        self.history.insert(0, (expression, shown_result))
        self.history_box.insert(0, f"{expression} = {shown_result}")
        self.display.icursor(tk.END)

    def _memory(self, action: str) -> None:
        if action == "clear":
            self.memory = 0.0
            self.status.set("تم مسح الذاكرة")
            return
        if action == "recall":
            self._insert(self._format_number(self.memory))
            self.status.set("تم استدعاء قيمة الذاكرة")
            return
        try:
            value = SafeCalculator.calculate(self.expression.get())
        except (ValueError, ZeroDivisionError, OverflowError):
            self.status.set("احسب قيمة صحيحة أولاً لاستخدام الذاكرة")
            self.bell()
            return
        updated_memory = self.memory + value if action == "add" else self.memory - value
        if not math.isfinite(updated_memory):
            self.status.set("قيمة الذاكرة خارج النطاق المسموح")
            self.bell()
            return
        self.memory = updated_memory
        self.status.set(f"قيمة الذاكرة: {self._format_number(self.memory)}")

    def _clear_history(self) -> None:
        self.history.clear()
        self.history_box.delete(0, tk.END)
        self.status.set("تم مسح السجل")

    def _reuse_history(self, _event: tk.Event) -> None:
        selection = self.history_box.curselection()
        if selection:
            self.expression.set(self.history[selection[0]][1])
            self.display.icursor(tk.END)
            self.display.focus_set()
            self.status.set("تمت إعادة استخدام النتيجة")

    @staticmethod
    def _format_number(value: float) -> str:
        return str(int(value)) if value.is_integer() else f"{value:.12g}"


if __name__ == "__main__":
    CalculatorApp().mainloop()
