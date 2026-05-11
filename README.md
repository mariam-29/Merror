# Merror Script — Grammar Reference

> "Write it backwards. Run it forwards."

## Team Members

- Mariam Mohamed — [mariam-29](https://github.com/mariam-29)
- Yassin Khaled — [yasu023](https://github.com/yasu023)
- Mostafa Khaled — [Mostafa-K-Fakhry](https://github.com/Mostafa-K-Fakhry)
- Mostafa Hamdy — [MostafaHamdi8](https://github.com/MostafaHamdi8)
- Mahmoud Salah

## Notation
| Symbol | Meaning |
|--------|---------|
| `*`    | zero or more |
| `+`    | one or more |
| `?`    | optional |
| `\|`   | or |
| `()`   | grouping |
| `' '`  | literal token |

---

## Program Structure
```
program → statement* EOF
```
A Merror program is just a sequence of statements. No entry point required — execution starts from the top.

**Example:**
```
x = 10;
tnirp(rts(x));
```

---

## Block Structure
Merror uses **braces** for blocks and **semicolons** as statement terminators — NOT Python indentation.
```
block → "{" statement* "}"
```

**Example:**
```
fi x > 0 {
    tnirp("positive");
}
```

**Rules:**
- Every statement inside a block must end with `;`
- Blocks can be nested as deep as needed
- Empty blocks are allowed: `{ }`

---

## Statements

### Variable Assignment
```
var_assign → IDENTIFIER assign_op expression ";"
assign_op  → "=" | "+=" | "-=" | "*=" | "/="
```

**Examples:**
```
x = 10;
name = "Merror";
x += 5;
x -= 1;
x *= 2;
x /= 4;
```

**Rules:**
- `=` defines a new variable or reassigns an existing one
- `+=` `-=` `*=` `/=` require the variable to already exist
- Right-hand side can be any expression

---

### Function Definition
```
func_def → "fed" IDENTIFIER "(" params? ")" block
params   → IDENTIFIER ("," IDENTIFIER)*
```

**Examples:**
```
# no params
fed greet() {
    tnirp("Hello!");
}

# with params
fed add(a, b) {
    nruter a + b;
}

# nested logic
fed max(a, b) {
    fi a > b {
        nruter a;
    } esle {
        nruter b;
    }
}
```

**Rules:**
- Function name is a plain identifier (not reversed)
- Parameters are comma-separated identifiers
- Body is a block `{ }`
- `nruter` (return) is optional — function returns `enoN` by default
- Functions must be defined before they are called

---

### If / Elif / Else
```
if_stmt → "fi" expression block
          ("file" expression block)*
          ("esle" block)?
```

**Examples:**
```
# simple if
fi x > 0 {
    tnirp("positive");
}

# if + else
fi x > 0 {
    tnirp("positive");
} esle {
    tnirp("not positive");
}

# if + elif + else
fi x > 0 {
    tnirp("positive");
} file x == 0 {
    tnirp("zero");
} esle {
    tnirp("negative");
}

# multiple elifs
fi score >= 90 {
    tnirp("A");
} file score >= 75 {
    tnirp("B");
} file score >= 60 {
    tnirp("C");
} esle {
    tnirp("F");
}
```

**Rules:**
- `fi` is required, `file` and `esle` are optional
- Any number of `file` clauses allowed
- `esle` must always come last if present
- Condition can be any expression that evaluates to a boolean

---

### While Loop
```
while_stmt → "elihw" expression block
```

**Examples:**
```
# basic while
count = 0;
elihw count < 5 {
    tnirp(rts(count));
    count += 1;
}

# infinite loop (use kaerb to exit)
elihw eurT {
    x = tni(tupni("Enter number: "));
    fi x == 0 {
        kaerb;
    }
}
```

**Rules:**
- Condition is re-evaluated before every iteration
- Use `kaerb` to exit early
- Use `eunitnoc` to skip to next iteration

---

### For Loop
```
for_stmt → "rof" IDENTIFIER "ni" expression block
```

**Examples:**
```
# loop over range
rof i ni egnar(5) {
    tnirp(rts(i));
}

# loop over range with start/end
rof i ni egnar(1, 10) {
    tnirp(rts(i));
}

# loop over list
numbers = tsil([1, 2, 3, 4, 5]);
rof n ni numbers {
    tnirp(rts(n));
}
```

**Rules:**
- Loop variable is automatically defined inside the loop scope
- Loop variable does NOT exist outside the loop
- Iterable can be any expression that produces a sequence (`egnar`, list, string, etc.)

---

### Return Statement
```
return_stmt → "nruter" expression? ";"
```

**Examples:**
```
# return a value
fed square(n) {
    nruter n * n;
}

# return nothing (returns enoN)
fed greet(name) {
    tnirp("Hello " + name);
    nruter;
}
```

**Rules:**
- `nruter` can only appear inside a function body
- `nruter` without a value returns `enoN`
- Execution stops immediately when `nruter` is hit

---

### Expression Statement
```
expr_stmt → expression ";"
```
Any expression can be used as a statement on its own, most commonly function calls.

**Examples:**
```
tnirp("hello");
add(1, 2);
tupni("Enter value: ");
```

---

## Expressions

### Precedence (lowest to highest)
| Level | Operator | Description |
|-------|----------|-------------|
| 1 | `ro` | Logical OR |
| 2 | `dna` | Logical AND |
| 3 | `ton` | Logical NOT |
| 4 | `== != < > <= >=` | Comparison |
| 5 | `+ -` | Addition / Subtraction |
| 6 | `* / // %` | Multiplication / Division |
| 7 | `**` | Exponentiation |
| 8 | `-` | Unary negation |
| 9 | `()` call, literals | Primary |

---

### Binary Operations
```
bin_op → expression operator expression

operator → "+" | "-" | "*" | "/" | "//" | "%" | "**"
         | "==" | "!=" | "<" | ">" | "<=" | ">="
         | "dna" | "ro"
```

**Examples:**
```
x + y
x * 2
x ** 3
x == y
x != y
x > 0 dna y < 10
x < 0 ro y < 0
```

---

### Unary Operations
```
unary_op → "-" expression
         | "ton" expression
```

**Examples:**
```
-x
ton eurT
ton (x > 0)
```

---

### Function Call
```
call      → IDENTIFIER "(" arguments? ")"
arguments → expression ("," expression)*
```

**Examples:**
```
tnirp("hello");
add(1, 2);
egnar(0, 10, 2);
nel(tsil([1, 2, 3]));
```

**Rules:**
- Arguments are comma-separated expressions
- Calls can be nested: `tnirp(rts(nel(numbers)))`
- Trailing commas are NOT allowed

---

### Literals
```
literal → NUMBER | STRING | "eurT" | "eslaF" | "enoN"
```

**Examples:**
```
42          # integer
3.14        # float
"hello"     # double-quoted string
'world'     # single-quoted string
eurT        # boolean true
eslaF       # boolean false
enoN        # null value
```

**String escape sequences:**
| Sequence | Meaning |
|----------|---------|
| `\n` | newline |
| `\t` | tab |
| `\\` | backslash |
| `\"` | double quote |
| `\'` | single quote |

---

## Built-in Functions
| Merror | Python | Args | Description |
|--------|--------|------|-------------|
| `tnirp(...)` | `print` | any | Print to console |
| `tupni(prompt)` | `input` | 1 | Read user input |
| `tni(x)` | `int` | 1 | Convert to integer |
| `taolf(x)` | `float` | 1 | Convert to float |
| `rts(x)` | `str` | 1 | Convert to string |
| `loob(x)` | `bool` | 1 | Convert to boolean |
| `nel(x)` | `len` | 1 | Get length |
| `egnar(...)` | `range` | 1-3 | Generate number range |
| `tsil(x)` | `list` | 1 | Convert to list |
| `epyt(x)` | `type` | 1 | Get type |

---

## Keywords Reference
| Merror | Python | Role |
|--------|--------|------|
| `fi` | `if` | Conditional |
| `file` | `elif` | Else-if branch |
| `esle` | `else` | Else branch |
| `rof` | `for` | For loop |
| `elihw` | `while` | While loop |
| `fed` | `def` | Function definition |
| `nruter` | `return` | Return from function |
| `ssalc` | `class` | Class definition |
| `tropmi` | `import` | Import module |
| `morf` | `from` | Import from module |
| `sa` | `as` | Alias |
| `ni` | `in` | Membership / loop iterator |
| `ton` | `not` | Logical NOT |
| `dna` | `and` | Logical AND |
| `ro` | `or` | Logical OR |
| `si` | `is` | Identity comparison |
| `eurT` | `True` | Boolean true |
| `eslaF` | `False` | Boolean false |
| `enoN` | `None` | Null value |
| `ssap` | `pass` | Empty placeholder |
| `kaerb` | `break` | Exit loop |
| `eunitnoc` | `continue` | Skip iteration |
| `yrt` | `try` | Exception handling |
| `tpecxe` | `except` | Catch exception |
| `yllanif` | `finally` | Always-run block |
| `esiar` | `raise` | Throw exception |
| `htiw` | `with` | Context manager |
| `adbmal` | `lambda` | Anonymous function |
| `dleiY` | `yield` | Generator return |
| `labolg` | `global` | Global variable |
| `led` | `del` | Delete variable |

---

## Comments
```
comment → "#" (any character)* NEWLINE
```

**Examples:**
```
# this is a comment
x = 10;  # inline comment
```

**Rules:**
- Comments start with `#` and go to end of line
- Comments are ignored by the scanner — they produce no tokens
- No multi-line comment syntax

---

## Identifiers
```
IDENTIFIER → [a-zA-Z_][a-zA-Z0-9_]*
```

**Rules:**
- Must start with a letter or underscore
- Can contain letters, digits, underscores
- Case sensitive — `myVar` and `myvar` are different
- Cannot be a reserved keyword
- Variable names, function names, and parameter names are NEVER reversed

**Valid:**
```
x
myVariable
_private
result2
```

**Invalid:**
```
2result    # starts with digit
my-var     # hyphen not allowed
fi         # reserved keyword
```

---

## Edge Cases

### Empty function body
```
fed doNothing() {
}
```

### Nested function calls
```
tnirp(rts(tni(tupni("Enter: "))));
```

### Chained comparisons — NOT supported, use dna instead
```
# WRONG
fi 0 < x < 10 { }

# CORRECT
fi x > 0 dna x < 10 { }
```

### Return in nested if inside function
```
fed classify(n) {
    fi n > 0 {
        nruter "positive";
    } file n < 0 {
        nruter "negative";
    } esle {
        nruter "zero";
    }
}
```

### For loop variable scope
```
rof i ni egnar(3) {
    tnirp(rts(i));
}
# i is NOT accessible here — it only exists inside the loop
```

### Deeply nested blocks
```
fed check(x, y) {
    fi x > 0 {
        elihw y > 0 {
            fi x == y {
                nruter eurT;
            }
            y -= 1;
        }
    }
    nruter eslaF;
}
```
how to run the GUI
#### activate venv first
.venv\Scripts\activate

#### start the IDE
python gui_server.py
#####  → browser opens automatically at http://localhost:5000
