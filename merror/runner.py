# runner.py

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from merror.compiler.scanner import Scanner
from merror.compiler.parser import Parser
from merror.compiler.semantic import SemanticAnalyzer


def run(source: str):
    """
    Full pipeline: source → tokens → AST → semantic check
    Returns (result, error)
    """
    try:
        scanner = Scanner(source)
        tokens = scanner.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()
        # this one gets us the ast in the terminal
        semantic = SemanticAnalyzer()
        semantic.analyze(ast)

        return ast, None


    except SyntaxError as e:
        return None, str(e)
    except Exception as e:
        return None, f"Unexpected error: {e}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python runner.py "<merror code>"')
        sys.exit(1)

    source = " ".join(sys.argv[1:])
    result, error = run(source)

    if error:
        print(f"Error: {error}")
    else:
        print(result)