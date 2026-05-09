# merror/compiler/transpiler.py
# Walks the AST and emits valid Python source code.

from merror.compiler.ast_nodes import *
from merror.utils.keyword_map import KEYWORDS, BUILTINS

# Combined reverse-map: merror name → python name
_NAME_MAP = {**KEYWORDS, **BUILTINS}


def _py_name(name: str) -> str:
    """Translate a Merror identifier/builtin/keyword to its Python equivalent."""
    return _NAME_MAP.get(name, name)


class Transpiler:
    def __init__(self):
        self._indent = 0

    # ── Indentation helpers ──────────────────────────────

    def _ind(self) -> str:
        return "    " * self._indent

    def _block(self, block: Block) -> str:
        self._indent += 1
        lines = []
        for stmt in block.statements:
            lines.append(self._ind() + self._emit(stmt))
        if not lines:
            lines.append(self._ind() + "pass")
        self._indent -= 1
        return "\n".join(lines)

    # ── Entry point ──────────────────────────────────────

    def transpile(self, program: Program) -> str:
        lines = []
        for stmt in program.statements:
            lines.append(self._emit(stmt))
        return "\n".join(lines) + "\n"

    # ── Dispatcher ───────────────────────────────────────

    def _emit(self, node: ASTNode) -> str:
        method = f"_emit_{type(node).__name__}"
        handler = getattr(self, method, None)
        if handler is None:
            raise NotImplementedError(f"Transpiler: no handler for {type(node).__name__}")
        return handler(node)

    # ── Statements ───────────────────────────────────────

    def _emit_Assignment(self, node: Assignment) -> str:
        return f"{node.name} = {self._emit(node.value)}"

    def _emit_IfStatement(self, node: IfStatement) -> str:
        lines = [f"if {self._emit(node.condition)}:"]
        lines.append(self._block(node.then_branch))

        for cond, blk in node.elif_branches:
            lines.append(f"{self._ind()}elif {self._emit(cond)}:")
            lines.append(self._block(blk))

        if node.else_branch:
            lines.append(f"{self._ind()}else:")
            lines.append(self._block(node.else_branch))

        return "\n".join(lines)

    def _emit_WhileStatement(self, node: WhileStatement) -> str:
        lines = [f"while {self._emit(node.condition)}:"]
        lines.append(self._block(node.body))
        return "\n".join(lines)

    def _emit_ForStatement(self, node: ForStatement) -> str:
        lines = [f"for {node.var} in {self._emit(node.iterable)}:"]
        lines.append(self._block(node.body))
        return "\n".join(lines)

    def _emit_FunctionDef(self, node: FunctionDef) -> str:
        params = ", ".join(node.params)
        lines = [f"def {node.name}({params}):"]
        lines.append(self._block(node.body))
        return "\n".join(lines)

    def _emit_ReturnStatement(self, node: ReturnStatement) -> str:
        if node.value is None:
            return "return"
        return f"return {self._emit(node.value)}"

    def _emit_ExpressionStatement(self, node: ExpressionStatement) -> str:
        return self._emit(node.expression)

    def _emit_BreakStatement(self, node: BreakStatement) -> str:
        return "break"

    def _emit_ContinueStatement(self, node: ContinueStatement) -> str:
        return "continue"

    # ── Expressions ──────────────────────────────────────

    def _emit_BinaryOp(self, node: BinaryOp) -> str:
        left = self._emit(node.left)
        right = self._emit(node.right)

        # Wrap compound sub-expressions in parens for safety
        if isinstance(node.left, BinaryOp):
            left = f"({left})"
        if isinstance(node.right, BinaryOp):
            right = f"({right})"

        return f"{left} {node.operator} {right}"

    def _emit_UnaryOp(self, node: UnaryOp) -> str:
        operand = self._emit(node.operand)
        if node.operator == "not":
            return f"not {operand}"
        return f"{node.operator}{operand}"

    def _emit_FunctionCall(self, node: FunctionCall) -> str:
        py_name = _py_name(node.name)
        args = ", ".join(self._emit(a) for a in node.args)
        return f"{py_name}({args})"

    def _emit_Identifier(self, node: Identifier) -> str:
        return node.name

    def _emit_Number(self, node: Number) -> str:
        return node.value

    def _emit_String(self, node: String) -> str:
        return node.value

    def _emit_Boolean(self, node: Boolean) -> str:
        return node.value  # "True" or "False"

    def _emit_NoneVal(self, node: NoneVal) -> str:
        return "None"
