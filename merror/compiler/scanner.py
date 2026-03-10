# merror/compiler/scanner.py

import re
# regular expressions library
from dataclasses import dataclass
# so we can make a class for data wout having to write boilerplate ( no need to write __init__ or repr or eq)
from enum import Enum, auto
#lets you create a list of named constants like KEYWORD, NUMBER, etc.
from typing import List

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from merror.utils.keyword_map import KEYWORDS, BUILTINS
# adds the project root to Python's search path so it can find keyword_map.py, then imports the two dicts


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
#just a list of all possible token categories. auto() means "give this a number automatically, I don't care what it is"

@dataclass
class Token:
    type:  TokenType
    value: str
    line:  int
    col:   int
#a single token — holds 4 things: what type it is, its raw text, what line it's on, what column it's on
    def __repr__(self):
        return f"Token({self.type.name:<12} {self.value!r:<20} line={self.line}, col={self.col})"
#controls how the token prints. :<12 means pad to 12 chars wide so columns line up nicely in output

class Scanner:
    def __init__(self, source: str):
        self.source = source  # the raw merror code string
        self.tokens = []  # list we'll fill with tokens
        self.pos = 0  # current character index we're reading
        self.line = 1  # current line number
        self.col = 1  # current column number

    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            ch = self.source[self.pos] # peek at current char
              # keeps looping through every character until we hit the end
            # Skip whitespace (including newlines — no indent rules anymore)
            if ch in (" ", "\r"):

                self.col += 1
                self.pos += 1

            elif ch == "#":
                self._scan_comment()
            elif ch == "\n":
                self.line = self.line + 1
                self.pos += 1
            elif ch =="\t":
                self.col =+4
                self.pos += 1

            elif ch in ('"', "'"):
                self._scan_string()

            elif ch.isdigit():
                self._scan_number()

            elif ch.isalpha() or ch == "_":
                self._scan_word()

            else:
                self._scan_operator()
                 #based on the current character, decide which scanner method to call
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.col))
        #after the loop ends, add an EOF token to signal "we're done", then return the full list

        return self.tokens

    # ── Helpers ──────────────────────────────────────

    def _add(self, type, value, line, col):
        self.tokens.append(Token(type, value, line, col))
        # helper function so  we don't write self.tokens.append(Token(...)) every time

    # ── Word: keyword / builtin / identifier ─────────

    def _scan_word(self):
        line, col = self.line, self.col
        #save position before we move forward, so the token knows where it started
        match = re.match(r'[a-zA-Z_][a-zA-Z0-9_]*', self.source[self.pos:])
        word = match.group()
        #regex that matches a word — must start with a letter or _, then any letters/digits/underscores.
        # self.source[self.pos:] means "look from current position to end"
        self.pos += len(word)
        self.col += len(word)
#advance position by however long the word was
        if word in KEYWORDS:
            self._add(TokenType.KEYWORD, word, line, col)
        elif word in BUILTINS:
            self._add(TokenType.BUILTIN, word, line, col)
        else:
            self._add(TokenType.IDENTIFIER, word, line, col)
#check if the word is a Merror keyword like fi, a builtin like tnirp, or just a variable name
    # ── Number ───────────────────────────────────────

    def _scan_number(self):
        line, col = self.line, self.col
        match = re.match(r'\d+(\.\d+)?', self.source[self.pos:])
        #\d+ means one or more digits. (\.\d+)? means optionally followed by a dot and more digits —
        # so it matches both integers and floats
        value = match.group()
        self.pos += len(value)
        self.col += len(value)
        self._add(TokenType.NUMBER, value, line, col)
        #advance and emit the number token and just move to the next pos

    # ── String ───────────────────────────────────────

    def _scan_string(self):
        line, col = self.line, self.col
        quote = self.source[self.pos]
        pattern = r'"(\\.|[^"\\])*"' if quote == '"' else r"'(\\.|[^'\\])*'"
        #picks the right pattern depending on whether the string uses " or '.
     #\\. matches any escaped character like \n or \"
     #[^"\\]* matches anything that's NOT a quote or backslash
        # "mariam
        match = re.match(pattern, self.source[self.pos:])
        if not match:
            raise SyntaxError(f"[Line {line}, Col {col}] Unterminated string")
        #if no closing quote found, throw an error
        value = match.group()
        self.pos += len(value)
        self.col += len(value)
        self._add(TokenType.STRING, value, line, col)
# advance and move on ig we alr saw it 5alas
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
#check multi-character operators first — if we see = we want to check if it's actually == before treating it as just =
        ch = self.source[self.pos]
        self.pos += 1
        self.col += 1
# move on bro
        if ch in "+-*/%=<>!&|^~":
            self._add(TokenType.OPERATOR, ch, line, col)

        elif ch in "{}();,.:[]":
            # { } open/close blocks
            # ; statement terminator
            # ( ) [ ] , . : standard delimiters
            self._add(TokenType.DELIMITER, ch, line, col)

        else:
            raise SyntaxError(f"[Line {line}, Col {col}] Unexpected character '{ch}'")
#single char operators, then delimiters (including { } ; for Merror blocks), then error if we don't recognize it

    # ── Comment ──────────────────────────────────────

    def _scan_comment(self):
        line, col = self.line, self.col
        match = re.match(r'#[^\n]*', self.source[self.pos:])
        ## followed by anything that's not a newline — so it grabs the whole comment line in one shot
        value = match.group()
        self.pos += len(value)
        self.col += len(value)
        self._add(TokenType.COMMENT, value, line, col)
