# merror/compiler/scanner.py

import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import List

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from merror.utils.keyword_map import KEYWORDS, BUILTINS


class TokenType(Enum):
    KEYWORD    = auto()
    BUILTIN    = auto()
    IDENTIFIER = auto()
    NUMBER     = auto()
    STRING     = auto()
    OPERATOR   = auto()
    DELIMITER  = auto()
    COMMENT    = auto()
    EOF        = auto()


@dataclass
class Token:
    type:  TokenType
    value: str
    line:  int
    col:   int

    def __repr__(self):
        return f"Token({self.type.name:<12} {self.value!r:<20} line={self.line}, col={self.col})"


class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.pos    = 0
        self.line   = 1
        self.col    = 1

    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            ch = self.source[self.pos]

            # Skip whitespace (including newlines — no indent rules anymore)
            if ch in (" ", "\t", "\n", "\r"):
                if ch == "\n":
                    self.line += 1
                    self.col = 1
                else:
                    self.col += 1
                self.pos += 1

            elif ch == "#":
                self._scan_comment()

            elif ch in ('"', "'"):
                self._scan_string()

            elif ch.isdigit():
                self._scan_number()

            elif ch.isalpha() or ch == "_":
                self._scan_word()

            else:
                self._scan_operator()

        self.tokens.append(Token(TokenType.EOF, "", self.line, self.col))
        return self.tokens

    # ── Helpers ──────────────────────────────────────

    def _add(self, type, value, line, col):
        self.tokens.append(Token(type, value, line, col))

    # ── Word: keyword / builtin / identifier ─────────

    def _scan_word(self):
        line, col = self.line, self.col
        match = re.match(r'[a-zA-Z_][a-zA-Z0-9_]*', self.source[self.pos:])
        word = match.group()
        self.pos += len(word)
        self.col += len(word)

        if word in KEYWORDS:
            self._add(TokenType.KEYWORD, word, line, col)
        elif word in BUILTINS:
            self._add(TokenType.BUILTIN, word, line, col)
        else:
            self._add(TokenType.IDENTIFIER, word, line, col)

    # ── Number ───────────────────────────────────────

    def _scan_number(self):
        line, col = self.line, self.col
        match = re.match(r'\d+(\.\d+)?', self.source[self.pos:])
        value = match.group()
        self.pos += len(value)
        self.col += len(value)
        self._add(TokenType.NUMBER, value, line, col)

    # ── String ───────────────────────────────────────

    def _scan_string(self):
        line, col = self.line, self.col
        quote = self.source[self.pos]
        pattern = r'"(\\.|[^"\\])*"' if quote == '"' else r"'(\\.|[^'\\])*'"
        match = re.match(pattern, self.source[self.pos:])
        if not match:
            raise SyntaxError(f"[Line {line}, Col {col}] Unterminated string")
        value = match.group()
        self.pos += len(value)
        self.col += len(value)
        self._add(TokenType.STRING, value, line, col)

    # ── Operators + Delimiters ───────────────────────

    def _scan_operator(self):
        line, col = self.line, self.col

        # Multi-char operators first (longest match wins)
        multi = ["==", "!=", "<=", ">=", "**", "//", "->", "+=", "-=", "*=", "/="]
        for op in multi:
            if self.source[self.pos:self.pos + len(op)] == op:
                self.pos += len(op)
                self.col += len(op)
                self._add(TokenType.OPERATOR, op, line, col)
                return

        ch = self.source[self.pos]
        self.pos += 1
        self.col += 1

        if ch in "+-*/%=<>!&|^~":
            self._add(TokenType.OPERATOR, ch, line, col)

        elif ch in "{}();,.:[]":
            # { } open/close blocks
            # ; statement terminator
            # ( ) [ ] , . : standard delimiters
            self._add(TokenType.DELIMITER, ch, line, col)

        else:
            raise SyntaxError(f"[Line {line}, Col {col}] Unexpected character '{ch}'")

    # ── Comment ──────────────────────────────────────

    def _scan_comment(self):
        line, col = self.line, self.col
        match = re.match(r'#[^\n]*', self.source[self.pos:])
        value = match.group()
        self.pos += len(value)
        self.col += len(value)
        self._add(TokenType.COMMENT, value, line, col)
