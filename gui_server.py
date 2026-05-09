# gui_server.py
# Merror IDE Backend -- Flask API that runs all compiler phases
# Usage: python gui_server.py  (then open gui.html in browser)

import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')  # Windows safe
import os
import json
import subprocess
import tempfile
import webbrowser
import threading

sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, request, jsonify
from flask_cors import CORS

from merror.compiler.scanner import Scanner
from merror.compiler.parser import Parser
from merror.compiler.semantic import SemanticAnalyzer
from merror.compiler.transpiler import Transpiler

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

GUI_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gui.html")

@app.route("/")
def index():
    return app.send_static_file("gui.html")


# ── Helpers ──────────────────────────────────────────────────────────


def _format_tokens(tokens):
    """Convert token list to a list of readable dicts."""
    rows = []
    for tok in tokens:
        if tok.type.name == "EOF":
            continue
        rows.append({
            "type":  tok.type.name,
            "value": tok.value,
            "line":  tok.line,
            "col":   tok.col,
        })
    return rows


def _ast_to_dict(node):
    """Recursively convert an AST dataclass node to a JSON-serialisable dict."""
    if node is None:
        return None

    # Primitives
    if isinstance(node, (str, int, float, bool)):
        return node

    # Lists (e.g. statements, params, args)
    if isinstance(node, list):
        return [_ast_to_dict(item) for item in node]

    # Tuples  (elif branches are (condition, block) tuples)
    if isinstance(node, tuple):
        return [_ast_to_dict(item) for item in node]

    # Dataclass AST nodes — use __dataclass_fields__ if available
    if hasattr(node, "__dataclass_fields__"):
        result = {"_type": type(node).__name__}
        for field_name in node.__dataclass_fields__:
            result[field_name] = _ast_to_dict(getattr(node, field_name))
        return result

    # Fallback
    return repr(node)


def _get_symbol_summary(analyzer: SemanticAnalyzer) -> dict:
    """Extract variables and functions from the symbol table."""
    st = analyzer.symbol_table

    # st.table  →  { name: [stack of values], ... }
    variables = []
    for name, stack in st.table.items():
        type_val = stack[-1] if stack else "unknown"
        variables.append({"name": name, "type": type_val})

    # st.functions  →  { name: param_count }
    functions = []
    for fname, arity in st.functions.items():
        functions.append({"name": fname, "params": arity})

    return {"variables": variables, "functions": functions}


# ── API Endpoint ──────────────────────────────────────────────────────


@app.route("/run", methods=["POST"])
def run_code():
    data    = request.get_json(force=True)
    source  = data.get("source", "")

    response = {
        "scanner":    {"ok": False, "tokens": [],  "error": None},
        "parser":     {"ok": False, "ast":    None, "error": None},
        "semantic":   {"ok": False, "symbols": None,"error": None},
        "transpiler": {"ok": False, "code":   None, "error": None},
        "execution":  {"ok": False, "stdout": None, "stderr": None,
                       "exit_code": None, "error": None},
    }

    # ── 1. Scanner ───────────────────────────────────────────────────
    try:
        scanner = Scanner(source)
        tokens  = scanner.tokenize()
        response["scanner"]["ok"]     = True
        response["scanner"]["tokens"] = _format_tokens(tokens)
    except Exception as e:
        response["scanner"]["error"] = str(e)
        return jsonify(response)

    # ── 2. Parser ────────────────────────────────────────────────────
    try:
        parser = Parser(tokens)
        ast    = parser.parse()
        response["parser"]["ok"]  = True
        response["parser"]["ast"] = _ast_to_dict(ast)
    except Exception as e:
        response["parser"]["error"] = str(e)
        return jsonify(response)

    # ── 3. Semantic ──────────────────────────────────────────────────
    try:
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        response["semantic"]["ok"]      = True
        response["semantic"]["symbols"] = _get_symbol_summary(analyzer)
    except Exception as e:
        response["semantic"]["error"] = str(e)
        return jsonify(response)

    # ── 4. Transpiler ────────────────────────────────────────────────
    try:
        transpiler  = Transpiler()
        python_code = transpiler.transpile(ast)
        response["transpiler"]["ok"]   = True
        response["transpiler"]["code"] = python_code
    except Exception as e:
        response["transpiler"]["error"] = str(e)
        return jsonify(response)

    # ── 5. Execution ─────────────────────────────────────────────────
    try:
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        )
        tmp.write(python_code)
        tmp.close()

        result = subprocess.run(
            [sys.executable, tmp.name],
            capture_output=True,
            text=True,
            timeout=10,
        )

        os.unlink(tmp.name)

        response["execution"]["ok"]        = (result.returncode == 0)
        response["execution"]["stdout"]    = result.stdout
        response["execution"]["stderr"]    = result.stderr
        response["execution"]["exit_code"] = result.returncode

    except subprocess.TimeoutExpired:
        response["execution"]["error"] = "Execution timed out (10 s limit)"
    except Exception as e:
        response["execution"]["error"] = str(e)

    return jsonify(response)


# ── Dev helper: open browser after start ─────────────────────────────


def _open_browser():
    import time
    time.sleep(1.2)
    gui_path = os.path.join(os.path.dirname(__file__), "gui.html")
    webbrowser.open(f"file:///{gui_path.replace(os.sep, '/')}")


if __name__ == "__main__":
    print("\n  [*] Merror IDE Server")
    print("  -------------------------------------")
    print("  API  -> http://localhost:5000/run")
    gui_path = os.path.join(os.path.dirname(__file__), "gui.html")
    print(f"  GUI  -> {gui_path}")
    print("  -------------------------------------")
    print("  Opening browser automatically...\n")

    threading.Thread(target=_open_browser, daemon=True).start()
    app.run(port=5000, debug=False)
