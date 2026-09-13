# explanation.py

# AI Code Explanation System

import re


def _has_word(word, line):
    return re.search(rf"\b{re.escape(word)}\b", line) is not None


def _has_assignment(line):
    # "==" (comparison) ko "=" (assignment) se alag karte hain
    # taaki "if x == 5:" ko galti se "variable update" na bola jaye
    without_comparisons = re.sub(r"==|!=|<=|>=", "", line)
    return "=" in without_comparisons


def explain_code(code):

    explanation = []

    lines = code.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if _has_assignment(line):

            explanation.append(
                f"'{line}' creates or updates a variable."
            )

        elif _has_word("print", line):

            explanation.append(
                f"'{line}' displays output on the screen."
            )

        elif _has_word("for", line) or _has_word("while", line):

            explanation.append(
                f"'{line}' represents a loop that repeats instructions."
            )

        else:

            explanation.append(
                f"'{line}' is a code statement."
            )

    return explanation


# Testing

if __name__ == "__main__":

    code = """
x = 10
print(x)
before = 5
if x == 5:
    pass
"""

    result = explain_code(code)

    for item in result:
        print(item)