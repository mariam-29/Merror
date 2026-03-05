
# Run with: python shell.py

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from merror.runner import run


def main():
    print("Merror Script Shell  |  type 'exit' to quit")
    print("─" * 45)

    while True:
        try:
            text = input("Merror >> ")
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")
            continue
        except EOFError:
            print("\nGoodbye.")
            break

        if text.strip() == "":
            continue

        if text.strip() == "exit":
            print("Goodbye.")
            break

        tokens, error = run(text)

        if error:
            print(f"Error: {error}")
        else:
            for tok in tokens:
                print(tok)


if __name__ == "__main__":
    main()