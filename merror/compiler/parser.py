# merror/compiler/parser.py

from typing import List
from merror.compiler.scanner import Token, TokenType
from merror.compiler.ast_nodes import *

# recursive descent parser
class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
# assign token and point the position of the token to 0
    # ── Helpers ─────────────────────────

    def current(self):
        return self.tokens[self.pos]
    # the current token is where we are

    def advance(self):
        self.pos += 1
        # just move on

    def expect(self, type_, value=None):
        tok = self.current()
        if tok.type != type_ or (value and tok.value != value):
            raise SyntaxError(
                f"[Line {tok.line}, Col {tok.col}] "
                f"Expected {value or type_.name}, got '{tok.value}'"
            )
        self.advance()
        return tok
    # get the curent token and if we find the type or value dont mach then raise an error

    def match(self, type_, value=None):
        tok = self.current()
        if tok.type == type_ and (value is None or tok.value == value):
            self.advance()
            return True
        return False
    # just an optional function to match


    def peek(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return self.tokens[self.pos]
#ادي بصة للي جاي منغير ما تتحرك
    # ── Entry ───────────────────────────

    def parse(self):
        # ast root
        statements = []
        while self.current().type != TokenType.EOF:
            # لف عالكود كله وسكيب الكومنتات ولو لقيت اننا وصلنا للاند اوف فايل كلسن
            self.skip_comments()
            if self.current().type == TokenType.EOF:
                break
            statements.append(self.parse_statement())
            # ابني لast
        return Program(statements)

    #cuz we used a dataclass that have a auto __repr__

    # ── Statements ──────────────────────

    def parse_statement(self):
        # هنقرر هنا البتاع دا جملة اساين ولا كونديشن ولا لوب
        self.skip_comments()
        tok = self.current()
# سكيب الكومنتات برضو وهات الكرنت
        # IF
        if tok.value == "fi":
            stmt = self.parse_if()
            # لو لقيت اولها ايف استدعي فانكشن بارس الايف وهكذا بقى لاخر الكود مش هعيد وازيد

        # WHILE
        elif tok.value == "elihw":
            stmt = self.parse_while()

        # RETURN
        elif tok.value == "nruter":
            stmt = self.parse_return()

        # ASSIGNMENT
        elif tok.type == TokenType.IDENTIFIER and self.peek().value == "=":
            stmt = self.parse_assignment()

        # EXPRESSION
        else:
            stmt = ExpressionStatement(self.parse_expression())

        #  consume semicolon AFTER parsing
        self.match(TokenType.DELIMITER, ";")

        return stmt

    # ── IF ──────────────────────────────

    def parse_if(self):
        self.expect(TokenType.KEYWORD, "fi")
        # هتتوقع ان بديهي اللي جاي ايف

        condition = self.parse_expression()
        # الكونديشن هتعمله بارس اكسبرشن
        then_branch = self.parse_block()
# هتبارس بلوك عشان تتاكد ان القوس مقفول
        elifs = []
        while self.match(TokenType.KEYWORD, "file"):
            cond = self.parse_expression()
            block = self.parse_block()
            elifs.append((cond, block))

        else_branch = None
        if self.match(TokenType.KEYWORD, "esle"):
            else_branch = self.parse_block()
# لو لقيت ايف هاتلي الكونديشن والاللي هيحصل والالس وكله
        return IfStatement(condition, then_branch, elifs, else_branch)

    # ── WHILE ───────────────────────────

    def parse_while(self):
        self.expect(TokenType.KEYWORD, "elihw")
        condition = self.parse_expression()
        body = self.parse_block()
        # هتتوقع وايل وهتجيب اللي فيها وتترجعها
        return WhileStatement(condition, body)

    # ── RETURN ──────────────────────────

    def parse_return(self):
        self.expect(TokenType.KEYWORD, "nruter")
        # هتتوقع ريترن

        if self.current().type == TokenType.DELIMITER and self.current().value == ";":
            return ReturnStatement(None)


        return ReturnStatement(self.parse_expression())

    # ── BLOCK ───────────────────────────

    def parse_block(self):
        self.expect(TokenType.DELIMITER, "{")
# هتتوقع قوس مفتوح
        statements = []
# ليست تحط فيها الجمل
        while True:
            self.skip_comments()
# سكيب كومنتتات
            if self.current().type == TokenType.EOF:
                tok = self.current()
                raise SyntaxError(
                    f"[Line {tok.line}] Expected '}}' before end of file"
                )
# لو ملقتش القوس التاني اضرب ايرور
            if self.match(TokenType.DELIMITER, "}"):
                break
                # لو لقيته اقفل وحط الستيتسمنت ورجع البلوك وخلاص متصدعناش

            statements.append(self.parse_statement())

        return Block(statements)

    # ── ASSIGNMENT ──────────────────────

    def parse_assignment(self):
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.OPERATOR, "=")
        value = self.parse_expression()
        return Assignment(name, value)
    # هتجيب ايدنتفاير ولازم = وخلاص رجعه


    # ── EXPRESSIONS ─────────────────────
    # كل واحد بيبدا باللي بعده عشان نظبط الترتيب

    def parse_expression(self):
        return self.parse_logical_or()
# بنستعمل اور عشان الترتيب
    def parse_logical_or(self):
        node = self.parse_logical_and()
        while self.match(TokenType.KEYWORD, "ro"):
            node = BinaryOp(node, "or", self.parse_logical_and())
        return node

    def parse_logical_and(self):
        node = self.parse_equality()
        while self.match(TokenType.KEYWORD, "dna"):
            node = BinaryOp(node, "and", self.parse_equality())
        return node
    # ماتش الاند وحطها في نود عادي

    def parse_equality(self):
        # حل المقارنات الاول
        node = self.parse_comparison()
        while True:
            if self.current().value == "=":
                tok = self.current()
                raise SyntaxError(
                    f"[Line {tok.line}, Col {tok.col}] "
                    f"Use '==' for comparison, not '='"
                )
# لو لقيت تمام مفيش خلاص شوف اليساوي او لا يساوي وحطهم في نود
            if self.current().value in ("==", "!="):
                op = self.current().value
                self.advance()
                node = BinaryOp(node, op, self.parse_comparison())
            else:
                break
        return node

    def parse_comparison(self):
        # حل التيرم قبل ما تقارن
        node = self.parse_term()
        while self.current().value in ("<", ">", "<=", ">="):
            op = self.current().value
            self.advance()
            node = BinaryOp(node, op, self.parse_term())
            # خلاص لقيت الدنيا تمما حط في نود وحط المقارنة بينهم اكبر ولا اصغر ولا ايه
        return node

    def parse_term(self):
        # التيرم جمع وطرح الفاكتور ضرب وقسمة فانت هتحل الفاكتور لو الدنيا تمام خلاص خش حط الزائد او ناقص واعمل نود
        node = self.parse_factor()
        while self.current().value in ("+", "-"):
            op = self.current().value
            self.advance()
            node = BinaryOp(node, op, self.parse_factor())
        return node

    def parse_factor(self):
        # بارس اليوناري اللي هي سالب موجب او نوت لو خلاص تمام اضرب واقسم براحتك وحط في النود
        node = self.parse_unary()
        while self.current().value in ("*", "/", "%"):
            op = self.current().value
            self.advance()
            node = BinaryOp(node, op, self.parse_unary())
        return node

    def parse_unary(self):
        # دا اصغر حاجة خلاص خش على طول شوف الدنيا
        if self.current().value in ("-", "+"):
            op = self.current().value
            self.advance()
            return UnaryOp(op, self.parse_unary())
# لو لقيت قدامها نوت حطها نوت
        if self.match(TokenType.KEYWORD, "ton"):
            return UnaryOp("not", self.parse_unary())

        return self.parse_primary()

    # ── PRIMARY ─────────────────────────

    def parse_primary(self):
        # دا رقم سترينج او ايدنتفاير

        tok = self.current()

        if tok.type == TokenType.NUMBER:
            self.advance()
            return Number(tok.value)
        # لو رقم حطه في رقم وهكذا للباقي

        if tok.type == TokenType.STRING:
            self.advance()
            return String(tok.value)

        if tok.type == TokenType.IDENTIFIER:
            if self.peek().value == "(":
                return self.parse_call()
            self.advance()
            return Identifier(tok.value)

        if tok.value == "(":
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.DELIMITER, ")")
            return expr
        # لو قوس توقع اخوه

        raise SyntaxError(
            f"[Line {tok.line}, Col {tok.col}] Unexpected '{tok.value}'"
        )

    def skip_comments(self):
        while self.current().type == TokenType.COMMENT:
            self.advance()
            # اول ما تلاقي التوكن كومنت اتحرك ومتحطهوش في الليستة

    def parse_call(self):
        # هنجيب الفانكشن بقى هتحط اسم الفانكشن وتتوقع قوس وتلم الرجيومنتس وتتوقع فصلة وتتوقع قوس وخلاص
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.DELIMITER, "(")

        args = []
        if self.current().value != ")":
            args.append(self.parse_expression())
            while self.match(TokenType.DELIMITER, ","):
                args.append(self.parse_expression())

        self.expect(TokenType.DELIMITER, ")")
        return FunctionCall(name, args)