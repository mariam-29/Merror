# shell.py
# Run a Merror (.mr) file end-to-end.
# Usage: python shell.py <file.mr>

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from merror.runner import run_file


def main():
    if len(sys.argv) < 2:
        print("Usage: python shell.py <file.mr>")
        sys.exit(1)

    filepath = sys.argv[1]

    if not os.path.exists(filepath):
        print(f"Error: file '{filepath}' not found")
        sys.exit(1)

    _, error = run_file(filepath)

    if error:
        print(f"\n[Merror] {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()