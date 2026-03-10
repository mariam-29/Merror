# Run with: python shell.py

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from merror.runner import run

# not gonna repeat

def main():
    print("Merror Script Shell  |  type 'exit' to quit")
    print("─" * 45)
# just make a line man
    while True:
        # run forever till the user types exit
        try:
            text = input("Merror >> ")
            # show this and take the input as text
        except KeyboardInterrupt:
            #KeyboardInterrupt is when the user presses the keyborad — instead of crashing we just remind them to type exit
            print("\nUse 'exit' to quit.")
            continue
        except EOFError:
            print("\nGoodbye.")
            #EOFError is when the terminal is closed or input stream ends — we exit cleanly
            break

        if text.strip() == "":
            #strip() removes spaces from both ends. if the user just hit enter with nothing, skip and show the prompt again
            continue

        if text.strip() == "exit":
            print("Goodbye.")
            break
            #if user types exit, print goodbye and break out of the loop which ends the program

        tokens, error = run(text)
#passes whatever the user typed to our run() function — gets back either a list of tokens or an error
        if error:
            print(f"Error: {error}")
        else:
            for tok in tokens:
                print(tok)

#if there was an error print it, otherwise loop through every token and print it one by one
if __name__ == "__main__":
    main()
    #same pattern as runner — only calls main() when you run python shell.py directly