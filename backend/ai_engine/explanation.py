# explanation.py

# AI Code Explanation System


def explain_code(code):

    explanation = []


    lines = code.split("\n")


    for line in lines:

        line = line.strip()


        if not line:
            continue


        if "=" in line:

            explanation.append(
                f"'{line}' creates or updates a variable."
            )


        elif "print" in line:

            explanation.append(
                f"'{line}' displays output on the screen."
            )


        elif "for" in line:

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
"""


    result = explain_code(code)


    for item in result:
        print(item)