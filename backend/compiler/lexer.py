# lexer.py

# Lexer ka kaam:
# Source code ko chote-chote tokens me todna


def tokenize(code):

    tokens = []

    current_token = ""

    for char in code:

        # Agar space mila toh current token save karo
        if char == " " or char == "\n":

            if current_token:
                tokens.append(current_token)
                current_token = ""

        # Operators ko alag token banana
        elif char in "+-*/=(){}":

            if current_token:
                tokens.append(current_token)
                current_token = ""

            tokens.append(char)

        else:
            current_token += char


    # Last token save karna
    if current_token:
        tokens.append(current_token)


    return tokens



# Testing

if __name__ == "__main__":

    code = """
    x = 10
    print(x)
    """

    result = tokenize(code)

    print(result)