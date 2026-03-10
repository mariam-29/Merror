# runner.py

import sys
import os
#sys lets us read command line arguments and exit the program. os lets us work with file paths
sys.path.insert(0, os.path.dirname(__file__))
#adds the folder where runner.py lives to Python's search path —
# so when we do from merror.compiler.scanner import Scanner Python knows where to look
# and we dont get a relative error
from merror.compiler.scanner import Scanner
#imports the Scanner class we built

def run(source: str):
    #takes a string of Merror code as input
    """
    Scan a Merror source string and return (tokens, error).
    Returns (list of tokens, None) on success.
    Returns (None, error message) on failure.
    """
    try:
        scanner = Scanner(source)
        tokens  = scanner.tokenize()
        return tokens, None
    #creates a Scanner with the source code, runs it, and returns (tokens, None) — the None means no error occurred
    except SyntaxError as e:
        return None, str(e)
    except Exception as e:
        return None, f"Unexpected error: {e}"

#if anything goes wrong, return (None, error message) instead of crashing.
# SyntaxError is what our scanner throws on bad input, the second except catches anything else unexpected
if __name__ == "__main__":
    #this block only runs when you call python runner.py directly —
    # it does NOT run when another file does from runner import run
    if len(sys.argv) < 2:
        #sys.argv is the list of things typed in the terminal.
        # sys.argv[0] is always the filename itself, so if len < 2 that means no code was passed in
        print('Usage: python runner.py "<merror code>"')
        sys.exit(1)


    source = " ".join(sys.argv[1:])
    #joins everything after the filename into one string — so python runner.py fi x > 0 becomes "fi x > 0"
    tokens, error = run(source)
#calls our run() function and unpacks the two return values

    if error:
        print(f"Error: {error}")
    else:
        print(f"── Input ──")
        print(source)
        print(f"\n── Tokens ──\n")
        for tok in tokens:
            print(tok)
#if there was an error print it, otherwise print the input code and then loop through every token and print it