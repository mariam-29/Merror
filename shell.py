# shell.py
# Interactive Merror Script shell
# Run with: python shell.py

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from merror.runner import run


def main():
    if len(sys.argv) < 2:
        print("Usage: python shell.py <file.mr>")
        sys.exit(1)

    filepath = sys.argv[1]

    if not os.path.exists(filepath):
        print(f"Error: file '{filepath}' not found")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    ast, error = run(source)

    if error:
        print(f"Error: {error}")
    else:

        print(ast)


if __name__ == "__main__":
    main()