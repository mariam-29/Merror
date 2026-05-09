# merror/compiler/ast_nodes.py

from dataclasses import dataclass
from typing import List, Optional

# الكلاس اللي كله بيورثه هو ابوهم ملوش لازمة غير انه بيتورث
class ASTNode:
    pass


# ── Program ─────────────────────────────

@dataclass
class Program(ASTNode):
    statements: List[ASTNode]

# اعلى نود بنلم فيها البروجرام كله
# ── Statements ─────────────────────────

@dataclass
class Block(ASTNode):
    statements: List[ASTNode]
# نود البلوك

@dataclass
class Assignment(ASTNode):
    name: str
    value: ASTNode


@dataclass
class IfStatement(ASTNode):
    condition: ASTNode
    then_branch: Block
    elif_branches: List[tuple]
    else_branch: Optional[Block]


@dataclass
class WhileStatement(ASTNode):
    condition: ASTNode
    body: Block


@dataclass
class ForStatement(ASTNode):
    var: str
    iterable: ASTNode
    body: Block


@dataclass
class FunctionDef(ASTNode):
    name: str
    params: List[str]
    body: Block


@dataclass
class ReturnStatement(ASTNode):
    value: Optional[ASTNode]


@dataclass
class ExpressionStatement(ASTNode):
    expression: ASTNode


@dataclass
class BreakStatement(ASTNode):
    pass


@dataclass
class ContinueStatement(ASTNode):
    pass


# ── Expressions ─────────────────────────

@dataclass
class BinaryOp(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class UnaryOp(ASTNode):
    operator: str
    operand: ASTNode


@dataclass
class Number(ASTNode):
    value: str


@dataclass
class String(ASTNode):
    value: str


@dataclass
class Boolean(ASTNode):
    value: str   # "True" or "False"


@dataclass
class NoneVal(ASTNode):
    pass


@dataclass
class Identifier(ASTNode):
    name: str


@dataclass
class FunctionCall(ASTNode):
    name: str
    args: List[ASTNode]