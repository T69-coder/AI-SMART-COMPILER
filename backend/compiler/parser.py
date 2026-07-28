# parser.py

# Parser ka kaam tokens ko check karna hai


def parse(tokens):

    if "=" in tokens:

        equal_index = tokens.index("=")


        # = ke left aur right side check karna

        if equal_index == 0:
            return "Syntax Error: Variable missing"


        if equal_index == len(tokens)-1:
            return "Syntax Error: Value missing"


        return "Valid Assignment Statement"


    else:

        return "Statement not supported"



# Testing

if __name__ == "__main__":

    tokens = ["x", "=", "10"]


    result = parse(tokens)


    print(result)