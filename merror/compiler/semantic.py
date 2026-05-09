# merror/compiler/semantic.py

from merror.compiler.ast_nodes import *
from merror.utils.keyword_map import BUILTINS
from merror.utils.symbol_table import SymbolTable


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        # هات السيمبول تيبل

    # ── Entry ───────────────────────────

    def analyze(self, node):
        method = f"visit_{type(node).__name__}"
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

#هيحلل ويزور النود لو موجودة استخدمها مش موجةدة جينيريك فيزيت
    def generic_visit(self, node):
        raise Exception(f"No visit method for {type(node).__name__}")
# مش معانا فيزيت فانكشن ليها فبنضرب ايرور
    # ── Program ─────────────────────────

    def visit_Program(self, node):
        for stmt in node.statements:
            self.analyze(stmt)


    # ── Block ───────────────────────────

    def visit_Block(self, node):
        self.symbol_table.enter_scope()

        for stmt in node.statements:
            self.analyze(stmt)

        self.symbol_table.exit_scope()
        # خش البلوك وحلل كله واطلع

    # ── Assignment ──────────────────────

    def visit_Assignment(self, node):
        value = self.analyze(node.value)

        # define variable in current scope
        self.symbol_table.define(node.name, value)
        # هتشوف الفاليو وتحددها

    # ── Identifier ──────────────────────

    def visit_Identifier(self, node):
        value = self.symbol_table.lookup(node.name)
        # هنشوفها ولو مفيش فليو يبقى اضرب ايرور ولو في رجعها عادي

        if value is None:
            raise Exception(f"Undefined variable '{node.name}'")

        # print(f"[Semantic] Using variable: {node.name}")


        return value

    # ── Expressions ─────────────────────

    def visit_Number(self, node):
        return "number"
    # رجع رقم

    def visit_String(self, node):
        return "string"
    # رجع السترينج

    def visit_BinaryOp(self, node):
        left = self.analyze(node.left)
        right = self.analyze(node.right)

        # Only reject when BOTH sides are known concrete types that actually differ
        # (unknown means a function return — we can't know its type yet, so skip)
        arithmetic_ops = {"+", "-", "*", "/", "//", "%", "**"}
        known = {"number", "string", "bool"}
        if (node.operator in arithmetic_ops
                and left in known and right in known
                and left != right):
            raise Exception(
                f"Type mismatch: cannot apply '{node.operator}' to {left} and {right}"
            )

        return left

    def visit_UnaryOp(self, node):
        # analyze the inner expression first
        operand_type = self.analyze(node.operand)

        # حل الرقم اللي عاملينه يوناري
        # print(f"[Semantic] UnaryOp: {node.operator}{operand_type}")

        # ── handle numeric unary operators ──
        if node.operator in ("-", "+"):
            if operand_type != "number":
                raise Exception(
                    f"Type error: unary '{node.operator}' expects number but got {operand_type}"
                )
            return "number"
        # لو سالب او موجب توقع رقم لو مفيش اضرب ايرور

        # ── handle logical NOT ──
        if node.operator == "not":
            if operand_type != "bool":
                raise Exception(
                    f"Type error: 'not' expects bool but got {operand_type}"
                )
            return "bool"
        # توقع ان لازم الاوبراند يبقى بوليان لو مش وليان اضرب ايرور

        # fallback (safety)
        raise Exception(f"Unknown unary operator '{node.operator}'")
# لو حط حاجة غريبة هوب ايرور

    # ── Control Flow ────────────────────

    def visit_IfStatement(self, node):
        self.analyze(node.condition)
        self.analyze(node.then_branch)
        # هات الكونديشن والفروع

        for cond, block in node.elif_branches:
            self.analyze(cond)
            self.analyze(block)
# حل كله برضو في الفروع
        if node.else_branch:
            self.analyze(node.else_branch)
            # لو في الس برضو

    def visit_WhileStatement(self, node):
        self.analyze(node.condition)
        self.analyze(node.body)
        # هات الكونديشن والبادي

    def visit_ReturnStatement(self, node):
        if node.value:
            self.analyze(node.value)
            # لو في ليها قيمة اصلا هاتها

    def visit_FunctionDef(self, node):
        # register function in symbol table
        self.symbol_table.define_function(node.name, len(node.params))
        self.symbol_table.enter_scope()
        for param in node.params:
            self.symbol_table.define(param, "unknown")
        for stmt in node.body.statements:
            self.analyze(stmt)
        self.symbol_table.exit_scope()

    def visit_ForStatement(self, node):
        self.analyze(node.iterable)
        self.symbol_table.enter_scope()
        self.symbol_table.define(node.var, "unknown")
        for stmt in node.body.statements:
            self.analyze(stmt)
        self.symbol_table.exit_scope()

    def visit_BreakStatement(self, node):
        pass

    def visit_ContinueStatement(self, node):
        pass

    def visit_Boolean(self, node):
        return "bool"

    def visit_NoneVal(self, node):
        return "none"

    def visit_ExpressionStatement(self, node):
        self.analyze(node.expression)

    def visit_FunctionCall(self, node):
        # 1. check function exists
        if node.name not in self.symbol_table.functions and node.name not in BUILTINS:
            raise Exception(f"Undefined function '{node.name}'")

        # 2. analyze args
        arg_types = []
        for arg in node.args:
            arg_types.append(self.analyze(arg))

        # print(f"[Semantic] Function call: {node.name}({arg_types})")

        # 3. return type (temporary)
        return "unknown"

##### we get an output of it in the terminal
    def visit_Assignment(self, node):
        value = self.analyze(node.value)
        # هات الفيمة لو القيمة دي بالصدفة رقمين
        # مثلا x= 2+3
        # هيحلل الرقمين ويجمعهم ويخزنهم في المتغير

        # print(f"[Semantic] Defining variable: {node.name}")

        self.symbol_table.define(node.name, value)


        return "unknown"