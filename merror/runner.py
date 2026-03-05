# runner.py

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from merror.compiler.scanner import Scanner


def run(source: str):
    """
    Scan a Merror source string and return (tokens, error).
    Returns (list of tokens, None) on success.
    Returns (None, error message) on failure.
    """
    try:
        scanner = Scanner(source)
        tokens  = scanner.tokenize()
        return tokens, None
    except SyntaxError as e:
        return None, str(e)
    except Exception as e:
        return None, f"Unexpected error: {e}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python runner.py "<merror code>"')
        sys.exit(1)

    source = " ".join(sys.argv[1:])
    tokens, error = run(source)

    if error:
        print(f"Error: {error}")
    else:
        print(f"── Input ──")
        print(source)
        print(f"\n── Tokens ──\n")
        for tok in tokens:
            print(tok)
