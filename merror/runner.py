# merror/runner.py
# Full pipeline: source → tokens → AST → semantic check → transpile → execute

import sys
import os
import subprocess

sys.path.insert(0, os.path.dirname(__file__))
from merror.compiler.scanner import Scanner
from merror.compiler.parser import Parser
from merror.compiler.semantic import SemanticAnalyzer
from merror.compiler.transpiler import Transpiler


def run(source: str):
    """
    Full pipeline: source → tokens → AST → semantic check
    Returns (ast, error)  [kept for backward-compat with shell.py]
    """
    try:
        scanner = Scanner(source)
        tokens = scanner.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        semantic = SemanticAnalyzer()
        semantic.analyze(ast)

        return ast, None

    except SyntaxError as e:
        return None, str(e)
    except Exception as e:
        return None, f"Unexpected error: {e}"


def run_file(filepath: str):
    """
    Transpile a .mr file to Python, write the .py next to it, then execute it.
    Returns (py_filepath, error)
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()

        # ── Scan ────────────────────────────────────────
        scanner = Scanner(source)
        tokens = scanner.tokenize()

        # ── Parse ───────────────────────────────────────
        parser = Parser(tokens)
        ast = parser.parse()

        # ── Semantic analysis ───────────────────────────
        semantic = SemanticAnalyzer()
        semantic.analyze(ast)

        # ── Transpile ───────────────────────────────────
        transpiler = Transpiler()
        python_code = transpiler.transpile(ast)

        # ── Write .py next to the .mr file ──────────────
        base = os.path.splitext(filepath)[0]
        py_path = base + ".py"
        with open(py_path, "w", encoding="utf-8") as f:
            f.write(python_code)

        print(f"\n[Merror] Generated: {py_path}")
        print(f"[Merror] Running...\n" + "-" * 40)

        # ── Execute ─────────────────────────────────────
        result = subprocess.run(
            [sys.executable, py_path],
            capture_output=False,   # let stdout/stderr flow straight to terminal
        )

        print("-" * 40)
        print(f"[Merror] Exit code: {result.returncode}")

        return py_path, None

    except SyntaxError as e:
        return None, f"Syntax error: {e}"
    except Exception as e:
        return None, f"Error: {e}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python runner.py <file.mr>')
        sys.exit(1)

    py_path, error = run_file(sys.argv[1])
    if error:
        print(error)
        sys.exit(1)